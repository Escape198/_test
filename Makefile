# Makefile

ENV_FILE=.env

.DEFAULT_GOAL := up

print-start:
	@echo "🔧 Starting Wallet API Project..."

create-env:
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "DEBUG=True" > $(ENV_FILE); \
		echo "SECRET_KEY=dev-key" >> $(ENV_FILE); \
		echo "DATABASE_URL=postgres://postgres:postgres@db:5432/postgres" >> $(ENV_FILE); \
		echo "✅ .env created"; \
	else \
		echo "⚠️  .env already exists"; \
	fi

down:
	@echo "🛑 Stopping and removing containers..."
	docker compose down --remove-orphans

up: print-start create-env down
	@echo "🚀 Building and starting containers..."
	docker compose up --build

lint:
	@echo "🧹 Running formatters and linters..."
	black . && isort . && flake8

test:
	@echo "🧪 Running tests..."
	docker compose exec web pytest
