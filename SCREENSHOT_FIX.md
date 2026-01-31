# 🔧 Quick Fix for Screenshot Capture

## Issue
The chatbot is showing an error: `Failed to call a function... 'search_documents'`

This happens because the Groq LLM is trying to use function calling, but we haven't configured any functions.

## Workaround for Screenshots

### Option 1: Use Simple Questions
Try asking very simple, direct questions that don't trigger function calling:
- "Summarize this document"
- "What are the main points?"
- "List the key topics"

### Option 2: Skip Chat Screenshot for Now
You can capture:
1. ✅ Web home screen (no chat needed)
2. ✅ Web upload screen (no chat needed)
3. ⏭️ Skip web chat screenshot for now

We can fix the chatbot and recapture later if needed.

### Option 3: Use a Different Query
If you uploaded a PDF, try:
- "What is in this document?" (very simple)
- "Give me a summary" (direct)

## For Mobile App
The mobile app should work the same way - use simple queries or skip the chat screenshot.

---

## Quick Screenshot Plan

**Minimum needed:**
1. `web-home.png` - Home screen ✅
2. `web-upload.png` - After uploading PDF ✅  
3. `mobile-home.png` - Mobile home screen ✅

**Optional (if chat works):**
4. `web-chat.png` - Chat interaction
5. `mobile-chat.png` - Mobile chat

---

**Let me know when you have the screenshots and I'll update the README!**
