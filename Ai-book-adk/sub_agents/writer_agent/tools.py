from dotenv import load_dotenv
import os
import json
import time
import datetime
import logging
from pathlib import Path
import re
from typing import Dict, Any

from google import genai

# Set up logging
logger = logging.getLogger(__name__)

load_dotenv()
# Configure the client with your API key
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))


def headline_agent(topic: str) -> str:
    """
    Generate an engaging and creative title for a story.
    
    Args:
        topic: The topic or theme for the story title
        
    Returns:
        A creative and engaging story title
    """
    prompt = f"Come up with an engaging and creative title for a story about: {topic}"
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text.strip()

def writer_agent(title: str) -> str:
    """
    Write a fictional short story based on the provided title.
    
    Args:
        title: The title to base the story on
        
    Returns:
        A complete fictional short story of 700-1000 words
    """
    prompt = f"Write a fictional short story based on the title: '{title}'. Make it around 700-1000 words."
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text.strip()


def chapter_writer_agent(book_plan: str, chapter_index: int) -> str:
    """
    Write a full chapter based on the book plan and chapter specifications.
    
    Args:
        book_plan: JSON string containing the complete book plan with chapters
        chapter_index: Index of the chapter to write (0-based)
        
    Returns:
        A complete chapter of approximately 1500-2000 words
    """
    try:
        # Parse the JSON string
        plan_data = json.loads(book_plan) if isinstance(book_plan, str) else book_plan
        
        if chapter_index >= len(plan_data["chapters"]):
            logger.error(f"Chapter index {chapter_index} out of range")
            return "# Error\n\nChapter index out of range"
        
        chapter = plan_data["chapters"][chapter_index]
        
        prompt = f"""
        Write Chapter {chapter['chapter_number']}: "{chapter['chapter_title']}" for the book "{plan_data['book_title']}".
    
    Use this synopsis as a guide: {chapter['synopsis']}
    
    Include these key points/scenes:
    {', '.join(chapter['key_points'])}
    
    Write a compelling chapter of approximately 1500-2000 words that advances the overall narrative.
    Use engaging dialogue, vivid descriptions, and well-developed characters.
    
    If this is chapter 1, introduce the main characters and setting.
    If this is the final chapter, provide appropriate closure while leaving room for reader interpretation.
    """
    
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
        
    except Exception as e:
        logger.error(f"Error writing chapter: {e}")
        return f"# Chapter {chapter_index + 1}: Error\n\nError generating chapter content."


def story_pipeline(topic: str) -> str:
    """
    Complete pipeline to create a short story from topic to final output.
    
    Args:
        topic: The topic or theme for the story
        
    Returns:
        The final edited story ready for publishing
    """
    logger.info("Generating headline...")
    title = headline_agent(topic)
    logger.info(f"Title: {title}")

    logger.info("Writing story...")
    raw_story = writer_agent(title)

    logger.info("Story writing completed")
    # Note: Additional editing and publishing would be handled by other agents
    
    return raw_story
