# In-Flight Code Standards & Autonomous Subagent Delegation Rules

## 1. Multi-Agent Delegation Map
- **AI Swarms & State Graphs**: Delegate to `swarm-architect` (LangGraph.js, state channels, tool calling).
- **TypeScript Backend & API**: Delegate to `ts-backend-coder` (Claude Sonnet 4.6).
- **Prisma & Database**: Delegate to `prisma-db-architect` (Prisma ORM v5, schema, migrations).
- **Frontend UI/UX**: Delegate to `frontend-designer` (Claude Sonnet 4.6).
- **Reviews & Acceptance**: Audited by `ts-backend-reviewer` and `frontend-reviewer`.
- **Testing & QA**: Executed by `qa-tester`.

## 2. TypeScript & Clean Architecture Standards
- **Zero `any` Policy**: 100% strict type coverage across backend and frontend.
- **Layered Clean Architecture**: Domain -> Use Cases (Services) -> Infrastructure (Prisma) -> Presentation (Controllers).
- **Dependency Injection**: Pass repository interfaces into service classes/factories.
- **Request Validation**: Enforce `zod` validation on all incoming API request payloads and query parameters.

## 3. Frontend Modularity & Scoping Standards (Next.js 15)
- **Zero Redundancy (DRY)**: Replicated JSX markup must be extracted into dedicated components immediately.
- **Hierarchical Scoping (Rule of 2+)**:
  - Route-local components/hooks/utils stay under `apps/frontend/src/app/<route>/_components/`, `_hooks/`, or `_utils/`.
  - Reused items (2+ routes) must be hoisted to `apps/frontend/src/components/`, `src/hooks/`, or `src/utils/`.
- **Stateful Encapsulation**: Extract complex stateful logic into custom hooks.
- **Boundary Hygiene**: Keep `'use client'` strictly on interactive leaf components.

## 4. Prisma ORM & Database Standards
- Explicit foreign key relations with appropriate cascade rules.
- Indexes on frequently queried and filtered columns.
- Wrap multi-table operations in transactions.
