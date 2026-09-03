import { tool } from "@langchain/core/tools";
import { z } from "zod";

export const wikipediaTool = tool(
  async ({ query }) => {
    try {
      const res = await fetch(`https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(query)}&utf8=&format=json`);
      const data = await res.json();
      
      if (!data.query || !data.query.search || data.query.search.length === 0) {
        return `No Wikipedia results found for "${query}".`;
      }

      // Return the top 3 snippets stripped of HTML tags
      return data.query.search
        .slice(0, 3)
        .map((s: any) => s.snippet.replace(/<[^>]*>?/gm, ''))
        .join('\n\n');
    } catch (error) {
      return `Failed to search Wikipedia: ${String(error)}`;
    }
  },
  {
    name: "searchWeb",
    description: "Search Wikipedia for real factual information.",
    schema: z.object({
      query: z.string().describe("The search query"),
    }),
  }
);
