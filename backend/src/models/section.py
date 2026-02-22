"""
Section model for chapter sections.

Each chapter can have multiple sections with hierarchical subsections.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from ..core.database import Base


class Section(Base):
    """
    Section model representing a section within a chapter.

    Attributes:
        id: Primary key
        chapter_id: Foreign key to chapter
        section_number: Section number within chapter (1, 2, 3, ...)
        title: Section title
        content: Section content (Markdown)
        subsections: Hierarchical subsections (JSON array of {title, content})
        created_at: Creation timestamp
    """

    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    section_number = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=True)
    subsections = Column(JSONB, nullable=True, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    chapter = relationship("Chapter", back_populates="sections")

    def __repr__(self) -> str:
        return f"<Section(id={self.id}, number={self.section_number}, title={self.title})>"
