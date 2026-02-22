"""
Script to index textbook content into the RAG vector database.

Usage:
    python -m scripts.index_content --docs-dir ../docs/docs --chapter-id intro
"""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.rag import get_rag_service


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Text to chunk
        chunk_size: Maximum characters per chunk
        overlap: Number of overlapping characters between chunks

    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap
    return chunks


def index_markdown_file(
    rag_service,
    file_path: str,
    chapter_id: str,
    section_id: str | None = None,
) -> list[str]:
    """
    Index a markdown file into the vector database.

    Args:
        rag_service: RAG service instance
        file_path: Path to markdown file
        chapter_id: Chapter identifier
        section_id: Optional section identifier

    Returns:
        List of chunk IDs
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into chunks
    chunks = chunk_text(content)

    # Index each chunk
    chunk_ids = []
    for i, chunk in enumerate(chunks):
        if len(chunk.strip()) < 50:  # Skip very small chunks
            continue

        metadata = {
            "file_name": os.path.basename(file_path),
            "chunk_index": i,
        }

        chunk_id = rag_service.index_document(
            content=chunk,
            chapter_id=chapter_id,
            section_id=section_id,
            metadata=metadata,
        )
        chunk_ids.append(chunk_id)
        print(f"  Indexed chunk {i + 1}/{len(chunks)}")

    return chunk_ids


def index_docs_directory(
    rag_service,
    docs_dir: str,
    default_chapter_id: str = "general",
) -> dict[str, list[str]]:
    """
    Index all markdown files in a docs directory.

    Args:
        rag_service: RAG service instance
        docs_dir: Path to docs directory
        default_chapter_id: Default chapter ID to use

    Returns:
        Dictionary mapping file paths to chunk IDs
    """
    docs_path = Path(docs_dir)
    results = {}

    for md_file in docs_path.glob("**/*.md"):
        print(f"Indexing: {md_file}")

        # Extract chapter/section from path
        relative_path = md_file.relative_to(docs_path)
        parts = relative_path.parts

        if len(parts) > 1:
            chapter_id = parts[0]
            section_id = parts[-1].replace(".md", "")
        else:
            chapter_id = default_chapter_id
            section_id = None

        try:
            chunk_ids = index_markdown_file(
                rag_service,
                str(md_file),
                chapter_id=chapter_id,
                section_id=section_id,
            )
            results[str(md_file)] = chunk_ids
            print(f"  -> Indexed {len(chunk_ids)} chunks\n")
        except Exception as e:
            print(f"  -> Error: {e}\n")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Index textbook content into RAG vector database"
    )
    parser.add_argument(
        "--docs-dir",
        type=str,
        default="../docs/docs",
        help="Path to docs directory",
    )
    parser.add_argument(
        "--chapter-id",
        type=str,
        default="general",
        help="Default chapter ID",
    )
    parser.add_argument(
        "--clear-first",
        action="store_true",
        help="Clear existing index before indexing",
    )

    args = parser.parse_args()

    print("Initializing RAG service...")
    rag_service = get_rag_service()

    if args.clear_first:
        print("Clearing existing index...")
        rag_service.clear_all()

    print(f"Indexing docs from: {args.docs_dir}")
    results = index_docs_directory(
        rag_service,
        args.docs_dir,
        args.chapter_id,
    )

    total_chunks = sum(len(ids) for ids in results.values())
    print(f"\n✅ Indexing complete!")
    print(f"   Files indexed: {len(results)}")
    print(f"   Total chunks: {total_chunks}")


if __name__ == "__main__":
    main()
