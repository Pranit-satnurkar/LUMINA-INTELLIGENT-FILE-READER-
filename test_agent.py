
import os
import sys
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from bot import get_rag_chain
import traceback
from dotenv import load_dotenv

load_dotenv()

DB_DIR = "./faiss_index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

print("--- TESTING AGENT CREATION ---")

try:
    print(f"1. Loading Embeddings: {EMBEDDING_MODEL}...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    print("   Success.")

    print(f"2. Loading Vector Store from {DB_DIR}...")
    if not os.path.exists(DB_DIR):
        print("   FAILED: DB Directory does not exist!")
        sys.exit(1)
        
    vector_store = FAISS.load_local(DB_DIR, embeddings, allow_dangerous_deserialization=True)
    print("   Success.")

    print("3. Creating Agent Chain...")
    chain = get_rag_chain(vector_store)
    print("   Success.")

    print("4. Invoking Chain...")
    result = chain.invoke({"input": "Hello", "chat_history": []})
    print(f"   Success. Output: {result.get('output', 'No output key')}")

except Exception as e:
    print("\n!!! CRASHED !!!")
    traceback.print_exc()
