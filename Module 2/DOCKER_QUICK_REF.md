# 🚀 Docker Quick Reference - Snake Game

## One-Line Commands

```bash
# Start everything (production)
docker-compose up -d

# Start everything (development with hot reload)
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Rebuild and start
docker-compose up -d --build
```

## 📍 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost | Play the game |
| Backend | http://localhost:8000 | API endpoints |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Database | localhost:5432 | PostgreSQL |

**Database Credentials:**
- User: `snake_user`
- Password: `snake_password_change_in_production`
- Database: `snake_game`

## 🎯 Common Tasks

### First Time Setup
```bash
docker-compose build
docker-compose up -d
docker-compose exec backend uv run python -m scripts.seed_db
```

### Development Workflow
```bash
# Use dev compose file for hot reload
docker-compose -f docker-compose.dev.yml up -d
docker-compose -f docker-compose.dev.yml logs -f
```

### Database Operations
```bash
# Run migrations
docker-compose exec backend uv run alembic upgrade head

# Seed demo data
docker-compose exec backend uv run python -m scripts.seed_db

# Connect to database
docker-compose exec postgres psql -U snake_user -d snake_game

# Backup
docker-compose exec postgres pg_dump -U snake_user snake_game > backup.sql

# Restore
docker-compose exec -T postgres psql -U snake_user snake_game < backup.sql
```

### Debugging
```bash
# Check status
docker-compose ps

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Access container shell
docker-compose exec backend /bin/bash
docker-compose exec frontend /bin/sh

# Test health endpoints
curl http://localhost:8000/health
curl http://localhost:8000/health/db
curl http://localhost/health
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
docker-compose restart postgres
```

### Clean Up
```bash
# Stop containers
docker-compose down

# Stop and remove volumes (deletes data!)
docker-compose down -v

# Clean everything
docker-compose down -v && docker system prune -f
```

## 🛠️ Make Commands (Shortcuts)

```bash
make build      # Build containers
make up         # Start services
make down       # Stop services
make logs       # View logs
make ps         # List containers
make restart    # Restart all
make clean      # Remove everything (including volumes!)
make migrate    # Run DB migrations
make seed       # Seed demo data
make shell-backend   # Backend shell
make shell-frontend  # Frontend shell
```

## 🏗️ Architecture

```
Browser (localhost)
    ↓
nginx:80 (Frontend)
    ↓
FastAPI:8000 (Backend)
    ↓
PostgreSQL:5432 (Database)
```

## 🔄 Production vs Development

### Production (`docker-compose.yml`)
- Frontend: nginx serving static build
- Backend: Production settings
- Database: PostgreSQL with persistence
- Ports: 80, 8000, 5432

### Development (`docker-compose.dev.yml`)
- Frontend: Vite dev server with hot reload (port 8080)
- Backend: Uvicorn with --reload
- Database: Same PostgreSQL
- Ports: 8080, 8000, 5432
- Volume mounts for live code changes

## 📦 What's Included

✅ PostgreSQL 15 Alpine (lightweight)
✅ FastAPI backend with auto-migrations
✅ React frontend with nginx
✅ Health checks for all services
✅ Persistent database volume
✅ Docker networking
✅ Development & production configs
✅ Automatic database migrations
✅ Optimized multi-stage builds

## ⚠️ Before Production

1. Change `POSTGRES_PASSWORD` in docker-compose.yml
2. Update `CORS_ORIGINS` to your domain
3. Set `VITE_API_URL` to production API URL
4. Add SSL/TLS certificates
5. Set up database backups
6. Configure monitoring

## 📚 Documentation

- `DOCKER_README.md` - Full Docker documentation
- `DOCKER_SETUP_COMPLETE.md` - Setup summary
- `PROJECT_SUMMARY.md` - Project overview
- `docker-compose.yml` - Production config
- `docker-compose.dev.yml` - Development config

## 🆘 Troubleshooting

**Port already in use:**
```bash
# Change port in docker-compose.yml
ports:
  - "8080:80"  # Use 8080 instead of 80
```

**Database connection refused:**
```bash
docker-compose ps  # Check if postgres is healthy
docker-compose logs postgres
```

**Frontend build fails:**
```bash
docker-compose build --no-cache frontend
```

**Start fresh:**
```bash
docker-compose down -v
docker-compose build
docker-compose up -d
```

## ✅ Quick Health Check

```bash
# 1. Are services running?
docker-compose ps

# 2. Are services healthy?
curl http://localhost:8000/health
curl http://localhost:8000/health/db
curl http://localhost/

# 3. Check logs for errors
docker-compose logs --tail=50
```

---

**Need more details?** See `DOCKER_README.md`

