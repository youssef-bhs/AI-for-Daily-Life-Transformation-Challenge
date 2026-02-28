"""
API router – RAG-powered AI Chat
Endpoint: POST /api/chat/ask
"""
from fastapi import APIRouter, HTTPException
from models import ChatRequest, ChatResponse
from llm_client import chat_with_rag
from rag import rag_engine

router = APIRouter()

# Initialise the RAG index when the router module is first imported
rag_engine.init()


@router.post("/ask", response_model=ChatResponse, summary="Ask SmartStudent AI (RAG-powered)")
def ask(request: ChatRequest):
    """
    Send a question to the SmartStudent AI assistant.
    The assistant retrieves relevant knowledge base documents (RAG) before
    generating an answer, ensuring grounded and accurate responses.

    Supports multi-turn conversation via `conversation_history`.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # 1. Retrieve relevant context from the vector store
    rag_ctx = rag_engine.get_context_for_query(request.question, top_k=request.top_k_docs)

    # Extract doc titles for transparency
    from rag import vector_store
    retrieved_docs_raw = vector_store.retrieve(request.question, top_k=request.top_k_docs)
    doc_titles = [d.get("title", "") for d in retrieved_docs_raw]

    # 2. Format conversation history
    history = None
    if request.conversation_history:
        history = [{"role": m.role, "content": m.content} for m in request.conversation_history]

    # 3. Call LLM with RAG-augmented prompt
    try:
        answer = chat_with_rag(
            question=request.question,
            rag_context=rag_ctx,
            conversation_history=history,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    from llm_client import get_provider_name
    return ChatResponse(answer=answer, retrieved_docs=doc_titles, provider=get_provider_name())


@router.get("/topics", summary="List available RAG knowledge topics")
def list_topics():
    """Returns the topics covered by the RAG knowledge base."""
    from rag.knowledge_base import get_all_documents
    docs = get_all_documents()
    topics = sorted(set(d["topic"] for d in docs))
    titles_by_topic = {}
    for d in docs:
        titles_by_topic.setdefault(d["topic"], []).append(d["title"])
    return {"topics": topics, "documents": titles_by_topic}
