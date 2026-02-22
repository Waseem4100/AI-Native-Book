"""
Firebase authentication and security middleware.

This module handles Firebase Admin SDK initialization, JWT verification,
and authentication dependencies for FastAPI routes.
"""

from typing import Optional

import firebase_admin
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from ..models.user import User

# Initialize Firebase Admin SDK
_firebase_app: Optional[firebase_admin.App] = None


def initialize_firebase() -> None:
    """
    Initialize Firebase Admin SDK on application startup.

    Loads credentials from the path specified in FIREBASE_CREDENTIALS setting.
    Should be called once during app initialization.

    Raises:
        FileNotFoundError: If credentials file not found
        ValueError: If credentials file is invalid
    """
    global _firebase_app

    if _firebase_app is not None:
        return  # Already initialized

    try:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
        _firebase_app = firebase_admin.initialize_app(cred)
    except Exception as e:
        raise ValueError(f"Failed to initialize Firebase Admin SDK: {e}")


# HTTP Bearer token security scheme
security = HTTPBearer()


async def verify_firebase_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Verify Firebase ID token from Authorization header.

    Extracts and verifies the JWT token from the Bearer authorization header.
    Returns the decoded token payload if valid.

    Args:
        credentials: HTTP Authorization credentials with Bearer token

    Returns:
        dict: Decoded token payload containing user info (uid, email, etc.)

    Raises:
        HTTPException: 401 if token is invalid, expired, or revoked
    """
    token = credentials.credentials

    try:
        # Verify the ID token and decode it
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    token_data: dict = Depends(verify_firebase_token),
    db: Session = Depends(get_db),
) -> User:
    """
    Get current authenticated user from database.

    Retrieves the User model instance for the authenticated Firebase user.
    Creates a new User record if this is the first login.

    Args:
        token_data: Decoded Firebase token from verify_firebase_token
        db: Database session

    Returns:
        User: Current authenticated user model instance

    Raises:
        HTTPException: 401 if user cannot be found or created
    """
    firebase_uid = token_data.get("uid")
    email = token_data.get("email")

    if not firebase_uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
        )

    # Try to find existing user by Firebase UID
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()

    # Create new user if this is first login
    if not user:
        user = User(
            firebase_uid=firebase_uid,
            email=email,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


# Optional authentication dependency (returns None if not authenticated)
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise.

    Useful for endpoints that have different behavior for authenticated vs anonymous users.

    Args:
        credentials: Optional HTTP Authorization credentials
        db: Database session

    Returns:
        Optional[User]: Current user if authenticated, None otherwise
    """
    if not credentials:
        return None

    try:
        token_data = await verify_firebase_token(credentials)
        return await get_current_user(token_data, db)
    except HTTPException:
        return None
