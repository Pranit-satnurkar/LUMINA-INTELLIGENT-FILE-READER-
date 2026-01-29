import re

class PIIScrubber:
    """
    Experimental PII Redaction Layer.
    Removes Emails, Phone Numbers, and Credit Card patterns from text.
    """
    
    def __init__(self):
        # Regex patterns
        self.patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
            # Generic Credit Card (simple check)
            "credit_card": r'\b(?:\d[ -]*?){13,16}\b'
        }

    def scrub(self, text):
        """
        Replaces found PII with [REDACTED <Type>]
        """
        scrubbed_text = text
        for pii_type, pattern in self.patterns.items():
            scrubbed_text = re.sub(pattern, f"[REDACTED {pii_type.upper()}]", scrubbed_text)
        
        return scrubbed_text

def clean_document_content(documents):
    """
    Helper to clean a list of LangChain Document objects properly.
    """
    scrubber = PIIScrubber()
    cleaned_docs = []
    
    for doc in documents:
        # Create a deep copy or new object to avoid mutating original if needed
        doc.page_content = scrubber.scrub(doc.page_content)
        cleaned_docs.append(doc)
        
    return cleaned_docs

if __name__ == "__main__":
    # Test
    scrubber = PIIScrubber()
    test_text = "Contact me at john.doe@example.com or call 555-0199."
    print(f"Original: {test_text}")
    print(f"Scrubbed: {scrubber.scrub(test_text)}")
