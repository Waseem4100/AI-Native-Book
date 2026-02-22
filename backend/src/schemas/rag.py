"""
RAG chatbot schemas.

This module defines request/response models for the RAG chatbot API.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single message in the chat conversation."""

    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(..., description="User's question or message")
    conversation_history: List[ChatMessage] = Field(
        default_factory=list,
        description="Previous conversation messages",
    )
    chapter_id: Optional[str] = Field(
        None,
        description="Optional chapter ID to scope the search",
    )
    section_id: Optional[str] = Field(
        None,
        description="Optional section ID to scope the search",
    )
    selected_text: Optional[str] = Field(
        None,
        description="Optional text selected by user for context",
    )


class SourceDocument(BaseModel):
    """A source document chunk used in the response."""

    content: str = Field(..., description="Document content")
    chapter_id: str = Field(..., description="Chapter identifier")
    section_id: str = Field(..., description="Section identifier")
    score: float = Field(..., description="Relevance score")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    answer: str = Field(..., description="AI-generated answer")
    sources: List[SourceDocument] = Field(
        default_factory=list,
        description="Source documents used in the answer",
    )
    conversation_history: List[ChatMessage] = Field(
        default_factory=list,
        description="Updated conversation history",
    )


class IndexRequest(BaseModel):
    """Request model for indexing documents."""

    content: str = Field(..., description="Document content to index")
    chapter_id: str = Field(..., description="Chapter identifier")
    section_id: Optional[str] = Field(None, description="Section identifier")
    metadata: Optional[dict] = Field(
        None, description="Additional metadata"
    )


class IndexBatchRequest(BaseModel):
    """Request model for batch indexing documents."""

    documents: List[IndexRequest] = Field(
        ..., description="List of documents to index"
    )


class IndexResponse(BaseModel):
    """Response model for indexing endpoints."""

    success: bool = Field(..., description="Whether indexing succeeded")
    chunk_ids: List[str] = Field(
        default_factory=list, description="IDs of indexed chunks"
    )
    message: str = Field(..., description="Status message")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(..., description="Service status")
    qdrant_connected: bool = Field(
        ..., description="Whether Qdrant is connected"
    )
    openai_connected: bool = Field(
        ..., description="Whether OpenAI is accessible"
    )
