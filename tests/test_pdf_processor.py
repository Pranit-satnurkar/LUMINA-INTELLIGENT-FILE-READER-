"""
Unit tests for PDF processor module.
"""
import pytest
import io
from backend.pdf_processor import PDFProcessor


class TestPDFProcessor:
    """Test suite for PDFProcessor class."""
    
    def test_pdf_processor_initialization(self):
        """Test that PDFProcessor initializes correctly."""
        processor = PDFProcessor()
        assert processor is not None
        assert hasattr(processor, 'process_pdf')
    
    def test_process_pdf_with_valid_file(self, sample_pdf_bytes):
        """Test PDF processing with a valid PDF file."""
        processor = PDFProcessor()
        pdf_stream = io.BytesIO(sample_pdf_bytes)
        
        chunks = processor.process_pdf(pdf_stream, "test.pdf")
        
        assert chunks is not None
        assert len(chunks) > 0
        assert all(hasattr(chunk, 'page_content') for chunk in chunks)
    
    def test_process_pdf_extracts_text(self, sample_pdf_bytes):
        """Test that PDF processing extracts text content."""
        processor = PDFProcessor()
        pdf_stream = io.BytesIO(sample_pdf_bytes)
        
        chunks = processor.process_pdf(pdf_stream, "test.pdf")
        
        # Check that text was extracted
        all_text = " ".join(chunk.page_content for chunk in chunks)
        assert "LUMINA" in all_text or "test" in all_text.lower()
    
    def test_process_pdf_with_empty_file(self):
        """Test PDF processing with an empty file."""
        processor = PDFProcessor()
        empty_stream = io.BytesIO(b"")
        
        with pytest.raises(Exception):
            processor.process_pdf(empty_stream, "empty.pdf")
    
    def test_process_pdf_chunks_have_metadata(self, sample_pdf_bytes):
        """Test that processed chunks contain metadata."""
        processor = PDFProcessor()
        pdf_stream = io.BytesIO(sample_pdf_bytes)
        
        chunks = processor.process_pdf(pdf_stream, "test.pdf")
        
        for chunk in chunks:
            assert hasattr(chunk, 'metadata')
            assert 'source' in chunk.metadata or 'page' in chunk.metadata
    
    def test_process_pdf_chunk_size(self, sample_pdf_bytes):
        """Test that chunks are reasonably sized."""
        processor = PDFProcessor()
        pdf_stream = io.BytesIO(sample_pdf_bytes)
        
        chunks = processor.process_pdf(pdf_stream, "test.pdf")
        
        for chunk in chunks:
            # Chunks should not be empty
            assert len(chunk.page_content) > 0
            # Chunks should not be excessively large (default is 1000 chars)
            assert len(chunk.page_content) <= 2000
