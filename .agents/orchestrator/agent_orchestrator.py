#!/usr/bin/env python3
"""
Autonomous Multi-Agent Orchestrator for Enterprise AI Platform.

Orchestrates specialized subagents across:
- prisma-db-architect (Prisma ORM v5, Schema, Migrations)
- swarm-architect (LangGraph.js, State Machines, Swarm Graphs)
- ts-backend-coder (TypeScript Express/Next.js API, Clean Architecture)
- frontend-designer (Next.js 15, Tailwind, Framer Motion, Workflow Dashboard)
- ts-backend-reviewer (Clean Architecture, DI, Zod, Security Gatekeeper)
- frontend-reviewer (App Router, DRY Scoping, CWV Gatekeeper)
- qa-tester (Automated Tests, Build Verification)
"""

import os
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AGY_BINARY = r"C:\Users\MSI\AppData\Local\agy\bin\agy.exe"
METRICS_PATH = os.path.join(WORKSPACE_DIR, ".agents", "metrics", "metrics.jsonl")

AGENT_ROSTER = {
    "agent-orchestrator": {
        "role": "Master Multi-Agent Orchestrator",
        "model": "Gemini 3.1 Pro (High)",
        "phase": "ORCHESTRATION",
        "description": "Master task planning, multi-agent dispatch & pipeline synthesis."
    },
    "swarm-architect": {
        "role": "AI Swarm & LangGraph.js Architect",
        "model": "Gemini 3.1 Pro (High)",
        "phase": "AI_WORKFLOW",
        "description": "LangGraph.js state machines, multi-agent graphs, streaming logs."
    },
    "ts-backend-coder": {
        "role": "Principal TypeScript Backend Engineer",
        "model": "Claude Sonnet 4.6",
        "phase": "BACKEND",
        "description": "Clean Architecture, Express/Next API routes, Prisma, Zod validation."
    },
    "ts-backend-reviewer": {
        "role": "Staff TypeScript Backend Reviewer",
        "model": "Claude Sonnet 4.6",
        "phase": "AUDIT",
        "description": "Clean Architecture boundaries, DI, Zod enforcement, security reviews."
    },
    "frontend-designer": {
        "role": "Frontend UI/UX Designer & Craftsman",
        "model": "Claude Sonnet 4.6",
        "phase": "FRONTEND",
        "description": "Next.js 15 App Router, Tailwind CSS, Framer Motion, agent dashboards."
    },
    "frontend-reviewer": {
        "role": "Frontend & Next.js Quality Gatekeeper",
        "model": "Claude 3.7 Sonnet (Thinking)",
        "phase": "AUDIT",
        "description": "RSC boundary hygiene, DRY modularity, hierarchical scoping, CWV."
    },
    "prisma-db-architect": {
        "role": "Prisma Database Architect",
        "model": "Gemini 3.1 Pro (High)",
        "phase": "DATABASE",
        "description": "Prisma ORM schema modeling, SQLite/Postgres migrations, indexes."
    },
    "qa-tester": {
        "role": "Principal QA Automation Tester",
        "model": "Gemini 3.1 Pro (High)",
        "phase": "VERIFICATION",
        "description": "Automated API route tests, Prisma integration tests, build checks."
    },
    "code-reviewer": {
        "role": "General Code Reviewer",
        "model": "Gemini 3.1 Pro (High)",
        "phase": "AUDIT",
        "description": "Multi-language code audits, security scans, git diff reviews."
    }
}

def log_event(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def execute_agent_task(agent_name: str, prompt: str, workspace: str = WORKSPACE_DIR) -> Dict[str, Any]:
    """Execute a task with a specific subagent using the native Antigravity CLI."""
    if not os.path.isfile(AGY_BINARY):
        return {
            "success": False,
            "output": f"Antigravity CLI binary not found at {AGY_BINARY}",
            "duration": 0.0
        }

    agent_info = AGENT_ROSTER.get(agent_name, AGENT_ROSTER["agent-orchestrator"])
    log_event(f"🚀 Invoking [{agent_name}] ({agent_info['model']}): {prompt[:60]}...")
    
    cmd = [
        AGY_BINARY,
        "--agent", agent_name,
        "-p", prompt,
        "--add-dir", workspace,
        "--dangerously-skip-permissions"
    ]

    start_time = time.time()
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=workspace,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        stdout_bytes, _ = proc.communicate(timeout=360)
        duration = round(time.time() - start_time, 2)
        output = stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
        
        # Filter profile noise
        clean_lines = [l for l in output.splitlines() if not any(x in l for x in ["conda.exe", "WindowsPowerShell", "CommandNotFoundException"])]
        clean_output = "\n".join(clean_lines).strip()
        
        return {
            "success": proc.returncode == 0,
            "output": clean_output,
            "duration": duration,
            "agent": agent_name,
            "model": agent_info["model"]
        }
    except subprocess.TimeoutExpired:
        proc.kill()
        return {"success": False, "output": "❌ Task timed out.", "duration": 360.0, "agent": agent_name, "model": agent_info["model"]}
    except Exception as e:
        return {"success": False, "output": f"❌ Execution error: {e}", "duration": 0.0, "agent": agent_name, "model": agent_info["model"]}

def run_pipeline(goal: str, workspace: str = WORKSPACE_DIR):
    """Execute full autonomous multi-agent pipeline."""
    print("\n" + "═" * 75)
    print(f"👑 MASTER MULTI-AGENT ORCHESTRATION PIPELINE")
    print(f"Goal: {goal}")
    print("═" * 75 + "\n")

    pipeline_start = time.time()
    results = []

    # Phase 1: Database & Schema Design
    print("📌 PHASE 1: Database & Schema Modeling (prisma-db-architect)")
    db_res = execute_agent_task(
        "prisma-db-architect",
        f"Design and update Prisma schema models and migrations for: {goal}",
        workspace
    )
    results.append(db_res)
    print(db_res.get("output", "")[:500] + "\n")

    # Phase 2: AI Swarm Workflow Design
    print("📌 PHASE 2: AI Swarm & LangGraph State Graph (swarm-architect)")
    swarm_res = execute_agent_task(
        "swarm-architect",
        f"Implement LangGraph state graph nodes, edges and streaming handlers for: {goal}",
        workspace
    )
    results.append(swarm_res)
    print(swarm_res.get("output", "")[:500] + "\n")

    # Phase 3: TypeScript Backend API
    print("📌 PHASE 3: TypeScript Backend & Clean Services (ts-backend-coder)")
    backend_res = execute_agent_task(
        "ts-backend-coder",
        f"Implement Clean Architecture services, controllers, and Zod routes for: {goal}",
        workspace
    )
    results.append(backend_res)
    print(backend_res.get("output", "")[:500] + "\n")

    # Phase 4: Frontend UI/UX
    print("📌 PHASE 4: Frontend Dashboard & Components (frontend-designer)")
    ui_res = execute_agent_task(
        "frontend-designer",
        f"Build modular Next.js 15 UI components and dashboard views for: {goal}",
        workspace
    )
    results.append(ui_res)
    print(ui_res.get("output", "")[:500] + "\n")

    # Phase 5: Quality Gate & Audit
    print("📌 PHASE 5: Dual Quality Audit (ts-backend-reviewer & frontend-reviewer)")
    be_rev = execute_agent_task(
        "ts-backend-reviewer",
        f"Audit TypeScript backend code for Clean Architecture and security for: {goal}",
        workspace
    )
    fe_rev = execute_agent_task(
        "frontend-reviewer",
        f"Audit Next.js frontend code for DRY modularity and RSC boundaries for: {goal}",
        workspace
    )
    results.extend([be_rev, fe_rev])

    # Phase 6: Automated QA Verification
    print("📌 PHASE 6: Automated Verification & Typecheck (qa-tester)")
    qa_res = execute_agent_task(
        "qa-tester",
        f"Run automated tests and verify Next.js/TypeScript build for: {goal}",
        workspace
    )
    results.append(qa_res)
    print(qa_res.get("output", "")[:500] + "\n")

    total_duration = round(time.time() - pipeline_start, 2)
    print("═" * 75)
    print(f"🎉 MULTI-AGENT PIPELINE COMPLETED in {total_duration}s")
    print("═" * 75)

def print_roster():
    print("\n👥 ACTIVE MULTI-AGENT ROSTER FOR AGENT ORCHESTRATOR PLATFORM\n")
    print("| Subagent Name | Role | Model | Phase |")
    print("| :--- | :--- | :--- | :--- |")
    for name, info in AGENT_ROSTER.items():
        print(f"| **`{name}`** | {info['role']} | `{info['model']}` | `{info['phase']}` |")
    print("\nUse `python agent_orchestrator.py run --agent <name> --prompt \"<task>\"` to trigger any agent.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Agent Platform Orchestrator")
    subparsers = parser.add_subparsers(dest="command")

    # list command
    subparsers.add_parser("list", help="List all available agents and roles")

    # run command
    run_parser = subparsers.add_parser("run", help="Run a specific agent on a prompt")
    run_parser.add_argument("--agent", required=True, choices=list(AGENT_ROSTER.keys()), help="Agent name")
    run_parser.add_argument("--prompt", required=True, help="Task prompt")

    # pipeline command
    pipe_parser = subparsers.add_parser("pipeline", help="Run full autonomous multi-agent pipeline")
    pipe_parser.add_argument("--goal", required=True, help="High-level goal description")

    args = parser.parse_args()

    if args.command == "list":
        print_roster()
    elif args.command == "run":
        res = execute_agent_task(args.agent, args.prompt)
        print(f"\n[{res['agent']}] ({res['model']}) Duration: {res['duration']}s\n")
        print(res.get("output", ""))
    elif args.command == "pipeline":
        run_pipeline(args.goal)
    else:
        print_roster()
