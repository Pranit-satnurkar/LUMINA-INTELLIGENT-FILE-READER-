# Deployment Guide

## Quick Start

### 1. Deploy Backend to Railway

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

Get your URL: `https://your-app.railway.app`

### 2. Update Mobile App

Edit `mobile-app/App.js`:
```javascript
const API_URL = 'https://your-app.railway.app';
```

### 3. Build APK

```bash
cd mobile-app
eas build --platform android --profile production
```

### 4. Create GitHub Release

1. Go to Releases → Create new release
2. Tag: `v1.0.0`
3. Upload APK file
4. Publish

### 5. Update Website

Edit `website/index.html`:
- Replace `YOUR_USERNAME` with your GitHub username
- Update download link

### 6. Enable GitHub Pages

Settings → Pages → Source: `main` → `/website` → Save

Your site: `https://YOUR_USERNAME.github.io/RAG-Powered-Chatbot/`

## Environment Variables (Railway)

```
GROQ_API_KEY=your_groq_api_key
API_KEY=your_secret_api_key_for_mobile_app
```

## Done! 🎉

Users can now download your app from your website!
