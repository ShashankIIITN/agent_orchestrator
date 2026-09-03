#!/usr/bin/env python3
"""
Slack Progress & Event Notifier for Autonomous Agents.

Can send notifications via:
1. Incoming Webhook URL (zero extra dependencies, simple setup).
2. Slack Bot Token (chat.postMessage API).
"""

import os
import sys
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List

def get_slack_webhook_url() -> Optional[str]:
    return os.environ.get("SLACK_WEBHOOK_URL")

def get_slack_bot_token() -> Optional[str]:
    return os.environ.get("SLACK_BOT_TOKEN")

def get_slack_channel() -> str:
    return os.environ.get("SLACK_CHANNEL", "#agent-progress")

def send_slack_webhook(message: str, title: Optional[str] = None, color: str = "#2eb886") -> bool:
    """Send formatted notification via Slack Incoming Webhook."""
    webhook_url = get_slack_webhook_url()
    if not webhook_url:
        print("Warning: SLACK_WEBHOOK_URL not set in environment.", file=sys.stderr)
        return False

    payload = {
        "attachments": [
            {
                "color": color,
                "title": title or "🤖 Agent Progress Update",
                "text": message,
                "mrkdwn_in": ["text", "pretext"]
            }
        ]
    }

    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"Error sending Slack webhook: {e}", file=sys.stderr)
        return False

def send_agent_completion_alert(agent_name: str, task: str, verdict: str, duration: float, cost: float) -> bool:
    """Send structured alert when an agent finishes a task."""
    color = "#2eb886" if "ACCEPTED" in verdict else ("#e01e5a" if "CHANGES" in verdict else "#ecb22e")
    emoji = "✅" if "ACCEPTED" in verdict else ("❌" if "CHANGES" in verdict else "⚠️")
    
    text = f"""*Agent*: `{agent_name}`
*Task*: {task}
*Verdict*: {emoji} *{verdict}*
*Duration*: `{duration:.1f}s` | *Est. Cost*: `${cost:.4f}`"""

    return send_slack_webhook(text, title=f"🚀 Agent Run Completed: {agent_name}", color=color)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        msg = " ".join(sys.argv[1:])
        success = send_slack_webhook(msg)
        if success:
            print("✅ Notification sent to Slack successfully.")
        else:
            print("❌ Failed to send notification. Check your SLACK_WEBHOOK_URL.")
    else:
        # Test alert
        send_agent_completion_alert("frontend-designer", "UI/UX Confession Feed Component", "ACCEPTED", 4.2, 0.035)
        print("Test alert sent (if webhook is configured).")
