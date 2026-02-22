"""
RAG (Retrieval-Augmented Generation) service for textbook Q&A.

This module handles document embedding, vector storage, and semantic search
using Qdrant vector database and OpenAI embeddings.
"""

import hashlib
from typing import List, Optional

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams

from ..core.config import settings


class RAGService:
    """
    Service for RAG operations including document indexing and retrieval.

    Uses OpenAI for embeddings and Qdrant for vector storage.
    """

    def __init__(self):
        """Initialize RAG service with OpenAI and Qdrant clients."""
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.qdrant_client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self.embedding_model = settings.OPENAI_EMBEDDING_MODEL
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """
        Ensure the Qdrant collection exists with proper configuration.

        Creates the collection if it doesn't exist.
        """
        collections = self.qdrant_client.get_collections().collections
        collection_exists = any(
            c.name == self.collection_name for c in collections
        )

        if not collection_exists:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1536,  # text-embedding-3-small dimension
                    distance=Distance.COSINE,
                ),
            )
            # Create payload index for efficient filtering
            self.qdrant_client.create_payload_index(
                collection_name=self.collection_name,
                field_name="chapter_id",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )
            self.qdrant_client.create_payload_index(
                collection_name=self.collection_name,
                field_name="section_id",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )

    def _get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text using OpenAI.

        Args:
            text: Text to embed

        Returns:
            List[float]: Embedding vector (1536 dimensions)
        """
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text,
        )
        return response.data[0].embedding

    def _generate_chunk_id(self, content: str, metadata: dict) -> str:
        """
        Generate unique ID for a chunk based on content and metadata.

        Args:
            content: Chunk content
            metadata: Chunk metadata

        Returns:
            str: Unique chunk ID
        """
        unique_string = f"{content}:{metadata.get('chapter_id', '')}:{metadata.get('section_id', '')}"
        return hashlib.md5(unique_string.encode()).hexdigest()

    def index_document(
        self,
        content: str,
        chapter_id: str,
        section_id: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> str:
        """
        Index a document chunk in the vector database.

        Args:
            content: Document content to index
            chapter_id: Chapter identifier
            section_id: Optional section identifier
            metadata: Additional metadata to store

        Returns:
            str: Chunk ID
        """
        # Generate embedding
        embedding = self._get_embedding(content)

        # Prepare metadata
        payload = {
            "content": content,
            "chapter_id": chapter_id,
            "section_id": section_id or "",
            **(metadata or {}),
        }

        # Generate unique ID
        chunk_id = self._generate_chunk_id(content, payload)

        # Upsert to Qdrant
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=chunk_id,
                    vector=embedding,
                    payload=payload,
                )
            ],
        )

        return chunk_id

    def index_documents(
        self, documents: List[dict]
    ) -> List[str]:
        """
        Index multiple document chunks in batch.

        Args:
            documents: List of dicts with keys: content, chapter_id, section_id, metadata

        Returns:
            List[str]: List of chunk IDs
        """
        if not documents:
            return []

        # Generate embeddings in batch
        contents = [doc["content"] for doc in documents]
        embeddings_response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=contents,
        )
        embeddings = [e.embedding for e in embeddings_response.data]

        # Prepare points
        points = []
        chunk_ids = []
        for i, doc in enumerate(documents):
            payload = {
                "content": doc["content"],
                "chapter_id": doc["chapter_id"],
                "section_id": doc.get("section_id", ""),
                **(doc.get("metadata") or {}),
            }
            chunk_id = self._generate_chunk_id(doc["content"], payload)
            chunk_ids.append(chunk_id)
            points.append(
                models.PointStruct(
                    id=chunk_id,
                    vector=embeddings[i],
                    payload=payload,
                )
            )

        # Upsert batch
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

        return chunk_ids

    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
        chapter_id: Optional[str] = None,
        section_id: Optional[str] = None,
    ) -> List[dict]:
        """
        Search for relevant document chunks.

        Args:
            query: Search query
            top_k: Number of results (defaults to settings.RAG_TOP_K)
            chapter_id: Optional filter by chapter
            section_id: Optional filter by section

        Returns:
            List[dict]: Search results with content and metadata
        """
        # Generate query embedding
        query_embedding = self._get_embedding(query)

        # Build filter
        filter_conditions = []
        if chapter_id:
            filter_conditions.append(
                models.FieldCondition(
                    key="chapter_id",
                    match=models.MatchValue(value=chapter_id),
                )
            )
        if section_id:
            filter_conditions.append(
                models.FieldCondition(
                    key="section_id",
                    match=models.MatchValue(value=section_id),
                )
            )

        search_filter = (
            models.Filter(must=filter_conditions) if filter_conditions else None
        )

        # Search
        results = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            query_filter=search_filter,
            limit=top_k or settings.RAG_TOP_K,
            with_payload=True,
        )

        # Format results
        return [
            {
                "content": result.payload.get("content", ""),
                "chapter_id": result.payload.get("chapter_id", ""),
                "section_id": result.payload.get("section_id", ""),
                "score": result.score,
            }
            for result in results
        ]

    def delete_chapter(self, chapter_id: str) -> int:
        """
        Delete all chunks for a chapter.

        Args:
            chapter_id: Chapter identifier

        Returns:
            int: Number of deleted points
        """
        result = self.qdrant_client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="chapter_id",
                            match=models.MatchValue(value=chapter_id),
                        )
                    ]
                )
            ),
        )
        return result.status

    def clear_all(self) -> None:
        """Delete all documents from the vector database."""
        self.qdrant_client.delete_collection(self.collection_name)
        self._ensure_collection()


# Singleton instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """
    Get or create RAG service singleton.

    Returns:
        RAGService: RAG service instance
    """
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
