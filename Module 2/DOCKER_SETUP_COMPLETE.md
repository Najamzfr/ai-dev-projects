# Snake Game - Docker Setup Complete ✅

## 🎉 What's Been Added

Your Snake Game project is now fully containerized with Docker! Here's what's been set up:

### 📦 New Files Created

1. **`docker-compose.yml`** - Production Docker Compose configuration
2. **`docker-compose.dev.yml`** - Development Docker Compose configuration
3. **`backend/Dockerfile`** - Backend container definition
4. **`backend/.dockerignore`** - Backend Docker ignore rules
5. **`frontend/Dockerfile`** - Frontend production container (multi-stage with nginx)
6. **`frontend/Dockerfile.dev`** - Frontend development container
7. **`frontend/nginx.conf`** - nginx configuration for serving frontend
8. **`frontend/.dockerignore`** - Frontend Docker ignore rules
9. **`Makefile`** - Convenient make commands for Docker operations
10. **`DOCKER_README.md`** - Comprehensive Docker documentation

### 🛠️ Modified Files

1. **`backend/pyproject.toml`** - Added `asyncpg` for PostgreSQL support
2. **`.gitignore`** - Added Docker-related ignore rules

## 🚀 Quick Start Guide

### Production Mode (nginx + PostgreSQL)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Stop services
docker-compose down
```

Your app will be available at:
- **Frontend:** http://localhost
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Development Mode (Hot Reload)

```bash
# Build and start dev environment
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

Dev mode features:
- Hot reload for both frontend and backend
- Volume mounts for live code changes
- Debug logging enabled
- Port 8080 for frontend (Vite dev server)

## 🎯 Using Make Commands

```bash
make help           # Show all available commands
make build          # Build all containers
make up             # Start all services
make down           # Stop all services
make logs           # View logs
make ps             # List containers
make restart        # Restart services
make clean          # Remove containers and volumes
make shell-backend  # Access backend shell
make migrate        # Run database migrations
make seed           # Seed database with demo data
```

## 🏗️ Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   nginx     │  (Frontend - React/Vite)
│   Port 80   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   FastAPI   │  (Backend - Python)
│  Port 8000  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ PostgreSQL  │  (Database)
│  Port 5432  │
└─────────────┘
```

## 🗄️ Database

- **Engine:** PostgreSQL 15 Alpine
- **User:** snake_user
- **Password:** snake_password_change_in_production (⚠️ CHANGE THIS!)
- **Database:** snake_game
- **Port:** 5432
- **Volume:** postgres_data (persistent)

### Database Commands

```bash
# Run migrations
docker-compose exec backend uv run alembic upgrade head

# Seed demo data
docker-compose exec backend uv run python -m scripts.seed_db

# Access database
docker-compose exec postgres psql -U snake_user -d snake_game

# Backup database
docker-compose exec postgres pg_dump -U snake_user snake_game > backup.sql

# Restore database
docker-compose exec -T postgres psql -U snake_user snake_game < backup.sql
```

## 🔧 Configuration

### Environment Variables

All configured in `docker-compose.yml`:

**Backend:**
- `DATABASE_URL` - PostgreSQL connection string
- `CORS_ORIGINS` - Allowed origins
- `LOG_LEVEL` - Logging level (INFO/DEBUG/ERROR)
- `RATE_LIMIT_PER_MINUTE` - API rate limiting

**Frontend:**
- `VITE_API_URL` - Backend API URL (build-time)

### Production Checklist

Before deploying to production:

- [ ] Change `POSTGRES_PASSWORD` in docker-compose.yml
- [ ] Update `CORS_ORIGINS` to your domain
- [ ] Update `VITE_API_URL` to your production API
- [ ] Set up SSL/TLS certificates
- [ ] Configure backups for PostgreSQL
- [ ] Review rate limiting settings
- [ ] Set up monitoring and logging

## 🧪 Testing the Setup

```bash
# 1. Build containers
docker-compose build

# 2. Start services
docker-compose up -d

# 3. Wait for services to be healthy (30-40 seconds)
docker-compose ps

# 4. Test backend health
curl http://localhost:8000/health

# 5. Test database health
curl http://localhost:8000/health/db

# 6. Test frontend
curl http://localhost/

# 7. Open in browser
# Frontend: http://localhost
# API Docs: http://localhost:8000/docs

# 8. Seed demo data (optional)
docker-compose exec backend uv run python -m scripts.seed_db
```

## 📊 Features

### Backend Container
- ✅ Python 3.12
- ✅ uv for fast dependency management
- ✅ Automatic database migrations on startup
- ✅ Health checks
- ✅ PostgreSQL connection with asyncpg
- ✅ Waits for database before starting

### Frontend Container
- ✅ Multi-stage build (builder + nginx)
- ✅ Optimized production build
- ✅ Gzip compression
- ✅ Security headers
- ✅ Static asset caching
- ✅ SPA routing support
- ✅ Health check endpoint

### Database Container
- ✅ PostgreSQL 15 Alpine (lightweight)
- ✅ Persistent volume
- ✅ Health checks
- ✅ UTF-8 encoding
- ✅ Ready for production

## 🔍 Troubleshooting

### Service won't start

```bash
# Check logs
docker-compose logs -f [service_name]

# Check if ports are in use
netstat -an | grep :80
netstat -an | grep :8000
netstat -an | grep :5432

# Restart specific service
docker-compose restart [service_name]
```

### Database connection errors

```bash
# Check if postgres is healthy
docker-compose ps

# Check postgres logs
docker-compose logs postgres

# Verify connection
docker-compose exec backend pg_isready -h postgres -U snake_user -d snake_game
```

### Frontend can't connect to backend

- Verify `VITE_API_URL` is correct
- Rebuild frontend: `docker-compose up -d --build frontend`
- Check CORS settings in backend

### Start fresh

```bash
# WARNING: This deletes all data!
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 📚 Additional Resources

- **Full Docker Guide:** See `DOCKER_README.md`
- **Project Overview:** See `PROJECT_SUMMARY.md`
- **API Documentation:** http://localhost:8000/docs (when running)
- **Backend Details:** `backend/README.md`
- **Frontend Details:** `frontend/README.md`

## 🎮 Play the Game!

Once everything is running:

1. Open http://localhost in your browser
2. Enter a username
3. Choose game mode (walls or walls-through)
4. Play and compete on the leaderboard!

## 💡 Tips

**Development:**
- Use `docker-compose.dev.yml` for hot reload
- Mount volumes to edit code without rebuilding
- Use `LOG_LEVEL=DEBUG` for more logs

**Production:**
- Use `docker-compose.yml` (default)
- Change all default passwords
- Set up SSL with Let's Encrypt
- Configure proper backup strategy
- Monitor with Docker stats or external tools

**Performance:**
- Scale services: `docker-compose up -d --scale backend=3`
- Monitor resources: `docker stats`
- Check health: `docker-compose ps`

## 🆘 Need Help?

1. Check service status: `docker-compose ps`
2. View logs: `docker-compose logs -f`
3. Test health endpoints: `curl http://localhost:8000/health`
4. Read full documentation: `DOCKER_README.md`
5. Check backend logs: `docker-compose logs backend`
6. Check frontend logs: `docker-compose logs frontend`

---

**Ready to ship! 🚀**

Your Snake Game is now fully containerized and ready for deployment!

