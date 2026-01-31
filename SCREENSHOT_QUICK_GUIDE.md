# 📸 Screenshot Capture - Quick Guide

## ✅ Both Apps Are Running!

### Web App
- **URL**: http://localhost:8501
- **Status**: ✅ Running

### Mobile App  
- **Status**: ✅ Expo server running
- **Access**: Scan QR code with Expo Go app

---

## 📱 How to View Mobile App

### Option 1: Expo Go App (Recommended)
1. Install **Expo Go** on your phone:
   - iOS: https://apps.apple.com/app/expo-go/id982107779
   - Android: https://play.google.com/store/apps/details?id=host.exp.exponent

2. Open Expo Go app

3. Scan the QR code shown in your terminal

4. App will load on your phone

### Option 2: Android Emulator
```bash
# In the Expo terminal, press 'a'
a
```

### Option 3: iOS Simulator (Mac only)
```bash
# In the Expo terminal, press 'i'
i
```

---

## 📸 Screenshots to Capture

### Web Interface (3 screenshots)

1. **`web-home.png`**
   - Go to http://localhost:8501
   - Capture the initial upload screen
   - Show LUMINA branding and sidebar

2. **`web-upload.png`**
   - Upload any PDF file
   - Capture after successful upload
   - Show the uploaded document indicator

3. **`web-chat.png`**
   - Ask a question like "What is this document about?"
   - Wait for AI response
   - Capture the chat conversation

### Mobile App (3-4 screenshots)

4. **`mobile-home.png`**
   - Capture the home screen
   - Show upload button

5. **`mobile-upload.png`**
   - Tap upload button
   - Capture the file picker or upload screen

6. **`mobile-chat.png`**
   - After uploading, send a message
   - Capture the chat interface

7. **`mobile-dark.png`** (optional)
   - If dark mode exists, toggle it
   - Capture dark mode view

---

## 💾 Save Screenshots

Create a folder and save all screenshots:

```bash
mkdir screenshots
# Then move your captured screenshots to this folder
```

Expected structure:
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

---

## ⚡ Quick Capture Tips

**Windows**: Win + Shift + S (Snipping Tool)
**Mac**: Cmd + Shift + 4
**Phone**: Power + Volume Down (Android) or Power + Volume Up (iOS)

---

## ✅ When Done

Once you have all screenshots saved in the `screenshots/` folder, let me know and I'll:
1. Update README with embedded screenshots
2. Add Codecov badge
3. Commit all changes
4. Push to GitHub

---

**Note**: If mobile app doesn't connect to backend, update the API_URL in `mobile-app/App.js` to your computer's local IP address (e.g., `http://192.168.0.10:8000`)
