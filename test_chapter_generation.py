"""Test script to debug chapter generation."""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Add the parent directory to sys.path so we can import the tools
sys.path.append(str(Path(__file__).parent))

load_dotenv()

def test_chapter_writing():
    """Test the chapter writing process step by step."""
    print("Testing Chapter Writing Process...")
    print("=" * 50)
    
    try:
        # Import tools
        import importlib.util
        tools_path = Path(__file__).parent / "Ai-book-adk" / "sub_agents" / "writer_agent" / "tools.py"
        spec = importlib.util.spec_from_file_location("writer_tools", tools_path)
        writer_tools = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(writer_tools)
        
        editor_tools_path = Path(__file__).parent / "Ai-book-adk" / "sub_agents" / "editor_agent" / "tools.py"
        spec = importlib.util.spec_from_file_location("editor_tools", editor_tools_path)
        editor_tools = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(editor_tools)
        
        print("✅ Successfully imported writing tools")
        
        # Create a test book plan
        test_book_plan = {
            "book_title": "Test Book - Chapter Generation",
            "book_description": "A test book to verify chapter generation",
            "chapters": [
                {
                    "chapter_number": 1,
                    "chapter_title": "The Beginning",
                    "synopsis": "This is the first chapter of our test book",
                    "key_points": ["Introduce main character", "Set the scene", "Establish conflict"]
                }
            ]
        }
        
        print("📖 Testing chapter writing...")
        
        # Test chapter writing
        raw_chapter = writer_tools.chapter_writer_agent(json.dumps(test_book_plan), 0)
        
        if raw_chapter and len(raw_chapter.strip()) > 0:
            print(f"✅ Chapter writing successful! Length: {len(raw_chapter)} characters")
            print(f"First 200 characters: {raw_chapter[:200]}...")
            
            # Test chapter editing
            print("📝 Testing chapter editing...")
            edited_chapter = editor_tools.chapter_editor_agent(raw_chapter, "The Beginning")
            
            if edited_chapter and len(edited_chapter.strip()) > 0:
                print(f"✅ Chapter editing successful! Length: {len(edited_chapter)} characters")
                print(f"First 200 characters: {edited_chapter[:200]}...")
                
                # Test file writing
                print("💾 Testing file writing...")
                test_file = Path("test_chapter.md")
                try:
                    with open(test_file, "w", encoding="utf-8") as f:
                        f.write(f"# Chapter 1: The Beginning\n\n")
                        f.write("![Test Illustration](test.png)\n\n")
                        f.write(edited_chapter)
                    
                    # Verify file was written
                    if test_file.exists() and test_file.stat().st_size > 0:
                        print(f"✅ File writing successful! File size: {test_file.stat().st_size} bytes")
                        
                        # Clean up
                        test_file.unlink()
                        print("🧹 Test file cleaned up")
                        
                        return True
                    else:
                        print("❌ File was not written or is empty")
                        return False
                        
                except Exception as e:
                    print(f"❌ File writing failed: {e}")
                    return False
            else:
                print("❌ Chapter editing failed - empty result")
                return False
        else:
            print("❌ Chapter writing failed - empty result")
            return False
            
    except Exception as e:
        print(f"❌ Error in chapter writing test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_existing_book_chapter_regeneration():
    """Test regenerating chapters for the existing book."""
    print("\n" + "=" * 50)
    print("Testing Existing Book Chapter Regeneration...")
    
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
        tools_path = Path(__file__).parent / "Ai-book-adk" / "sub_agents" / "writer_agent" / "tools.py"
        spec = importlib.util.spec_from_file_location("writer_tools", tools_path)
        writer_tools = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(writer_tools)
        
        editor_tools_path = Path(__file__).parent / "Ai-book-adk" / "sub_agents" / "editor_agent" / "tools.py"
        spec = importlib.util.spec_from_file_location("editor_tools", editor_tools_path)
        editor_tools = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(editor_tools)
        
        # Test writing the first chapter
        print("🔄 Regenerating Chapter 1...")
        raw_chapter = writer_tools.chapter_writer_agent(json.dumps(book_plan), 0)
        
        if raw_chapter and len(raw_chapter.strip()) > 0:
            print(f"✅ Chapter 1 regeneration successful! Length: {len(raw_chapter)} characters")
            
            # Edit the chapter
            edited_chapter = editor_tools.chapter_editor_agent(raw_chapter, book_plan["chapters"][0]["chapter_title"])
            
            if edited_chapter and len(edited_chapter.strip()) > 0:
                print(f"✅ Chapter 1 editing successful! Length: {len(edited_chapter)} characters")
                
                # Save the regenerated chapter
                chapter_path = Path("books/book_book_about_broken_love/ch01_regenerated.md")
                with open(chapter_path, "w", encoding="utf-8") as f:
                    f.write(f"# {book_plan['chapters'][0]['chapter_title']}\n\n")
                    f.write("![Chapter Illustration](illustrations/ch01_chapter_1_understan_20250716_004706.png)\n\n")
                    f.write(edited_chapter)
                
                print(f"💾 Regenerated chapter saved to: {chapter_path}")
                return True
            else:
                print("❌ Chapter editing failed")
                return False
        else:
            print("❌ Chapter regeneration failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in chapter regeneration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Chapter Generation Debug Test")
    print("=" * 50)
    
    # Test basic chapter writing
    basic_test = test_chapter_writing()
    
    if basic_test:
        # Test regenerating existing book chapters
        regen_test = test_existing_book_chapter_regeneration()
        
        if regen_test:
            print("\n🎉 All chapter generation tests passed!")
        else:
            print("\n⚠️  Basic test passed but regeneration failed")
    else:
        print("\n❌ Basic chapter generation test failed")
