.PHONY: run-dev test docker-dev docker-down logs help migrate-new migrate-up

# Run app in dev mode with .env.local
run-dev:
	@echo "🚀 Running FastAPI app in development mode..."
	python -m dotenv -f .env.local run -- uvicorn src.quotes_api.main:app --reload

# Run tests with .env.test (uses SQLite by default)
test:
	@echo "🧪 Running tests..."
	pytest -v --maxfail=1 --disable-warnings

# Start Docker services (Postgres + pgAdmin)
docker-dev:
	@echo "🐳 Starting Docker containers..."
	docker-compose up -d

# Stop and remove Docker services
docker-down:
	@echo "🧹 Stopping and cleaning up Docker containers..."
	docker-compose down -v

# Tail logs from Docker
logs:
	@echo "📜 Showing logs from Docker services..."
	docker-compose logs -f

# Create a new Alembic migration
migrate-new:
	@echo "🗺️  Creating new database migration..."
	python -m dotenv -f .env.local run -- alembic revision --autogenerate -m "$(m)"

# Apply migrations to the database
migrate-up:
	@echo "🏗️  Applying database migrations..."
	python -m dotenv -f .env.local run -- alembic upgrade head

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make run-dev       🚀 Run FastAPI app in dev mode (uvicorn + .env.local)"
	@echo "  make test          🧪 Run tests with .env.test (SQLite)"
	@echo "  make docker-dev    🐳 Start Postgres + pgAdmin in Docker"
	@echo "  make docker-down   🧹 Stop and clean Docker containers"
	@echo "  make logs          📜 Tail Docker logs"
	@echo "  make migrate-new   🗺️  Create a new database migration (e.g., make migrate-new m=\"add_users\")"
	@echo "  make migrate-up    🏗️  Apply database migrations"
	@echo "  make help          📖 Show this help message"