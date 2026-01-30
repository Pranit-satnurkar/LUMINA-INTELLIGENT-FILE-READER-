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
        return HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'local_files_only': True}
        )
    except Exception:
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize Retrieval
if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "embeddings" not in st.session_state:
    with st.spinner("Waking up Lumina..."):
        st.session_state.embeddings = load_embeddings()

# Initialize Chat History (Critical for Hero Section Logic)
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------------------------------------
# CUSTOM CSS: V4 DARK TECH REVOLUTION
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* 0. ROOT VARIABLES */
    :root {
        --primary: #000000;
        --secondary: #555555;
        --accent: #2563eb; /* Electric Blue */
        --accent-hover: #1d4ed8;
        --danger: #ef4444;
        --bg-color: #ffffff;
        --grid-color: #f3f4f6;
        --panel-bg: #151515;
        --panel-border: #2a2a2a;
        --text-body: #a1a1aa;
        --text-head: #ffffff;
    }

    /* 1. UNIVERSAL RESET & FONTS */
    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif !important;
        background-color: var(--bg-color) !important;
    }
    
    /* 2. BACKGROUND GRID (Subtle Tech Texture) */
    .stApp, div[data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        background-image: 
            linear-gradient(var(--grid-color) 1px, transparent 1px),
            linear-gradient(90deg, var(--grid-color) 1px, transparent 1px) !important;
        background-size: 40px 40px !important;
    }

    /* 3. SIDEBAR (The Control Center) */
    section[data-testid="stSidebar"] {
        background-color: #fafafa !important;
        border-right: 1px solid #e5e5e5;
    }
    section[data-testid="stSidebar"] * {
        color: #0d0d0d;
    }

    /* 4. "Step 1" UPLOAD PANEL (Active State) */
    [data-testid='stFileUploader'] {
        background-color: #f0f9ff !important; /* Light Blue Tint */
        border: 2px dashed #bae6fd !important;
        border-radius: 12px !important;
        padding: 20px !important;
        transition: all 0.3s ease;
    }
    [data-testid='stFileUploader']:hover {
        border-color: var(--accent) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
    }
    /* Force Dropzone text styles AND Backgrounds */
    [data-testid='stFileUploader'] section, 
    [data-testid='stFileUploader'] div,
    [data-testid='stFileUploader'] span,
    [data-testid='stFileUploader'] small {
        color: #0f172a !important; /* Dark Slate to contrast with Light Blue */
        background-color: transparent !important; /* Remove ANY dark angular backgrounds */
    }
    
    /* Target the SVG icon specifically if needed */
    [data-testid='stFileUploader'] svg {
        fill: #2563eb !important; /* Make upload icon blue */
    }
    [data-testid='stFileUploader'] button {
        /* "Browse files" button style inside uploader */
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        font-weight: 600 !important;
    }

    /* 5. PRIMARY BUTTON ("Analyze Document") */
    div[data-testid="stSidebar"] button[kind="primary"] {
        background-color: var(--accent) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        padding: 12px 20px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stSidebar"] button[kind="primary"]:hover {
        background-color: var(--accent-hover) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4) !important;
    }

    /* 6. DESTRUCTIVE BUTTON ("Clear Session") */
    /* Target ONLY the specific Clear button if possible, or generic secondary buttons NOT in uploader */
    section[data-testid="stSidebar"] button[kind="secondary"]:not([data-testid="baseButton-secondary"]) {
        background-color: transparent !important;
        border: 1px solid #fecaca !important;
        color: #ef4444 !important;
        font-size: 0.9em !important;
    }
    /* Specific override for clear button to be safe, using adjacent sibling or order? 
       Streamlit doesn't give IDs. Let's rely on the specific uploader override below taking precedence 
       due to specificity or !important if we scope it tightly. 
    */
    
    /* BETTER: Just style the Uploader Button to win the specificity war */
    [data-testid='stFileUploader'] button {
        background-color: #ffffff !important;
        color: #0f172a !important; /* Force Dark Text, NOT Red */
        border: 1px solid #cbd5e1 !important;
        font-weight: 600 !important;
    }

    /* 7. CHAT - USER BUBBLE (Right Aligned, Light) */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        flex-direction: row-reverse; /* Streamlit native reversal? No, CSS hacking */
        background-color: transparent;
    }
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: transparent;
    }
    
    /* User Message Container */
    div[data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stMarkdownContainer"] {
        background-color: #e5e5e5 !important; /* Lighter Gray */
        color: #171717 !important;
        border-radius: 18px 18px 0px 18px !important;
        padding: 12px 20px !important;
        max-width: 80% !important;
        margin-left: auto !important; /* Push to right */
        box-shadow: none !important;
        border: 1px solid #d4d4d4;
    }

    /* 8. CHAT - AI PANEL (Dark Tech) */
    /* This overrides the default Assistant message */
    div[data-testid="stChatMessage"]:nth-child(even) div[data-testid="stMarkdownContainer"] {
        background-color: var(--panel-bg) !important;
        color: var(--text-body) !important;
        border: 1px solid var(--panel-border) !important;
        border-radius: 16px !important;
        padding: 28px !important;
        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.3) !important;
    }
    
    /* AI Panel Typography */
    div[data-testid="stChatMessage"]:nth-child(even) h1, 
    div[data-testid="stChatMessage"]:nth-child(even) h2, 
    div[data-testid="stChatMessage"]:nth-child(even) h3, 
    div[data-testid="stChatMessage"]:nth-child(even) h4 {
        color: var(--text-head) !important;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 12px;
        letter-spacing: -0.5px;
    }
    div[data-testid="stChatMessage"]:nth-child(even) p {
        line-height: 1.7; /* Readability */
        margin-bottom: 16px;
    }
    div[data-testid="stChatMessage"]:nth-child(even) strong {
        color: #ffffff !important;
        font-weight: 600;
        text-shadow: 0 0 20px rgba(255,255,255,0.2);
    }
    
    /* "Experience Details" Data Block Simulation with CSS */
    /* Target lists in AI message to look like data blocks */
    div[data-testid="stChatMessage"]:nth-child(even) ul {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 16px 20px;
        list-style-type: none; /* Hide default bullets */
    }
    div[data-testid="stChatMessage"]:nth-child(even) li {
        color: #d4d4d4;
        padding: 8px 0;
        border-bottom: 1px solid #333;
        display: flex;
    }
    div[data-testid="stChatMessage"]:nth-child(even) li:last-child {
        border-bottom: none;
    }
    
    /* Decoration: AI Icon Label */
    div[data-testid="stChatMessage"]:nth-child(even) div[data-testid="stMarkdownContainer"]::before {
        content: "✨ SYSTEM ANALYSIS"; 
        display: block;
        font-size: 10px;
        color: var(--accent);
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 24px;
        border-bottom: 1px solid var(--panel-border);
        padding-bottom: 12px;
    }

    /* 9. VIEW EVIDENCE BUTTON (Expander Hack) */
    .streamlit-expanderHeader {
        background-color: transparent !important;
        border: 1px solid var(--secondary) !important;
        border-radius: 8px !important;
        color: var(--text-body) !important;
        font-size: 14px !important;
        padding: 8px 16px !important;
        margin-top: 10px;
        display: inline-block; /* Look like button */
    }
    .streamlit-expanderHeader:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        background-color: #1a1a1a !important;
    }

    /* 10. INPUT BAR POLISH */
    [data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--primary) !important;
    }
    /* FIX PLACEHOLDER VISIBILITY (Re-added) */
    [data-testid="stChatInput"] textarea::placeholder {
        color: #6b7280 !important;
        opacity: 1 !important;
    }
    ::-webkit-input-placeholder {
        color: #6b7280 !important;
        opacity: 1 !important;
    }
    
    /* HIDE JUNK */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] { background: transparent !important; }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR CONTENT
# -----------------------------------------------------------------------------
with st.sidebar:
    # Branding
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="font-weight: 900; margin: 0; font-size: 26px; letter-spacing: -1.5px; color: #000;">LUMINA</h2>
        <p style="font-size: 11px; color: #666; margin: 0; font-weight: 600; letter-spacing: 1px;">
            INTELLIGENT WORKSPACE <span style="color: #2563eb;">V4.0</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # STEP 1: UPLOAD (Visual Guide)
    st.markdown("""
    <div style="margin-bottom: 8px;">
        <span style="background: #eff6ff; color: #2563eb; font-size: 10px; padding: 4px 8px; border-radius: 4px; font-weight: 700;">STEP 1</span>
        <span style="font-size: 14px; font-weight: 700; color: #0f172a; margin-left: 8px;">Upload Document</span>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Drag & drop PDF here", type="pdf")
    
    if uploaded_file:
        st.markdown(f"""
        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 10px; margin-top: 10px; display: flex; align-items: center;">
            <div style="font-size: 20px; margin-right: 10px;">📄</div>
            <div>
                <div style="font-size: 12px; font-weight: 700; color: #166534;">{uploaded_file.name[:18]}...</div>
                <div style="font-size: 10px; color: #15803d;">Ready for analysis</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # PRIMARY BUTTON: ANALYZE
        if st.button("⚡ ANALYZE DOCUMENT", type="primary", use_container_width=True):
            with st.spinner("Decoding Knowledge Matrix..."):
                try:
                    processor = PDFProcessor()
                    chunks = processor.process_pdf(uploaded_file, uploaded_file.name)
                    if chunks:
                        st.session_state.vector_store = FAISS.from_documents(chunks, st.session_state.embeddings)
                        st.success(f"Processing Complete. {len(chunks)} fragments indexed.")
                        st.session_state.messages = [] 
                    else:
                        st.error("Empty Document Warning.")
                except Exception as e:
                    st.error(f"System Error: {e}")
    
    st.markdown("<div style='flex-grow: 1; height: 50px;'></div>", unsafe_allow_html=True) # Spacer
    st.markdown("---")
    
    # DESTRUCTIVE ACTION (Styled CSS targets secondary buttons in sidebar)
    st.markdown("<small style='color: #94a3b8; font-weight: 600; display: block; margin-bottom: 5px;'>SESSION CONTROLS</small>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Session Memory", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -----------------------------------------------------------------------------
# MAIN COMPONENT
# -----------------------------------------------------------------------------

# Top Nav / Status
c1, c2 = st.columns([1, 1])
with c1:
    st.markdown("""
    <div style="display: flex; align-items: center; color: #111; font-weight: 700; font-size: 14px;">
        STATUS: ONLINE <span class="pulsing-dot"></span>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div style="text-align: right; cursor: pointer; color: #111;">
        <span style="font-size: 11px; color: #94a3b8; margin-right: 8px; font-weight: 700;">MODEL</span>
        <b style="color: #000;">PRECISE v3</b> <span style="font-size: 10px; color: #2563eb;">▼</span>
    </div>
    """, unsafe_allow_html=True)

st.write("") # Spacer

# Hero Section
if not st.session_state.messages:
    st.markdown("""
    <div style="padding: 60px 0px; text-align: left;">
        <h1 style="font-size: 72px; line-height: 0.95; color: #000; letter-spacing: -3px; font-weight: 800; margin-bottom: 24px;">
            RAW DATA.<br>
            <span style="color: #2563eb;">REFINED INSIGHT.</span>
        </h1>
        <p style="font-size: 20px; font-weight: 500; color: #64748b; line-height: 1.6; max-width: 500px;">
            Upload your complex PDFs. Let Lumina structure, analyze, and extract the truth.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Chat History
# (Initialized at top of APP LOGIC)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    # Role-specific rendering happens via CSS
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input("Query your document..."):
    # User
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        source_docs = []
        
        message_placeholder.markdown("`Computing...`")
        
        try:
            if st.session_state.vector_store:
                response = chat_with_bot(prompt, st.session_state.vector_store)
                if isinstance(response, dict) and "answer" in response:
                    response_text = response["answer"]
                    source_docs = response["context"]
                else:
                    response_text = str(response)
            else:
                response_text = "⚠️ No data source detected. Please upload a document in the sidebar."
        except Exception as e:
            response_text = f"Processing Error: {str(e)}"

        # Streaming Output
        for char in response_text:
            full_response += char
            if len(full_response) % 3 == 0: 
                message_placeholder.markdown(full_response + "▪")
                time.sleep(0.002)
        message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Evidence / Citations (Styled as Button Action)
        if source_docs:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🔍 View Verified Sources"):
                for doc in source_docs:
                    src = os.path.basename(doc.metadata.get("source", "File"))
                    st.caption(f"**SOURCE: {src}**")
                    st.markdown(f"> *{doc.page_content[:200].replace(chr(10), ' ')}...*")
