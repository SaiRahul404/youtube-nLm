"""Test script to verify source clearing functionality."""

import sys
sys.path.insert(0, 'src')

from notebooklm_handler import NotebookLMHandler
from config import Config

def main():
    print("=" * 60)
    print("NotebookLM Source Management Test")
    print("=" * 60)
    print()
    
    # Initialize handler
    handler = NotebookLMHandler(Config.NOTEBOOKLM_NOTEBOOK_ID)
    
    # Check authentication
    print("1. Checking authentication...")
    if not handler.ensure_authenticated():
        print("   ❌ Not authenticated. Run: nlm login")
        return
    print("   ✓ Authenticated")
    print()
    
    # List current sources
    print("2. Listing current sources in notebook...")
    sources = handler.list_sources()
    if sources is None:
        print("   ❌ Failed to list sources")
        return
    
    print(f"   Found {len(sources)} source(s):")
    for i, source in enumerate(sources, 1):
        source_type = source.get('type', 'unknown')
        source_title = source.get('title', 'No title')
        source_id = source.get('id', 'No ID')
        print(f"   {i}. [{source_type}] {source_title[:60]}")
        print(f"      ID: {source_id}")
    print()
    
    # Test clearing sources
    if len(sources) > 0:
        print("3. Testing clear_all_sources()...")
        if handler.clear_all_sources():
            print("   ✓ Successfully cleared all sources")
        else:
            print("   ❌ Failed to clear sources")
        print()
        
        # Verify sources are cleared
        print("4. Verifying sources were cleared...")
        sources_after = handler.list_sources()
        if sources_after is not None:
            print(f"   Sources remaining: {len(sources_after)}")
            if len(sources_after) == 0:
                print("   ✓ All sources successfully removed")
            else:
                print("   ⚠ Some sources still present:")
                for source in sources_after:
                    print(f"      - {source.get('title', 'Unknown')}")
        print()
    else:
        print("3. No sources to clear (notebook is empty)")
        print()
    
    # Test adding a source (example URL)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print(f"5. Testing add_source() with example URL...")
    print(f"   URL: {test_url}")
    print("   Note: This will clear existing sources and add the test video")
    print()
    
    confirm = input("   Proceed with test? (y/n): ")
    if confirm.lower() != 'y':
        print("   Test cancelled")
        return
    
    if handler.add_source(test_url):
        print("   ✓ Successfully added source")
        print()
        
        # Verify source was added
        print("6. Verifying source was added...")
        sources_final = handler.list_sources()
        if sources_final:
            print(f"   Total sources: {len(sources_final)}")
            if len(sources_final) == 1:
                print("   ✓ Exactly one source present (as expected)")
                print(f"   Source: {sources_final[0].get('title', 'Unknown')}")
            else:
                print(f"   ⚠ Expected 1 source, found {len(sources_final)}")
    else:
        print("   ❌ Failed to add source")
    
    print()
    print("=" * 60)
    print("Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    try:
        Config.validate()
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
