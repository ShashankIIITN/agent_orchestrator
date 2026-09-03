# Project Handover: Multi-Agent Orchestration Platform

## Project Overview
We are building a **Multi-Agent Enterprise Orchestration Platform**. It allows users to trigger and monitor a swarm of AI agents (e.g., Researcher, Writer, Reviewer) working together to accomplish complex tasks.

## Tech Stack
*   **Monorepo:** Turborepo + pnpm (structured matching the `UniConnect` project).
*   **Frontend/API:** Next.js 15 (App Router, TypeScript, Tailwind CSS) located in `apps/web`.
*   **Database:** Prisma ORM v5 + local SQLite (`dev.db`).
*   **AI Framework:** LangGraph.js (pending installation).

## Current State & Progress
1.  **Monorepo Scaffolded:** Root `package.json`, `pnpm-workspace.yaml`, and `turbo.json` are properly configured.
2.  **Web App Scaffolding:** A fresh Next.js app has been successfully generated in `apps/web`.
3.  **Database Layer:** 
    *   Prisma v5 is installed in `apps/web`.
    *   The `schema.prisma` is written and pushed to the local SQLite database (`dev.db`).
    *   It contains two core models: `WorkflowRun` (tracks the overall task) and `AgentLog` (tracks individual agent actions/thoughts).

## Immediate Next Steps (For the next AI Agent)
1.  **LLM Configuration:** Ask the user which LLM provider they are using (OpenAI, Anthropic, or Gemini) and set up the respective API keys in `apps/web/.env`.
2.  **Install LangGraph:** Run `pnpm add @langchain/core @langchain/langgraph` inside `apps/web`.
3.  **Build the Orchestrator:** Create the Next.js API route (`app/api/swarm/route.ts`) that initializes the LangGraph state machine.
4.  **Build the UI:** Scaffold a dashboard on `app/page.tsx` to trigger workflows and stream agent logs in real-time.

## Directory Structure Context
```
agent_orchestrator/
├── apps/
│   └── web/            (Next.js App + Prisma + AI API Routes)
├── packages/           (Empty for now, ready for shared UI/config)
├── pnpm-workspace.yaml
├── turbo.json
└── package.json
```
