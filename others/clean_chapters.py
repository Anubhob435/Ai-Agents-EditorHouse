"""Script to clean up editor agent meta-commentary from chapter files."""

import os
import re
from pathlib import Path

def clean_chapter_files():
    """Remove editor agent meta-commentary from chapter files."""
    print("Cleaning Chapter Files...")
    print("=" * 50)
    
    books_dir = Path("books")
    if not books_dir.exists():
        print("❌ Books directory not found")
        return
    
    # Patterns to remove
    intro_patterns = [
        r"Okay, here's an edited version of your chapter[^.]*\.",
        r"Here's an edited version of your chapter[^.]*\.",
        r"I've edited your chapter[^.]*\.",
        r"Here's the edited chapter[^.]*\.",
    ]
    
    # Pattern for the rationale section at the end
    rationale_pattern = r"\*\*Key Changes and Rationale:\*\*.*?(?=\n\n|$)"
    closing_pattern = r"I hope these edits are helpful.*?(?=\n\n|$)"
    
    cleaned_files = []
    
    for book_dir in books_dir.iterdir():
        if book_dir.is_dir():
            for chapter_file in book_dir.glob("ch*.md"):
                print(f"🔍 Checking: {chapter_file}")
                
                try:
                    with open(chapter_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # Remove intro patterns
                    for pattern in intro_patterns:
                        content = re.sub(pattern, "", content, flags=re.DOTALL | re.IGNORECASE)
                    
                    # Remove rationale section
                    content = re.sub(rationale_pattern, "", content, flags=re.DOTALL)
                    content = re.sub(closing_pattern, "", content, flags=re.DOTALL)
                    
                    # Clean up extra newlines
                    content = re.sub(r'\n\n\n+', '\n\n', content)
                    content = content.strip()
                    
                    # Check if changes were made
                    if content != original_content:
                        with open(chapter_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"✅ Cleaned: {chapter_file}")
                        cleaned_files.append(chapter_file)
                    else:
                        print(f"✓ Already clean: {chapter_file}")
                        
                except Exception as e:
                    print(f"❌ Error processing {chapter_file}: {e}")
    
    print(f"\n🎉 Cleaned {len(cleaned_files)} chapter files")
    if cleaned_files:
        print("\nCleaned files:")
        for file in cleaned_files:
            print(f"  📄 {file}")
    
    return len(cleaned_files)

if __name__ == "__main__":
    print("Chapter File Cleanup Script")
    print("=" * 50)
    
    count = clean_chapter_files()
    
    if count > 0:
        print(f"\n✨ Successfully cleaned {count} chapter files!")
    else:
        print("\n✓ All chapter files are already clean!")
