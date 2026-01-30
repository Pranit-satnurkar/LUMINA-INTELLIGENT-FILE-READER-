from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import uvicorn
import shutil
import os
import io
from .pdf_processor import PDFProcessor
from .bot import chat_with_bot, DB_DIR, EMBEDDING_MODEL
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

app = FastAPI(title="Lumina API Brain")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Vector Store (In-Memory for now, or loaded from disk)
vector_store = None

# Initialize Vector Store if exists
if os.path.exists(DB_DIR):
    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vector_store = FAISS.load_local(DB_DIR, embeddings, allow_dangerous_deserialization=True)
        print("✅ Loaded existing Vector Store.")
    except Exception as e:
        print(f"⚠️ Could not load Vector Store: {e}")

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

@app.get("/")
def health_check():
    return {"status": "Lumina Brain is active"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store
    try:
        print(f"📄 Receiving file: {file.filename}")
        print(f"📊 Content type: {file.content_type}")
        
        # Read file into bytes
        content = await file.read()
        print(f"✅ File read: {len(content)} bytes")
        file_stream = io.BytesIO(content)
        
        # Process PDF
        processor = PDFProcessor()
        print(f"🔄 Processing PDF...")
        chunks = processor.process_pdf(file_stream, file.filename)
        print(f"✅ Extracted {len(chunks)} chunks")
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No text found in PDF.")
            
        # Create/Update Vector Store
        print(f"🧠 Creating embeddings...")
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        
        if vector_store is None:
            vector_store = FAISS.from_documents(chunks, embeddings)
            print(f"✅ Created new vector store")
        else:
            new_vs = FAISS.from_documents(chunks, embeddings)
            vector_store.merge_from(new_vs)
            print(f"✅ Merged into existing vector store")
            
        # Save to disk
        os.makedirs(DB_DIR, exist_ok=True)
        vector_store.save_local(DB_DIR)
        print(f"💾 Saved to {DB_DIR}")
        
        return {"message": f"Successfully uploaded {file.filename}", "chunks": len(chunks)}
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    global vector_store
    if not vector_store:
        raise HTTPException(status_code=400, detail="Brain is empty. Send a PDF first.")
    
    response = chat_with_bot(request.message, vector_store)
    
    # response is normally dict {'answer': ..., 'context': ...} or string error
    if isinstance(response, str):
         return {"answer": response, "citations": []}
         
    return {"answer": response.get('answer', 'No answer generated.'), "citations": response.get('context', [])}

@app.delete("/session")
async def delete_session():
    global vector_store
    try:
        vector_store = None
        # Optionally delete from disk
        if os.path.exists(DB_DIR):
            shutil.rmtree(DB_DIR)
        return {"message": "Session cleared"}
    except Exception as e:
        print(f"Error deleting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# For Render deployment - bind to PORT environment variable
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)
