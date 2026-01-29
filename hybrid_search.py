from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from typing import List

class HybridRetriever(BaseRetriever):
    """
    A simple Hybrid Retriever that combines BM25 and Vector Search results 
    using Reciprocal Rank Fusion (RRF).
    Bypasses the 'langchain.retrievers.EnsembleRetriever' import issues.
    """
    bm25_retriever: BaseRetriever
    faiss_retriever: BaseRetriever
    k: int = 5

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun = None
    ) -> List[Document]:
        
        # 1. Get results from both
        bm25_docs = self.bm25_retriever.invoke(query)
        faiss_docs = self.faiss_retriever.invoke(query)
        
        # 2. RRF Algorithm
        # Assign scores: 1 / (k + rank)
        rrf_score = {}
        const_k = 60
        
        for rank, doc in enumerate(bm25_docs):
            if doc.page_content not in rrf_score:
                rrf_score[doc.page_content] = {"doc": doc, "score": 0}
            rrf_score[doc.page_content]["score"] += 1 / (const_k + rank + 1)
            
        for rank, doc in enumerate(faiss_docs):
            if doc.page_content not in rrf_score:
                rrf_score[doc.page_content] = {"doc": doc, "score": 0}
            rrf_score[doc.page_content]["score"] += 1 / (const_k + rank + 1)
            
        # 3. Sort by score
        sorted_docs = sorted(rrf_score.values(), key=lambda x: x["score"], reverse=True)
        
        # Return top k docs
        return [item["doc"] for item in sorted_docs[:self.k]]
