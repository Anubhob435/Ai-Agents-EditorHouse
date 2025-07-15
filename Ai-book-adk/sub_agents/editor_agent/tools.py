from dotenv import load_dotenv
import os
import json
import time
import datetime
import logging
from pathlib import Path
import re
from typing import Optional

from google import genai

# Set up logging
logger = logging.getLogger(__name__)

load_dotenv()
# Configure the client with your API key
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))


def editor_agent(story: str) -> str:
    """
    Edit a story for grammar, clarity, and flow while preserving creative style.
    
    Args:
        story: The story content to edit
        
    Returns:
        The edited story with improved grammar, clarity, and flow
    """
    prompt = f"Please edit the following story for grammar, clarity, and flow. Keep the creative style:\n\n{story}"
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text.strip()


def publish_story(title: str, story: str, output_dir: str = ".") -> str:
    """
    Save a story to a file with proper formatting.
    
    Args:
        title: The title of the story
        story: The story content to save
        output_dir: Directory to save the file (default: current directory)
        
    Returns:
        The filename where the story was saved
    """
    filename = title.replace(" ", "_").replace(":", "").lower() + ".txt"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n\n{story}")
    logger.info(f"Story saved as '{filepath}'")
    return filepath


def chapter_editor_agent(chapter_content: str, chapter_title: str) -> str:
    """
    Edit a chapter for grammar, style, and narrative coherence.
    
    Args:
        chapter_content: The raw chapter content to edit
        chapter_title: The title of the chapter being edited
        
    Returns:
        The edited chapter with improved quality while preserving the original voice
    """
    prompt = f"""
    Please edit the following chapter titled "{chapter_title}" for grammar, clarity, flow, and narrative coherence.
    Preserve the creative style and voice while improving the overall quality.
    
    Chapter content:
    {chapter_content}
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text.strip()


