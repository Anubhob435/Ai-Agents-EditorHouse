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

# Import BookMetadata from thinker agent
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'thinker_agent'))
from tools import BookMetadata

# Set up logging
logger = logging.getLogger(__name__)

load_dotenv()
# Configure the client with your API key
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))


def compile_book(book_title: str, force: bool = False) -> Optional[str]:
    """
    Compile all written chapters into a complete book with cover and table of contents.
    
    Args:
        book_title: The title of the book to compile
        force: Whether to force compilation even if not all chapters are complete
        
    Returns:
        The filename of the compiled book if successful, None otherwise
    """
    # Initialize the metadata manager
    book_metadata = BookMetadata("books", book_title)
    metadata = book_metadata.load()
    
    if not metadata:
        logger.error(f"Book '{book_title}' not found. Please create a book plan first with book_pipeline().")
        return
    
    book_plan = metadata["generation_info"]["book_plan"]
    cover_description = metadata["generation_info"]["cover_description"]
    toc = metadata["generation_info"]["toc"]
    
    completed = sum(1 for chapter in metadata["chapters"] if chapter["status"] == "published")
    total = len(metadata["chapters"])
    
    if completed < total and not force:
        logger.warning(f"Not all chapters are complete. {completed}/{total} chapters have been written.")
        logger.info(f"To continue writing, use: write_next_chapter('{book_title}')")
        logger.info(f"Or force compilation with incomplete chapters by using: compile_book('{book_title}', force=True)")
        return
    
    # Compile chapters
    chapters = []
    for chapter in metadata["chapters"]:
        if chapter["status"] == "published" and chapter["filename"]:
            with open(chapter["filename"], "r", encoding="utf-8") as f:
                # Skip the title line (first line) since we'll add it in the book compilation
                content = f.read()
                header_end = content.find('\n\n')
                if header_end > -1:
                    chapter_content = content[header_end + 2:]
                else:
                    chapter_content = content
                chapters.append(chapter_content)
        else:
            # For incomplete chapters, add a placeholder if force=True
            if force:
                chapters.append("*[This chapter is not yet written]*")
            
    # Compile book content
    book_filename = book_metadata.book_dir / f"{book_metadata.safe_title}.md"
    book_content = f"# {metadata['book_info']['title']}\n\n"
    book_content += f"*{metadata['book_info']['description']}*\n\n"
    book_content += f"**Topic:** {metadata['book_info']['topic']}\n\n"
    book_content += f"**Created:** {metadata['book_info']['creation_date']}\n"
    book_content += f"**Last Updated:** {metadata['book_info']['last_updated']}\n"
    book_content += f"**Word Count:** {metadata['book_info']['estimated_word_count']}\n"
    book_content += f"**Page Count:** {metadata['book_info']['estimated_page_count']}\n\n"
    book_content += "---\n\n"
    book_content += toc
    book_content += "\n\n---\n\n"
    
    # Add cover description
    book_content += "## Cover Design Description\n\n"
    book_content += f"{cover_description}\n\n"
    book_content += "---\n\n"
    
    # Add each chapter
    for i, chapter_content in enumerate(chapters):
        if i < len(metadata["chapters"]):
            chapter = metadata["chapters"][i]
            book_content += f"## Chapter {chapter['chapter_number']}: {chapter['chapter_title']}\n\n"
            book_content += f"{chapter_content}\n\n"
            book_content += "---\n\n"
    
    # Write to file
    with open(book_filename, "w", encoding="utf-8") as f:
        f.write(book_content)
    
    logger.info(f"Book successfully compiled and published as '{book_filename}'")
    logger.info(f"Individual chapters are available in '{book_metadata.chapters_dir}'")
    
    # Generate a JSON export of all metadata
    export_filename = book_metadata.book_dir / f"{book_metadata.safe_title}_metadata_export.json"
    with open(export_filename, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Complete book metadata exported to '{export_filename}'")
    
    return str(book_filename)

def get_book_status(book_title: Optional[str] = None) -> None:
    """
    Get the status of a book or list all available books with their progress.
    
    Args:
        book_title: The specific book title to get status for (optional)
                   If None, lists all available books
        
    Returns:
        None (prints status information to console)
    """
    book_dir = Path("books")
    
    if not book_dir.exists():
        logger.info("No books found yet. Create one with book_pipeline()")
        return
    
    # If no specific book is requested, list all books
    if book_title is None:
        books = []
        for item in book_dir.iterdir():
            if item.is_dir():
                metadata_file = item / "book_metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, "r", encoding="utf-8") as f:
                            metadata = json.load(f)
                            books.append({
                                "title": metadata["book_info"]["title"],
                                "status": metadata["book_info"]["status"],
                                "completed": f"{metadata['book_info']['completed_chapters']}/{metadata['book_info']['total_chapters']}",
                                "word_count": metadata["book_info"]["estimated_word_count"],
                                "page_count": metadata["book_info"]["estimated_page_count"]
                            })
                    except Exception as e:
                        logger.error(f"Error reading metadata for {item.name}: {e}")
        
        if not books:
            logger.info("No books found yet. Create one with book_pipeline()")
            return
        
        logger.info("\nAVAILABLE BOOKS:")
        logger.info("=" * 80)
        for book in books:
            logger.info(f"Title: {book['title']}")
            logger.info(f"Status: {book['status']} ({book['completed']} chapters)")
            logger.info(f"Word Count: {book['word_count']} (~{book['page_count']} pages)")
            logger.info("-" * 80)
        
    else:
        # Get status for a specific book
        book_metadata = BookMetadata("books", book_title)
        book_info = book_metadata.get_book_info()
        
        if not book_info:
            logger.error(f"Book '{book_title}' not found.")
            return
        
        metadata = book_metadata.get_all_metadata()
        
        logger.info(f"\nBOOK STATUS: {book_info['title']}")
        logger.info("=" * 80)
        logger.info(f"Status: {book_info['status']}")
        logger.info(f"Chapters: {book_info['completed']}")
        logger.info(f"Word Count: {book_info['word_count']}")
        logger.info(f"Page Count: {book_info['page_count']}")
        logger.info("-" * 80)
        logger.info("CHAPTERS:")
        
        for chapter in metadata["chapters"]:
            status_indicator = "[COMPLETE]" if chapter["status"] == "published" else "[PENDING]"
            logger.info(f"{status_indicator} Chapter {chapter['chapter_number']}: {chapter['chapter_title']}")
            logger.info(f"   Status: {chapter['status']}")
            if chapter["publication_date"]:
                logger.info(f"   Published: {chapter['publication_date']}")
            if chapter["word_count"] > 0:
                logger.info(f"   Words: {chapter['word_count']} (~{chapter['page_count']} pages)")
            logger.info("")
