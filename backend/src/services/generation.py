"""
Textbook generation service using Gemini API.

This module handles AI-powered textbook outline and content generation.
"""

import json
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader

from ..core.ai import count_tokens, generate_completion
from ..schemas.textbook import ChapterOutline, SectionOutline

# Setup Jinja2 environment for prompt templates
PROMPTS_DIR = Path(__file__).parent / "prompts"
jinja_env = Environment(loader=FileSystemLoader(str(PROMPTS_DIR)))


class TextbookGenerator:
    """
    Generates textbook outlines and content using OpenAI API.

    Methods:
        generate_outline: Generate complete textbook outline with chapters and sections
        generate_chapter_content: Generate detailed content for a specific chapter (US2)
    """

    def __init__(self):
        """Initialize the textbook generator."""
        self.system_message = (
            "You are an expert educational content creator specializing in textbook development. "
            "Your task is to create comprehensive, pedagogically sound textbook content that is "
            "appropriate for the specified educational level. Focus on clarity, accuracy, and "
            "effective learning progression."
        )

    async def generate_outline(
        self,
        subject: str,
        level: str,
        num_chapters: int = 10,
        temperature: float = 0.7,
    ) -> List[ChapterOutline]:
        """
        Generate a complete textbook outline with chapters and sections.

        Args:
            subject: Subject matter (e.g., "Introduction to Python Programming")
            level: Educational level (e.g., "High School", "Undergraduate")
            num_chapters: Number of chapters to generate
            temperature: Sampling temperature for generation

        Returns:
            List[ChapterOutline]: List of chapter outlines with sections

        Raises:
            ValueError: If generation fails or output is invalid
        """
        # Load prompt template
        template = jinja_env.get_template("outline.jinja2")
        prompt = template.render(
            subject=subject,
            level=level,
            num_chapters=num_chapters,
        )

        # Count input tokens
        input_tokens = count_tokens(prompt)
        print(f"📊 Input tokens: {input_tokens}")

        # Generate outline using OpenAI
        try:
            generated_text, total_tokens = await generate_completion(
                prompt=prompt,
                temperature=temperature,
                max_tokens=4000,
                system_message=self.system_message,
            )

            print(f"📊 Total tokens used: {total_tokens}")

            # Parse JSON response
            outline_data = json.loads(generated_text)

            # Convert to ChapterOutline objects
            chapters = []
            for chapter_data in outline_data.get("chapters", []):
                sections = [
                    SectionOutline(**section_data)
                    for section_data in chapter_data.get("sections", [])
                ]
                chapter = ChapterOutline(
                    chapter_number=chapter_data["chapter_number"],
                    title=chapter_data["title"],
                    objectives=chapter_data.get("objectives"),
                    sections=sections,
                )
                chapters.append(chapter)

            return chapters

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse generated outline: {e}")
        except Exception as e:
            raise ValueError(f"Outline generation failed: {e}")

    async def generate_chapter_content(
        self,
        chapter_title: str,
        chapter_objectives: str,
        subject: str,
        level: str,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate detailed content for a specific chapter.

        This method will be fully implemented in User Story 2 (Phase 4).

        Args:
            chapter_title: Chapter title
            chapter_objectives: Learning objectives
            subject: Subject matter
            level: Educational level
            temperature: Sampling temperature

        Returns:
            str: Generated chapter content in Markdown format
        """
        # Placeholder for US2 implementation
        raise NotImplementedError("Chapter content generation will be implemented in User Story 2")
