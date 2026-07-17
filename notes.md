cd ~/Desktop
mkdir roadtrip-ai
cd roadtrip-ai

uv init
uv python install 3.12
uv python pin 3.12
uv add fastapi uvicorn httpx pydantic-settings
uv add --dev pytest ruff
uv run python main.py