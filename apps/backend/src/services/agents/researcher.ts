import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { StateAnnotation, logToDbAndStream, delay } from "../state";
import { wikipediaTool } from "../tools/wikipedia";

export const createResearcherNode = (model: ChatGoogleGenerativeAI) => {
  const modelWithTools = model.bindTools([wikipediaTool]);

  return async (state: typeof StateAnnotation.State) => {
    await delay(4000); 
    await logToDbAndStream(state.workflowRunId, "Researcher", "Thinking", `Gathering info for: ${state.prompt}`);
    
    const response = await modelWithTools.invoke([
      { role: "system", content: "You are a Researcher. Use the searchWeb tool to gather info, then summarize it." },
      { role: "user", content: state.prompt }
    ]);

    let researchContent = response.content as string;

    if (response.tool_calls && response.tool_calls.length > 0) {
      await logToDbAndStream(state.workflowRunId, "Researcher", "Searching Web", `Calling tool: searchWeb for query: ${response.tool_calls[0].args.query}`);
      const toolMsg = await wikipediaTool.invoke(response.tool_calls[0]);
      
      const finalRes = await model.invoke([
        { role: "system", content: "You are a Researcher. Summarize the research." },
        { role: "user", content: state.prompt },
        response,
        toolMsg
      ]);
      researchContent = finalRes.content as string;
    }

    await logToDbAndStream(state.workflowRunId, "Researcher", "Finished Research", researchContent);
    return { research: researchContent };
  };
};
