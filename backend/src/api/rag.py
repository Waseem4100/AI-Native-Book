"""
RAG Chatbot API endpoints.

This module provides endpoints for the RAG-based chatbot,
including chat, document indexing, and health checks.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from openai import OpenAI
from sqlalchemy.orm import Session

from ..core.config import settings
from ..core.database import get_db
from ..core.security import get_current_user_optional
from ..models.user import User
from ..schemas.rag import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    HealthResponse,
    IndexBatchRequest,
    IndexRequest,
    IndexResponse,
    SourceDocument,
)
from ..services.rag import get_rag_service

router = APIRouter(prefix="/rag", tags=["RAG Chatbot"])


def _build_system_prompt() -> str:
    """
    Build the system prompt for the RAG chatbot.

    Returns:
        str: System prompt instructing the AI on how to respond
    """
    return """You are an intelligent textbook assistant for "Physical AI & Humanoid Robotics".

RULES:
1. Answer questions ONLY based on the provided context from the textbook
2. If the answer cannot be found in the context, say: "I don't have enough information from the textbook to answer this question."
3. Always cite which chapter/section your answer comes from
4. Be concise but thorough
5. Use technical terms appropriately for a university-level audience
6. If asked about something outside the textbook scope, politely decline

When providing answers:
- Start with a direct answer
- Explain the concept clearly
- Reference the specific chapter/section
- If relevant, connect to related concepts in the textbook"""


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with the textbook AI",
    description="Ask questions about the textbook content. The AI will answer based on the textbook.",
)
async def chat(
    request: ChatRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Chat with the RAG-powered textbook AI.

    This endpoint:
    1. Retrieves relevant context from the vector database
    2. Sends the context + question to OpenAI
    3. Returns the AI-generated answer with sources

    Args:
        request: Chat request with message and optional context
        current_user: Optional authenticated user

    Returns:
        ChatResponse: AI answer with sources and updated conversation history
    """
    rag_service = get_rag_service()

    # Build search query (combine message with selected text if provided)
    search_query = request.message
    if request.selected_text:
        search_query = f"{request.selected_text} {request.message}"

    # Search for relevant context
    context_docs = rag_service.search(
        query=search_query,
        chapter_id=request.chapter_id,
        section_id=request.section_id,
    )

    if not context_docs:
        return ChatResponse(
            answer="I don't have enough information from the textbook to answer this question. Please try rephrasing or selecting a different topic.",
            sources=[],
            conversation_history=request.conversation_history
            + [
                ChatMessage(role="user", content=request.message),
                ChatMessage(
                    role="assistant",
                    content="I don't have enough information from the textbook to answer this question.",
                ),
            ],
        )

    # Build context string
    context_parts = []
    for i, doc in enumerate(context_docs, 1):
        context_parts.append(
            f"[Source {i}] (Chapter: {doc['chapter_id']}, Section: {doc['section_id']})\n{doc['content']}"
        )
    context_text = "\n\n".join(context_parts)

    # Build messages for OpenAI
    messages = [
        {"role": "system", "content": _build_system_prompt()},
    ]

    # Add conversation history
    for msg in request.conversation_history:
        messages.append({"role": msg.role, "content": msg.content})

    # Add current context and question
    user_message = f"""Context from textbook:
{context_text}

Question: {request.message}"""

    if request.selected_text:
        user_message = f"""Selected text: {request.selected_text}

{user_message}"""

    messages.append({"role": "user", "content": user_message})

    # Call OpenAI
    openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = openai_client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        max_tokens=settings.RAG_MAX_TOKENS,
        temperature=settings.RAG_TEMPERATURE,
    )

    answer = response.choices[0].message.content

    # Format sources
    sources = [
        SourceDocument(
            content=doc["content"],
            chapter_id=doc["chapter_id"],
            section_id=doc["section_id"],
            score=doc["score"],
        )
        for doc in context_docs
    ]

    # Update conversation history
    updated_history = request.conversation_history + [
        ChatMessage(role="user", content=request.message),
        ChatMessage(role="assistant", content=answer),
    ]

    return ChatResponse(
        answer=answer,
        sources=sources,
        conversation_history=updated_history,
    )


@router.post(
    "/index",
    response_model=IndexResponse,
    summary="Index a document chunk",
    description="Add a document chunk to the vector database for RAG search.",
)
async def index_document(
    request: IndexRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Index a single document chunk.

    Args:
        request: Document indexing request
        current_user: Optional authenticated user

    Returns:
        IndexResponse: Status and chunk ID
    """
    try:
        rag_service = get_rag_service()
        chunk_id = rag_service.index_document(
            content=request.content,
            chapter_id=request.chapter_id,
            section_id=request.section_id,
            metadata=request.metadata,
        )
        return IndexResponse(
            success=True,
            chunk_ids=[chunk_id],
            message="Document indexed successfully",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to index document: {str(e)}",
        )


@router.post(
    "/index/batch",
    response_model=IndexResponse,
    summary="Index multiple document chunks",
    description="Add multiple document chunks to the vector database in batch.",
)
async def index_documents_batch(
    request: IndexBatchRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Index multiple document chunks in batch.

    Args:
        request: Batch indexing request with list of documents
        current_user: Optional authenticated user

    Returns:
        IndexResponse: Status and list of chunk IDs
    """
    try:
        rag_service = get_rag_service()
        documents = [
            {
                "content": doc.content,
                "chapter_id": doc.chapter_id,
                "section_id": doc.section_id,
                "metadata": doc.metadata,
            }
            for doc in request.documents
        ]
        chunk_ids = rag_service.index_documents(documents)
        return IndexResponse(
            success=True,
            chunk_ids=chunk_ids,
            message=f"Successfully indexed {len(chunk_ids)} documents",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to index documents: {str(e)}",
        )


@router.delete(
    "/chapter/{chapter_id}",
    response_model=IndexResponse,
    summary="Delete chapter documents",
    description="Remove all indexed documents for a specific chapter.",
)
async def delete_chapter_documents(
    chapter_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Delete all indexed documents for a chapter.

    Args:
        chapter_id: Chapter identifier
        current_user: Optional authenticated user

    Returns:
        IndexResponse: Status message
    """
    try:
        rag_service = get_rag_service()
        rag_service.delete_chapter(chapter_id)
        return IndexResponse(
            success=True,
            chunk_ids=[],
            message=f"Deleted all documents for chapter {chapter_id}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete chapter documents: {str(e)}",
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health status of RAG services.",
)
async def health_check():
    """
    Check health of RAG services.

    Returns:
        HealthResponse: Status of Qdrant and OpenAI connections
    """
    rag_service = get_rag_service()

    # Check Qdrant
    qdrant_connected = False
    try:
        rag_service.qdrant_client.get_collections()
        qdrant_connected = True
    except Exception:
        pass

    # Check OpenAI
    openai_connected = False
    try:
        openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        openai_client.models.list()
        openai_connected = True
    except Exception:
        pass

    return HealthResponse(
        status="healthy" if qdrant_connected and openai_connected else "degraded",
        qdrant_connected=qdrant_connected,
        openai_connected=openai_connected,
    )
