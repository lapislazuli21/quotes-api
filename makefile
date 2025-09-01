.PHONY: run-dev test docker-dev docker-down logs help

# Run app in dev mode with .env.dev
run-dev:
	@echo "Running FastAPI app in development mode..."
	uv run uvicorn quotes_api.main:app --reload --app-dir src --env-file .env.dev

# Run tests with .env.test (uses SQLite by default)
test:
	@echo "Running tests..."
	pytest -v --maxfail=1 --disable-warnings

# Start Docker services (Postgres + pgAdmin)
docker-dev:
	@echo "Starting Docker containers..."
	docker-compose up -d

# Stop and remove Docker services
docker-down:
	@echo "Stopping and cleaning up Docker containers..."
	docker-compose down -v

# Tail logs from Docker
logs:
	@echo "Showing logs from Docker services..."
	docker-compose logs -f

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make run-dev       Run FastAPI app in dev mode (uv + .env.dev)"
	@echo "  make test          Run pytest with .env.test (SQLite)"
	@echo "  make docker-dev    Start Postgres + pgAdmin in Docker"
	@echo "  make docker-down   Stop and clean Docker containers"
	@echo "  make logs          Tail Docker logs"
	@echo "  make help          Show this help message"
