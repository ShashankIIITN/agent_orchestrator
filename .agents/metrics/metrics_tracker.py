#!/usr/bin/env python3
"""
Multi-Agent Observability, Usage & Performance Tracker for Agent Orchestrator Platform.

Features:
- Strict Deduplication by Unique Turn ID
- Real-time token usage and latency metrics
- Multi-model pricing (Claude Sonnet 4.6, Gemini 3.1 Pro)
- Leaderboard & Efficiency Scoring across TypeScript & AI Swarm agents
"""

import os
import sys
import json
import glob
import time
import hashlib
import argparse
from datetime import datetime
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

MODEL_PRICING = {
    "claude-sonnet-4.6": {"input": 3.00, "output": 15.00},
    "claude-3-7-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "gemini-3.1-pro": {"input": 1.25, "output": 5.00},
    "gemini-2.5-flash": {"input": 0.075, "output": 0.30},
    "default": {"input": 1.00, "output": 4.00}
}

DEFAULT_METRICS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "metrics.jsonl"
)

def calculate_cost(model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
    key = "default"
    model_lower = model_name.lower()
    for m in MODEL_PRICING:
        if m in model_lower:
            key = m
            break
    rates = MODEL_PRICING[key]
    cost = (prompt_tokens / 1_000_000 * rates["input"]) + (completion_tokens / 1_000_000 * rates["output"])
    return round(cost, 6)

def calculate_efficiency_score(duration_sec: float, total_tokens: int, files_mod: int, verdict: str) -> int:
    score = 100
    if duration_sec > 15:
        score -= min(25, int((duration_sec - 15) * 1.5))
    if total_tokens > 10000:
        score -= min(15, int((total_tokens - 10000) / 1000))
    if verdict in ["CHANGES REQUESTED", "REJECTED"]:
        score -= 20
    elif verdict == "ACCEPTED WITH SUGGESTIONS":
        score -= 5
    if files_mod > 0:
        score += min(10, files_mod * 2)
    return max(10, min(100, score))

def load_metrics(metrics_file: str = DEFAULT_METRICS_PATH) -> List[Dict[str, Any]]:
    if not os.path.isfile(metrics_file):
        return []
    records = []
    seen_ids = set()
    with open(metrics_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                turn_id = data.get("turn_id") or data.get("timestamp", "") + "_" + data.get("task_type", "")
                if turn_id not in seen_ids:
                    seen_ids.add(turn_id)
                    records.append(data)
            except json.JSONDecodeError:
                continue
    return records

def save_deduplicated_metrics(records: List[Dict[str, Any]], metrics_file: str = DEFAULT_METRICS_PATH):
    os.makedirs(os.path.dirname(os.path.abspath(metrics_file)), exist_ok=True)
    with open(metrics_file, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

def log_agent_run(
    agent_name: str,
    model_name: str,
    task_type: str,
    duration_sec: float,
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    thinking_tokens: int = 0,
    verdict: str = "ACCEPTED",
    tool_calls_count: int = 0,
    files_modified_count: int = 0,
    turn_id: Optional[str] = None,
    metrics_file: str = DEFAULT_METRICS_PATH
) -> Optional[Dict[str, Any]]:
    records = load_metrics(metrics_file)
    
    if not turn_id:
        turn_id = hashlib.sha256(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_{task_type}_{agent_name}".encode()).hexdigest()[:16]

    for r in records:
        if r.get("turn_id") == turn_id:
            return None

    total_tokens = prompt_tokens + completion_tokens + thinking_tokens
    cost = calculate_cost(model_name, prompt_tokens, completion_tokens)
    efficiency = calculate_efficiency_score(duration_sec, total_tokens, files_modified_count, verdict)

    entry = {
        "turn_id": turn_id,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "agent": agent_name,
        "model": model_name,
        "task_type": task_type,
        "duration_sec": round(duration_sec, 2),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "thinking_tokens": thinking_tokens,
        "total_tokens": total_tokens,
        "estimated_cost_usd": cost,
        "verdict": verdict,
        "tool_calls": tool_calls_count,
        "files_modified": files_modified_count,
        "efficiency_score": efficiency
    }

    records.append(entry)
    save_deduplicated_metrics(records, metrics_file)
    return entry

def generate_summary(metrics_file: str = DEFAULT_METRICS_PATH) -> str:
    records = load_metrics(metrics_file)
    save_deduplicated_metrics(records, metrics_file)

    if not records:
        return "No agent metrics recorded yet. Run multi-agent tasks to populate observability telemetry."

    total_runs = len(records)
    total_time = sum(r.get("duration_sec", 0) for r in records)
    total_cost = sum(r.get("estimated_cost_usd", 0) for r in records)
    total_tokens = sum(r.get("total_tokens", 0) for r in records)

    agent_stats: Dict[str, Dict[str, Any]] = {}
    for r in records:
        agent = r.get("agent", "unknown")
        if agent not in agent_stats:
            agent_stats[agent] = {
                "runs": 0,
                "total_duration": 0.0,
                "total_tokens": 0,
                "total_cost": 0.0,
                "accepted": 0,
                "efficiency_scores": []
            }
        s = agent_stats[agent]
        s["runs"] += 1
        s["total_duration"] += r.get("duration_sec", 0)
        s["total_tokens"] += r.get("total_tokens", 0)
        s["total_cost"] += r.get("estimated_cost_usd", 0)
        if "ACCEPTED" in r.get("verdict", ""):
            s["accepted"] += 1
        s["efficiency_scores"].append(r.get("efficiency_score", 100))

    report = []
    report.append("# [METRICS] Agent Orchestrator Multi-Agent Telemetry Report")
    report.append(f"Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total Runs: {total_runs} | Total Compute Time: {total_time:.1f}s | Total Estimated Cost: ${total_cost:.4f} | Total Tokens: {total_tokens:,}\n")
    report.append("## Agent Performance & Verification Leaderboard\n")
    report.append("| Agent Name | Total Runs | Avg Latency | Total Tokens | Acceptance Rate | Avg Efficiency | Est. Cost |")
    report.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    for agent, s in sorted(agent_stats.items(), key=lambda x: x[1]["runs"], reverse=True):
        avg_dur = s["total_duration"] / s["runs"] if s["runs"] else 0
        acc_rate = (s["accepted"] / s["runs"] * 100) if s["runs"] else 0
        avg_eff = sum(s["efficiency_scores"]) / len(s["efficiency_scores"]) if s["efficiency_scores"] else 100
        report.append(
            f"| **`{agent}`** | {s['runs']} | {avg_dur:.1f}s | {s['total_tokens']:,} | {acc_rate:.0f}% | **{int(avg_eff)}/100** | ${s['total_cost']:.4f} |"
        )

    return "\n".join(report)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Agent Metrics Observability")
    parser.add_argument("command", choices=["summary", "reset"], default="summary", nargs="?")
    args = parser.parse_args()

    if args.command == "reset":
        save_deduplicated_metrics([])
        print("✅ Metrics reset.")
    else:
        print(generate_summary())
