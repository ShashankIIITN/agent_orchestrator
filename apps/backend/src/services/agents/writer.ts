import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { StateAnnotation, logToDbAndStream, delay } from "../state";

export const createWriterNode = (model: ChatGoogleGenerativeAI) => {
  return async (state: typeof StateAnnotation.State) => {
    await delay(4000); 
    await logToDbAndStream(state.workflowRunId, "Writer", "Drafting", "Drafting content based on research.");
    
    const response = await model.invoke(`
      You are an expert Writer. Write a comprehensive response to the original prompt based ONLY on the provided research.
      Original Prompt: ${state.prompt}
      Research: ${state.research}
      Previous Draft (if any): ${state.draft || "None"}
    `);
    
    await logToDbAndStream(state.workflowRunId, "Writer", "Finished Draft", response.content as string);
    return { draft: response.content as string };
  };
};
