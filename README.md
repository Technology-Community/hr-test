# FastAPI Backend Application

A modern FastAPI backend application with PostgreSQL, following clean architecture principles.

## Prerequisites

- Docker and Docker Compose
- Make

## Installation & Running

### First Time Setup

```bash
# 1. Clone the repository
git clone <repository-url>
cd hr-test

# 2. Create .env file from example
cp .env.example .env

# 3. (Optional) Edit .env file to customize settings
# vim .env

# 4. Build and start all services
make build
make up

# 5. Run database migrations
make migrate-up

# 6. Seed database with sample data (optional but recommended for development)
make seed
```

### Subsequent Runs

```bash
# Start services
make dev

# Or just start without logs
make up
```

The application will be available at:
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
make db-reset     # Reset PostgreSQL database (WARNING: deletes all data)
make shell-db     # Access PostgreSQL shell

# Database Migrations
make migrate-up          # Apply all pending migrations
make migrate-down        # Rollback one migration
make migrate-generate    # Generate new migration (usage: make migrate-generate MESSAGE="your message")
make migrate-history     # Show migration history
make migrate-current     # Show current migration version

# Database Seeding
make seed         # Seed database with sample data
make seed-clear   # Clear all seeded data
make reseed       # Clear and reseed with fresh data

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
├── database/         # Database migrations and seeds
│   ├── migrations/   # Alembic migrations
│   └── seeds/        # Database seeding scripts
├── dependencies/     # Middleware and dependency injection
├── internal/         # Domain/business logic
│   ├── dtos/         # Data Transfer Objects
│   ├── exceptions/   # Domain exceptions
│   ├── models/       # PostgreSQL models
│   ├── repositories/ # Data access layer
│   └── services/     # Business logic
├── routers/          # API endpoints
├── tests/            # Test suite
│   ├── unit/         # Unit tests
│   └── e2e/          # End-to-end tests
└── main.py           # Application entry point
```

## Database Management

### Migrations

The project uses Alembic for database migrations:

```bash
# Apply all pending migrations (run after first setup)
make migrate-up

# Generate a new migration after model changes
make migrate-generate MESSAGE="add employee table"

# Rollback the last migration
make migrate-down

# View migration history
make migrate-history

# Check current migration version
make migrate-current
```

### Seeding Data

For development, you can populate the database with sample data:

```bash
# Seed database with sample organizations and employees
make seed

# Clear all seeded data
make seed-clear

# Reseed (clear and seed again with fresh data)
make reseed
```

**Seed Data Includes:**
- Sample organizations
- Sample employees with various statuses, departments, and locations
- Organization configurations for column visibility

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

## Troubleshooting

### First Time Setup Issues

**Problem:** Application won't start or shows database errors

**Solution:**
```bash
# Make sure migrations are applied
make migrate-up

# Check database is running
make ping-db

# View logs to see what's wrong
make logs
```

**Problem:** Port 8080 already in use

**Solution:** Change the `PORT` in your `.env` file to a different port (e.g., 8000, 8888)

### Database Issues

**Problem:** Need to reset everything

**Solution:**
```bash
# Stop services
make down

# Reset database
make db-reset

# Start services and reapply migrations
make up
make migrate-up
make seed
```

## Notes

- ✅ All commands run in Docker containers
- ✅ Never run Python commands locally
- ✅ Use `make` commands for all operations
- ✅ Always copy `.env.example` to `.env` before starting
- ✅ Run `make migrate-up` after first setup
- ✅ Use `make seed` to populate sample data for development