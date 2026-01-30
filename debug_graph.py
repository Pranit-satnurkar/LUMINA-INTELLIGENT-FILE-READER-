
import os
import sys
import traceback
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from bot import get_rag_chain, chat_with_bot
from dotenv import load_dotenv

load_dotenv()

DB_DIR = "./faiss_index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

print("--- TESTING GRAPH EXECUTION ---")

try:
    print(f"1. Loading Embeddings & DB...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    if not os.path.exists(DB_DIR):
        print("   FAILED: DB Directory does not exist! Please upload a doc first.")
        sys.exit(1)
        
    vector_store = FAISS.load_local(DB_DIR, embeddings, allow_dangerous_deserialization=True)
    print("   Success.")

    print("2. Calling chat_with_bot...")
    # This calls the function exactly as api/routes/chat.py does (indirectly)
    # Actually api calls get_rag_chain then invoke. Let's test chat_with_bot wrapper first.
    response = chat_with_bot("Hello", vector_store)
    
    print(f"3. Result: {response}")
    
    if "System Error" in str(response):
        print("   DETECTED SYSTEM ERROR IN RESPONSE")

except Exception as e:
    print("\n!!! CRASHED !!!")
    traceback.print_exc()
