#!/bin/bash
# Check if uv is installed
if ! command -v uv &> /dev/null
then
    echo "uv is not installed. Please install it first: https://astral.sh/uv/install.sh"
    exit
fi

echo "🚀 Starting Sparkspheartechsolutions Team Command Center..."
cd Sparkspheartechsolutions_team
# Ensure dependencies are synced
uv sync
# Launch the playground pointing to the specific agent package
uv run adk web brand_search_optimization --port 8501 --reload_agents
