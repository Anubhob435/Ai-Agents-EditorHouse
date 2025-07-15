from dotenv import load_dotenv
import os
import json
import time
import datetime
import logging
from pathlib import Path
import re
from typing import Dict, Optional, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError

from google import genai

# Set up logging
logger = logging.getLogger(__name__)

load_dotenv()
# Configure the client with your API key
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# MongoDB configuration
MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING', 'mongodb://localhost:27017/')
DB_NAME = "BooksMeta"
COLLECTION_NAME = "Books"


def book_planner_agent(topic: str, num_chapters: int = 5) -> str:
    """
    Creates a detailed book outline with chapters based on the topic.
    
    Args:
        topic: The main topic or theme for the book
        num_chapters: Number of chapters to plan (default: 5)
        
    Returns:
        A JSON string containing the book plan with title, description, and chapter details
    """
    prompt = f"""
    Create a detailed outline for a book about '{topic}' with {num_chapters} chapters.
    For each chapter, provide:
    1. A compelling chapter title
    2. A brief synopsis of what happens in the chapter (100-150 words)
    3. Key points or scenes to include
    
    Also provide an overall book title and a short description of the book.
    Format your response as a JSON object with this structure:
    {{
        "book_title": "Title of the Book",
        "book_description": "Short description of the book's premise",
        "chapters": [
            {{
                "chapter_number": 1,
                "chapter_title": "Chapter Title",
                "synopsis": "Brief description of the chapter",
                "key_points": ["point 1", "point 2", "point 3"]
            }},
            // additional chapters...
        ]
    }}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        book_plan = json.loads(response.text)
        return json.dumps(book_plan)  # Return as JSON string
    except Exception as e:
        logger.error(f"Error in creating book plan: {e}")
        # Fallback to a simpler format if JSON parsing fails
        fallback_plan = {
            "book_title": f"Book about {topic}",
            "book_description": f"A collection of stories about {topic}",
            "chapters": [{"chapter_number": i, "chapter_title": f"Chapter {i}", 
                         "synopsis": f"A story about {topic}", 
                         "key_points": [f"Explore {topic}"]} 
                        for i in range(1, num_chapters + 1)]
        }
        return json.dumps(fallback_plan)



def table_of_contents_generator(book_plan: str) -> str:
    """
    Generates a table of contents for the book.
    
    Args:
        book_plan: JSON string containing the book plan with chapters
        
    Returns:
        A formatted table of contents as a markdown string
    """
    try:
        # Parse the JSON string
        plan_data = json.loads(book_plan) if isinstance(book_plan, str) else book_plan
        
        toc = f"# {plan_data['book_title']}\n\n"
        toc += "## Table of Contents\n\n"
        
        for chapter in plan_data["chapters"]:
            toc += f"{chapter['chapter_number']}. {chapter['chapter_title']}\n"
        
        return toc
    except Exception as e:
        logger.error(f"Error generating table of contents: {e}")
        return "# Table of Contents\n\nError generating table of contents"

def book_cover_description_agent(book_plan: str) -> str:
    """
    Generates a detailed description for a book cover design.
    
    Args:
        book_plan: JSON string containing the book plan with title and description
        
    Returns:
        A detailed description for book cover design with visual direction
    """
    try:
        # Parse the JSON string
        plan_data = json.loads(book_plan) if isinstance(book_plan, str) else book_plan
        
        prompt = f"""
        Create a detailed description for a book cover design for the book titled "{plan_data['book_title']}".
        Book description: {plan_data['book_description']}
        
        Include suggestions for:
        1. Main imagery or illustration
        2. Color scheme
        3. Typography style
        4. Overall mood/feeling the cover should convey
        
        The description should provide clear visual direction for a book cover designer.
        """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating book cover description: {e}")
        return "A generic book cover with elegant typography and appealing imagery."

class BookMetadata:
    """Class to manage book metadata tracking"""
    
    def __init__(self, book_dir, book_title):
        self.book_dir = Path(book_dir)
        self.original_title = book_title
        # Create a shorter, safer title for filesystem use
        self.safe_title = self._create_safe_title(book_title)
        self.chapters_dir = self.book_dir / self.safe_title
        self.metadata_file = self.chapters_dir / "book_metadata.json"
        
        # Create directories if they don't exist
        self.book_dir.mkdir(exist_ok=True)
        self.chapters_dir.mkdir(exist_ok=True)
    
    def _create_safe_title(self, title: str) -> str:
        """
        Create a filesystem-safe title with length limitations.
        
        Args:
            title: Original book title
            
        Returns:
            Safe, shortened title for filesystem use
        """
        # Remove special characters and replace spaces
        safe = re.sub(r'[^\w\s-]', '', title.lower())
        safe = re.sub(r'[-\s]+', '_', safe)
        
        # Truncate to a reasonable length (50 characters max)
        # This ensures the full path stays under Windows limits
        if len(safe) > 50:
            # Try to truncate at word boundary
            words = safe.split('_')
            truncated = ''
            for word in words:
                if len(truncated + '_' + word) <= 47:  # Leave room for 'book_about_'
                    if truncated:
                        truncated += '_' + word
                    else:
                        truncated = word
                else:
                    break
            safe = truncated if truncated else safe[:47]
        
        # Add prefix to make it descriptive
        return f"book_{safe}"
    
    def initialize(self, book_plan, cover_description, toc, topic):
        """Initialize a new book's metadata"""
        metadata = {
            "book_info": {
                "title": book_plan["book_title"],
                "description": book_plan["book_description"],
                "topic": topic,
                "creation_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "last_updated": datetime.datetime.now().strftime("%Y-%m-%d"),
                "status": "planning",  # planning, in-progress, complete
                "total_chapters": len(book_plan["chapters"]),
                "completed_chapters": 0,
                "estimated_word_count": 0,
                "estimated_page_count": 0
            },
            "generation_info": {
                "book_plan": book_plan,
                "cover_description": cover_description,
                "toc": toc
            },
            "chapters": []
        }
        
        # Create chapter entries with status tracking
        for chapter in book_plan["chapters"]:
            metadata["chapters"].append({
                "chapter_number": chapter["chapter_number"],
                "chapter_title": chapter["chapter_title"],
                "synopsis": chapter["synopsis"],
                "key_points": chapter["key_points"],
                "status": "planned",  # planned, writing, written, edited, published
                "creation_date": None,
                "last_edited": None,
                "publication_date": None,
                "word_count": 0,
                "page_count": 0,
                "filename": None
            })
        
        # Save metadata
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        
        return metadata
    
    def load(self):
        """Load existing book metadata"""
        try:
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def update_chapter(self, chapter_index, filename, content):
        """Update a chapter's metadata after writing/editing"""
        metadata = self.load()
        if not metadata:
            raise FileNotFoundError(f"Book metadata not found for {self.safe_title}")
        
        # Calculate metrics
        word_count = len(content.split())
        # Estimate page count (250 words per page is a common estimate)
        page_count = round(word_count / 250, 1)
        
        # Update chapter info
        chapter = metadata["chapters"][chapter_index]
        chapter["status"] = "published"
        chapter["last_edited"] = datetime.datetime.now().strftime("%Y-%m-%d")
        chapter["publication_date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        chapter["word_count"] = word_count
        chapter["page_count"] = page_count
        chapter["filename"] = str(filename)
        
        # Update book level info
        metadata["book_info"]["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d")
        metadata["book_info"]["completed_chapters"] = sum(1 for chapter in metadata["chapters"] if chapter["status"] == "published")
        
        if metadata["book_info"]["completed_chapters"] < metadata["book_info"]["total_chapters"]:
            metadata["book_info"]["status"] = "in-progress"
        else:
            metadata["book_info"]["status"] = "complete"
        
        # Recalculate total word and page count
        total_word_count = sum(chapter["word_count"] for chapter in metadata["chapters"] if chapter["word_count"] > 0)
        metadata["book_info"]["estimated_word_count"] = total_word_count
        metadata["book_info"]["estimated_page_count"] = round(total_word_count / 250, 1)
        
        # Save updated metadata
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        
        return metadata
    
    def get_next_chapter_index(self):
        """Get the index of the next chapter to write"""
        metadata = self.load()
        if not metadata:
            return None
        
        for i, chapter in enumerate(metadata["chapters"]):
            if chapter["status"] == "planned":
                return i
        
        return None
    
    def get_book_info(self):
        """Get a summary of the book's current state"""
        metadata = self.load()
        if not metadata:
            return None
        
        return {
            "title": metadata["book_info"]["title"],
            "status": metadata["book_info"]["status"],
            "completed": f"{metadata['book_info']['completed_chapters']}/{metadata['book_info']['total_chapters']}",
            "word_count": metadata["book_info"]["estimated_word_count"],
            "page_count": metadata["book_info"]["estimated_page_count"]
        }
    
    def get_all_metadata(self):
        """Get the complete metadata for export"""
        return self.load()


def _get_mongodb_collection():
    """
    Get MongoDB collection for book metadata.
    
    Returns:
        MongoDB collection object or None if connection fails
    """
    try:
        mongo_client = MongoClient(MONGODB_CONNECTION_STRING)
        # Test the connection
        mongo_client.admin.command('ping')
        db = mongo_client[DB_NAME]
        collection = db[COLLECTION_NAME]
        logger.info(f"Connected to MongoDB: {DB_NAME}.{COLLECTION_NAME}")
        return collection
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return None
    except Exception as e:
        logger.error(f"MongoDB connection error: {e}")
        return None


def store_book_metadata_to_mongodb(book_title: str) -> bool:
    """
    Store or update book metadata in MongoDB database instead of JSON file.
    
    Args:
        book_title: The title of the book to store metadata for
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get the collection
        collection = _get_mongodb_collection()
        if not collection:
            logger.error("Cannot connect to MongoDB")
            return False
        
        # Load metadata from the existing JSON file
        book_metadata = BookMetadata("books", book_title)
        metadata = book_metadata.load()
        
        if not metadata:
            logger.error(f"No metadata found for book '{book_title}'")
            return False
        
        # Prepare document for MongoDB
        document = {
            "_id": book_metadata.safe_title,  # Use safe title as unique identifier
            "book_title": book_metadata.original_title,  # Store original title
            "safe_title": book_metadata.safe_title,
            "metadata": metadata,
            "last_synced": datetime.datetime.now().isoformat(),
            "sync_source": "thinker_agent"
        }
        
        # Try to update existing document or insert new one
        result = collection.replace_one(
            {"_id": book_metadata.safe_title},
            document,
            upsert=True
        )
        
        if result.upserted_id:
            logger.info(f"Book metadata for '{book_metadata.original_title}' inserted into MongoDB")
        elif result.modified_count > 0:
            logger.info(f"Book metadata for '{book_metadata.original_title}' updated in MongoDB")
        else:
            logger.info(f"Book metadata for '{book_metadata.original_title}' already up to date in MongoDB")
        
        return True
        
    except DuplicateKeyError:
        logger.error(f"Duplicate book title in MongoDB: {book_title}")
        return False
    except Exception as e:
        logger.error(f"Error storing book metadata to MongoDB: {e}")
        return False


def load_book_metadata_from_mongodb(book_title: str) -> str:
    """
    Load book metadata from MongoDB database.
    
    Args:
        book_title: The title of the book to load metadata for
        
    Returns:
        Book metadata dictionary if found, None otherwise
    """
    try:
        # Get the collection
        collection = _get_mongodb_collection()
        if not collection:
            logger.error("Cannot connect to MongoDB")
            return None
        
        # Create safe title for lookup
        book_metadata = BookMetadata("books", book_title)
        safe_title = book_metadata.safe_title
        
        # Find the document
        document = collection.find_one({"_id": safe_title})
        
        if document:
            logger.info(f"Book metadata for '{book_title}' loaded from MongoDB")
            return json.dumps(document["metadata"])
        else:
            logger.warning(f"No metadata found in MongoDB for book '{book_title}'")
            return "{}"
            
    except Exception as e:
        logger.error(f"Error loading book metadata from MongoDB: {e}")
        return "{}"


def sync_all_books_to_mongodb() -> str:
    """
    Sync all book metadata from JSON files to MongoDB.
    
    Returns:
        Dictionary with book titles as keys and success status as values
    """
    results = {}
    book_dir = Path("books")
    
    if not book_dir.exists():
        logger.info("No books directory found")
        return results
    
    try:
        # Get the collection
        collection = _get_mongodb_collection()
        if not collection:
            logger.error("Cannot connect to MongoDB")
            return results
        
        # Process each book directory
        for item in book_dir.iterdir():
            if item.is_dir():
                metadata_file = item / "book_metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, "r", encoding="utf-8") as f:
                            metadata = json.load(f)
                            book_title = metadata["book_info"]["title"]
                            
                        # Store to MongoDB
                        success = store_book_metadata_to_mongodb(book_title)
                        results[book_title] = success
                        
                    except Exception as e:
                        logger.error(f"Error processing book metadata for {item.name}: {e}")
                        results[item.name] = False
        
        logger.info(f"Synced {len(results)} books to MongoDB")
        successful_syncs = sum(1 for success in results.values() if success)
        logger.info(f"Successful syncs: {successful_syncs}/{len(results)}")
        
        return json.dumps(results)
        
    except Exception as e:
        logger.error(f"Error during bulk sync to MongoDB: {e}")
        return json.dumps(results)


def get_all_books_from_mongodb() -> str:
    """
    Retrieve all book metadata from MongoDB.
    
    Returns:
        List of all book metadata documents, or None if error
    """
    try:
        # Get the collection
        collection = _get_mongodb_collection()
        if not collection:
            logger.error("Cannot connect to MongoDB")
            return "[]"
        
        # Get all documents
        documents = list(collection.find({}, {"_id": 1, "book_title": 1, "metadata.book_info": 1, "last_synced": 1}))
        
        logger.info(f"Retrieved {len(documents)} books from MongoDB")
        return json.dumps(documents, default=str)  # Use default=str to handle datetime objects
        
    except Exception as e:
        logger.error(f"Error retrieving books from MongoDB: {e}")
        return "[]"
