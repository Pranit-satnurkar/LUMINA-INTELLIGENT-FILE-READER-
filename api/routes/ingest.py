from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from pdf_processor import PDFProcessor
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

router = APIRouter()

# Configuration
DOCS_DIR = "./docs"
DB_DIR = "./faiss_index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Uploads a PDF, saves it, and adds it to the Vector DB.
    """
    try:
        # 1. Save File Locally
        file_path = os.path.join(DOCS_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Process PDF
        # Re-open the file for processing to ensure clean read
        with open(file_path, "rb") as f:
            processor = PDFProcessor()
            chunks = processor.process_pdf(f, file.filename)
            
        if not chunks:
            raise HTTPException(status_code=400, detail="No text extracted from PDF.")

        # 3. Update/Create Vector Store
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        
        if os.path.exists(DB_DIR):
            # Load existing
            try:
                vector_store = FAISS.load_local(DB_DIR, embeddings, allow_dangerous_deserialization=True)
                vector_store.add_documents(chunks)
            except:
                # If load fails (corrupt or old version), create new
                vector_store = FAISS.from_documents(chunks, embeddings)
        else:
            # Create new
            vector_store = FAISS.from_documents(chunks, embeddings)
            
        # Save updated index
        vector_store.save_local(DB_DIR)
        
        return {
            "status": "success", 
            "filename": file.filename, 
            "chunks_added": len(chunks),
            "message": "Document indexed successfully."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
