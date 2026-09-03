import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { StateAnnotation, logToDbAndStream, delay } from "../state";

export const createReviewerNode = (model: ChatGoogleGenerativeAI) => {
  return async (state: typeof StateAnnotation.State) => {
    await delay(4000); 
    await logToDbAndStream(state.workflowRunId, "Reviewer", "Reviewing", "Reviewing the draft.");
    
    const response = await model.invoke(`
      You are a strict Reviewer. Review the following draft.
      If it fully answers the prompt and is well-written, respond ONLY with "APPROVED".
      If it needs work, respond with "REJECTED: " followed by the feedback.
      
      Prompt: ${state.prompt}
      Draft: ${state.draft}
    `);
    
    const feedback = response.content as string;
    await logToDbAndStream(state.workflowRunId, "Reviewer", "Review Complete", feedback);
    
    if (feedback.includes("APPROVED")) {
      return { reviewStatus: "APPROVED", result: state.draft };
    } else {
      return { reviewStatus: "REJECTED", result: state.draft };
    }
  };
};
