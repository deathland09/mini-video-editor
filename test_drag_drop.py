#!/usr/bin/env python3
"""
Test script to verify drag-and-drop path handling
"""

import os
import sys

def test_path_handling():
    """Test the path handling logic"""
    
    # Simulate different drag-and-drop scenarios
    test_paths = [
        "/Users/hungnguyen/Desktop/video-editor/Screen Recording 2025-10-20 at 16.31.32.mov",
        '"/Users/hungnguyen/Desktop/video-editor/Screen Recording 2025-10-20 at 16.31.32.mov"',
        "'/Users/hungnguyen/Desktop/video-editor/Screen Recording 2025-10-20 at 16.31.32.mov'",
        "/Users/hungnguyen/Desktop/video-editor/Screen\\ Recording\\ 2025-10-20\\ at\\ 16.31.32.mov",
    ]
    
    print("🧪 Testing Drag-and-Drop Path Handling")
    print("=" * 50)
    
    for i, test_path in enumerate(test_paths, 1):
        print(f"\nTest {i}: {test_path}")
        
        # Apply the same logic as in the fixed CLI
        file_input = test_path.strip()
        file_input = file_input.strip('"').strip("'").strip()
        
        # Handle escaped spaces from drag-and-drop
        if '\\ ' in file_input:
            file_input = file_input.replace('\\ ', ' ')
        
        print(f"  Cleaned path: {file_input}")
        print(f"  File exists: {os.path.exists(file_input)}")
        
        if os.path.exists(file_input):
            file_size = os.path.getsize(file_input) / (1024 * 1024)
            print(f"  File size: {file_size:.2f} MB")
            print("  ✅ SUCCESS!")
        else:
            print("  ❌ File not found")

if __name__ == "__main__":
    test_path_handling()
