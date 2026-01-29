import os
import time
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from expert_tools import expert_tools
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DB_DIR = "./faiss_index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
# Using Groq Llama 3 for speed and free tier access
LLM_MODEL = "llama-3.3-70b-versatile" 

# System Prompt
# System Prompt
SYSTEM_PROMPT = """You are LUMINA, an advanced Universal Document Analyst.
You are capable of reading, understanding, and extracting precise insights from ANY technical or general document (Legal, Medical, Engineering, Financial).

CORE IDENTITY:
- You are Helpful, Intelligent, and Elegant.
- Your tone is: Polished, Concise, and Direct (Apple-like minimalism).
- You DO NOT hallucinate. You rely strictly on the provided context.

RULES:
1. CITATIONS: If you state a fact from the document, cite the section/page.
2. CLARITY: Use Markdown lists, bold text, and tables to make data beautiful and readable.
3. ADAPTABILITY: Adapt your complexity to the user's question.
4. HONESTY: If the information is missing, say: "That detail isn't available in the current document."

Context:
{context}
"""

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(vector_store):
    if "GROQ_API_KEY" not in os.environ:
         raise ValueError("GROQ_API_KEY not found. Required for Chat.")
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    # Standard RAG Chain
    llm = ChatGroq(model=LLM_MODEL, temperature=0.7)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ])
    
    rag_chain = (
        RunnableParallel({"context": retriever, "input": RunnablePassthrough()})
        .assign(context_str=lambda x: format_docs(x["context"]))
        .assign(answer=(
            prompt 
            | llm 
            | StrOutputParser()
        ))
    )
    
    return rag_chain

def chat_with_bot(query, vector_store):
    try:
        if not vector_store:
            return "System Error: Database not initialized."

        chain = get_rag_chain(vector_store)
        
        # Invoke
        result = chain.invoke(query)
        
        return {'answer': result['answer'], 'context': result['context']}

    except Exception as e:
         return f"System Error: {str(e)}"
                
    except Exception as e:
         return f"System Error: {str(e)}"

if __name__ == "__main__":
    # Test
    print(chat_with_bot("What is the average global temperature rise?"))
