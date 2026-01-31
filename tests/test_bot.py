"""
Unit tests for bot/RAG chain module.
"""
import pytest
from unittest.mock import patch, MagicMock
from backend.bot import chat_with_bot, get_rag_chain, format_docs


class TestBotFunctions:
    """Test suite for bot module functions."""
    
    def test_format_docs(self):
        """Test document formatting function."""
        mock_docs = [
            MagicMock(page_content="First document content"),
            MagicMock(page_content="Second document content"),
            MagicMock(page_content="Third document content")
        ]
        
        result = format_docs(mock_docs)
        
        assert "First document content" in result
        assert "Second document content" in result
        assert "Third document content" in result
        assert result.count("\n\n") == 2  # Two separators for three docs
    
    @patch('backend.bot.ChatGroq')
    def test_get_rag_chain_creation(self, mock_groq, mock_vector_store, mock_groq_api_key):
        """Test RAG chain creation."""
        mock_llm = MagicMock()
        mock_groq.return_value = mock_llm
        
        chain = get_rag_chain(mock_vector_store)
        
        assert chain is not None
        mock_groq.assert_called_once()
    
    @patch('backend.bot.ChatGroq')
    def test_get_rag_chain_without_api_key(self, mock_groq, mock_vector_store, monkeypatch):
        """Test RAG chain creation fails without API key."""
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        
        with pytest.raises(ValueError, match="GROQ_API_KEY"):
            get_rag_chain(mock_vector_store)
    
    @patch('backend.bot.get_rag_chain')
    def test_chat_with_bot_success(self, mock_get_chain, mock_vector_store, mock_groq_api_key):
        """Test successful chat interaction."""
        # Mock the chain to return a response
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "This is a test response from the AI."
        mock_get_chain.return_value = mock_chain
        
        result = chat_with_bot("What is this document about?", mock_vector_store)
        
        assert result is not None
        assert 'answer' in result
        assert isinstance(result['answer'], str)
        assert len(result['answer']) > 0
    
    def test_chat_with_bot_empty_vector_store(self, mock_groq_api_key):
        """Test chat with None vector store."""
        result = chat_with_bot("Test query", None)
        
        assert isinstance(result, str)
        assert "Error" in result or "error" in result.lower()
    
    @patch('backend.bot.get_rag_chain')
    def test_chat_with_bot_handles_exceptions(self, mock_get_chain, mock_vector_store, mock_groq_api_key):
        """Test that chat_with_bot handles exceptions gracefully."""
        mock_get_chain.side_effect = Exception("Test exception")
        
        result = chat_with_bot("Test query", mock_vector_store)
        
        assert isinstance(result, str)
        assert "Error" in result or "error" in result.lower()
    
    @patch('backend.bot.get_rag_chain')
    def test_chat_with_bot_returns_context(self, mock_get_chain, mock_vector_store, mock_groq_api_key):
        """Test that chat returns context information."""
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Test answer"
        mock_get_chain.return_value = mock_chain
        
        result = chat_with_bot("Test query", mock_vector_store)
        
        assert 'context' in result
        assert isinstance(result['context'], list)
