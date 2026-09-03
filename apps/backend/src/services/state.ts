import { Annotation } from "@langchain/langgraph";
import { prisma } from "../lib/prisma";
import { swarmEvents } from "../lib/events";

export const StateAnnotation = Annotation.Root({
  prompt: Annotation<string>(),
  research: Annotation<string>(),
  draft: Annotation<string>(),
  result: Annotation<string>(),
  workflowRunId: Annotation<string>(),
  reviewStatus: Annotation<string>(),
});

export const logToDbAndStream = async (workflowRunId: string, agentName: string, action: string, content: any) => {
  const stringContent = typeof content === "string" ? content : JSON.stringify(content, null, 2);
  const log = await prisma.agentLog.create({
    data: { workflowRunId, agentName, action, content: stringContent },
  });
  swarmEvents.emit("log", log);
};

export const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));
