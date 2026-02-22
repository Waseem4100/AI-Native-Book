"""
Textbook API endpoints.

This module handles textbook CRUD operations.
"""

from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.exceptions import NotFoundError
from ..core.security import get_current_user
from ..models.user import User
from ..schemas.errors import COMMON_RESPONSES
from ..schemas.textbook import TextbookResponse, TextbookUpdate
from ..services.textbook import TextbookService

router = APIRouter()


@router.get(
    "/me",
    response_model=Optional[TextbookResponse],
    responses={
        200: {"description": "User's textbook retrieved successfully"},
        **COMMON_RESPONSES,
    },
    summary="Get current user's textbook",
    description="Retrieve the authenticated user's textbook (one per user per FR-013)",
)
async def get_my_textbook(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get current user's textbook.

    Per FR-013, each user can have at most one textbook.

    Args:
        db: Database session
        current_user: Authenticated user

    Returns:
        Optional[TextbookResponse]: User's textbook or None if not exists

    Raises:
        401: If not authenticated
    """
    textbook = TextbookService.get_by_user(db=db, user=current_user)
    return textbook


@router.get(
    "/{textbook_id}",
    response_model=TextbookResponse,
    responses={
        200: {"description": "Textbook retrieved successfully"},
        **COMMON_RESPONSES,
    },
    summary="Get textbook by ID",
    description="Retrieve a specific textbook by ID (user must own the textbook)",
)
async def get_textbook(
    textbook_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get textbook by ID.

    Verifies that the textbook belongs to the requesting user.

    Args:
        textbook_id: Textbook ID
        db: Database session
        current_user: Authenticated user

    Returns:
        TextbookResponse: Textbook data

    Raises:
        401: If not authenticated
        403: If textbook doesn't belong to user
        404: If textbook not found
    """
    textbook = TextbookService.get_by_id(
        db=db,
        textbook_id=textbook_id,
        user=current_user,
    )
    return textbook


@router.put(
    "/{textbook_id}/structure",
    response_model=TextbookResponse,
    responses={
        200: {"description": "Textbook structure updated successfully"},
        **COMMON_RESPONSES,
    },
    summary="Update textbook structure",
    description="Update the chapter and section structure of a textbook",
)
async def update_textbook_structure(
    textbook_id: int,
    update_data: TextbookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update textbook structure.

    Allows updating the chapter and section outlines of an existing textbook.

    Args:
        textbook_id: Textbook ID
        update_data: Updated textbook data (title, description, chapters)
        db: Database session
        current_user: Authenticated user

    Returns:
        TextbookResponse: Updated textbook data

    Raises:
        401: If not authenticated
        403: If textbook doesn't belong to user
        404: If textbook not found
        422: If update data is invalid
    """
    # Get textbook (validates ownership)
    textbook = TextbookService.get_by_id(
        db=db,
        textbook_id=textbook_id,
        user=current_user,
    )

    # Update title and description if provided
    if update_data.title is not None:
        textbook.title = update_data.title
    if update_data.description is not None:
        textbook.description = update_data.description

    # Update chapter structure if provided
    if update_data.chapters is not None:
        textbook = TextbookService.update_structure(
            db=db,
            textbook=textbook,
            chapters=update_data.chapters,
        )
    else:
        db.commit()
        db.refresh(textbook)

    return textbook


@router.delete(
    "/{textbook_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Textbook deleted successfully"},
        **COMMON_RESPONSES,
    },
    summary="Delete textbook",
    description="Delete a textbook and all its chapters/sections",
)
async def delete_textbook(
    textbook_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a textbook.

    Cascade delete will remove all chapters, sections, and exercises.

    Args:
        textbook_id: Textbook ID
        db: Database session
        current_user: Authenticated user

    Returns:
        None: 204 No Content on success

    Raises:
        401: If not authenticated
        403: If textbook doesn't belong to user
        404: If textbook not found
    """
    # Get textbook (validates ownership)
    textbook = TextbookService.get_by_id(
        db=db,
        textbook_id=textbook_id,
        user=current_user,
    )

    # Delete textbook
    TextbookService.delete(db=db, textbook=textbook)
