# LUMINA - AI Document Reader

<div align="center">
  <h1>⚡ LUMINA</h1>
  <p><strong>Your AI-Powered Document Assistant</strong></p>
  <p>Upload PDFs and chat with your documents using advanced AI</p>
  
  <a href="https://YOUR_USERNAME.github.io/RAG-Powered-Chatbot/">
    <img src="https://img.shields.io/badge/Download-Android%20APK-blue?style=for-the-badge&logo=android" alt="Download APK">
  </a>
  <img src="https://img.shields.io/badge/Version-1.0.0-green?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</div>

---

## ✨ Features

- 📄 **Upload PDF Documents** - Support for any PDF file
- 💬 **AI Chat Interface** - Ask questions about your documents
- 🌙 **Dark Mode** - Beautiful light and dark themes
- ⚡ **Fast Responses** - Powered by Groq LLM
- 🔒 **Secure** - HTTPS encryption, no data storage

## 📱 Download

**Android**: [Download APK](https://github.com/YOUR_USERNAME/RAG-Powered-Chatbot/releases/latest)

## 🏗️ Project Structure

```
RAG-Powered-Chatbot/
├── backend/           # FastAPI backend with RAG
├── mobile-app/        # React Native (Expo) mobile app
├── website/           # Download page (GitHub Pages)
├── docs/              # Documentation
└── README.md
```

## 🚀 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain** - LLM orchestration
- **Groq** - Fast LLM inference
- **FAISS** - Vector similarity search
- **HuggingFace** - Embeddings

### Mobile App
- **React Native** - Cross-platform mobile framework
- **Expo** - Development and build platform
- **Axios** - HTTP client

### Deployment
- **Railway** - Backend hosting (free tier)
- **GitHub Releases** - APK distribution
- **GitHub Pages** - Download website

## 🛠️ Local Development

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Add your GROQ_API_KEY

# Run server
uvicorn backend.main:app --reload
```

### Mobile App

```bash
cd mobile-app

# Install dependencies
npm install

# Start Expo
npx expo start
```

## 📦 Building APK

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Build APK
cd mobile-app
eas build --platform android --profile production
```

## 🌐 Deployment

### Backend (Railway)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Website (GitHub Pages)

1. Go to repository Settings
2. Pages → Source: `main` branch → `/website` folder
3. Save
4. Visit: `https://YOUR_USERNAME.github.io/RAG-Powered-Chatbot/`

## 🔐 Security

- ✅ HTTPS encryption for all API calls
- ✅ API key authentication
- ✅ Rate limiting
- ✅ CORS configuration
- ✅ No data persistence on server
- ✅ Environment variable management

## 📄 License

MIT License - feel free to use for your own projects!

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

## 📧 Contact

For questions or support, open an issue on GitHub.

---

<div align="center">
  <p>Made with ⚡ by <a href="https://github.com/YOUR_USERNAME">Your Name</a></p>
  <p>⭐ Star this repo if you find it useful!</p>
</div>
