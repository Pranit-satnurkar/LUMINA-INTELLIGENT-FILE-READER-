# RAG-Powered Expert Chatbot
A versatile RAG-powered assistant designed to analyze technical documents, IS Codes, and reports with precision. Using **Groq (Llama 3.3)** for reasoning and **Local Embeddings** for privacy.

## Features
- **RAG Architecture**: Uses LangChain, FAISS, and Local Embeddings to retrieve relevant context.
- **Universal Expert**: Can analyze Civil Engineering standards, financial reports, or scientific papers.
- **Engineering Accuracy**: Uses **Hybrid Search** (Keyword + Semantic) to find exact clauses.
- **Advanced Tables**: Improved table parsing with `pdfplumber`.
- **Security First**: PII Redaction (scrubs emails/phones) and **Ephemeral Memory** (data vanishes on close).
- **Expert Tools**: Built-in Unit Converter and Compliance Checker.
- **Streamlit UI**: A simple chat interface.
- **Evaluation**: RAGAS integration for assessing Faithfulness and Answer Relevancy.

## Setup

1. **Install Dependencies**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   pip install reportlab  # For generating dummy data
   ```

2. **Environment Variables**:
   Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=gsk_your_groq_api_key
   # Note: Uses Groq (Llama 3.3) for Chat. Embeddings are local (HuggingFace).
   ```

3. **Data Ingestion**:
   - Place PDFs in `/docs` (or run `python create_dummy_pdf.py` to generate one).
   - Run the ingestion script:
     ```bash
     python ingest.py
     ```

4. **Run the Chatbot**:
   ```bash
   streamlit run app.py
   ```

5. **Run Evaluation**:
   ```bash
   python evaluate.py
   ```

## Directory Structure
- `/docs`: PDF documents.
- `/faiss_index`: Vector database storage.
- `bot.py`: Core chatbot logic.
- `app.py`: Streamlit application.
- `ingest.py`: Document processing script.
- `evaluate.py`: RAGAS evaluation script.
