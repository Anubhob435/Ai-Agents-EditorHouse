#!/usr/bin/env python3
"""
Example script demonstrating the full AI-Book generation workflow
including formatting and compilation.

This script will:
1. Generate a complete book on a specified topic
2. Apply advanced formatting to each chapter
3. Compile the book into a final markdown file
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Import components from main module
from main import (
    book_pipeline, 
    write_next_chapter, 
    compile_book,
    get_book_status
)

# Import formatting functions from editor module
from editor import FormatAgent, enhance_book_formatting

def generate_complete_book(topic, num_chapters=3, pause_between_chapters=2):
    """
    Generate a complete book with proper formatting
    
    Args:
        topic (str): The main topic/theme of the book
        num_chapters (int): Number of chapters to generate
        pause_between_chapters (int): Seconds to pause between chapter generation
        
    Returns:
        str: The title of the generated book
    """
    print("\n" + "="*80)
    print(f"🚀 STARTING COMPLETE BOOK GENERATION: '{topic}'")
    print("="*80)
    
    # Step 1: Create book plan and structure
    print("\n📝 STEP 1: Creating book plan...")
    book_title = book_pipeline(topic, num_chapters=num_chapters)
    
    # Step 2: Generate each chapter
    print(f"\n📖 STEP 2: Generating {num_chapters} chapters...")
    for i in range(num_chapters):
        print(f"\n--- Writing Chapter {i+1}/{num_chapters} ---")
        write_next_chapter(book_title)
        
        # Pause between chapters to avoid API rate limits
        if i < num_chapters - 1:
            print(f"\nPausing for {pause_between_chapters} seconds before next chapter...")
            time.sleep(pause_between_chapters)
    
    # Step 3: Ensure all chapters have enhanced formatting
    print("\n🎨 STEP 3: Applying enhanced formatting to all chapters...")
    enhance_book_formatting(book_title)
    
    # Step 4: Compile the final book
    print("\n📚 STEP 4: Compiling final book...")
    compile_book(book_title)
    
    # Show final book status
    print("\n📊 FINAL BOOK STATUS:")
    get_book_status(book_title)
    
    # Show where to find the output
    safe_title = book_title.replace(" ", "_").replace(":", "").lower()
    book_path = Path("books") / f"{safe_title}.md"
    print(f"\n✅ Book generation complete! Your book is available at: {book_path}")
    
    return book_title

def format_existing_book(book_title):
    """
    Apply formatting improvements to an existing book
    
    Args:
        book_title (str): Title of the existing book to format
    """
    print(f"\n🎨 Enhancing formatting for existing book: '{book_title}'")
    enhance_book_formatting(book_title)
    print(f"\n✅ Formatting complete for '{book_title}'")
    
    # Recompile the book with improved formatting
    print("\n📚 Recompiling book with new formatting...")
    compile_book(book_title)

def generate_short_story_example():
    """Demo of generating a single short story with formatting"""
    from main import story_pipeline
    
    print("\n📝 Generating a short story example...")
    topic = "a haunted lighthouse on a remote island"
    story_pipeline(topic)
    
    # The story is already saved to a file with the generated title
    print("\n✅ Short story generation complete!")

if __name__ == "__main__":
    # Ensure we have environment variables loaded
    load_dotenv()
    
    # Check if API key is configured
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️ ERROR: Google API key not found!")
        print("Please create a .env file with your GOOGLE_API_KEY")
        exit(1)
        
    print("🤖 AI-Book Generator - Complete Example")
    print("="*80)
    
    # List available options
    print("\nAvailable examples:")
    print("1. Generate a complete book with formatting")
    print("2. Format an existing book")
    print("3. Generate a short story")
    
    # Get user choice
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        # Example 1: Generate a complete book
        topic = input("\nEnter a topic for your book: ")
        num_chapters = int(input("Enter number of chapters (1-10): "))
        if num_chapters < 1 or num_chapters > 10:
            num_chapters = 3
            print("Using default of 3 chapters")
        
        generate_complete_book(topic, num_chapters)
        
    elif choice == "2":
        # Example 2: Format an existing book
        print("\nExisting books:")
        get_book_status()  # Lists all available books
        book_title = input("\nEnter the title of the book to format: ")
        format_existing_book(book_title)
        
    elif choice == "3":
        # Example 3: Generate a short story
        generate_short_story_example()
        
    else:
        print("Invalid choice. Please run the script again and select 1, 2, or 3.")
    
    print("\n🎉 Example complete! Thank you for using AI-Book Generator!")