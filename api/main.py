from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from dotenv import load_dotenv

# Import Routes
from api.routes import ingest, chat

# Load Environment
load_dotenv()

# Initialize App
app = FastAPI(
    title="Lumina API",
    description="Backend for Lumina Intelligent Doc Reader",
    version="4.0.0"
)

# CORS (Allow Mobile App to Connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for development (React Native/Expo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(ingest.router, prefix="/api/v1", tags=["Ingestion"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

# Routes
@app.get("/")
async def root():
    return {"status": "online", "system": "Lumina API v4.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
