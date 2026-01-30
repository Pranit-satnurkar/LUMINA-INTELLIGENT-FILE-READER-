
import sys
import traceback
import os

# Ensure root is in path
sys.path.append(os.getcwd())

print("--- TESTING IMPORTS ---")

try:
    print("Attempting: from bot import get_rag_chain")
    from bot import get_rag_chain
    print("SUCCESS: from bot import get_rag_chain")
except Exception:
    print("FAILED: from bot import get_rag_chain")
    traceback.print_exc()

print("-" * 20)

try:
    print("Attempting: from api.routes.chat import router")
    from api.routes.chat import router
    print("SUCCESS: from api.routes.chat import router")
except Exception:
    print("FAILED: from api.routes.chat import router")
    traceback.print_exc()
