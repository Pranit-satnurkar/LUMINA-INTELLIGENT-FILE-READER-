import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

try:
    import langchain
    print(f"LangChain Version: {langchain.__version__}")
    print(f"LangChain Path: {langchain.__file__}")
except ImportError as e:
    print(f"LangChain Import Failed: {e}")

try:
    import langchain.agents
    print(f"langchain.agents Path: {langchain.agents.__file__}")
    print(f"AgentExecutor in agents? {'AgentExecutor' in dir(langchain.agents)}")
except ImportError as e:
    print(f"langchain.agents Import Failed: {e}")

try:
    import langchain_community
    print(f"LangChain Community Version: {langchain_community.__version__}")
except ImportError:
    print("LangChain Community Not Found")

try:
    import langchain_groq
    print("LangChain Groq Found")
except ImportError:
    print("LangChain Groq Not Found")
