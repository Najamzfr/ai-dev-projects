# 🚀 Quick Start - Combined Container Deployment

Your Snake Game is now configured for single-container deployment!

## 📦 What's Changed

✅ **Combined Container:** Frontend + Backend in one Docker image
✅ **FastAPI serves static files:** No nginx needed
✅ **API at `/api` prefix:** Clean URL structure  
✅ **Ready for Render:** One-click deployment

---

## 🎯 Deploy to Render (5 Minutes)

### Method 1: Automatic (Recommended)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Go to Render:**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub repo
   - Click **"Apply"**

3. **Done!** ✅
   - Your app will be at: `https://snake-game.onrender.com`
   - Wait 5-10 minutes for initial build

### Method 2: Manual

See complete guide: **[DEPLOYMENT_RENDER.md](./DEPLOYMENT_RENDER.md)**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Single Docker Container           │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  FastAPI Application           │ │
│  │  (Port 8080)                   │ │
│  │                                 │ │
│  │  • API: /api/v1/*              │ │
│  │  • Static: /assets/*           │ │
│  │  • SPA: /*                      │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  React Build (static files)    │ │
│  │  in ./static/                   │ │
│  └────────────────────────────────┘ │
└──────────────┬──────────────────────┘
               │
               ▼
    ┌──────────────────┐
    │   PostgreSQL     │
    │   (Render)       │
    └──────────────────┘
```

---

## 📁 New Files

1. **`Dockerfile.production`** - Combined container build
2. **`render.yaml`** - Render blueprint config
3. **`DEPLOYMENT_RENDER.md`** - Complete deployment guide
4. **`env.production.template`** - Environment variables template

## 🔧 Modified Files

1. **`backend/main.py`** - Now serves static files
2. **`frontend/src/lib/api-client.ts`** - API URL uses `/api` prefix

---

## 🧪 Test Locally

Build and test the production container:

```bash
# Build production image
docker build -f Dockerfile.production -t snake-game:production .

# Run with environment variables
docker run -p 8080:8080 \
  -e PORT=8080 \
  -e ENVIRONMENT=production \
  -e DATABASE_URL=sqlite:///./snake_game.db \
  -e CORS_ORIGINS='["*"]' \
  snake-game:production

# Access at http://localhost:8080
```

---

## 🌐 Production URLs

Once deployed, your URLs will be:

| Endpoint | URL | Description |
|----------|-----|-------------|
| **Game** | `https://your-app.onrender.com/` | Play the game |
| **API** | `https://your-app.onrender.com/api/v1/leaderboard` | API endpoints |
| **Docs** | `https://your-app.onrender.com/docs` | API documentation |
| **Health** | `https://your-app.onrender.com/health` | Health check |

---

## 💰 Cost

**Render Starter Plan:**
- Web Service: $7/month
- PostgreSQL: $7/month  
- **Total: $14/month**

**Free Tier Available** (with limitations):
- Service spins down after 15 min inactivity
- Limited database size

---

## ✅ What Works

✅ **Frontend:** React app served by FastAPI  
✅ **Backend:** API at `/api/v1/*` prefix  
✅ **Database:** PostgreSQL with migrations  
✅ **Static Assets:** Cached and optimized  
✅ **SPA Routing:** React Router works  
✅ **Health Checks:** Automatic monitoring  
✅ **Auto-scaling:** Render handles traffic  

---

## 🚀 Next Steps

1. **Deploy to Render** using blueprint
2. **Test your deployment** 
3. **Update CORS** to your domain
4. **Enable auto-deploy** from GitHub
5. **Set up custom domain** (optional)

---

## 📚 Resources

- **Full Guide:** [DEPLOYMENT_RENDER.md](./DEPLOYMENT_RENDER.md)
- **Render Docs:** https://render.com/docs
- **Render Blueprint:** https://render.com/docs/blueprint-spec

---

**Ready to deploy! Push to GitHub and click "Apply" in Render! 🎉**

