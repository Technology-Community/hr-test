# FastAPI Backend Application

A modern FastAPI backend application with PostgreSQL, following clean architecture principles.

## Prerequisites

- Docker and Docker Compose
- Make

## Installation & Running

```bash
# Clone the repository
git clone <repository-url>
cd hr-test

# Create .env file from example
cp .env.example .env

# (Optional) Edit .env file to customize settings
# vim .env

# Build and start all services
make dev
```

That's it! The application will be available at:
- API Documentation: http://localhost:8080/docs
- Health Check: http://localhost:8080/health-check

## Common Commands

```bash
# Development
make dev          # Build and start services
make up           # Start services
make down         # Stop services
make restart      # Restart services

# Code Quality
make format       # Format code
make lint         # Run linting
make typecheck    # Run type checking
make fix          # Format and fix all issues

# Testing
make test         # Run unit tests
make test-cov     # Run tests with coverage report
make test-all     # Run all tests (unit + e2e)
make ci           # Run full CI pipeline (format, lint, typecheck, test)

# Database
make db-reset     # Reset PostgreSQL database
make shell-db     # Access PostgreSQL shell

# Utilities
make shell        # Access Python container shell
make health       # Check application health
```

## Technology Stack

- FastAPI with async support
- PostgreSQL with SQLAlchemy and SQLModel
- Docker & Docker Compose
- Python 3.12+
- pytest for testing
- Ruff for formatting and linting
- Pyright for type checking

## API Endpoints

- `GET /health-check` - Application health status
- `GET /version` - Application version
- `GET /docs` - Interactive API documentation

Full API documentation available at http://localhost:8080/docs

## Environment Configuration

### Quick Setup

```bash
# Copy example environment file
cp .env.example .env
```

The `.env.example` file includes all required settings with default values. For development, you can use it as-is.

### Environment Variables Reference

```env
# Application Configuration
APP_NAME=hr-app-test
APP_VERSION=0.1.0
APP_DESCRIPTION="Template for HR application use FastAPI"

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Environment Configuration
ENVIRONMENT=development    # Options: development, staging, production
DEBUG=false

# Security Configuration
SECRET_KEY=your-secret-key-change-in-production
CORS_ORIGINS=["*"]

# PostgreSQL Configuration
POSTGRES_USER=admin
POSTGRES_PASSWORD=example
POSTGRES_DB=database_develop
POSTGRES_HOST=postgresql
POSTGRES_PORT=5432

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Rate Limiting Configuration
RATE_LIMIT=10

# Logging Configuration
LOG_LEVEL=INFO    # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

⚠️ **Important:** Change `SECRET_KEY` in production environments!

## Project Structure

```
app/
├── configs/          # Configuration modules
├── dependencies/     # Middleware and dependency injection
├── internal/         # Domain/business logic
│   ├── dtos/         # Data Transfer Objects
│   ├── exceptions/   # Domain exceptions
│   ├── models/       # PostgreSQL models
│   ├── repositories/ # Data access layer
│   └── services/     # Business logic
├── routers/          # API endpoints
├── tests/            # Test suite
└── main.py           # Application entry point
```

## Testing

### Running Tests

All tests run inside Docker containers:

```bash
# Run unit tests only
make test

# Run tests with coverage report
make test-cov

# Run all tests (unit + e2e)
make test-all

# Run full CI pipeline (recommended before commits)
make ci
```

### Test Structure

```
app/tests/
├── unit/                    # Unit tests with mocks
│   └── test_employee_service.py
├── e2e/                     # End-to-end integration tests
└── conftest.py              # Shared test fixtures
```

### Writing Tests

- Unit tests: Mock external dependencies (database, repositories)
- E2E tests: Test full integration with real database
- Use `pytest` fixtures for reusable test data
- Follow existing test patterns in `app/tests/unit/`

### Test Coverage

View coverage report after running `make test-cov`:
- HTML report: `htmlcov/index.html`
- Terminal summary displayed after test run

## Notes

- All commands run in Docker containers
- Never run Python commands locally
- Use `make` commands for all operations
- Always copy `.env.example` to `.env` before starting