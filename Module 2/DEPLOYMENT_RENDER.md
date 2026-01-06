# 🚀 Deployment Guide - Render

This guide will help you deploy the Snake Game to Render in **under 10 minutes**.

---

## 📋 Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com) (free)
3. **Git** - Code pushed to GitHub

---

## 🎯 Quick Deploy (Automatic - Recommended)

### Option 1: Using render.yaml (Blueprint)

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Go to Render Dashboard:**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Click **"New +"** → **"Blueprint"**

3. **Connect Repository:**
   - Connect your GitHub account
   - Select your `snake-game` repository
   - Render will detect `render.yaml`

4. **Deploy:**
   - Click **"Apply"**
   - Render will create:
     - PostgreSQL database
     - Web service with combined container
   - Wait 5-10 minutes for build

5. **Done! ✅**
   - Your app will be at: `https://snake-game.onrender.com`
   - API at: `https://snake-game.onrender.com/api/v1/leaderboard`
   - API docs: `https://snake-game.onrender.com/docs`

---

## 🛠️ Manual Deploy (Step-by-Step)

### Step 1: Create PostgreSQL Database

1. **In Render Dashboard:**
   - Click **"New +"** → **"PostgreSQL"**

2. **Configure:**
   - **Name:** `snake-game-db`
   - **Database:** `snake_game`
   - **User:** `snake_user` (auto-generated)
   - **Region:** Oregon (or closest to you)
   - **Plan:** Starter ($7/month) or Free

3. **Create Database**
   - Wait for database to be ready
   - **Copy the Internal Database URL** (starts with `postgresql://`)

### Step 2: Create Web Service

1. **In Render Dashboard:**
   - Click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Connect GitHub
   - Select your repository

3. **Configure:**
   - **Name:** `snake-game`
   - **Region:** Same as database (Oregon)
   - **Branch:** `main`
   - **Runtime:** Docker
   - **Dockerfile Path:** `Dockerfile.production`
   - **Plan:** Starter ($7/month) or Free

4. **Environment Variables:**

   Click **"Advanced"** → **"Add Environment Variable"**

   Add these:
   ```
   PORT=8080
   HOST=0.0.0.0
   ENVIRONMENT=production
   DATABASE_URL=<paste from PostgreSQL database>
   DATABASE_POOL_SIZE_MIN=2
   DATABASE_POOL_SIZE_MAX=10
   CORS_ORIGINS=["*"]
   ALLOW_CREDENTIALS=true
   LOG_LEVEL=INFO
   LOG_FORMAT=json
   RATE_LIMIT_PER_MINUTE=60
   MAX_SCORE=999999
   MIN_SCORE=0
   ```

   **Important:** Replace `DATABASE_URL` with the Internal Database URL from Step 1!

5. **Health Check:**
   - **Health Check Path:** `/health`

6. **Create Web Service**
   - Click **"Create Web Service"**
   - Wait 5-10 minutes for build

---

## 🎮 Access Your App

Once deployed, your app will be available at:

- **Main App:** `https://your-service-name.onrender.com`
- **API Endpoint:** `https://your-service-name.onrender.com/api/v1/leaderboard`
- **API Docs:** `https://your-service-name.onrender.com/docs`
- **Health Check:** `https://your-service-name.onrender.com/health`

---

## 🔧 Configuration

### Update CORS Origins

After deployment, update CORS to your actual domain:

1. **Go to Web Service** → **Environment**
2. **Edit `CORS_ORIGINS`:**
   ```
   CORS_ORIGINS=["https://your-service-name.onrender.com"]
   ```
3. **Save Changes** (will trigger redeploy)

### Custom Domain

1. **In Web Service** → **Settings** → **Custom Domain**
2. **Add your domain:** `game.yourdomain.com`
3. **Update DNS** with provided CNAME
4. **Update CORS_ORIGINS** to include your custom domain

---

## 📊 Monitoring

### View Logs

1. **Web Service** → **Logs**
2. Real-time logs of your application
3. Look for:
   ```
   Snake Game - Combined Container Starting...
   Database is ready!
   Migrations completed successfully!
   Starting FastAPI server on port 8080...
   ```

### View Metrics

1. **Web Service** → **Metrics**
2. Monitor:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

### Health Checks

Render automatically monitors `/health` endpoint:
- Green = Healthy
- Red = Unhealthy (will auto-restart)

---

## 🐛 Troubleshooting

### Build Fails

**Error:** "No such file or directory"
- Check that `Dockerfile.production` exists in root
- Verify paths in Dockerfile

**Error:** "npm ci failed"
- Check `frontend/package-lock.json` exists
- Try deleting and regenerating: `npm install`

### Database Connection Fails

**Error:** "could not connect to server"
- Verify DATABASE_URL is correct
- Check database is running (Database → Overview)
- Ensure Internal Database URL is used (not External)

### App Starts But Shows Errors

1. **Check Logs:**
   - Web Service → Logs
   - Look for Python errors or exceptions

2. **Common Issues:**
   - Missing environment variables
   - Database migration failed
   - CORS configuration incorrect

3. **Test Database:**
   ```bash
   curl https://your-app.onrender.com/health/db
   ```
   Should return: `{"status":"healthy","db_connected":true}`

### Frontend Not Loading

1. **Check Build Logs:**
   - Look for "Build the React application" step
   - Verify it completed successfully

2. **Verify Static Files:**
   - In logs, should see: "Static file serving configured successfully"

3. **Test API:**
   ```bash
   curl https://your-app.onrender.com/api/v1/leaderboard
   ```

### Slow Cold Starts (Free Tier)

Free tier services spin down after 15 minutes of inactivity:
- First request after inactivity takes 30-60 seconds
- Solution: Upgrade to Starter plan ($7/month) for always-on

---

## 💰 Cost Breakdown

### Free Tier (Limited)
- **PostgreSQL:** Free (limited storage/connections)
- **Web Service:** Free (spins down after 15 min)
- **Total:** $0/month
- **Limitations:** 
  - Service sleeps after inactivity
  - Limited database size
  - 750 hours/month limit

### Starter Plan (Recommended)
- **PostgreSQL:** $7/month (1GB storage)
- **Web Service:** $7/month (always-on, 0.5GB RAM)
- **Total:** $14/month
- **Benefits:**
  - Always-on (no cold starts)
  - Better performance
  - More database capacity

### Standard Plan (High Traffic)
- **PostgreSQL:** $20/month (10GB storage)
- **Web Service:** $25/month (2GB RAM)
- **Total:** $45/month

---

## 🔄 Updates & Redeploy

### Auto-Deploy (Recommended)

Enable auto-deploy for automatic updates:
1. **Web Service** → **Settings** → **Build & Deploy**
2. **Enable Auto-Deploy:** On
3. Now every push to `main` branch auto-deploys!

### Manual Deploy

1. **Push changes to GitHub:**
   ```bash
   git add .
   git commit -m "Update feature X"
   git push origin main
   ```

2. **In Render Dashboard:**
   - Web Service → **Manual Deploy** → **Deploy latest commit**
   - Or wait for auto-deploy

### Rollback

If something breaks:
1. **Web Service** → **Events**
2. Find previous successful deploy
3. Click **"Rollback to this deploy"**

---

## 🎯 Production Checklist

Before going live, verify:

- [x] **Database:** PostgreSQL created and connected
- [x] **Environment Variables:** All set correctly
- [x] **CORS:** Updated to production domain
- [x] **Health Checks:** Passing (`/health` returns green)
- [x] **API Testing:** Test all endpoints work
- [x] **Frontend:** Game loads and plays correctly
- [x] **Leaderboard:** Scores save and display
- [x] **Custom Domain:** (Optional) Configured
- [x] **Monitoring:** Review logs and metrics
- [x] **Backups:** Enable database backups (Settings)

---

## 📚 Additional Resources

- **Render Docs:** https://render.com/docs
- **PostgreSQL Docs:** https://render.com/docs/databases
- **Docker Support:** https://render.com/docs/docker
- **Support:** support@render.com

---

## 🆘 Getting Help

1. **Check Logs First:** Most issues show in logs
2. **Render Community:** https://community.render.com
3. **Render Support:** Create ticket in dashboard
4. **GitHub Issues:** Report bugs in your repo

---

## ✅ Success Checklist

After deployment, you should have:
- ✅ App running at `https://your-app.onrender.com`
- ✅ Game playable in browser
- ✅ Leaderboard working
- ✅ Scores persisting to database
- ✅ API docs accessible at `/docs`
- ✅ Health checks passing
- ✅ Logs showing no errors

**Congratulations! Your Snake Game is deployed! 🎉🐍**

---

## 🚀 What's Next?

1. **Share your game** with friends
2. **Monitor performance** in Render dashboard
3. **Add custom domain** (optional)
4. **Enable backups** for database
5. **Set up monitoring/alerts**
6. **Scale up** if traffic increases

**Happy deploying! 🎮**

