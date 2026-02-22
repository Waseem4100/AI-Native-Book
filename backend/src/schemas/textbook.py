"""
Pydantic schemas for textbook generation API.

This module defines request/response models for textbook-related endpoints.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SectionOutline(BaseModel):
    """
    Section outline schema.

    Attributes:
        section_number: Sequential section number
        title: Section title
    """

    section_number: int = Field(..., ge=1, description="Section number (1, 2, 3, ...)")
    title: str = Field(..., min_length=1, max_length=500, description="Section title")

    class Config:
        json_schema_extra = {
            "example": {
                "section_number": 1,
                "title": "Variables and Data Types",
            }
        }


class ChapterOutline(BaseModel):
    """
    Chapter outline schema.

    Attributes:
        chapter_number: Sequential chapter number
        title: Chapter title
        objectives: Learning objectives for the chapter
        sections: List of section outlines
    """

    chapter_number: int = Field(..., ge=1, description="Chapter number (1, 2, 3, ...)")
    title: str = Field(..., min_length=1, max_length=500, description="Chapter title")
    objectives: Optional[str] = Field(None, description="Learning objectives")
    sections: List[SectionOutline] = Field(default_factory=list, description="Section outlines")

    class Config:
        json_schema_extra = {
            "example": {
                "chapter_number": 1,
                "title": "Introduction to Python",
                "objectives": "Understand basic Python syntax and data types",
                "sections": [
                    {"section_number": 1, "title": "Variables and Data Types"},
                    {"section_number": 2, "title": "Basic Operations"},
                ],
            }
        }


class TextbookCreate(BaseModel):
    """
    Request schema for creating/generating a textbook outline.

    Attributes:
        subject: Subject matter (e.g., "Introduction to Python Programming")
        level: Educational level (e.g., "High School", "Undergraduate")
        num_chapters: Number of chapters to generate (default: 10)
        description: Optional textbook description
    """

    subject: str = Field(..., min_length=3, max_length=255, description="Subject matter")
    level: str = Field(..., min_length=2, max_length=100, description="Educational level")
    num_chapters: int = Field(default=10, ge=3, le=30, description="Number of chapters to generate")
    description: Optional[str] = Field(None, max_length=1000, description="Textbook description")

    class Config:
        json_schema_extra = {
            "example": {
                "subject": "Introduction to Python Programming",
                "level": "High School",
                "num_chapters": 12,
                "description": "A comprehensive introduction to Python for beginners",
            }
        }


class TextbookUpdate(BaseModel):
    """
    Request schema for updating textbook structure.

    Attributes:
        title: Textbook title
        description: Textbook description
        chapters: Updated chapter outlines
    """

    title: Optional[str] = Field(None, min_length=1, max_length=500, description="Textbook title")
    description: Optional[str] = Field(None, max_length=1000, description="Textbook description")
    chapters: Optional[List[ChapterOutline]] = Field(None, description="Updated chapter outlines")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Python Programming: A Beginner's Guide",
                "description": "Updated description",
                "chapters": [
                    {
                        "chapter_number": 1,
                        "title": "Getting Started with Python",
                        "objectives": "Learn basic Python setup and syntax",
                        "sections": [
                            {"section_number": 1, "title": "Installing Python"},
                            {"section_number": 2, "title": "Your First Program"},
                        ],
                    }
                ],
            }
        }


class TextbookResponse(BaseModel):
    """
    Response schema for textbook data.

    Attributes:
        id: Textbook ID
        user_id: Owner user ID
        title: Textbook title
        subject: Subject matter
        level: Educational level
        description: Textbook description
        chapters: List of chapter outlines
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: int = Field(..., description="Textbook ID")
    user_id: int = Field(..., description="Owner user ID")
    title: str = Field(..., description="Textbook title")
    subject: str = Field(..., description="Subject matter")
    level: str = Field(..., description="Educational level")
    description: Optional[str] = Field(None, description="Textbook description")
    chapters: List[ChapterOutline] = Field(default_factory=list, description="Chapter outlines")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "title": "Introduction to Python Programming - High School",
                "subject": "Introduction to Python Programming",
                "level": "High School",
                "description": "A comprehensive guide to Python for beginners",
                "chapters": [
                    {
                        "chapter_number": 1,
                        "title": "Introduction to Python",
                        "objectives": "Understand basic Python syntax",
                        "sections": [
                            {"section_number": 1, "title": "Variables"},
                            {"section_number": 2, "title": "Data Types"},
                        ],
                    }
                ],
                "created_at": "2025-12-16T10:00:00Z",
                "updated_at": "2025-12-16T10:00:00Z",
            }
        }
