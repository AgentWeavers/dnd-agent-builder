# Makefile for DnD Agent Builder / AgentWeaver
# Usage examples:
#   make setup           # create venv and install deps
#   make api             # run FastAPI server (uvicorn)
#   make cli             # run Executor CLI loop
#   make planner-cli     # run Planner demo CLI loop

.PHONY: help setup api run cli planner-cli executor-cli clean

UV ?= uv
PY ?= python
HOST ?= 0.0.0.0
PORT ?= 8000

help:
	@echo "Available targets:"
	@echo "  setup         - Create venv and install project (editable)"
	@echo "  api           - Run FastAPI server (uvicorn src.api.main:app)"
	@echo "  run           - Alias for api"
	@echo "  cli           - Run Executor Supervisor CLI loop"
	@echo "  planner-cli   - Run Planner demo CLI loop"
	@echo "  executor-cli  - Alias for cli"
	@echo "  clean         - Remove common build artifacts"

setup:
	$(UV) venv
	$(UV) pip install -e .

# Run FastAPI server (loads .env automatically via dotenv)
api:
	$(UV) run uvicorn src.api.main:app --reload --host $(HOST) --port $(PORT)

# Alias for api
run: api

# Executor pipeline interactive CLI
cli executor-cli:
	$(UV) run -m src.executor_agent.main

# Planner demo CLI (demo loop around planner supervisor)
planner-cli:
	$(UV) run -m src.main

clean:
	@rm -rf .pytest_cache dist build *.egg-info || true
	@find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true

build:
	docker build -t dnd-agent-builder:dev .

dev-up:
	docker compose -f docker-compose.dev.yml up -d

dev-down:
	docker compose -f docker-compose.dev.yml down

dev-logs:
	docker compose -f docker-compose.dev.yml logs -f

dev-ps:
	docker compose -f docker-compose.dev.yml ps


