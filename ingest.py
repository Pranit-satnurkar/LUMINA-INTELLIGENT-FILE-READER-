import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DOCS_DIR = "./docs"
DB_DIR = "./faiss_index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def ingest_documents():
    # 1. Load Documents
    print(f"Loading PDFs from {DOCS_DIR}...")
    loader = PyPDFDirectoryLoader(DOCS_DIR)
    documents = loader.load()
    
    if not documents:
        return "No documents found in docs folder."

    print(f"Loaded {len(documents)} documents.")

    # 2. Split Text
    print("Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    # 3. Create Vector Store
    print(f"Creating Vector Store using {EMBEDDING_MODEL} (Local)...")
    
    # Using HuggingFace (Local CPU) - No API Key required
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # Create and Save FAISS index
    if len(chunks) > 0:
        vector_store = FAISS.from_documents(chunks, embeddings)
        vector_store.save_local(DB_DIR)
        return f"Ingestion complete. {len(documents)} documents loaded, {len(chunks)} chunks created."
    else:
        return "No chunks to ingest."

if __name__ == "__main__":
    ingest_documents()
