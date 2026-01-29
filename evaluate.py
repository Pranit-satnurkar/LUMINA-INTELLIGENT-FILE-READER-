import os
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset
from bot import chat_with_bot
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Configuration
# Note: RAGAS typically defaults to OpenAI. We need to configure it for Gemini if we want to use Gemini for evaluation.
# For simplicity in this script, we'll assume OpenAI key is available or we configure the LLC manually.
# Setting up Gemini for RAGAS metrics requires creating custom LLM/Embeddings wrappers or using recent RAGAS features.

def evaluate_bot():
    # 1. generated test set
    questions = [
        "What is the average global temperature rise?",
        "What is the Green Protocol?",
        "How much are sea levels rising?"
    ]
    
    ground_truths = [
        ["The average global temperature has risen by 1.2 degrees Celsius."],
        ["The Green Protocol of 2023 mandates a 50% reduction in industrial carbon output by 2030."],
        ["Sea levels are rising at a rate of 3.3 millimeters per year."]
    ]
    
    answers = []
    contexts = []
    
    print("Generating answers for evaluation...")
    for q in questions:
        # We need to capture the retrieved context from the bot.
        # This requires modifying bot.py to return context or using the chain directly here.
        # For now, we will simulate or we need to update bot.py to return 'source_documents'.
        
        # Let's use the chain directly to get contexts
        from bot import get_rag_chain
        chain = get_rag_chain()
        result = chain.invoke({"input": q})
        
        answers.append(result["answer"])
        # Extract page_content from documents
        retrieved_contexts = [doc.page_content for doc in result["context"]]
        contexts.append(retrieved_contexts)

    # 2. Create Dataset
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    dataset = Dataset.from_dict(data)

    # 3. Evaluate
    # We need to wrap Gemini for RAGAS if not using OpenAI
    # This part is tricky without an OpenAI key. RAGAS relies heavily on OpenAI by default.
    # We will assume the user provides OPENAI_API_KEY for evaluation or we skip this for now.
    
    print("Running RAGAS evaluation...")
    try:
        results = evaluate(
            dataset = dataset, 
            metrics=[
                faithfulness,
                answer_relevancy,
            ],
            # llm=..., # Pass Gemini LLM here if supported/configured
            # embeddings=... 
        )
        print(results)
        df = results.to_pandas()
        df.to_csv("ragas_results.csv")
        print("Results saved to ragas_results.csv")
    except Exception as e:
        print(f"RAGAS Evaluation failed (likely due to missing OpenAI Key or config): {e}")

if __name__ == "__main__":
    evaluate_bot()
