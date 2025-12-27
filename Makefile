.PHONY: help install install-dev clean lint format test test-cov type-check pre-commit run docker-build docker-up docker-down all

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ General

help: ## Display this help message
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Agentic AI on WatsonX with MCP Gateway - Makefile Help$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make $(YELLOW)<target>$(NC)\n\n"} \
		/^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } \
		/^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════$(NC)"

##@ Installation & Setup

install: ## Install production dependencies using uv
	@echo "$(GREEN)Installing production dependencies...$(NC)"
	@command -v uv >/dev/null 2>&1 || { echo "$(RED)Error: uv is not installed. Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh$(NC)"; exit 1; }
	uv sync --no-dev
	@echo "$(GREEN)✓ Production dependencies installed successfully$(NC)"

install-dev: ## Install all dependencies including dev tools using uv
	@echo "$(GREEN)Installing all dependencies (including dev tools)...$(NC)"
	@command -v uv >/dev/null 2>&1 || { echo "$(RED)Error: uv is not installed. Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh$(NC)"; exit 1; }
	uv sync
	@echo "$(GREEN)✓ All dependencies installed successfully$(NC)"

setup: install-dev ## Complete setup including pre-commit hooks
	@echo "$(GREEN)Setting up pre-commit hooks...$(NC)"
	uv run pre-commit install
	@echo "$(GREEN)✓ Development environment setup complete$(NC)"

##@ Code Quality

lint: ## Run linting checks with ruff
	@echo "$(GREEN)Running ruff linter...$(NC)"
	uv run ruff check agentic_ai tests
	@echo "$(GREEN)✓ Linting complete$(NC)"

format: ## Format code with black and isort
	@echo "$(GREEN)Formatting code with black...$(NC)"
	uv run black agentic_ai tests
	@echo "$(GREEN)Sorting imports with isort...$(NC)"
	uv run isort agentic_ai tests
	@echo "$(GREEN)✓ Code formatting complete$(NC)"

format-check: ## Check code formatting without modifying files
	@echo "$(GREEN)Checking code format...$(NC)"
	uv run black --check agentic_ai tests
	uv run isort --check-only agentic_ai tests
	@echo "$(GREEN)✓ Format check complete$(NC)"

type-check: ## Run type checking with mypy
	@echo "$(GREEN)Running type checks with mypy...$(NC)"
	uv run mypy agentic_ai
	@echo "$(GREEN)✓ Type checking complete$(NC)"

pre-commit: ## Run all pre-commit hooks
	@echo "$(GREEN)Running pre-commit hooks...$(NC)"
	uv run pre-commit run --all-files
	@echo "$(GREEN)✓ Pre-commit checks complete$(NC)"

check-all: format-check lint type-check ## Run all code quality checks
	@echo "$(GREEN)✓ All quality checks passed$(NC)"

##@ Testing

test: ## Run tests with pytest
	@echo "$(GREEN)Running tests...$(NC)"
	uv run pytest tests/ -v
	@echo "$(GREEN)✓ Tests complete$(NC)"

test-cov: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	uv run pytest tests/ -v --cov --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/index.html$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(GREEN)Running tests in watch mode...$(NC)"
	uv run pytest-watch tests/

##@ Application

run: ## Run the application server
	@echo "$(GREEN)Starting Agentic AI server...$(NC)"
	uv run agentic-server

cli: ## Run the CLI application
	@echo "$(GREEN)Starting Agentic AI CLI...$(NC)"
	uv run agentic-ai --help

demo: ## Run a demo workflow
	@echo "$(GREEN)Running demo workflow...$(NC)"
	uv run agentic-ai demo

##@ Docker

docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t agentic-ai-watsonx-mcp:latest .
	@echo "$(GREEN)✓ Docker image built$(NC)"

docker-up: ## Start all services with docker-compose
	@echo "$(GREEN)Starting services with docker-compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Services started$(NC)"
	@echo "$(YELLOW)Gateway UI: http://localhost:8080$(NC)"
	@echo "$(YELLOW)Gateway API: http://localhost:8080/docs$(NC)"

docker-down: ## Stop all services
	@echo "$(YELLOW)Stopping services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Services stopped$(NC)"

docker-logs: ## View docker-compose logs
	docker-compose logs -f

docker-ps: ## Show running containers
	docker-compose ps

##@ Database

db-upgrade: ## Run database migrations
	@echo "$(GREEN)Running database migrations...$(NC)"
	uv run alembic upgrade head
	@echo "$(GREEN)✓ Database upgraded$(NC)"

db-downgrade: ## Rollback last database migration
	@echo "$(YELLOW)Rolling back last migration...$(NC)"
	uv run alembic downgrade -1

db-reset: ## Reset database (WARNING: destructive)
	@echo "$(RED)Resetting database...$(NC)"
	rm -f agentic_ai.db
	uv run alembic upgrade head
	@echo "$(GREEN)✓ Database reset complete$(NC)"

##@ Cleanup

clean: ## Remove build artifacts and cache files
	@echo "$(YELLOW)Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

clean-all: clean ## Remove all generated files including venv
	@echo "$(YELLOW)Removing virtual environment...$(NC)"
	rm -rf .venv
	@echo "$(GREEN)✓ Full cleanup complete$(NC)"

##@ Development

shell: ## Start interactive Python shell with context
	@echo "$(GREEN)Starting interactive shell...$(NC)"
	uv run ipython

notebook: ## Start Jupyter notebook
	@echo "$(GREEN)Starting Jupyter notebook...$(NC)"
	uv run jupyter notebook

build: ## Build package distributions
	@echo "$(GREEN)Building package...$(NC)"
	uv build
	@echo "$(GREEN)✓ Package built in dist/$(NC)"

##@ Comprehensive Targets

all: clean install-dev check-all test ## Run complete workflow: clean, install, check, and test
	@echo "$(GREEN)✓ Complete workflow finished successfully$(NC)"

ci: format-check lint type-check test-cov ## Run CI pipeline checks
	@echo "$(GREEN)✓ CI pipeline checks passed$(NC)"

dev-init: ## Initialize development environment from scratch
	@command -v uv >/dev/null 2>&1 || { echo "$(RED)Installing uv...$(NC)"; curl -LsSf https://astral.sh/uv/install.sh | sh; }
	make install-dev
	make setup
	cp .env.example .env || echo "$(YELLOW)Note: .env.example not found, skipping .env creation$(NC)"
	@echo "$(GREEN)✓ Development environment initialized$(NC)"
	@echo "$(BLUE)Next steps:$(NC)"
	@echo "  1. Edit .env with your configuration"
	@echo "  2. Run 'make docker-up' to start services"
	@echo "  3. Run 'make test' to verify installation"
