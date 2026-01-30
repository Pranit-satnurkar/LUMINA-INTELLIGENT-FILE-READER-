from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from bot import get_rag_chain
import os

router = APIRouter()

# Configuration
DB_DIR = "./faiss_index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

class ChatRequest(BaseModel):
    query: str
    history: list = [] # Future support for history

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    RAG Chat Endpoint.
    """

    try:
        print("--- DEBUG: Entering Chat Endpoint ---")
        # 1. Load Vector Store
        if not os.path.exists(DB_DIR):
             raise HTTPException(status_code=404, detail="Knowledge Base not found. Please upload a document first.")
             
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        try:
            vector_store = FAISS.load_local(DB_DIR, embeddings, allow_dangerous_deserialization=True)
            print("--- DEBUG: Vector Store Loaded ---")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load knowledge base: {str(e)}")

        # 2. Get Chain
        try:
            chain = get_rag_chain(vector_store)
            print("--- DEBUG: Chain Created ---")
        except ValueError as e:
             raise HTTPException(status_code=500, detail=str(e)) # Likely Missing API Key

        # 3. Invoke
        # LangGraph inputs
        print(f"--- DEBUG: Invoking Chain with query: {request.query} ---")
        result = chain.invoke({"messages": [{"role": "user", "content": request.query}]})
        print(f"--- DEBUG: Invoke Result Type: {type(result)} ---")
        
        # 4. Format Response
        last_msg = result["messages"][-1]
        print(f"--- DEBUG: Last Message: {last_msg.content} ---")
        return {
            "answer": last_msg.content,
            "citations": [] 
        }

    except Exception as e:
        import traceback
        print("!!! EXCEPTION IN CHAT ENDPOINT !!!")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
