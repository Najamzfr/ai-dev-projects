FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Copy application code
COPY . .

# Create a startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Waiting for database to be ready..."\n\
while ! pg_isready -h postgres -U snake_user -d snake_game > /dev/null 2>&1; do\n\
  sleep 1\n\
done\n\
echo "Database is ready!"\n\
echo "Running database migrations..."\n\
uv run alembic upgrade head\n\
echo "Starting application..."\n\
uv run uvicorn main:app --host 0.0.0.0 --port 8000\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["/app/start.sh"]

