"""
User model for authenticated users.

Each user has a unique Firebase UID and can have one textbook per spec (FR-013).
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..core.database import Base


class User(Base):
    """
    User model representing authenticated users.

    Attributes:
        id: Primary key
        firebase_uid: Unique Firebase user identifier
        email: User's email address
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        textbook: One-to-one relationship with Textbook (one textbook per user per spec)
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firebase_uid = Column(String(128), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    textbook = relationship("Textbook", back_populates="user", uselist=False, cascade="all, delete-orphan")
    generation_jobs = relationship("GenerationJob", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
