import logging
import csv
import os
from datetime import datetime

class AuditLogger:
    """
    Enterprise Compliance Logger.
    Logs every user query, tool usage, and citation for liability audit trails.
    """
    def __init__(self, log_file="audit_log.csv"):
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        # Create CSV header if file doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "User_ID", "Action", "Query", "Tool_Used", "Citations_Source", "Compliance_Status"])

    def log_event(self, user_id="session_user", action="QUERY", query="", tool_used=None, citations=None, compliance="INFO"):
        """
        Logs a single event to the CSV audit trail.
        """
        timestamp = datetime.now().isoformat()
        
        # Flatten citations for CSV
        citation_str = ""
        if citations:
            citation_str = "; ".join([f"{c.metadata.get('source', 'unknown')}:p{c.metadata.get('page','?')}" for c in citations])

        try:
            with open(self.log_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, user_id, action, query, tool_used, citation_str, compliance])
        except Exception as e:
            print(f"AUDIT LOG FAILURE: {e}")

# Singleton Instance
audit_logger = AuditLogger()
