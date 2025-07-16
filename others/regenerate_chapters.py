"""Script to regenerate the missing chapters with correct filenames."""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Add the parent directory to sys.path so we can import the tools
sys.path.append(str(Path(__file__).parent))

load_dotenv()

def regenerate_book_chapters():
    """Regenerate all chapters for the existing book with correct filenames."""
    print("Regenerating Book Chapters...")
    print("=" * 50)
    
    try:
        # Read the existing book metadata
        book_metadata_path = Path("books/book_book_about_broken_love/book_metadata.json")
        
        if not book_metadata_path.exists():
            print("❌ Book metadata not found")
            return False
            
        with open(book_metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            
        book_plan = metadata["generation_info"]["book_plan"]
        print(f"📖 Found book: {book_plan['book_title']}")
        print(f"📚 Chapters: {len(book_plan['chapters'])}")
        
        # Import tools
        import importlib.util
        
        writer_tools_path = Path(__file__).parent / "Ai-book-adk" / "sub_agents" / "writer_agent" / "tools.py"
        spec = importlib.util.spec_from_file_location("writer_tools", writer_tools_path)
        writer_tools = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(writer_tools)
        
        editor_tools_path = Path(__file__).parent / "Ai-book-adk" / "sub_agents" / "editor_agent" / "tools.py"
        spec = importlib.util.spec_from_file_location("editor_tools", editor_tools_path)
        editor_tools = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(editor_tools)
        
        book_dir = Path("books/book_book_about_broken_love")
        
        # Find existing illustration files
        illustrations_dir = book_dir / "illustrations"
        illustration_files = {}
        if illustrations_dir.exists():
            for file in illustrations_dir.iterdir():
                if file.name.startswith("ch01"):
                    illustration_files[1] = file.name
                elif file.name.startswith("ch02"):
                    illustration_files[2] = file.name
        
        # Regenerate each chapter
        for i, chapter in enumerate(book_plan["chapters"]):
            chapter_num = chapter["chapter_number"]
            chapter_title = chapter["chapter_title"]
            
            print(f"\n🔄 Regenerating Chapter {chapter_num}: {chapter_title}")
            
            # Generate chapter content
            raw_chapter = writer_tools.chapter_writer_agent(json.dumps(book_plan), i)
            
            if raw_chapter and len(raw_chapter.strip()) > 0:
                print(f"✅ Chapter {chapter_num} writing successful! Length: {len(raw_chapter)} characters")
                
                # Edit the chapter
                edited_chapter = editor_tools.chapter_editor_agent(raw_chapter, chapter_title)
                
                if edited_chapter and len(edited_chapter.strip()) > 0:
                    print(f"✅ Chapter {chapter_num} editing successful! Length: {len(edited_chapter)} characters")
                    
                    # Create proper filename (removing invalid characters)
                    chapter_short_title = chapter_title[:20].replace(' ', '_').replace(':', '').replace('/', '').replace('\\', '').lower()
                    chapter_filename = book_dir / f"ch{chapter_num:02d}_{chapter_short_title}.md"
                    
                    # Create illustration reference
                    if chapter_num in illustration_files:
                        illustration_ref = f"![Chapter {chapter_num} Illustration: {chapter_title}](illustrations/{illustration_files[chapter_num]})"
                    else:
                        illustration_ref = f"*[Illustration for Chapter {chapter_num} could not be found]*"
                    
                    # Save the chapter
                    with open(chapter_filename, "w", encoding="utf-8") as f:
                        f.write(f"# Chapter {chapter_num}: {chapter_title}\n\n")
                        f.write(illustration_ref + "\n\n")
                        f.write(edited_chapter)
                    
                    print(f"💾 Chapter {chapter_num} saved to: {chapter_filename}")
                    
                    # Remove old empty files if they exist
                    old_file = book_dir / f"ch{chapter_num:02d}_chapter_{chapter_num}"
                    if old_file.exists():
                        old_file.unlink()
                        print(f"🗑️  Removed old empty file: {old_file}")
                        
                else:
                    print(f"❌ Chapter {chapter_num} editing failed")
                    return False
            else:
                print(f"❌ Chapter {chapter_num} writing failed")
                return False
        
        print(f"\n🎉 All {len(book_plan['chapters'])} chapters regenerated successfully!")
        print("\nGenerated files:")
        for file in book_dir.glob("*.md"):
            print(f"  📄 {file.name}")
            
        return True
            
    except Exception as e:
        print(f"❌ Error in chapter regeneration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Chapter Regeneration Script")
    print("=" * 50)
    
    success = regenerate_book_chapters()
    
    if success:
        print("\n✨ Chapter regeneration completed successfully!")
    else:
        print("\n❌ Chapter regeneration failed")
