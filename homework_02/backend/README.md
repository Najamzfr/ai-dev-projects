# Snake Game Backend API

Backend API for the Snake Game leaderboard system.

## Features

- RESTful API with FastAPI
- SQLAlchemy async ORM with database support
- Alembic database migrations
- Leaderboard management (GET, POST)
- User score tracking
- Pagination and filtering
- Request validation with Pydantic
- Structured logging
- Error handling
- Health check endpoints

## Setup

### Prerequisites

- Python 3.12+
- uv (recommended) or pip

### Installation

1. Install dependencies:
```bash
uv sync
# or
pip install -e .
```

2. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

3. Initialize database and run migrations:
```bash
# Create initial migration (first time only)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

4. (Optional) Seed database with test data:
```bash
python -m scripts.seed_db
```

5. Run the server:
```bash
uvicorn main:app --reload
# or
python main.py
```

The API will be available at `http://localhost:8000`

## Database

### SQLite (Development)
The default configuration uses SQLite for development. The database file will be created at `./snake_game.db`.

### PostgreSQL (Production)
To use PostgreSQL, update your `.env` file:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/snake_game
```

### Migrations

See [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) for detailed migration instructions.

Quick commands:
```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /health` - Basic health check
- `GET /health/db` - Database health check

### Leaderboard
- `GET /api/v1/leaderboard` - Get leaderboard entries (with pagination and filtering)
  - Query params: `limit`, `offset`, `mode`, `sort`
- `POST /api/v1/leaderboard` - Submit a new score
- `GET /api/v1/leaderboard/{username}` - Get scores for a specific user
- `GET /api/v1/leaderboard/stats/summary` - Get aggregate statistics

## Development

### Code Quality

Install dev dependencies:
```bash
uv sync --extra dev
```

Run formatters:
```bash
black .
isort .
```

Run type checking:
```bash
mypy .
```

Run linter:
```bash
ruff check .
```

### Pre-commit Hooks

Install pre-commit:
```bash
pip install pre-commit
pre-commit install
```

### Testing

Run tests:
```bash
pytest
```

## Project Structure

```
backend/
├── alembic/              # Database migrations
│   ├── versions/        # Migration files
│   ├── env.py          # Alembic environment
│   └── script.py.mako  # Migration template
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── leaderboard.py
│   │       └── router.py
│   ├── config.py          # Configuration management
│   ├── database.py        # Database setup
│   ├── exceptions.py      # Custom exceptions
│   ├── logging_config.py  # Logging setup
│   ├── middleware.py      # Request/response middleware
│   ├── models.py          # Pydantic models
│   ├── models_db.py       # SQLAlchemy models
│   ├── repository_db.py   # Database repository
│   ├── security.py        # Security utilities
│   └── services.py        # Business logic layer
├── scripts/
│   └── seed_db.py         # Database seeding script
├── tests/
│   ├── conftest.py        # Test configuration
│   ├── test_api.py        # API endpoint tests
│   ├── test_models.py     # Model tests
│   ├── test_repository.py # Repository tests
│   └── test_services.py   # Service tests
├── alembic.ini            # Alembic configuration
├── main.py                # Application entry point
└── pyproject.toml         # Project configuration
```

## Environment Variables

See `.env.example` for all available environment variables.

Key variables:
- `DATABASE_URL` - Database connection string
- `PORT` - Server port (default: 8000)
- `CORS_ORIGINS` - Allowed CORS origins
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FORMAT` - Log format (json, text)

## License

MIT
