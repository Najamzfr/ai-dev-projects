# Docker Setup for Snake Game

This project is fully dockerized with Docker Compose, including PostgreSQL database, FastAPI backend, and React frontend served with nginx.

## 🐳 Quick Start

### Prerequisites
- Docker (20.10+)
- Docker Compose (2.0+)

### First Time Setup

```bash
# Build all containers
docker-compose build

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Seed database with demo data (optional)
docker-compose exec backend uv run python -m scripts.seed_db
```

### Access Your Application

- **Frontend:** http://localhost
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc
- **Database:** localhost:5432
  - User: `snake_user`
  - Password: `snake_password_change_in_production`
  - Database: `snake_game`

## 📋 Available Commands

### Using Make (recommended)

```bash
make help           # Show all available commands
make build          # Build all containers
make up             # Start all services
make down           # Stop all services
make logs           # View logs from all services
make ps             # List running containers
make restart        # Restart all services
make clean          # Remove containers and volumes (WARNING: deletes data)
make shell-backend  # Access backend container shell
make shell-frontend # Access frontend container shell
make migrate        # Run database migrations
make seed           # Seed database with demo data
```

### Using Docker Compose directly

```bash
# Build containers
docker-compose build

# Start services (detached)
docker-compose up -d

# Start services (with logs)
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# List running containers
docker-compose ps

# Execute command in container
docker-compose exec backend /bin/bash
docker-compose exec frontend /bin/sh

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose up -d --build

# Remove everything including volumes (WARNING: deletes database)
docker-compose down -v
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                   User Browser                  │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │   nginx (port 80)    │
          │   Frontend (React)   │
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Backend (port 8000) │
          │    FastAPI + uv      │
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ PostgreSQL (port 5432)│
          │   postgres:15-alpine │
          └──────────────────────┘
```

## 🔧 Configuration

### Environment Variables

The main configuration is in `docker-compose.yml`. For production, you should:

1. **Change database password:**
   ```yaml
   POSTGRES_PASSWORD: your_secure_password_here
   ```

2. **Update CORS origins:**
   ```yaml
   CORS_ORIGINS: '["https://yourdomain.com"]'
   ```

3. **Update frontend API URL:**
   ```yaml
   args:
     VITE_API_URL: https://api.yourdomain.com
   ```

### Production Environment File

Copy and modify `.env.production` for production use:

```bash
cp .env.production .env
# Edit .env with your production values
```

## 🗄️ Database Management

### Migrations

Migrations run automatically when the backend container starts. To run manually:

```bash
docker-compose exec backend uv run alembic upgrade head
```

### Create New Migration

```bash
docker-compose exec backend uv run alembic revision --autogenerate -m "Description"
```

### Rollback Migration

```bash
docker-compose exec backend uv run alembic downgrade -1
```

### Seed Demo Data

```bash
docker-compose exec backend uv run python -m scripts.seed_db
```

### Database Backups

```bash
# Backup
docker-compose exec postgres pg_dump -U snake_user snake_game > backup.sql

# Restore
docker-compose exec -T postgres psql -U snake_user snake_game < backup.sql
```

### Connect to Database

```bash
# Using docker
docker-compose exec postgres psql -U snake_user -d snake_game

# Using local psql client
psql -h localhost -U snake_user -d snake_game
```

## 🔍 Troubleshooting

### View Service Status

```bash
docker-compose ps
```

### Check Health Status

```bash
# Backend health
curl http://localhost:8000/health

# Database health
curl http://localhost:8000/health/db

# Frontend health
curl http://localhost/health
```

### View Service Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Restart a Service

```bash
docker-compose restart backend
docker-compose restart frontend
docker-compose restart postgres
```

### Rebuild a Service

```bash
docker-compose up -d --build backend
docker-compose up -d --build frontend
```

### Clean Everything and Start Fresh

```bash
# WARNING: This will delete all data
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Common Issues

**Issue: Port already in use**
```bash
# Find what's using the port
netstat -an | grep :80
netstat -an | grep :8000
netstat -an | grep :5432

# Change port in docker-compose.yml
ports:
  - "8080:80"  # Use port 8080 instead of 80
```

**Issue: Database connection refused**
```bash
# Check if postgres is healthy
docker-compose ps
docker-compose logs postgres

# Wait for database to be ready
docker-compose exec backend bash -c 'while ! pg_isready -h postgres -U snake_user; do sleep 1; done'
```

**Issue: Frontend can't connect to backend**
- Check that `VITE_API_URL` is set correctly during build
- Rebuild frontend: `docker-compose up -d --build frontend`

**Issue: Permission denied**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

## 📦 Development vs Production

### Development Mode

For development, you may want to:
- Mount source code as volumes for live reloading
- Use SQLite instead of PostgreSQL
- Run services directly without Docker

```bash
# Backend
cd backend
uv sync
uv run uvicorn main:app --reload

# Frontend  
cd frontend
npm install
npm run dev
```

### Production Mode

The current Docker setup is optimized for production:
- Multi-stage builds for smaller images
- Health checks for all services
- Proper networking and security
- Volume persistence for database
- nginx for serving static files
- Compressed assets (gzip)
- Security headers

## 🚀 Deployment

### Deploy to a Server

1. Copy files to server:
```bash
rsync -avz --exclude 'node_modules' --exclude '.git' . user@server:/path/to/app/
```

2. On the server:
```bash
cd /path/to/app
docker-compose build
docker-compose up -d
```

### Deploy with SSL/HTTPS

1. Install certbot:
```bash
docker-compose exec frontend sh
apk add certbot certbot-nginx
```

2. Get SSL certificate:
```bash
certbot --nginx -d yourdomain.com
```

3. Update nginx.conf with SSL configuration

### Environment-Specific Builds

```bash
# Build with production API URL
docker-compose build --build-arg VITE_API_URL=https://api.yourdomain.com frontend
```

## 📊 Monitoring

### View Resource Usage

```bash
docker stats
```

### Container Information

```bash
docker-compose ps
docker-compose top
```

### Check Logs Size

```bash
docker-compose logs --tail=100 backend
```

## 🔒 Security Checklist

- [ ] Change default database password
- [ ] Update CORS origins to your domain
- [ ] Add SSL/TLS certificates
- [ ] Set up database backups
- [ ] Use secrets management
- [ ] Review rate limiting settings
- [ ] Enable firewall rules
- [ ] Set up monitoring and alerts
- [ ] Regular security updates

## 📝 Notes

- Database data persists in Docker volume `postgres_data`
- Backend automatically runs migrations on startup
- Frontend is built during container build (not at runtime)
- All services have health checks configured
- Services communicate via internal Docker network `snake-network`

## 🆘 Getting Help

If you encounter issues:

1. Check service logs: `docker-compose logs -f`
2. Check service health: `curl http://localhost:8000/health`
3. Verify all services are running: `docker-compose ps`
4. Try rebuilding: `docker-compose up -d --build`
5. Clean restart: `docker-compose down && docker-compose up -d`

For more information, see:
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)

