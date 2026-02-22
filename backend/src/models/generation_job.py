"""
GenerationJob model for tracking async content generation jobs.

Jobs are processed by Python-RQ workers with 5-minute timeout per spec.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..core.database import Base


class GenerationJob(Base):
    """
    GenerationJob model for tracking async content generation.

    Attributes:
        id: Primary key
        user_id: Foreign key to user who initiated the job
        chapter_id: Foreign key to chapter being generated (nullable for outline jobs)
        status: Job status (pending, running, completed, failed)
        progress: Progress percentage (0-100)
        tokens_used: Total OpenAI tokens consumed
        error_message: Error details if status is failed
        started_at: Job start timestamp
        completed_at: Job completion timestamp
    """

    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=True, index=True)
    status = Column(
        Enum("pending", "running", "completed", "failed", name="job_status"),
        nullable=False,
        default="pending",
        index=True
    )
    progress = Column(Integer, default=0, nullable=False)  # 0-100
    tokens_used = Column(Integer, default=0, nullable=False)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="generation_jobs")
    chapter = relationship("Chapter", back_populates="generation_jobs")

    def __repr__(self) -> str:
        return f"<GenerationJob(id={self.id}, status={self.status}, progress={self.progress}%)>"
