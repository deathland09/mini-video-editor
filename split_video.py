#!/usr/bin/env python3
"""
Direct video splitter - no interactive input needed
Splits your screen recording into manageable parts
"""

import subprocess
import os
from pathlib import Path

def split_video_by_time(input_file, segment_time="60"):
    """Split video by time duration"""
    
    print(f"🎬 Splitting: {input_file}")
    print(f"⏱️  Duration: {segment_time} seconds per segment")
    print("=" * 50)
    
    # Create output directory
    input_path = Path(input_file)
    output_dir = input_path.parent / f"{input_path.stem}_split"
    output_dir.mkdir(exist_ok=True)
    output_pattern = output_dir / f"{input_path.stem}_part%03d.mp4"
    
    print(f"📁 Output: {output_dir}")
    print()
    
    try:
        # Run FFmpeg split command
        result = subprocess.run([
            "ffmpeg", "-i", input_file,
            "-c", "copy",
            "-map", "0",
            "-segment_time", segment_time,
            "-f", "segment",
            "-reset_timestamps", "1",
            str(output_pattern)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Count created files
            parts = list(output_dir.glob(f"{input_path.stem}_part*.mp4"))
            total_size = sum(p.stat().st_size for p in parts) / (1024 * 1024)
            
            print("✅ Split complete!")
            print(f"📊 Created {len(parts)} parts")
            print(f"📊 Total size: {total_size:.2f} MB")
            print(f"📁 Saved to: {output_dir}")
            print()
            
            # Show first few parts
            print("📄 Parts created:")
            for i, part in enumerate(sorted(parts)[:10], 1):
                size = part.stat().st_size / (1024 * 1024)
                print(f"  {i}. {part.name} ({size:.2f} MB)")
            
            if len(parts) > 10:
                print(f"  ... and {len(parts) - 10} more parts")
            
            print()
            print("🎉 Success! Your video has been split into manageable parts.")
            print(f"📁 Check the folder: {output_dir}")
            
        else:
            print(f"❌ Split failed: {result.stderr[:200]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    # Find the screen recording file
    video_file = "Screen Recording 2025-10-20 at 16.31.32.mov"
    
    if not os.path.exists(video_file):
        print(f"❌ File not found: {video_file}")
        return
    
    # Get file size
    file_size = os.path.getsize(video_file) / (1024 * 1024)
    print(f"📁 File: {video_file}")
    print(f"📊 Size: {file_size:.2f} MB")
    print()
    
    # Split into 60-second segments
    split_video_by_time(video_file, "60")
    
    print()
    print("💡 Tips:")
    print("  • Each part is about 60 seconds")
    print("  • Perfect for email sharing")
    print("  • No quality loss (lossless split)")
    print("  • Original file is unchanged")

if __name__ == "__main__":
    main()
