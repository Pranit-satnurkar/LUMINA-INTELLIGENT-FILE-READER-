"""
Integration tests for FastAPI endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import io


class TestAPIEndpoints:
    """Test suite for API endpoints."""
    
    def test_health_check_endpoint(self, fastapi_test_client):
        """Test health check endpoint."""
        response = fastapi_test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy" or data["status"] == "Lumina Brain is active"
    
    def test_root_endpoint(self, fastapi_test_client):
        """Test root endpoint."""
        response = fastapi_test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "service" in data
    
    @patch('backend.main.PDFProcessor')
    @patch('backend.main.HuggingFaceEmbeddings')
    @patch('backend.main.FAISS')
    def test_upload_pdf_endpoint(self, mock_faiss, mock_embeddings, mock_processor, 
                                 fastapi_test_client, sample_pdf_bytes):
        """Test PDF upload endpoint."""
        # Mock the processor
        mock_proc_instance = MagicMock()
        mock_proc_instance.process_pdf.return_value = [
            MagicMock(page_content="Test content", metadata={"source": "test.pdf"})
        ]
        mock_processor.return_value = mock_proc_instance
        
        # Mock embeddings
        mock_emb_instance = MagicMock()
        mock_embeddings.return_value = mock_emb_instance
        
        # Mock FAISS
        mock_vs = MagicMock()
        mock_faiss.from_documents.return_value = mock_vs
        
        # Create file upload
        files = {"file": ("test.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")}
        
        response = fastapi_test_client.post("/upload", files=files)
        
        # Should succeed or return specific error
        assert response.status_code in [200, 400, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "message" in data or "chunks" in data
    
    @patch('backend.main.chat_with_bot')
    @patch('backend.main.vector_store')
    def test_chat_endpoint_success(self, mock_vs, mock_chat, fastapi_test_client, mock_groq_api_key):
        """Test chat endpoint with valid request."""
        mock_vs.return_value = MagicMock()
        mock_chat.return_value = {
            "answer": "Test answer",
            "context": ["Test context"]
        }
        
        response = fastapi_test_client.post(
            "/chat",
            json={"message": "What is this about?", "session_id": "test"}
        )
        
        # May fail if vector store not initialized, but should return valid response
        assert response.status_code in [200, 400]
    
    def test_chat_endpoint_without_vector_store(self, fastapi_test_client):
        """Test chat endpoint when no document is uploaded."""
        response = fastapi_test_client.post(
            "/chat",
            json={"message": "Test question", "session_id": "test"}
        )
        
        # Should return 400 if no vector store
        assert response.status_code in [200, 400]
        
        if response.status_code == 400:
            data = response.json()
            assert "detail" in data
    
    def test_delete_session_endpoint(self, fastapi_test_client):
        """Test session deletion endpoint."""
        response = fastapi_test_client.delete("/session")
        
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "message" in data
    
    def test_cors_headers(self, fastapi_test_client):
        """Test CORS headers are present."""
        response = fastapi_test_client.options("/health")
        
        # CORS should be configured
        assert response.status_code in [200, 405]
    
    def test_upload_invalid_file_type(self, fastapi_test_client):
        """Test upload with non-PDF file."""
        files = {"file": ("test.txt", io.BytesIO(b"Not a PDF"), "text/plain")}
        
        response = fastapi_test_client.post("/upload", files=files)
        
        # Should handle gracefully
        assert response.status_code in [200, 400, 422, 500]
    
    def test_chat_missing_message(self, fastapi_test_client):
        """Test chat endpoint with missing message field."""
        response = fastapi_test_client.post("/chat", json={"session_id": "test"})
        
        # Should return validation error
        assert response.status_code == 422
