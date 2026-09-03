# 📱 Antigravity Slack Remote Command & Control Bridge

Control your autonomous agent team, trigger code reviews, check git status, and monitor live metrics directly from Slack on your phone or laptop while you're away from your PC.

---

## ⚡ How It Works

* Uses **Slack Socket Mode** (WebSocket) — no public IP, ngrok, or open ports required on your Windows PC.
* Works seamlessly behind home Wi-Fi and firewalls.

---

## 🚀 3-Minute Setup Guide

### Step 1: Create a Slack App
1. Go to [api.slack.com/apps](https://api.slack.com/apps) and click **Create New App** -> **From scratch**.
2. Name it (e.g., `Antigravity Bot`) and select your workspace.

### Step 2: Enable Socket Mode & Generate App Token
1. In the left sidebar, click **Socket Mode** and toggle **Enable Socket Mode** to `On`.
2. Generate an **App-Level Token** with the scope `connections:write`.
3. Copy the token starting with `xapp-...` (this is your `SLACK_APP_TOKEN`).

### Step 3: Add Bot Permissions & Install App
1. In the left sidebar, go to **OAuth & Permissions**.
2. Scroll to **Scopes** -> **Bot Token Scopes** and add:
   * `chat:write` (Allows bot to send messages)
   * `app_mentions:read` (Allows bot to receive mentions)
   * `im:history` (Allows bot to receive direct messages)
   * `im:read`
3. Scroll to the top of the page and click **Install to Workspace**.
4. Copy the **Bot User OAuth Token** starting with `xoxb-...` (this is your `SLACK_BOT_TOKEN`).

### Step 4: Enable Event Subscriptions
1. In the left sidebar, click **Event Subscriptions** and toggle **Enable Events** to `On`.
2. Under **Subscribe to bot events**, add:
   * `app_mention`
   * `message.im`
3. Click **Save Changes**.

---

## 🔑 Configure Environment

Create a `.env` file in `D:\My Project\UniConnect\.agents\slack\.env`:

```env
SLACK_BOT_TOKEN="xoxb-your-bot-token"
SLACK_APP_TOKEN="xapp-your-app-token"
WORKSPACE_DIR="D:\My Project\UniConnect"
```

Install the Slack Python libraries:
```bash
pip install slack_bolt slack_sdk
```

---

## 🏃 Run the Slack Bot

Double-click `run_slack_bot.bat` or run:
```powershell
python "D:\My Project\UniConnect\.agents\slack\slack_bridge.py"
```

---

## 💬 Commands You Can Send From Slack

Invite the bot to a channel (e.g. `/invite @Antigravity Bot`) or send it a Direct Message:

| Command | What It Does |
| :--- | :--- |
| `@bot status` | Returns active Git branch and list of modified files. |
| `@bot metrics` | Returns live multi-agent performance leaderboard and cost summary. |
| `@bot review --staged` | Runs code review on staged Git changes and posts ACCEPT/REJECT report. |
| `@bot review --files src/app.py` | Reviews specific files for bugs and security issues. |
| `@bot run pnpm test` | Runs tests or commands in your workspace and replies with output. |
| `@bot /goal <task>` | Dispatches an autonomous goal to the agent team. |
