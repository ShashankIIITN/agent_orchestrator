# 🛡️ Autonomous Multi-Agent Orchestration Platform Protocol

> [!IMPORTANT]
> **FULL AUTONOMY & ZERO-ASKING DIRECTIVE**:
> 1. NEVER call the `ask_question` tool.
> 2. NEVER pause execution or prompt the user for permission, clarification, design choices, or confirmations.
> 3. Automatically make all architectural and design decisions using sensible, industry-standard defaults.
> 4. Proceed directly to executing commands, writing files, and finishing the goal end-to-end.

---

## 👥 Multi-Agent Roster (TypeScript + Next.js + Prisma + LangGraph.js)

| Agent Role | Subagent Name | Optimal Model | Core Responsibility |
| :--- | :--- | :--- | :--- |
| **Master Orchestrator** | `agent-orchestrator` | `Gemini 3.1 Pro (High)` | End-to-end task decomposition, multi-agent dispatch, cross-agent handoffs. |
| **AI Swarm Architect** | `swarm-architect` | `Gemini 3.1 Pro (High)` | LangGraph.js state machines, multi-agent workflows, nodes, edges, LLM integrations. |
| **TS Backend Coder** | `ts-backend-coder` | `Claude Sonnet 4.6` | Express & Next.js API routes, Clean Architecture, Zod validation, services. |
| **TS Backend Reviewer** | `ts-backend-reviewer` | `Claude Sonnet 4.6` | Clean Architecture boundary audit, DI, Zod enforcement, security reviews. |
| **Frontend UI/UX Designer** | `frontend-designer` | `Claude Sonnet 4.6` | Next.js 15, Tailwind CSS, Framer Motion, real-time workflow dashboards & logs. |
| **Frontend Reviewer** | `frontend-reviewer` | `Claude 3.7 Sonnet (Thinking)` | RSC boundary hygiene, modular components, DRY scoping, CWV, zero `any`. |
| **Prisma DB Architect** | `prisma-db-architect` | `Gemini 3.1 Pro (High)` | Prisma ORM v5 schemas, SQLite/Postgres migrations, relation modeling, indexes. |
| **QA Automation Tester** | `qa-tester` | `Gemini 3.1 Pro (High)` | Automated API tests, Prisma database tests, Next.js build verification. |
| **Code Reviewer** | `code-reviewer` | `Gemini 3.1 Pro (High)` | General multi-language code audits, security scans, git diff reviews. |

---

## ⚡ Autonomous Multi-Agent Execution Pipeline

When executing goals, the Lead Orchestrator delegates across the lifecycle:

```text
1. [PLAN & DB]        prisma-db-architect  --> Schema modeling & migrations (schema.prisma)
2. [AI WORKFLOW]      swarm-architect      --> LangGraph.js state graphs, nodes & streaming
3. [BACKEND API]      ts-backend-coder     --> Clean Architecture services, controllers & Zod
4. [FRONTEND UI]      frontend-designer    --> Next.js 15 App Router pages, components & logs
5. [QUALITY GATES]    frontend-reviewer    --> Audit UI, RSC boundaries & DRY scoping
                      ts-backend-reviewer  --> Audit backend architecture, DI & security
6. [VERIFICATION]     qa-tester            --> Run build, typechecks & test suites
```

---

## 📊 Mandatory Turn-End Telemetry & Observability Protocol

At the end of **EVERY** CLI task, `/goal`, and code generation turn, you **MUST append this structured Agent Utilization & Quality Telemetry Card**:

```markdown
---
### 🤖 Agent Utilization & Quality Telemetry
- **Active Specialist**: `<agent-name>` (`<model-name>`)
- **Quality Gatekeeper**: `ts-backend-reviewer` OR `frontend-reviewer`
- **Acceptance Verdict**: `ACCEPTED (100% Pass)` / `ACCEPTED WITH SUGGESTIONS`
- **Verification Status**: `TypeScript Build & Prisma Check PASSED (0 errors)`
- **Efficiency Score**: `98/100` ⭐
- **Files Modified**: `<list of files created/modified>`
```
