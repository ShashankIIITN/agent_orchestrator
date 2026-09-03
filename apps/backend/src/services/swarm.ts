import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { StateGraph, START, END, MemorySaver } from "@langchain/langgraph";
import { prisma } from "../lib/prisma";
import { swarmEvents } from "../lib/events";
import { StateAnnotation, logToDbAndStream } from "./state";
import { createResearcherNode } from "./agents/researcher";
import { createWriterNode } from "./agents/writer";
import { createReviewerNode } from "./agents/reviewer";

const checkpointer = new MemorySaver(); // Globally save state in memory

export const runSwarm = async (prompt: string | null, workflowRunId: string) => {
  const model = new ChatGoogleGenerativeAI({
    model: "gemini-3.7-flash",
    apiKey: process.env.GEMINI_API_KEY,
  });

  const workflow = new StateGraph(StateAnnotation)
    .addNode("researcher", createResearcherNode(model))
    .addNode("writer", createWriterNode(model))
    .addNode("reviewer", createReviewerNode(model))
    .addEdge(START, "researcher")
    .addEdge("researcher", "writer")
    .addEdge("writer", "reviewer")
    .addConditionalEdges("reviewer", (state) => {
      if (state.reviewStatus === "APPROVED") return END;
      return "writer";
    });

  const app = workflow.compile({ checkpointer });

  try {
    const config = { configurable: { thread_id: workflowRunId } };
    
    let finalState;
    try {
      finalState = await app.invoke(prompt ? { prompt, workflowRunId } : null, config);
    } catch (invokeErr: any) {
      if (!prompt && (invokeErr.name === "EmptyInputError" || (invokeErr.message && invokeErr.message.includes("Received no input writes")))) {
        const run = await prisma.workflowRun.findUnique({ where: { id: workflowRunId } });
        if (run && run.prompt) {
          await logToDbAndStream(workflowRunId, "System", "Info", "Session memory was wiped (server restarted). Restarting workflow from the beginning...");
          finalState = await app.invoke({ prompt: run.prompt, workflowRunId }, config);
        } else {
          throw invokeErr;
        }
      } else {
        throw invokeErr;
      }
    }
    
    await prisma.workflowRun.update({
      where: { id: workflowRunId },
      data: { status: "COMPLETED", result: finalState.result },
    });
    swarmEvents.emit("status", { workflowRunId, status: "COMPLETED", result: finalState.result });
  } catch (error) {
    const errString = String(error);
    await logToDbAndStream(workflowRunId, "System", "Error", errString);
    await prisma.workflowRun.update({
      where: { id: workflowRunId },
      data: { status: "FAILED", result: errString },
    });
    swarmEvents.emit("status", { workflowRunId, status: "FAILED", result: errString });
  }
};
