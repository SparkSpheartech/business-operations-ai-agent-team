@echo off
echo 🚀 Starting Sparkspheartechsolutions Team Command Center...
cd Sparkspheartechsolutions_team
uv sync
uv run adk web brand_search_optimization --port 8501 --reload_agents
pause
