# Makefile for backend-fastapi-app (Docker-first)

# Default shell
SHELL := /bin/bash

# Docker compose configuration
DOCKER_COMPOSE_DEV := docker-compose -f docker-compose.development.yaml
DOCKER_COMPOSE_PROD := docker-compose -f docker-compose.production.yaml
APP_CONTAINER := backend-fastapi-app-server_python

# Colors for output
BOLD := \033[1m
RESET := \033[0m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
BLUE := \033[34m

# Default target
.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help message
	@echo "$(BOLD)FastAPI Backend Commands (Docker-first)$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BLUE)%-20s$(RESET) %s\n", $$1, $$2}'

# Environment Setup
.PHONY: build
build: ## Build docker images
	@echo "$(GREEN)Building docker images...$(RESET)"
	$(DOCKER_COMPOSE_DEV) build

.PHONY: up
up: ## Start all services (development)
	@echo "$(GREEN)Starting development services...$(RESET)"
	$(DOCKER_COMPOSE_DEV) up -d

.PHONY: up-logs
up-logs: ## Start all services with logs (development)
	@echo "$(GREEN)Starting development services with logs...$(RESET)"
	$(DOCKER_COMPOSE_DEV) up

.PHONY: down
down: ## Stop all services
	@echo "$(YELLOW)Stopping all services...$(RESET)"
	$(DOCKER_COMPOSE_DEV) down

.PHONY: restart
restart: down up ## Restart all services
	@echo "$(GREEN)Services restarted!$(RESET)"

.PHONY: rebuild
rebuild: down build up ## Rebuild and restart all services
	@echo "$(GREEN)Services rebuilt and restarted!$(RESET)"

# Code Quality (runs inside Docker)
.PHONY: format
format: ## Format code with ruff (in Docker)
	@echo "$(GREEN)Formatting code with ruff...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run ruff format

.PHONY: format-check
format-check: ## Check code formatting (in Docker)
	@echo "$(YELLOW)Checking code formatting...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run ruff format --check

.PHONY: lint
lint: ## Run linting with ruff (in Docker)
	@echo "$(YELLOW)Running ruff linter...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run ruff check

.PHONY: lint-fix
lint-fix: ## Run linting with auto-fix (in Docker)
	@echo "$(GREEN)Running ruff linter with auto-fix...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run ruff check --fix

.PHONY: typecheck
typecheck: ## Run type checking with pyright (in Docker)
	@echo "$(YELLOW)Running type checking with pyright...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run pyright

.PHONY: check
check: format-check lint typecheck ## Run all code quality checks (in Docker)
	@echo "$(GREEN)All code quality checks completed!$(RESET)"

.PHONY: fix
fix: format lint-fix ## Format and fix all code issues (in Docker)
	@echo "$(GREEN)Code formatting and linting completed!$(RESET)"

# Testing (runs inside Docker)
.PHONY: test
test: ## Run unit tests (in Docker)
	@echo "$(GREEN)Running unit tests...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run pytest app/tests/unit/ -v

.PHONY: test-cov
test-cov: ## Run unit tests with coverage report (in Docker)
	@echo "$(GREEN)Running unit tests with coverage...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run pytest app/tests/unit/ --cov=app --cov-report=term-missing --cov-report=html

.PHONY: test-integration
test-integration: ## Run integration tests (in Docker)
	@echo "$(GREEN)Running integration tests...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run pytest app/tests/e2e/ -v

.PHONY: test-all
test-all: ## Run all tests (in Docker)
	@echo "$(GREEN)Running all tests...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run pytest app/tests/ -v

.PHONY: test-watch
test-watch: ## Run tests in watch mode (in Docker)
	@echo "$(GREEN)Running tests in watch mode...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run pytest app/tests/unit/ -v --tb=short -x --lf

# Installation and Dependencies (in Docker)
.PHONY: install
install: ## Install dependencies (in Docker)
	@echo "$(GREEN)Installing dependencies...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry install --no-root

.PHONY: install-dev
install-dev: ## Install dependencies including dev tools (in Docker)
	@echo "$(GREEN)Installing dependencies with dev tools...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry install --no-root --with dev

.PHONY: update
update: ## Update dependencies (in Docker)
	@echo "$(GREEN)Updating dependencies...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry update

# Shell Access
.PHONY: shell
shell: ## Access Python container shell
	@echo "$(GREEN)Accessing Python container shell...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python bash

.PHONY: shell-python
shell-python: ## Access Python REPL (in Docker)
	@echo "$(GREEN)Accessing Python REPL...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python python

.PHONY: shell-postgres
shell-postgres: ## Access PostgreSQL shell
	@echo "$(GREEN)Accessing PostgreSQL shell...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec postgresql psql -U admin -d database_develop

# Logs and Monitoring
.PHONY: logs
logs: ## Show application logs
	@echo "$(GREEN)Showing application logs...$(RESET)"
	$(DOCKER_COMPOSE_DEV) logs -f python

.PHONY: logs-db
logs-db: ## Show PostgreSQL logs
	@echo "$(GREEN)Showing PostgreSQL logs...$(RESET)"
	$(DOCKER_COMPOSE_DEV) logs -f postgresql

.PHONY: logs-all
logs-all: ## Show all services logs
	@echo "$(GREEN)Showing all services logs...$(RESET)"
	$(DOCKER_COMPOSE_DEV) logs -f

.PHONY: status
status: ## Show services status
	@echo "$(GREEN)Services status:$(RESET)"
	$(DOCKER_COMPOSE_DEV) ps

# Database Management
.PHONY: db-up
db-up: ## Start only PostgreSQL
	@echo "$(GREEN)Starting PostgreSQL...$(RESET)"
	$(DOCKER_COMPOSE_DEV) up -d postgresql

.PHONY: db-down
db-down: ## Stop PostgreSQL
	@echo "$(YELLOW)Stopping PostgreSQL...$(RESET)"
	$(DOCKER_COMPOSE_DEV) stop postgresql

.PHONY: db-reset
db-reset: ## Reset PostgreSQL data (WARNING: deletes all data)
	@echo "$(RED)Resetting PostgreSQL data...$(RESET)"
	$(DOCKER_COMPOSE_DEV) down postgresql
	docker volume rm hr-app-test_postgresql_volume || true
	$(DOCKER_COMPOSE_DEV) up -d postgresql

.PHONY: shell-db
shell-db: ## Access PostgreSQL shell
	@echo "$(GREEN)Accessing PostgreSQL shell...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec postgresql psql -U admin -d database_develop

# Database Migrations
.PHONY: migrate-generate
migrate-generate: ## Generate new migration (usage: make migrate-generate MESSAGE="your message")
	@echo "$(GREEN)Generating new migration...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run alembic revision --autogenerate -m "$(MESSAGE)"

.PHONY: migrate-up
migrate-up: ## Apply all pending migrations
	@echo "$(GREEN)Applying migrations...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run alembic upgrade head

.PHONY: migrate-down
migrate-down: ## Rollback one migration
	@echo "$(YELLOW)Rolling back one migration...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run alembic downgrade -1

.PHONY: migrate-history
migrate-history: ## Show migration history
	@echo "$(BLUE)Migration history:$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run alembic history

.PHONY: migrate-current
migrate-current: ## Show current migration version
	@echo "$(BLUE)Current migration:$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run alembic current

.PHONY: migrate-reset
migrate-reset: ## Reset all migrations (WARNING: destroys all data)
	@echo "$(RED)Resetting all migrations...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run alembic downgrade base

# Database Seeding
.PHONY: seed
seed: ## Seed database with sample data
	@echo "$(GREEN)Seeding database with sample data...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python python app/database/seeds/seed_runner.py seed

.PHONY: seed-clear
seed-clear: ## Clear all seeded data (WARNING: removes sample data)
	@echo "$(YELLOW)Clearing all seeded data...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python python app/database/seeds/seed_runner.py clear

.PHONY: reseed
reseed: seed-clear seed ## Clear and reseed database with fresh sample data

# Production Commands
.PHONY: prod-build
prod-build: ## Build production images
	@echo "$(GREEN)Building production images...$(RESET)"
	$(DOCKER_COMPOSE_PROD) build

.PHONY: prod-up
prod-up: ## Start production services
	@echo "$(GREEN)Starting production services...$(RESET)"
	$(DOCKER_COMPOSE_PROD) up -d

.PHONY: prod-down
prod-down: ## Stop production services
	@echo "$(YELLOW)Stopping production services...$(RESET)"
	$(DOCKER_COMPOSE_PROD) down

.PHONY: prod-logs
prod-logs: ## Show production logs
	@echo "$(GREEN)Showing production logs...$(RESET)"
	$(DOCKER_COMPOSE_PROD) logs -f

# Cleanup
.PHONY: clean
clean: ## Clean Docker containers and images
	@echo "$(YELLOW)Cleaning Docker containers and images...$(RESET)"
	$(DOCKER_COMPOSE_DEV) down --rmi local --volumes --remove-orphans
	docker system prune -f

.PHONY: clean-all
clean-all: ## Deep clean Docker (WARNING: removes all containers, images, volumes)
	@echo "$(RED)Deep cleaning Docker...$(RESET)"
	$(DOCKER_COMPOSE_DEV) down --rmi all --volumes --remove-orphans
	$(DOCKER_COMPOSE_PROD) down --rmi all --volumes --remove-orphans
	docker system prune -a -f --volumes

.PHONY: clean-cache
clean-cache: ## Clean Python cache files (in Docker)
	@echo "$(YELLOW)Cleaning Python cache files...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python find . -type f -name "*.pyc" -delete
	$(DOCKER_COMPOSE_DEV) exec python find . -type d -name "__pycache__" -delete
	$(DOCKER_COMPOSE_DEV) exec python find . -type d -name ".pytest_cache" -exec rm -rf {} +

# Development Workflow
.PHONY: dev
dev: build up logs ## Full development setup (build, up, logs)

.PHONY: dev-reset
dev-reset: down clean-cache up ## Reset development environment

.PHONY: ci
ci: build up test-cov check ## Run CI pipeline (build, up, test with coverage, check)
	@echo "$(GREEN)CI pipeline completed successfully!$(RESET)"

.PHONY: verify
verify: ## Quick verification (ensure services are up, run checks and tests)
	@echo "$(GREEN)Verifying services...$(RESET)"
	@$(DOCKER_COMPOSE_DEV) ps
	@$(MAKE) check test
	@echo "$(GREEN)Verification completed successfully!$(RESET)"

# Health Checks
.PHONY: health
health: ## Check application health
	@echo "$(GREEN)Checking application health...$(RESET)"
	@curl -f http://localhost:8080/health-check || echo "$(RED)Health check failed$(RESET)"

.PHONY: ping-db
ping-db: ## Ping PostgreSQL
	@echo "$(GREEN)Pinging PostgreSQL...$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec postgresql pg_isready -U admin -d database_develop

# Utilities
.PHONY: version
version: ## Show application version (in Docker)
	@echo "$(BLUE)Application version:$(RESET)"
	$(DOCKER_COMPOSE_DEV) exec python poetry run python -c "from app.configs.version import get_app_version; print(get_app_version())"

.PHONY: docs
docs: ## Show API documentation URLs
	@echo "$(GREEN)API documentation available at: http://localhost:8080/docs$(RESET)"
	@echo "$(GREEN)ReDoc documentation available at: http://localhost:8080/redoc$(RESET)"
