"""
SmartStudent AI – RAG Engine
Orchestrates document retrieval and prompt augmentation.
Initialised once at application startup.
"""
from typing import List, Dict
from rag.knowledge_base import get_all_documents
from rag import vector_store

_initialized = False


def init() -> None:
    """Build the vector index from the knowledge base. Call once at startup."""
    global _initialized
    if _initialized:
        return
    docs = get_all_documents()
    vector_store.build_index(docs)
    _initialized = True


def get_context_for_query(query: str, top_k: int = 3) -> str:
    """
    Retrieve relevant documents for `query` and format them as
    a context block to be injected into the LLM system prompt.
    """
    if not _initialized:
        init()

    docs: List[Dict] = vector_store.retrieve(query, top_k=top_k)
    if not docs:
        return ""

    lines = ["Relevant knowledge base context:"]
    for i, doc in enumerate(docs, 1):
        lines.append(f"\n[{i}] {doc['title']} ({doc['topic']})")
        lines.append(doc["content"])

    return "\n".join(lines)
