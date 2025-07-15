from dotenv import load_dotenv
import os
import json
import time
import datetime
import logging
from pathlib import Path
import re
from typing import Dict, Optional

from google import genai

# Import functions from sub-agents
from .sub_agents.thinker_agent.tools import book_planner_agent, table_of_contents_generator, book_cover_description_agent, BookMetadata
from .sub_agents.writer_agent.tools import chapter_writer_agent
from .sub_agents.editor_agent.tools import chapter_editor_agent
from .sub_agents.illustrator_agent.illustrator import generate_illustration

# Set up logging
logger = logging.getLogger(__name__)

load_dotenv()
# Configure the client with your API key
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))


def book_pipeline(topic: str, num_chapters: int = 5) -> str:
    """
    Complete pipeline to create and publish a book from topic to structure.
    
    Args:
        topic: The main topic or theme for the book
        num_chapters: Number of chapters to plan (default: 5)
        
    Returns:
        The book title for reference in subsequent operations
    """
    logger.info(f"Starting book creation process on topic: {topic}")
    
    # Plan the book
    logger.info("Planning book structure...")
    book_plan_json = book_planner_agent(topic, num_chapters)
    
    try:
        # Parse the JSON string returned by book_planner_agent
        book_plan = json.loads(book_plan_json) if isinstance(book_plan_json, str) else book_plan_json
        logger.info(f"Book Title: {book_plan['book_title']}")
        logger.info(f"Book Plan: {len(book_plan['chapters'])} chapters planned")
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        logger.error(f"Error parsing book plan: {e}")
        logger.error(f"Book plan content: {book_plan_json}")
        # Create a fallback book plan
        book_plan = {
            "book_title": f"Book about {topic}",
            "book_description": f"A comprehensive guide to {topic}",
            "chapters": [{"chapter_number": i, "chapter_title": f"Chapter {i}", 
                         "synopsis": f"Exploring {topic}", 
                         "key_points": [f"Understanding {topic}"]} 
                        for i in range(1, num_chapters + 1)]
        }
        logger.info(f"Using fallback book plan: {book_plan['book_title']}")
    
    # Generate cover description
    logger.info("Generating cover description...")
    cover_description = book_cover_description_agent(json.dumps(book_plan))
    
    # Generate table of contents
    logger.info("Creating table of contents...")
    toc = table_of_contents_generator(json.dumps(book_plan))
    
    # Initialize metadata manager and create initial metadata
    book_metadata = BookMetadata("books", book_plan["book_title"])
    book_metadata.initialize(book_plan, cover_description, toc, topic)
    
    logger.info(f"Book structure planned and saved. You can now generate chapters one by one.")
    logger.info(f"To generate a chapter, use: write_next_chapter('{book_plan['book_title']}')")
    
    # Return the book title for reference
    return book_plan['book_title']

def write_next_chapter(book_title: str) -> Optional[str]:
    """
    Write the next chapter in the book sequence.
    
    Args:
        book_title: The title of the book to continue writing
        
    Returns:
        The filename of the written chapter if successful, None if book not found or complete
    """
    # Initialize the metadata manager
    book_metadata = BookMetadata("books", book_title)
    metadata = book_metadata.load()
    
    if not metadata:
        logger.error(f"Book '{book_title}' not found. Please create a book plan first with book_pipeline().")
        return
    
    # Get the next chapter to write
    chapter_index = book_metadata.get_next_chapter_index()
    
    if chapter_index is None:
        logger.info("All chapters have been completed. You can now compile the book.")
        logger.info(f"To compile the book, use: compile_book('{book_title}')")
        return
    
    chapter = metadata["chapters"][chapter_index]
    book_plan_data = metadata["generation_info"]["book_plan"]
    
    # Ensure book_plan_data is a dictionary (parse if it's a JSON string)
    if isinstance(book_plan_data, str):
        try:
            book_plan = json.loads(book_plan_data)
        except json.JSONDecodeError:
            logger.error("Failed to parse book plan from metadata")
            return
    else:
        book_plan = book_plan_data
    
    logger.info(f"Writing chapter {chapter['chapter_number']}: {chapter['chapter_title']}...")
    raw_chapter = chapter_writer_agent(json.dumps(book_plan), chapter_index)
    
    logger.info(f"Editing chapter {chapter['chapter_number']}...")
    edited_chapter = chapter_editor_agent(raw_chapter, chapter['chapter_title'])
    
    # Generate illustration for the chapter
    logger.info(f"Generating illustration for chapter {chapter['chapter_number']}...")
    illustration_prompt = f"Based on chapter {chapter['chapter_number']} titled '{chapter['chapter_title']}' from the book '{book_plan['book_title']}', create a detailed description for an illustration that captures a key scene or theme."
    
    # Create a shorter prefix for the illustration filename to avoid path length issues
    chapter_num = f"{chapter['chapter_number']:02d}"
    illustration_prefix = f"ch{chapter_num}_{chapter['chapter_title'][:20].replace(' ', '_').lower()}"
    
    # Get the book directory for saving illustrations
    book_dir = str(book_metadata.chapters_dir)
    
    # Generate the illustration
    illustration_path = generate_illustration(illustration_prompt, illustration_prefix, book_dir)
    
    if illustration_path:
        # Create markdown for the illustration
        relative_path = os.path.relpath(illustration_path, book_metadata.chapters_dir)
        illustration_markdown = f"![Chapter {chapter['chapter_number']} Illustration: {chapter['chapter_title']}]({relative_path})"
    else:
        illustration_markdown = f"*[Illustration for Chapter {chapter['chapter_number']} could not be generated]*"
    
    # Use the edited chapter as the final formatted content
    formatted_chapter = edited_chapter
    
    # Save the chapter
    chapter_short_title = chapter['chapter_title'][:20].replace(' ', '_').lower()
    chapter_filename = book_metadata.chapters_dir / f"ch{chapter['chapter_number']:02d}_{chapter_short_title}.md"
    with open(chapter_filename, "w", encoding="utf-8") as f:
        f.write(f"# Chapter {chapter['chapter_number']}: {chapter['chapter_title']}\n\n")
        f.write(illustration_markdown + "\n\n")
        f.write(formatted_chapter)
    
    # Update metadata with chapter details
    book_metadata.update_chapter(chapter_index, chapter_filename, formatted_chapter)
    
    # Get updated information
    book_info = book_metadata.get_book_info()
    
    logger.info(f"Chapter {chapter['chapter_number']} completed and saved as '{chapter_filename}'")
    logger.info(f"Book Progress: {book_info['completed']} chapters | {book_info['word_count']} words | ~{book_info['page_count']} pages")
    
    if book_info['status'] != 'complete':
        logger.info(f"To continue with the next chapter, use: write_next_chapter('{book_title}')")
    else:
        logger.info("All chapters completed! You can now compile the book.")
        logger.info(f"To compile the book, use: compile_book('{book_title}')")
    
    return str(chapter_filename)
