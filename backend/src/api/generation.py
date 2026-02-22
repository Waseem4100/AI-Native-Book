"""
Generation API endpoints.

This module handles textbook outline generation endpoints.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..schemas.errors import COMMON_RESPONSES
from ..schemas.textbook import TextbookCreate, TextbookResponse
from ..services.generation import TextbookGenerator
from ..services.moderation import moderation_service
from ..services.textbook import TextbookService

router = APIRouter()


@router.post(
    "/generate-outline",
    response_model=TextbookResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Textbook outline generated successfully"},
        **COMMON_RESPONSES,
    },
    summary="Generate textbook outline",
    description="Generate a complete textbook outline with chapters and sections using AI",
)
async def generate_outline(
    textbook_data: TextbookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate a complete textbook outline.

    This endpoint:
    1. Validates that user doesn't already have a textbook (one per user per FR-013)
    2. Checks content moderation for subject
    3. Generates outline using OpenAI API
    4. Creates textbook with chapters and sections in database

    Args:
        textbook_data: Textbook generation parameters (subject, level, num_chapters)
        db: Database session
        current_user: Authenticated user

    Returns:
        TextbookResponse: Generated textbook with outline

    Raises:
        400: If user already has a textbook or content fails moderation
        401: If not authenticated
        500: If generation fails
    """
    # Check content moderation
    moderation_service.check_content(textbook_data.subject)
    if textbook_data.description:
        moderation_service.check_content(textbook_data.description)

    # Generate outline using AI
    generator = TextbookGenerator()
    chapters = await generator.generate_outline(
        subject=textbook_data.subject,
        level=textbook_data.level,
        num_chapters=textbook_data.num_chapters,
    )

    # Create textbook in database
    textbook = TextbookService.create(
        db=db,
        user=current_user,
        textbook_data=textbook_data,
        chapters=chapters,
    )

    return textbook
