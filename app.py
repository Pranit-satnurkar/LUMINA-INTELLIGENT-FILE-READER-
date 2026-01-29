import streamlit as st
import time
from bot import chat_with_bot
from pdf_processor import PDFProcessor
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Lumina | Intelligent Reader",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# APP LOGIC (Cached for Speed)
# -----------------------------------------------------------------------------
@st.cache_resource
def load_embeddings():
    """Load and cache the embedding model to boost performance."""
    try:
        # Phase 1: Try aggressive local loading (Fastest, avoids network timeouts)
        # This fixes the 'httpx.ReadTimeout' if the model is already downloaded
        return HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'local_files_only': True}
        )
    except Exception:
        # Phase 2: Fallback to network download if local file is missing
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize Retrieval
if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "embeddings" not in st.session_state:
    with st.spinner("Waking up Lumina..."):
        st.session_state.embeddings = load_embeddings()

# -----------------------------------------------------------------------------
# CUSTOM CSS: THE 10-POINT POLISH
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* 0. ROOT VARIABLES */
    :root {
        --primary: #000000;
        --secondary: #555555;
        --accent: #2563eb; /* Electric Blue for subtle accents */
        --bg-color: #ffffff;
        --grid-color: #f6f6f6; /* Super subtle grid */
    }

    /* 1. UNIVERSAL RESET & FONTS */
    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif !important;
        background-color: var(--bg-color) !important;
        color: var(--primary) !important;
    }
    
    /* 2. BACKGROUND GRID (Subtle Canvas) */
    .stApp, div[data-testid="stAppViewContainer"], div[data-testid="stHeader"] {
        background-color: #ffffff !important;
        background-image: 
            linear-gradient(var(--grid-color) 1px, transparent 1px),
            linear-gradient(90deg, var(--grid-color) 1px, transparent 1px) !important;
        background-size: 50px 50px !important;
    }

    /* 3. SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #fafafa !important; /* Very slight tint */
        border-right: 1px solid #e5e5e5;
    }
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    /* 4. FILE UPLOADER (The "Big Opportunity") */
    [data-testid='stFileUploader'] {
        background-color: #f0f2f6 !important; /* Soft tint wrapper */
        border: 2px dashed #d1d5db !important;
        border-radius: 16px !important;
        padding: 20px !important;
    }
    /* FORCE INTERNAL DROPZONE TO BE LIGHT */
    [data-testid='stFileUploader'] section, 
    [data-testid='stFileUploader'] div, 
    [data-testid='stFileUploader'] span, 
    [data-testid='stFileUploader'] small {
        background-color: transparent !important; /* Let soft tint show */
        color: #000000 !important; /* FORCE BLACK TEXT */
    }
    /* "Browse files" Button */
    [data-testid='stFileUploader'] button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
    }

    /* 5. GHOST BUTTON (Secondary Actions - "Clear Memory") */
    .stButton button {
        background-color: transparent !important;
        color: #6b7280 !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        transition: all 0.2s;
    }
    .stButton button:hover {
        border-color: #000000 !important;
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    /* Specific target for PRIMARY buttons if we add any manually */
    /* Note: File uploader button is targeted separately above */

    /* 6. CHAT INTERFACE */
    /* User Message */
    div[data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stMarkdownContainer"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        border-radius: 20px 20px 4px 20px;
        padding: 16px 24px;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.2);
    }
    div[data-testid="stChatMessage"]:nth-child(odd) * {
        color: #ffffff !important;
    }
    
    /* Lumina Message */
    div[data-testid="stChatMessage"]:nth-child(even) div[data-testid="stMarkdownContainer"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e5e5e5;
        border-radius: 20px 20px 20px 4px;
        padding: 16px 24px;
        box-shadow: 0 5px 20px -5px rgba(0,0,0,0.05);
    }

    /* 7. INPUT BAR (Bottom) */
    [data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e5e5e5 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        caret-color: #000000 !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #000000 !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    /* FIX PLACEHOLDER VISIBILITY */
    [data-testid="stChatInput"] textarea::placeholder {
        color: #6b7280 !important;
        opacity: 1 !important; /* Firefox override */
        font-weight: 500;
    }
    ::-webkit-input-placeholder { /* Chrome/Opera/Safari */
        color: #6b7280 !important;
        opacity: 1 !important;
    }
    
    /* 8. TYPOGRAPHY UTILS */
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; }
    
    /* 9. ANIMATIONS */
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(0.95); }
        100% { opacity: 1; transform: scale(1); }
    }
    .pulsing-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        margin-left: 8px;
        animation: pulse 2s infinite;
    }
    
    /* 10. HIDE JUNK */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Re-enable header for sidebar toggle */
    header[data-testid="stHeader"] { background: transparent !important; }
    [data-testid="collapsedControl"] { color: #000 !important; }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR CONTENT
# -----------------------------------------------------------------------------
with st.sidebar:
    # Branding Polish
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="font-weight: 800; margin: 0; font-size: 24px; letter-spacing: -1px;">LUMINA</h2>
        <p style="font-size: 12px; color: #6b7280; margin: 0; font-weight: 500;">
            INTELLIGENT FILE READER <span style="color: #2563eb;">v3.0</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Upload Section ("The Big Opportunity")
    st.markdown("**📄 Document Context**")
    uploaded_file = st.file_uploader("Upload a document to begin", type="pdf")
    
    if uploaded_file:
        st.markdown("<br>", unsafe_allow_html=True)
        # Primary Action Button
        # We use a little hack to make this button look primary via inline CSS injection later if needed,
        # but the general stButton style is now 'Ghost'. 
        # For the primary 'Process' button, we might want it bold.
        if st.button("⚡ Analyze Document", use_container_width=True):
            with st.spinner("Processing..."):
                try:
                    processor = PDFProcessor()
                    chunks = processor.process_pdf(uploaded_file, uploaded_file.name)
                    if chunks:
                        st.session_state.vector_store = FAISS.from_documents(chunks, st.session_state.embeddings)
                        st.success(f"Ready. {len(chunks)} chunks loaded.")
                        st.session_state.messages = [] 
                    else:
                        st.error("Document is empty.")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    
    # Clear Memory (Destructive - placed low)
    if st.button("Clear Session Memory", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -----------------------------------------------------------------------------
# MAIN COMPONENT
# -----------------------------------------------------------------------------

# Top Nav / Status
c1, c2 = st.columns([1, 1])
with c1:
    # "System Online" - Alive Status
    st.markdown("""
    <div style="display: flex; align-items: center; color: #374151; font-weight: 600; font-size: 14px;">
        SYSTEM ONLINE <span class="pulsing-dot"></span>
    </div>
    """, unsafe_allow_html=True)
with c2:
    # Mode Dropdown Simulation
    st.markdown("""
    <div style="text-align: right; cursor: pointer; color: #111;">
        <span style="font-size: 12px; color: #6b7280; margin-right: 5px;">MODE</span>
        <b>PRECISE</b> <span style="font-size: 10px;">▼</span>
    </div>
    """, unsafe_allow_html=True)

st.write("") # Spacer

# Hero Section (Balanced Hierarchy)
st.markdown("""
<div style="padding: 40px 0px 60px 0px;">
    <h1 style="font-size: 80px; line-height: 0.9; color: #000; letter-spacing: -3px; font-weight: 800; margin-bottom: 24px;">
        ASK.<br>
        <span style="color: #404040;">ANALYZE.</span><br>
        <span style="color: #737373;">SOLVE.</span>
    </h1>
    <p style="font-size: 22px; font-weight: 500; color: #4b5563; line-height: 1.5; max-width: 600px;">
        Your creative partner for complex documents.
    </p>
</div>
""", unsafe_allow_html=True)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Area styling via CSS above (Placeholder text change below)
if prompt := st.chat_input("Ask about your uploaded document..."):
    # User
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        source_docs = []
        
        # Micro-interaction: Loading state
        message_placeholder.markdown("`Thinking...`")
        
        try:
            if st.session_state.vector_store:
                response = chat_with_bot(prompt, st.session_state.vector_store)
                if isinstance(response, dict) and "answer" in response:
                    response_text = response["answer"]
                    source_docs = response["context"]
                else:
                    response_text = str(response)
            else:
                response_text = "Please upload a document to begin the analysis."
        except Exception as e:
            response_text = f"Error: {str(e)}"

        # Streaming Output
        for char in response_text:
            full_response += char
            if len(full_response) % 3 == 0: 
                message_placeholder.markdown(full_response + "▪")
                time.sleep(0.002)
        message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Evidence / Citations
        if source_docs:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("View Supported Evidence"):
                for doc in source_docs:
                    src = os.path.basename(doc.metadata.get("source", "Doc"))
                    pg = doc.metadata.get("page", "?")
                    st.caption(f"**{src}** (Page {pg})")
                    st.markdown(f"> *{doc.page_content[:200].replace(chr(10), ' ')}...*")
