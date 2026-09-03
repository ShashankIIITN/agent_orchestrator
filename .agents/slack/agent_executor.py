#!/usr/bin/env python3
"""
Native Antigravity Agent Executor for Slack.

Uses the local authenticated Antigravity CLI binary (agy.exe) directly.
- Zero API keys required (uses your PC's logged-in Antigravity account).
- Executes real multi-agent coding goals with full tool access.
- Runs with --dangerously-skip-permissions for true zero-interruption execution.
"""

import os
import sys
import subprocess
import time
from typing import Dict, Any

AGY_BINARY = r"C:\Users\MSI\AppData\Local\agy\bin\agy.exe"

def execute_with_antigravity_cli(prompt: str, workspace_dir: str = r"D:\My Project\UniConnect", timeout: int = 300) -> Dict[str, Any]:
    """Execute task via local Antigravity CLI runner."""
    if not os.path.isfile(AGY_BINARY):
        return {
            "success": False,
            "output": f"Antigravity CLI binary not found at {AGY_BINARY}"
        }

    cmd = [
        AGY_BINARY,
        "-p", prompt,
        "--add-dir", workspace_dir,
        "--dangerously-skip-permissions"
    ]

    try:
        start_time = time.time()
        proc = subprocess.run(
            cmd,
            cwd=workspace_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout
        )
        duration = round(time.time() - start_time, 2)
        output = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")

        # Filter PowerShell profile noise if present
        clean_lines = []
        for line in output.splitlines():
            if "conda.exe" in line or "OneDrive\\Documents\\WindowsPowerShell" in line or "CommandNotFoundException" in line or "shell.powershell" in line:
                continue
            clean_lines.append(line)
        clean_output = "\n".join(clean_lines).strip()

        return {
            "success": proc.returncode == 0,
            "output": clean_output if clean_output else "[Task completed successfully]",
            "duration_sec": duration
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": f"Task timed out after {timeout} seconds."
        }
    except Exception as e:
        return {
            "success": False,
            "output": f"Error running Antigravity agent: {e}"
        }

if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "say hello"
    print(f"Executing: {task}")
    res = execute_with_antigravity_cli(task)
    print(res["output"])
