
try:
    from langchain.agents import create_tool_calling_agent
    print("SUCCESS: langchain.agents.create_tool_calling_agent")
except ImportError as e:
    print(f"FAIL: langchain.agents.create_tool_calling_agent - {e}")

try:
    from langchain.agents import AgentExecutor
    print("SUCCESS: langchain.agents.AgentExecutor")
except ImportError as e:
    print(f"FAIL: langchain.agents.AgentExecutor - {e}")
