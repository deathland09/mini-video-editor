#!/usr/bin/env python3
"""
Simple wrapper to run the FFmpeg CLI app interactively
"""

import subprocess
import sys
import os

def main():
    print("🎬 FFmpeg Mini App - Quick Start")
    print("=" * 50)
    print()
    print("Available files in current directory:")
    
    # List video files
    video_files = []
    for file in os.listdir('.'):
        if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm')):
            size = os.path.getsize(file) / (1024 * 1024)
            video_files.append((file, size))
            print(f"  📹 {file} ({size:.1f} MB)")
    
    if not video_files:
        print("  No video files found in current directory")
        print()
        print("💡 To use the app:")
        print("   python3 ffmpeg_cli.py")
        print("   Then enter a file path when prompted")
        return
    
    print()
    print("🚀 Quick Start Options:")
    print("  1. Run with first video file")
    print("  2. Run interactive mode")
    print("  3. Show help")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        # Run with first video file
        video_file = video_files[0][0]
        print(f"\n🎬 Starting with: {video_file}")
        print("=" * 50)
        print("💡 In the app, select option 7 for Split Video!")
        print("=" * 50)
        
        # Run the CLI app with the video file
        try:
            subprocess.run([sys.executable, "ffmpeg_cli.py", video_file])
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
    
    elif choice == "2":
        # Run interactive mode
        print("\n🎬 Starting interactive mode...")
        print("💡 You can drag and drop a file when prompted!")
        print("=" * 50)
        
        try:
            subprocess.run([sys.executable, "ffmpeg_cli.py"])
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
    
    elif choice == "3":
        # Show help
        print("\n📚 FFmpeg Mini App Help")
        print("=" * 30)
        print()
        print("🎯 Features:")
        print("  1. Get File Info - View detailed information")
        print("  2. Convert to MP4 - Change video format")
        print("  3. Convert to MP3 - Extract audio")
        print("  4. Extract Audio - Get audio track")
        print("  5. Compress Video - Reduce file size")
        print("  6. Cut/Trim Video - Trim sections")
        print("  7. Split Video ⭐ - Split into multiple parts")
        print("  8. Select Different File - Load another video")
        print()
        print("💡 Split Video Options:")
        print("  • By Time: Split into equal duration segments")
        print("  • By Size: Split into equal file sizes")
        print("  • By Parts: Split into specific number of parts")
        print()
        print("🚀 Quick Examples:")
        print("  • Email: Split 100MB video → 5x 20MB chunks")
        print("  • Social: Split 5min video → 10x 30sec clips")
        print("  • Tutorial: Split 30min → 6x 5min parts")
        print()
        print("📁 Output: Creates {filename}_split/ folder")
        print("⚡ Fast: No re-encoding, lossless quality")
    
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
