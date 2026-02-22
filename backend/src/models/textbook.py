"""
Textbook model for generated textbooks.

Each user can have exactly one textbook (one-to-one relationship per FR-013).
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..core.database import Base


class Textbook(Base):
    """
    Textbook model representing a generated textbook.

    Attributes:
        id: Primary key
        user_id: Foreign key to user (one textbook per user)
        title: Textbook title
        subject: Subject matter (e.g., "Introduction to Python Programming")
        level: Educational level (e.g., "High School", "Undergraduate")
        description: Optional textbook description
        created_at: Creation timestamp
        updated_at: Last update timestamp
        chapters: One-to-many relationship with Chapter
    """

    __tablename__ = "textbooks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    subject = Column(String(255), nullable=False)
    level = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="textbook")
    chapters = relationship("Chapter", back_populates="textbook", cascade="all, delete-orphan", order_by="Chapter.chapter_number")

    def __repr__(self) -> str:
        return f"<Textbook(id={self.id}, title={self.title}, subject={self.subject})>"
