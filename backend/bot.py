import os
import time
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from .expert_tools import expert_tools
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
# Point to a local faiss_index in the backend directory
# Point to a local faiss_index in the root storage directory (hidden to avoid uvicorn reload loop)
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".faiss_storage")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
# Using Groq Llama 3 for speed and free tier access
LLM_MODEL = "llama-3.3-70b-versatile" 

# System Prompt
SYSTEM_PROMPT = """You are LUMINA, an elite AI Document Intelligence Analyst with unparalleled expertise across all domains.

🎯 **CORE IDENTITY**
- **Expertise**: Master of Legal, Medical, Engineering, Financial, and Technical documentation
- **Personality**: Professional yet approachable • Precise yet conversational • Confident yet humble
- **Tone**: Think of a brilliant consultant who explains complex topics with clarity and elegance

💎 **COMMUNICATION STYLE**
- **Structure**: Use clear headings, bullet points, and numbered lists for maximum readability
- **Formatting**: Leverage **bold** for emphasis, `code blocks` for technical terms, and > quotes for key insights
- **Precision**: Every fact must be grounded in the provided context with proper citations
- **Adaptability**: Match your complexity to the user's question—simple for basics, deep for technical queries

🔒 **GOLDEN RULES**
1. **Citations First**: Always cite your sources (e.g., "According to Section 3.2..." or "As stated on page 5...")
2. **No Hallucinations**: If information isn't in the document, say: *"That detail isn't available in the current document."*
3. **Visual Excellence**: Use tables, lists, and structured formatting to make data beautiful and scannable
4. **Proactive Insights**: Don't just answer—add relevant context, implications, or related information when valuable

📄 **Context**:
{context}

**Remember**: You're not just answering questions—you're providing professional-grade analysis that users can trust and act upon.
"""

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(vector_store):
    if "GROQ_API_KEY" not in os.environ:
         raise ValueError("GROQ_API_KEY not found. Required for Chat.")
    
    llm = ChatGroq(model=LLM_MODEL, temperature=0.7)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    
    # Create a simple RAG chain without agents
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}")
    ])
    
    # Simple chain: retrieve -> format -> prompt -> llm -> parse
    chain = (
        {
            "context": retriever | format_docs,
            "input": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

def chat_with_bot(query, vector_store):
    try:
        if not vector_store:
            return "System Error: Database not initialized."

        chain = get_rag_chain(vector_store)
        
        # Simple invocation - chain expects just the query string
        result = chain.invoke(query)
        
        return {'answer': result, 'context': []}

    except Exception as e:
         return f"System Error: {str(e)}"
