
try:
    from langchain.tools.retriever import create_retriever_tool
    print("SUCCESS: langchain.tools.retriever")
except ImportError as e:
    print(f"FAIL: langchain.tools.retriever - {e}")

try:
    from langchain.tools import create_retriever_tool
    print("SUCCESS: langchain.tools")
except ImportError as e:
    print(f"FAIL: langchain.tools - {e}")

try:
    from langchain_core.tools import create_retriever_tool
    print("SUCCESS: langchain_core.tools")
except ImportError as e:
    print(f"FAIL: langchain_core.tools - {e}")
