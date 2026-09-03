# 🤖 Autonomous Multi-Agent Orchestrator

An enterprise-grade Multi-Agent orchestration platform built with **LangGraph.js**, **Next.js 15**, **Express**, and **Prisma**. It features a robust, stateful multi-agent swarm capable of reasoning, searching the web, drafting, and reviewing content autonomously.

## ✨ Features
- **LangGraph.js State Machine**: A resilient cyclic graph orchestrating multiple specialized AI agents (`Researcher`, `Writer`, `Reviewer`).
- **Real-Time SSE Streaming**: Live agent terminal streaming thought processes, tool executions, and state changes to the UI via Server-Sent Events.
- **Fault-Tolerant Session Resumption**: State checkpointing allows workflows to resume seamlessly if interrupted (e.g., due to rate limits or network issues).
- **Clean Architecture**: Modular agent design separating tools, state management, and node execution.
- **Live Tool Calling**: Native integration with the Wikipedia API for real-time internet search and fact-checking.
- **Session History Tracker**: A built-in sidebar allowing you to review past workflows, AI reasoning logs, and terminal states.

## 🏗️ Architecture
- **Frontend**: Next.js 15, React, Tailwind CSS (Glassmorphism Dashboard & Terminal UI)
- **Backend**: Express, TypeScript, LangGraph.js, `@langchain/google-genai`
- **Database**: Prisma ORM, SQLite (Logging & Session history tracking)
- **Monorepo**: Turborepo, `pnpm`

## 🚀 Getting Started

### 1. Install Dependencies
This project utilizes `pnpm` as the package manager within a Turborepo workspace.
```bash
pnpm install
```

### 2. Environment Variables
Create a `.env` file in the `apps/backend/` directory and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Setup Database
Initialize the SQLite database and sync the Prisma schema:
```bash
cd apps/backend
pnpm dlx prisma db push
cd ../..
```

### 4. Run the Platform
Start the Turborepo development servers:
```bash
pnpm dev
```
- The Next.js UI will be available at `http://localhost:3000`
- The Express API and SSE stream run on `http://localhost:3001`

## 🧠 Meet the Swarm

1. **Researcher Agent**: Takes the initial prompt and determines what real-world facts are needed. It uses the `searchWeb` tool to query Wikipedia and compiles an accurate research context.
2. **Writer Agent**: Ingests the Researcher's context and drafts a highly detailed, comprehensive response to the original task.
3. **Reviewer Agent**: The Quality Gatekeeper. It critiques the Writer's draft. If it meets standards, it approves the output. If it falls short, it rejects the draft and dynamically creates a feedback loop, sending it back to the Writer for revision.
