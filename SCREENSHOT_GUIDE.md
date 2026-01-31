# Screenshot Capture Guide

## Overview

This guide will help you capture high-quality screenshots of the LUMINA web and mobile applications for the README.

---

## Web Interface Screenshots

### Prerequisites
- Streamlit app is running at http://localhost:8501
- Have a sample PDF ready (or use one from `docs/` folder)

### Screenshots Needed

#### 1. **web-home.png** - Home/Upload Screen
**What to capture**:
- Initial state of the app
- LUMINA branding visible
- Upload interface in sidebar
- Clean, empty chat area

**Steps**:
1. Open http://localhost:8501 in your browser
2. Ensure the page is fully loaded
3. Take a full-page screenshot
4. Save as `screenshots/web-home.png`

#### 2. **web-upload.png** - Document Uploaded State
**What to capture**:
- Sidebar showing uploaded document
- Success message
- "Analyze Document" button visible

**Steps**:
1. Upload a PDF using the file uploader
2. Wait for upload confirmation
3. Take screenshot showing the uploaded state
4. Save as `screenshots/web-upload.png`

#### 3. **web-chat.png** - Chat Interaction
**What to capture**:
- User question in chat
- AI response with formatting
- Professional conversation flow

**Steps**:
1. After uploading a document, ask a question like:
   - "What is this document about?"
   - "Summarize the main points"
2. Wait for AI response
3. Scroll to show both question and answer
4. Take screenshot
5. Save as `screenshots/web-chat.png`

### Screenshot Tips
- Use **1920x1080** resolution or higher
- Ensure good lighting/contrast
- Capture full browser window (including sidebar)
- Use browser's built-in screenshot tool or:
  - **Windows**: Win + Shift + S
  - **Mac**: Cmd + Shift + 4
  - **Linux**: PrtScn or Shift + PrtScn

---

## Mobile App Screenshots

### Prerequisites
- Mobile app running in Expo Go or simulator
- Backend API accessible from mobile device

### Screenshots Needed

#### 1. **mobile-home.png** - Home Screen
**What to capture**:
- LUMINA branding
- Upload PDF button
- Clean interface

**Steps**:
1. Start Expo: `cd mobile-app && npx expo start`
2. Open in Expo Go app or simulator
3. Capture home screen
4. Save as `screenshots/mobile-home.png`

#### 2. **mobile-upload.png** - Upload Interface
**What to capture**:
- File picker or upload in progress
- Upload button highlighted

**Steps**:
1. Tap "Upload PDF" button
2. Capture the file picker or upload screen
3. Save as `screenshots/mobile-upload.png`

#### 3. **mobile-chat.png** - Chat Interface
**What to capture**:
- Chat messages
- User input field
- AI responses

**Steps**:
1. After uploading, send a message
2. Wait for response
3. Capture chat conversation
4. Save as `screenshots/mobile-chat.png`

#### 4. **mobile-dark.png** - Dark Mode (if available)
**What to capture**:
- App in dark mode
- Same view as mobile-home or mobile-chat

**Steps**:
1. Toggle dark mode (if available)
2. Capture screenshot
3. Save as `screenshots/mobile-dark.png`

### Mobile Screenshot Tips
- Use device's native screenshot:
  - **iOS**: Power + Volume Up
  - **Android**: Power + Volume Down
- Ensure good screen brightness
- Hide status bar if possible
- Use portrait orientation

---

## After Capturing Screenshots

### 1. Create Screenshots Directory
```bash
mkdir screenshots
```

### 2. Move Screenshots
Move all captured screenshots to the `screenshots/` directory:
```
screenshots/
├── web-home.png
├── web-upload.png
├── web-chat.png
├── mobile-home.png
├── mobile-upload.png
├── mobile-chat.png
└── mobile-dark.png (optional)
```

### 3. Optimize Images (Optional)
- Resize to reasonable dimensions (max 1920px width)
- Compress to reduce file size
- Use PNG format for clarity

### 4. Notify Me
Once screenshots are captured and saved in the `screenshots/` directory, let me know and I'll:
- Update the README with embedded screenshots
- Add image captions
- Commit everything to the repository

---

## Screenshot Checklist

### Web Interface
- [ ] web-home.png (Home/Upload screen)
- [ ] web-upload.png (Document uploaded)
- [ ] web-chat.png (Chat interaction)

### Mobile App
- [ ] mobile-home.png (Home screen)
- [ ] mobile-upload.png (Upload interface)
- [ ] mobile-chat.png (Chat interface)
- [ ] mobile-dark.png (Dark mode - optional)

---

## Troubleshooting

### Web app not loading
- Check if Streamlit is running: `ps aux | grep streamlit`
- Restart: `.\venv\Scripts\python.exe -m streamlit run app.py`
- Check port 8501 is not in use

### Mobile app not connecting to backend
- Ensure backend is running
- Update API_URL in App.js to your local IP
- Check firewall settings

### Screenshots too large
- Use image compression tools
- Resize to 1920px width max
- Convert to WebP format for smaller size

---

<div align="center">
  <p><strong>Ready to capture screenshots!</strong></p>
  <p>The Streamlit app is running at http://localhost:8501</p>
</div>
