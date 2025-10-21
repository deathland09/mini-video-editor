#!/usr/bin/env python3
"""
Demo script to show the split video feature
This demonstrates splitting the screen recording into smaller parts
"""

import subprocess
import os
from pathlib import Path

def demo_split_video():
    """Demonstrate the split video feature"""
    
    # Check if FFmpeg is available
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("❌ FFmpeg not found!")
            return
    except:
        print("❌ FFmpeg not found!")
        return
    
    # Input file
    input_file = "Screen Recording 2025-10-20 at 16.31.32.mov"
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    print("🎬 FFmpeg Split Video Demo")
    print("=" * 50)
    print(f"📁 Input file: {input_file}")
    
    # Get file size
    file_size = os.path.getsize(input_file) / (1024 * 1024)
    print(f"📊 File size: {file_size:.2f} MB")
    
    # Create output directory
    input_path = Path(input_file)
    output_dir = input_path.parent / f"{input_path.stem}_split"
    output_dir.mkdir(exist_ok=True)
    output_pattern = output_dir / f"{input_path.stem}_part%03d.mp4"
    
    print(f"📁 Output directory: {output_dir}")
    print()
    
    # Demo 1: Split by time (60 seconds each)
    print("🔪 Demo 1: Split by Time (60 seconds per segment)")
    print("-" * 50)
    
    try:
        result = subprocess.run([
            "ffmpeg", "-i", input_file,
            "-c", "copy",
            "-map", "0",
            "-segment_time", "60",
            "-f", "segment",
            "-reset_timestamps", "1",
            str(output_pattern)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Count created files
            parts = list(output_dir.glob(f"{input_path.stem}_part*.mp4"))
            total_size = sum(p.stat().st_size for p in parts) / (1024 * 1024)
            
            print(f"✅ Success! Created {len(parts)} parts")
            print(f"📊 Total size: {total_size:.2f} MB")
            print(f"📁 Saved to: {output_dir}")
            print()
            
            # Show parts
            print("📄 Parts created:")
            for i, part in enumerate(sorted(parts), 1):
                size = part.stat().st_size / (1024 * 1024)
                print(f"  {i}. {part.name} ({size:.2f} MB)")
            
        else:
            print(f"❌ Split failed: {result.stderr[:200]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("🎉 Demo complete!")
    print(f"📁 Check the folder: {output_dir}")
    print()
    print("💡 To use the full CLI app:")
    print("   python3 ffmpeg_cli.py")
    print("   Then select option 7 for Split Video")

if __name__ == "__main__":
    demo_split_video()
