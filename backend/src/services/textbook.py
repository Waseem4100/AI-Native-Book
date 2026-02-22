"""
Textbook service for CRUD operations.

This module handles database operations for textbooks, chapters, and sections.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from ..core.exceptions import ForbiddenError, NotFoundError
from ..models.chapter import Chapter
from ..models.section import Section
from ..models.textbook import Textbook
from ..models.user import User
from ..schemas.textbook import ChapterOutline, SectionOutline, TextbookCreate


class TextbookService:
    """
    Service for textbook CRUD operations.

    Methods:
        create: Create a new textbook for a user
        get_by_id: Get textbook by ID
        get_by_user: Get user's textbook (one per user per FR-013)
        update_structure: Update textbook chapters and sections from outline
        delete: Delete a textbook
    """

    @staticmethod
    def create(
        db: Session,
        user: User,
        textbook_data: TextbookCreate,
        chapters: Optional[List[ChapterOutline]] = None,
    ) -> Textbook:
        """
        Create a new textbook for a user.

        Per FR-013, each user can have only one textbook. If user already has
        a textbook, this will raise an error.

        Args:
            db: Database session
            user: User creating the textbook
            textbook_data: Textbook creation data
            chapters: Optional initial chapter outlines

        Returns:
            Textbook: Created textbook instance

        Raises:
            ValueError: If user already has a textbook
        """
        # Check if user already has a textbook (one per user per FR-013)
        existing = db.query(Textbook).filter(Textbook.user_id == user.id).first()
        if existing:
            raise ValueError("User already has a textbook. Only one textbook per user is allowed.")

        # Generate title from subject and level
        title = f"{textbook_data.subject} - {textbook_data.level}"

        # Create textbook
        textbook = Textbook(
            user_id=user.id,
            title=title,
            subject=textbook_data.subject,
            level=textbook_data.level,
            description=textbook_data.description,
        )
        db.add(textbook)
        db.flush()  # Get textbook.id before creating chapters

        # Create chapters if provided
        if chapters:
            TextbookService._create_chapters(db, textbook.id, chapters)

        db.commit()
        db.refresh(textbook)
        return textbook

    @staticmethod
    def get_by_id(db: Session, textbook_id: int, user: User) -> Textbook:
        """
        Get textbook by ID.

        Verifies that the textbook belongs to the requesting user.

        Args:
            db: Database session
            textbook_id: Textbook ID
            user: Requesting user

        Returns:
            Textbook: Textbook instance

        Raises:
            NotFoundError: If textbook not found
            ForbiddenError: If textbook doesn't belong to user
        """
        textbook = db.query(Textbook).filter(Textbook.id == textbook_id).first()

        if not textbook:
            raise NotFoundError("Textbook", textbook_id)

        if textbook.user_id != user.id:
            raise ForbiddenError("You don't have permission to access this textbook")

        return textbook

    @staticmethod
    def get_by_user(db: Session, user: User) -> Optional[Textbook]:
        """
        Get user's textbook.

        Per FR-013, each user has at most one textbook.

        Args:
            db: Database session
            user: User to get textbook for

        Returns:
            Optional[Textbook]: User's textbook or None if not exists
        """
        return db.query(Textbook).filter(Textbook.user_id == user.id).first()

    @staticmethod
    def update_structure(
        db: Session,
        textbook: Textbook,
        chapters: List[ChapterOutline],
    ) -> Textbook:
        """
        Update textbook chapter structure.

        Replaces existing chapters and sections with new outline.

        Args:
            db: Database session
            textbook: Textbook to update
            chapters: New chapter outlines

        Returns:
            Textbook: Updated textbook instance
        """
        # Delete existing chapters (cascade will delete sections)
        db.query(Chapter).filter(Chapter.textbook_id == textbook.id).delete()

        # Create new chapters
        TextbookService._create_chapters(db, textbook.id, chapters)

        db.commit()
        db.refresh(textbook)
        return textbook

    @staticmethod
    def delete(db: Session, textbook: Textbook) -> None:
        """
        Delete a textbook.

        Cascade delete will remove all chapters, sections, and exercises.

        Args:
            db: Database session
            textbook: Textbook to delete
        """
        db.delete(textbook)
        db.commit()

    @staticmethod
    def _create_chapters(
        db: Session,
        textbook_id: int,
        chapters: List[ChapterOutline],
    ) -> None:
        """
        Create chapters and sections for a textbook.

        Internal helper method.

        Args:
            db: Database session
            textbook_id: Textbook ID
            chapters: Chapter outlines to create
        """
        for chapter_outline in chapters:
            # Create chapter
            chapter = Chapter(
                textbook_id=textbook_id,
                chapter_number=chapter_outline.chapter_number,
                title=chapter_outline.title,
                objectives=chapter_outline.objectives,
            )
            db.add(chapter)
            db.flush()  # Get chapter.id before creating sections

            # Create sections
            for section_outline in chapter_outline.sections:
                section = Section(
                    chapter_id=chapter.id,
                    section_number=section_outline.section_number,
                    title=section_outline.title,
                )
                db.add(section)
