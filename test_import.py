try:
    import langchain
    print(f"LangChain version: {langchain.__version__}")
    from langchain.chains import create_retrieval_chain
    print("Successfully imported create_retrieval_chain")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
