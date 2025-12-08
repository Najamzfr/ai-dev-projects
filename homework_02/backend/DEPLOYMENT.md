# Deployment Guide

This guide covers deploying the Snake Game Backend API to production.

## Prerequisites

- Python 3.12+
- PostgreSQL database (or SQLite for small deployments)
- Server with systemd (for Linux) or similar process manager
- Domain name and SSL certificate (recommended)

## Environment Setup

### 1. Create Production Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# or with uv
uv sync
```

### 2. Configure Environment Variables

Create a `.env` file with production settings:

```env
# Server
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=production

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/snake_game
DATABASE_POOL_SIZE_MIN=10
DATABASE_POOL_SIZE_MAX=50

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ALLOW_CREDENTIALS=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Security
RATE_LIMIT_PER_MINUTE=60
MAX_SCORE=999999
MIN_SCORE=0
```

### 3. Database Setup

#### PostgreSQL Setup

```bash
# Create database
createdb snake_game

# Run migrations
alembic upgrade head

# (Optional) Seed initial data
python -m scripts.seed_db
```

#### SQLite (Not Recommended for Production)

```bash
# Run migrations
alembic upgrade head
```

## Deployment Options

### Option 1: Systemd Service (Linux)

Create `/etc/systemd/system/snake-game-api.service`:

```ini
[Unit]
Description=Snake Game API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/snake-game-api/backend
Environment="PATH=/opt/snake-game-api/venv/bin"
ExecStart=/opt/snake-game-api/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable snake-game-api
sudo systemctl start snake-game-api
sudo systemctl status snake-game-api
```

### Option 2: Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install uv && uv sync

# Copy application
COPY . .

# Run migrations and start server
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
```

Build and run:
```bash
docker build -t snake-game-api .
docker run -d -p 8000:8000 --env-file .env snake-game-api
```

### Option 3: Cloud Platforms

#### Heroku

```bash
# Install Heroku CLI
heroku create snake-game-api

# Set environment variables
heroku config:set DATABASE_URL=postgresql://...
heroku config:set ENVIRONMENT=production

# Deploy
git push heroku main

# Run migrations
heroku run alembic upgrade head
```

#### Railway

1. Connect your GitHub repository
2. Set environment variables in dashboard
3. Railway will automatically deploy on push

#### AWS/GCP/Azure

Use their respective container services (ECS, Cloud Run, Container Instances) with the Dockerfile above.

## Reverse Proxy (Nginx)

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## SSL/TLS Setup

Use Let's Encrypt with Certbot:

```bash
sudo certbot --nginx -d api.yourdomain.com
```

## Monitoring

### Health Checks

Monitor these endpoints:
- `GET /health` - Basic health check
- `GET /health/db` - Database health check

### Logging

Logs are written to stdout in JSON format. Use a log aggregation service:
- **Cloud**: CloudWatch, Stackdriver, Azure Monitor
- **Self-hosted**: ELK Stack, Loki, Grafana

### Metrics

Consider adding:
- Prometheus metrics endpoint
- Application Performance Monitoring (APM)
- Error tracking (Sentry, Rollbar)

## Backup Strategy

### Database Backups

```bash
# PostgreSQL
pg_dump snake_game > backup_$(date +%Y%m%d).sql

# Restore
psql snake_game < backup_20240115.sql
```

### Automated Backups

Set up cron job:
```bash
0 2 * * * pg_dump snake_game > /backups/snake_game_$(date +\%Y\%m\%d).sql
```

## Security Checklist

- [ ] Use strong database passwords
- [ ] Enable SSL/TLS
- [ ] Configure proper CORS origins
- [ ] Set up rate limiting
- [ ] Use environment variables for secrets
- [ ] Keep dependencies updated
- [ ] Regular security audits
- [ ] Enable firewall rules
- [ ] Use non-root user for service
- [ ] Regular backups

## Scaling

### Horizontal Scaling

Run multiple instances behind a load balancer:
- Use a shared PostgreSQL database
- Configure session affinity if needed
- Use Redis for shared caching (optional)

### Vertical Scaling

Increase server resources:
- More CPU cores
- More RAM
- Faster database storage (SSD)

## Troubleshooting

### Check Logs

```bash
# Systemd
sudo journalctl -u snake-game-api -f

# Docker
docker logs snake-game-api

# Direct
tail -f logs/app.log
```

### Database Connection Issues

```bash
# Test connection
psql $DATABASE_URL

# Check migrations
alembic current
alembic history
```

### Performance Issues

1. Check database query performance
2. Review connection pool settings
3. Monitor resource usage (CPU, memory)
4. Check for slow queries in logs

## Rollback Procedure

If deployment fails:

1. Stop the service
2. Restore previous code version
3. Rollback database migration if needed:
   ```bash
   alembic downgrade -1
   ```
4. Restart service
5. Verify health endpoints

## Maintenance

### Regular Tasks

- Update dependencies monthly
- Review and rotate secrets quarterly
- Test backup restoration quarterly
- Security audit annually

### Updates

1. Test in staging first
2. Backup database
3. Deploy to production
4. Run migrations
5. Monitor health endpoints
6. Verify functionality

