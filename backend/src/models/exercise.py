"""
Exercise model for chapter exercises and practice problems.

Each chapter can have multiple exercises with varying difficulty levels.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..core.database import Base


class Exercise(Base):
    """
    Exercise model representing practice problems and exercises.

    Attributes:
        id: Primary key
        chapter_id: Foreign key to chapter
        question: Exercise question or problem statement
        difficulty: Difficulty level (easy, medium, hard)
        solution: Model solution or answer
        explanation: Step-by-step explanation of solution
        created_at: Creation timestamp
    """

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    question = Column(Text, nullable=False)
    difficulty = Column(
        Enum("easy", "medium", "hard", name="difficulty_level"),
        nullable=False,
        default="medium"
    )
    solution = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    chapter = relationship("Chapter", back_populates="exercises")

    def __repr__(self) -> str:
        return f"<Exercise(id={self.id}, difficulty={self.difficulty})>"
