"""
Pytest configuration and shared fixtures for LUMINA tests.
"""
import pytest
import os
import io
from unittest.mock import Mock, MagicMock
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


@pytest.fixture
def mock_groq_api_key(monkeypatch):
    """Mock GROQ API key for testing."""
    monkeypatch.setenv("GROQ_API_KEY", "test_groq_api_key_12345")
    return "test_groq_api_key_12345"


@pytest.fixture
def sample_pdf_bytes():
    """Create a sample PDF file in memory for testing."""
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    # Add some content
    pdf.drawString(100, 750, "LUMINA Test Document")
    pdf.drawString(100, 730, "This is a test PDF document for unit testing.")
    pdf.drawString(100, 710, "It contains sample text that can be extracted and processed.")
    pdf.drawString(100, 690, "The RAG system should be able to answer questions about this content.")
    
    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    return buffer.getvalue()


@pytest.fixture
def sample_pdf_file(sample_pdf_bytes, tmp_path):
    """Create a temporary PDF file for testing."""
    pdf_path = tmp_path / "test_document.pdf"
    pdf_path.write_bytes(sample_pdf_bytes)
    return str(pdf_path)


@pytest.fixture
def sample_text_chunks():
    """Sample text chunks for testing vector store."""
    return [
        "LUMINA is an AI-powered document reader that uses RAG technology.",
        "The system can process PDF documents and answer questions about them.",
        "It uses FAISS for vector similarity search and Groq for LLM inference.",
        "The backend is built with FastAPI and the mobile app uses React Native."
    ]


@pytest.fixture
def mock_vector_store():
    """Mock FAISS vector store for testing."""
    mock_store = MagicMock()
    mock_store.as_retriever = MagicMock(return_value=MagicMock())
    mock_store.similarity_search = MagicMock(return_value=[
        MagicMock(page_content="Sample context from document", metadata={"source": "test.pdf"})
    ])
    return mock_store


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""
    return {
        "answer": "This is a test answer from the AI assistant.",
        "context": ["Sample context from document"]
    }


@pytest.fixture
def mock_embeddings():
    """Mock HuggingFace embeddings for testing."""
    mock_emb = MagicMock()
    mock_emb.embed_documents = MagicMock(return_value=[[0.1] * 384])
    mock_emb.embed_query = MagicMock(return_value=[0.1] * 384)
    return mock_emb


@pytest.fixture(autouse=True)
def cleanup_test_files(tmp_path):
    """Cleanup any test files created during testing."""
    yield
    # Cleanup happens automatically with tmp_path


@pytest.fixture
def fastapi_test_client():
    """Create a test client for FastAPI."""
    from fastapi.testclient import TestClient
    from backend.main import app
    return TestClient(app)
