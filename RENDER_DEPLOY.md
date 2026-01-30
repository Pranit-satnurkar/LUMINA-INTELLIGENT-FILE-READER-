# Render Deployment Guide

## Quick Deploy to Render

### 1. Create Render Account
- Go to https://render.com/
- Sign up with GitHub (free)

### 2. Create Web Service
1. Dashboard → New → Web Service
2. Connect your GitHub repo: `RAG-Powered-Chatbot`
3. Configure:
   - **Name**: `lumina-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty (or `.`)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

### 3. Add Environment Variables
Click "Environment" → Add:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for first deploy
- Get your URL: `https://lumina-backend.onrender.com`

### 5. Update Mobile App
Edit `mobile-app/App.js` line 7:
```javascript
const API_URL = 'https://lumina-backend.onrender.com';
```

## Important Notes

**Free Tier Limitations:**
- Service sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (enough for testing)

**To keep it awake** (optional):
- Use a service like UptimeRobot to ping every 14 minutes
- Or upgrade to paid tier ($7/month for always-on)

## Testing Backend

Visit: `https://lumina-backend.onrender.com/docs`

You should see the FastAPI documentation page!

## Done! ✅

Your backend is now live and accessible from anywhere!
