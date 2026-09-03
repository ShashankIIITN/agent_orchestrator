@echo off
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
echo Starting Antigravity Slack Remote Bridge...
python slack_bridge.py
pause
