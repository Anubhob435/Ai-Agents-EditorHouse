"""Test the fixed editor agent to ensure it only returns clean content."""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

def test_editor_agent():
    """Test that the editor agent only returns clean content without meta-commentary."""
    print("Testing Fixed Editor Agent...")
    print("=" * 50)
    
    try:
        # Import the fixed editor tools
        import importlib.util
        
        editor_tools_path = Path(__file__).parent / "Ai-book-adk" / "sub_agents" / "editor_agent" / "tools.py"
        spec = importlib.util.spec_from_file_location("editor_tools", editor_tools_path)
        editor_tools = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(editor_tools)
        
        # Test content
        test_content = """
        This is a test chapter with some grammer mistakes and unclear sentances. 
        The writing need improvement but the story is good. It has potential.
        """
        
        test_title = "Test Chapter"
        
        print(f"🧪 Testing editor with content: {test_content[:50]}...")
        
        # Call the editor agent
        edited_content = editor_tools.chapter_editor_agent(test_content, test_title)
        
        print(f"✅ Editor returned content length: {len(edited_content)} characters")
        
        # Check for unwanted patterns
        unwanted_patterns = [
            "Okay, here's an edited version",
            "Here's an edited version",
            "Key Changes and Rationale",
            "I hope these edits are helpful",
            "Let me know if you'd like any further revisions"
        ]
        
        found_unwanted = False
        for pattern in unwanted_patterns:
            if pattern.lower() in edited_content.lower():
                print(f"❌ Found unwanted pattern: {pattern}")
                found_unwanted = True
        
        if not found_unwanted:
            print("✅ No unwanted meta-commentary found!")
            print(f"📝 Edited content preview: {edited_content[:100]}...")
            return True
        else:
            print("❌ Editor agent still including meta-commentary")
            return False
            
    except Exception as e:
        print(f"❌ Error testing editor agent: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Editor Agent Test")
    print("=" * 50)
    
    success = test_editor_agent()
    
    if success:
        print("\n✨ Editor agent test passed! Clean content only.")
    else:
        print("\n❌ Editor agent test failed")
