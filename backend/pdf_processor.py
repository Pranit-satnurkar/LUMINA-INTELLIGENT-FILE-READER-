import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from .security_layer import PIIScrubber

class PDFProcessor:
    """
    Handles PDF extraction and PII scrubbing in-memory.
    """
    def __init__(self):
        self.scrubber = PIIScrubber()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            add_start_index=True,
        )

    def process_pdf(self, file_stream, filename):
        """
        Reads a PDF file stream (BytesIO), extracts text/tables, scrubs PII, 
        and returns a list of LangChain Documents.
        """
        raw_text = ""
        
        # 1. Extract Text using PDFPlumber (Better for tables)
        with pdfplumber.open(file_stream) as pdf:
            for i, page in enumerate(pdf.pages):
                # Extract text
                text = page.extract_text()
                if text:
                    # Scrub PII immediately
                    clean_text = self.scrubber.scrub(text)
                    raw_text += f"\n\n--- Page {i+1} ---\n{clean_text}"
                
                # Future: Extract tables and format as Markdown here
                # tables = page.extract_tables() ...

        if not raw_text.strip():
            return None

        # 2. Create Base Document
        doc = Document(page_content=raw_text, metadata={"source": filename})

        # 3. Split into Chunks
        chunks = self.text_splitter.split_documents([doc])
        
        # Add page numbers to chunks (approximate, since we concatenated)
        # For a truly accurate page number, we'd split page-by-page.
        # Let's refine this to be page-based for better citations.
        
        final_chunks = []
        with pdfplumber.open(file_stream) as pdf:
             for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text: continue
                
                clean_text = self.scrubber.scrub(text)
                page_doc = Document(
                    page_content=clean_text, 
                    metadata={"source": filename, "page": i+1}
                )
                page_chunks = self.text_splitter.split_documents([page_doc])
                final_chunks.extend(page_chunks)

        return final_chunks
