from dotenv import load_dotenv
import os
import json
import time
import datetime
from pathlib import Path
import re

# Update the import for the Google Generative AI client
from google import genai

# Import from illustrator.py
from illustrator import generate_illustration
# Import from editor.py
from editor import FormatAgent

load_dotenv()
# Configure the client with your API key
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Existing single story agents




# Book metadata management

# New book creation agents




# New illustrator agent
def illustrator_agent(chapter_content: str, chapter_title: str, book_title: str, chapter_number: int) -> str:
    """Generates an illustration for a chapter based on its content"""
    print(f"🎨 Generating illustration for chapter: {chapter_title}...")
    
    # Create a prompt for the illustration
    prompt = f"""
    Based on the following chapter titled "{chapter_title}" from the book "{book_title}", 
    generate a detailed description for an illustration that captures a key scene or theme.
    Limit your description to 1-2 sentences that clearly describe what to illustrate.
    
    Chapter content:
    {chapter_content[:1500]}  # Using first 1500 chars to stay within token limits
    """
    
    # Get illustration description from AI
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    illustration_description = response.text.strip()
    
    # Generate the actual illustration using the description
    illustration_filename = generate_illustration(illustration_description, f"chapter_{chapter_number:02d}_{chapter_title}")
    
    # Return the relative path to be used in markdown
    relative_path = os.path.relpath(illustration_filename, os.path.dirname(__file__))
    
    print(f"✅ Illustration generated and saved as '{os.path.basename(illustration_filename)}'")
    return f"![Chapter {chapter_number} Illustration: {chapter_title}]({relative_path})"



# Example usage
if __name__ == "__main__":
    print("Welcome to the AI Book Assistant!")
    # For a single story
    # story_pipeline("a magical forest")
    
    # For a complete book, chapter by chapter
    # Step 1: Create book plan
    #book_title = book_pipeline("An indian crime thriller", num_chapters=3)
    
    # Step 2: Write each chapter one at a time
    #write_next_chapter(book_title)
    
    # Step 3: After all chapters are written, compile the book
    #compile_book(book_title)


    #write_next_chapter('Book about An indian crime thriller')
    #compile_book('Book about space exploration in the distant future')
    
    # Get status of books
    # get_book_status()  # List all books
    # get_book_status(book_title)  # Get details about a specific book
    
    # For demonstration, uncomment one of these lines:
    #book_pipeline("magical adventure in a hidden kingdom", num_chapters=3)