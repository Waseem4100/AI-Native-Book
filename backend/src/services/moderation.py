"""
Content moderation service for filtering inappropriate content.

This module implements hybrid approach per Phase 0 research:
- Basic keyword filtering (custom blocklist with educational whitelist)
- OpenAI Moderation API integration (placeholder for future enhancement)
"""

from typing import List, Set

from ..core.config import settings
from ..core.exceptions import ContentModerationError


class ContentModerationService:
    """
    Content moderation service with keyword filtering.

    Methods:
        check_content: Check if content passes moderation
        is_content_safe: Boolean check for content safety
    """

    def __init__(self):
        """Initialize content moderation service."""
        # Load filter keywords from settings
        self.blocklist: Set[str] = set(settings.CONTENT_FILTER_KEYWORDS)

        # Educational whitelist - common educational terms that might trigger false positives
        self.whitelist: Set[str] = {
            "cell",  # Biology, spreadsheets
            "nucleus",  # Biology, physics
            "reproduction",  # Biology
            "organism",  # Biology
            "anatomy",  # Medicine
            "chemistry",  # Science
            "reaction",  # Chemistry, physics
            "force",  # Physics
            "explosion",  # Chemistry, physics
            "fire",  # Chemistry, science
            "weapon",  # History, physics
            "war",  # History
            "death",  # History, literature, biology
            "kill",  # Biology (cell death), chemistry
            "attack",  # History, biology (immune system)
        }

    def check_content(self, text: str) -> None:
        """
        Check if content passes moderation filters.

        Args:
            text: Content to check

        Raises:
            ContentModerationError: If content fails moderation
        """
        if not self.is_content_safe(text):
            raise ContentModerationError(
                "Content contains inappropriate keywords and cannot be used for textbook generation"
            )

    def is_content_safe(self, text: str) -> bool:
        """
        Check if content is safe for educational use.

        Uses keyword filtering with educational whitelist to reduce false positives.

        Args:
            text: Content to check

        Returns:
            bool: True if content is safe, False otherwise
        """
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()

        # Split into words
        words = set(text_lower.split())

        # Check for blocklisted words that aren't in whitelist
        blocked_words = self.blocklist & words - self.whitelist

        if blocked_words:
            print(f"⚠️ Content blocked due to keywords: {blocked_words}")
            return False

        return True

    def get_blocked_keywords(self, text: str) -> List[str]:
        """
        Get list of blocked keywords found in text.

        Useful for debugging and user feedback.

        Args:
            text: Content to check

        Returns:
            List[str]: List of blocked keywords found
        """
        text_lower = text.lower()
        words = set(text_lower.split())
        blocked_words = self.blocklist & words - self.whitelist
        return sorted(list(blocked_words))


# Global service instance
moderation_service = ContentModerationService()
