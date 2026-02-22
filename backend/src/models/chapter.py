"""
Chapter model for textbook chapters.

Each chapter belongs to a textbook and contains sections and exercises.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..core.database import Base


class Chapter(Base):
    """
    Chapter model representing a textbook chapter.

    Attributes:
        id: Primary key
        textbook_id: Foreign key to textbook
        chapter_number: Sequential chapter number (1, 2, 3, ...)
        title: Chapter title
        objectives: Learning objectives for this chapter
        content: Main chapter content (Markdown)
        created_at: Creation timestamp
        sections: One-to-many relationship with Section
        exercises: One-to-many relationship with Exercise
    """

    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    textbook_id = Column(Integer, ForeignKey("textbooks.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    objectives = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    textbook = relationship("Textbook", back_populates="chapters")
    sections = relationship("Section", back_populates="chapter", cascade="all, delete-orphan", order_by="Section.section_number")
    exercises = relationship("Exercise", back_populates="chapter", cascade="all, delete-orphan")
    generation_jobs = relationship("GenerationJob", back_populates="chapter", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Chapter(id={self.id}, number={self.chapter_number}, title={self.title})>"
