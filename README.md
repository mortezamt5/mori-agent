# MORI AGENT
Local Agent For Myself 
## How to run
Before run ollama and qwen3:4b must be installed and run 
```bash
uv run python -m mori_agent.main
uv run uvicorn mori_agent.api:app --reload --host 127.0.0.1 --port 8000
```