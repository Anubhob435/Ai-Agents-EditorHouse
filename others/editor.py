import re
import os
import json
from pathlib import Path
from google import genai

# Load the API key from environment variables
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

class FormatAgent:
    """
    Agent responsible for enhancing the formatting of generated book content.
    Applies styling like bold and italics, cleans up unnecessary content,
    and improves the overall presentation of the markdown.
    """
    def __init__(self):
        self.model = "gemini-2.0-flash"
    
    def format_chapter(self, chapter_content, chapter_title, chapter_number):
        """
        Apply formatting enhancements to a chapter's content
        
        Args:
            chapter_content (str): The raw chapter content
            chapter_title (str): The title of the chapter
            chapter_number (int): The chapter number
            
        Returns:
            str: The enhanced chapter content with better formatting
        """
        print(f"🎨 Enhancing formatting for Chapter {chapter_number}: {chapter_title}...")
        
        # First, let's use the AI to format the dialogue and apply other stylistic improvements
        formatted_content = self._apply_ai_formatting(chapter_content, chapter_title)
        
        # Then apply rules-based formatting for consistency
        formatted_content = self._apply_rule_based_formatting(formatted_content)
        
        # Finally, remove any undesirable conclusion texts
        formatted_content = self._remove_undesirable_text(formatted_content)
        
        print(f"✅ Formatting enhanced for Chapter {chapter_number}")
        return formatted_content
    
    def _apply_ai_formatting(self, content, chapter_title):
        """Use AI to enhance the formatting of the content"""
        prompt = f"""
        Format the following chapter content with proper Markdown formatting.
        
        Guidelines:
        1. Put all dialogue in italics (using *dialogue*)
        2. Use **bold** for emphasis on important phrases and moments
        3. Add proper section breaks (---) between scenes
        4. Ensure paragraphs have proper spacing
        5. DO NOT add any new content or conclusions
        6. DO NOT add any notes to the reader or meta-commentary
        7. DO NOT change the actual story content, just enhance the formatting
        
        Chapter: {chapter_title}
        
        {content}
        """
        
        try:
            response = client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error in AI formatting: {e}")
            # If AI formatting fails, return original content
            return content
    
    def _apply_rule_based_formatting(self, content):
        """Apply consistent rule-based formatting"""
        # Ensure dialogue is properly formatted with italics
        # Find text in quotes that isn't already italicized
        content = re.sub(r'(?<!\*)"([^"]*)"(?!\*)', r'*"\1"*', content)
        
        # Ensure headers are properly formatted
        content = re.sub(r'^(?!#)(.+?)\n={3,}$', r'# \1', content, flags=re.MULTILINE)
        content = re.sub(r'^(?!##)(.+?)\n-{3,}$', r'## \1', content, flags=re.MULTILINE)
        
        # Ensure proper spacing between paragraphs
        content = re.sub(r'([^\n])\n([^\n])', r'\1\n\n\2', content)
        
        # Fix inconsistent formatting in markdown
        content = re.sub(r'\*\*\*\*(.*?)\*\*\*\*', r'**\1**', content)  # Fix over-emphasized text
        
        return content
    
    def _remove_undesirable_text(self, content):
        """Remove common undesirable text patterns from the content"""
        # Remove common conclusion formulas that might be generated
        patterns_to_remove = [
            r'(?i)The End\.?\s*$',
            r'(?i)To be continued\.?\s*$',
            r'(?i)Thanks for reading\.?\s*$',
            r'(?i)I hope you enjoyed .*?\s*$',
            r'(?i)Stay tuned for the next chapter.*?\s*$',
            r'(?i)This concludes chapter \d+\.?\s*$',
            r'(?i)Author\'s Note:.*?$'
        ]
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        # Remove trailing whitespace at the end of the content
        content = content.rstrip()
        
        return content

def enhance_chapter_formatting(chapter_filepath):
    """
    Function to enhance formatting of a chapter file
    
    Args:
        chapter_filepath (str or Path): Path to the chapter markdown file
    
    Returns:
        bool: True if successful, False otherwise
    """
    filepath = Path(chapter_filepath)
    
    if not filepath.exists():
        print(f"❌ File not found: {filepath}")
        return False
    
    try:
        # Extract chapter number and title from filename
        filename = filepath.name
        match = re.match(r'chapter_(\d+)_(.*?)\.md', filename)
        
        if match:
            chapter_number = int(match.group(1))
            chapter_title = match.group(2).replace('_', ' ')
        else:
            # If filename doesn't match pattern, try to infer from content
            chapter_number = 0
            chapter_title = filepath.stem.replace('_', ' ')
        
        # Read the chapter content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Try to extract title from content
            title_match = re.search(r'# Chapter \d+: (.*?)\n', content)
            if title_match:
                chapter_title = title_match.group(1)
            
            # Extract the core content (skip title and illustration if present)
            illustration_end = content.find('\n\n', content.find('!['))
            if illustration_end > 0:
                core_content = content[illustration_end+2:]
            else:
                # Skip just the title
                title_end = content.find('\n\n')
                if title_end > 0:
                    core_content = content[title_end+2:]
                else:
                    core_content = content
        
        # Apply formatting
        formatter = FormatAgent()
        formatted_content = formatter.format_chapter(core_content, chapter_title, chapter_number)
        
        # Reconstruct full content with title and illustration (if present)
        if illustration_end > 0:
            # Keep title and illustration, replace rest with formatted content
            new_content = content[:illustration_end+2] + formatted_content
        else:
            # Keep just the title if present
            if title_end > 0:
                new_content = content[:title_end+2] + formatted_content
            else:
                new_content = formatted_content
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Enhanced formatting for {filepath.name}")
        return True
    
    except Exception as e:
        print(f"❌ Error enhancing chapter: {e}")
        return False

def enhance_book_formatting(book_title):
    """
    Enhance formatting for all chapters of a book
    
    Args:
        book_title (str): The title of the book to enhance
    
    Returns:
        int: Number of chapters successfully formatted
    """
    # Format book title for directory search
    safe_title = book_title.replace(" ", "_").replace(":", "").lower()
    book_dir = Path("books") / safe_title
    
    if not book_dir.exists():
        print(f"❌ Book directory not found: {book_dir}")
        return 0
    
    # Find all markdown files in the book directory
    chapter_files = list(book_dir.glob("chapter_*.md"))
    
    if not chapter_files:
        print(f"❌ No chapter files found in {book_dir}")
        return 0
    
    print(f"🎨 Enhancing formatting for {len(chapter_files)} chapters in '{book_title}'")
    
    # Process each chapter
    success_count = 0
    for chapter_file in sorted(chapter_files):
        if enhance_chapter_formatting(chapter_file):
            success_count += 1
    
    print(f"✅ Completed formatting {success_count} out of {len(chapter_files)} chapters")
    return success_count

if __name__ == "__main__":
    # Example usage
    # enhance_chapter_formatting("books/my_book/chapter_01_introduction.md")
    # enhance_book_formatting("My Amazing Book Title")
    pass