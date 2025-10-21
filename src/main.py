#!/usr/bin/env python3
"""
FFmpeg Mini Application - Command Line Version
Works on any Python installation without GUI dependencies
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path


class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.RESET}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.RESET} {text}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ{Colors.RESET} {text}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {text}")


def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            version = version_line.split()[2] if len(version_line.split()) > 2 else "unknown"
            print_success(f"FFmpeg {version} detected")
            return "ffmpeg"
    except:
        pass
    
    print_error("FFmpeg not found!")
    print_info("Install FFmpeg:")
    print("  macOS: brew install ffmpeg")
    print("  Linux: sudo apt install ffmpeg")
    print("  Windows: Download from ffmpeg.org")
    return None


def get_file_info(ffmpeg_path, file_path):
    """Get detailed file information"""
    print_info(f"Getting information for: {os.path.basename(file_path)}")
    
    try:
        ffprobe = ffmpeg_path.replace("ffmpeg", "ffprobe")
        result = subprocess.run(
            [ffprobe, file_path],
            capture_output=True,
            text=True
        )
        
        print("\n" + result.stderr)
        return True
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def convert_file(ffmpeg_path, input_file, output_format):
    """Convert file to specified format"""
    input_path = Path(input_file)
    output_path = input_path.parent / f"{input_path.stem}_converted.{output_format}"
    
    print_info(f"Converting to {output_format.upper()}...")
    print(f"  Input: {input_file}")
    print(f"  Output: {output_path}")
    
    try:
        result = subprocess.run(
            [ffmpeg_path, "-i", input_file, "-y", str(output_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            size = os.path.getsize(output_path) / (1024 * 1024)
            print_success(f"Conversion complete! Output size: {size:.2f} MB")
            print_success(f"Saved to: {output_path}")
            return True
        else:
            print_error("Conversion failed!")
            print(result.stderr[:500])
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def extract_audio(ffmpeg_path, input_file):
    """Extract audio from video"""
    input_path = Path(input_file)
    output_path = input_path.parent / f"{input_path.stem}_audio.mp3"
    
    print_info("Extracting audio...")
    print(f"  Input: {input_file}")
    print(f"  Output: {output_path}")
    
    try:
        result = subprocess.run(
            [ffmpeg_path, "-i", input_file, "-vn", "-acodec", "libmp3lame", "-ab", "192k", "-y", str(output_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            size = os.path.getsize(output_path) / (1024 * 1024)
            print_success(f"Audio extracted! Output size: {size:.2f} MB")
            print_success(f"Saved to: {output_path}")
            return True
        else:
            print_error("Extraction failed!")
            print(result.stderr[:500])
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def compress_video(ffmpeg_path, input_file):
    """Compress video file"""
    input_path = Path(input_file)
    output_path = input_path.parent / f"{input_path.stem}_compressed.mp4"
    
    original_size = os.path.getsize(input_file) / (1024 * 1024)
    
    print_info("Compressing video...")
    print(f"  Input: {input_file} ({original_size:.2f} MB)")
    print(f"  Output: {output_path}")
    
    try:
        result = subprocess.run(
            [ffmpeg_path, "-i", input_file, "-vcodec", "libx264", "-crf", "28", "-y", str(output_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            new_size = os.path.getsize(output_path) / (1024 * 1024)
            reduction = ((original_size - new_size) / original_size) * 100
            print_success(f"Video compressed! New size: {new_size:.2f} MB ({reduction:.1f}% smaller)")
            print_success(f"Saved to: {output_path}")
            return True
        else:
            print_error("Compression failed!")
            print(result.stderr[:500])
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def cut_video(ffmpeg_path, input_file):
    """Cut/trim video"""
    print("\n" + "─"*60)
    print(f"{Colors.CYAN}Cut/Trim Video{Colors.RESET}")
    print("─"*60)
    
    start_time = input(f"{Colors.CYAN}Enter start time (HH:MM:SS or seconds, e.g., 00:00:30):{Colors.RESET} ").strip()
    duration = input(f"{Colors.CYAN}Enter duration (HH:MM:SS or seconds, e.g., 00:01:00):{Colors.RESET} ").strip()
    
    if not start_time or not duration:
        print_error("Invalid input!")
        return False
    
    input_path = Path(input_file)
    output_path = input_path.parent / f"{input_path.stem}_cut.mp4"
    
    print_info("Cutting video...")
    print(f"  Input: {input_file}")
    print(f"  Start: {start_time}")
    print(f"  Duration: {duration}")
    print(f"  Output: {output_path}")
    
    try:
        result = subprocess.run(
            [ffmpeg_path, "-i", input_file, "-ss", start_time, "-t", duration, "-c", "copy", "-y", str(output_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            size = os.path.getsize(output_path) / (1024 * 1024)
            print_success(f"Video trimmed! Output size: {size:.2f} MB")
            print_success(f"Saved to: {output_path}")
            return True
        else:
            print_error("Trimming failed!")
            print(result.stderr[:500])
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def split_video(ffmpeg_path, input_file):
    """Split video into multiple parts"""
    print("\n" + "─"*60)
    print(f"{Colors.CYAN}Split Video{Colors.RESET}")
    print("─"*60)
    print(f"\n{Colors.BOLD}Split by:{Colors.RESET}")
    print(f"  {Colors.GREEN}1{Colors.RESET}. Time (equal duration segments)")
    print(f"  {Colors.GREEN}2{Colors.RESET}. Size (approximate file size)")
    print(f"  {Colors.GREEN}3{Colors.RESET}. Number of parts")
    
    split_choice = input(f"\n{Colors.CYAN}Select split method (1-3):{Colors.RESET} ").strip()
    
    input_path = Path(input_file)
    output_dir = input_path.parent / f"{input_path.stem}_split"
    output_dir.mkdir(exist_ok=True)
    
    try:
        if split_choice == "1":
            # Split by time duration
            segment_time = input(f"{Colors.CYAN}Enter segment duration (HH:MM:SS or seconds, e.g., 00:01:00 or 60):{Colors.RESET} ").strip()
            if not segment_time:
                print_error("Invalid input!")
                return False
            
            output_pattern = output_dir / f"{input_path.stem}_part%03d.mp4"
            
            print_info("Splitting video by time...")
            print(f"  Input: {input_file}")
            print(f"  Segment duration: {segment_time}")
            print(f"  Output folder: {output_dir}")
            
            result = subprocess.run(
                [
                    ffmpeg_path, "-i", input_file,
                    "-c", "copy",
                    "-map", "0",
                    "-segment_time", segment_time,
                    "-f", "segment",
                    "-reset_timestamps", "1",
                    str(output_pattern)
                ],
                capture_output=True,
                text=True
            )
            
        elif split_choice == "2":
            # Split by size
            size_mb = input(f"{Colors.CYAN}Enter target size per segment in MB (e.g., 10):{Colors.RESET} ").strip()
            if not size_mb or not size_mb.isdigit():
                print_error("Invalid input!")
                return False
            
            size_bytes = int(size_mb) * 1024 * 1024
            output_pattern = output_dir / f"{input_path.stem}_part%03d.mp4"
            
            print_info("Splitting video by size...")
            print(f"  Input: {input_file}")
            print(f"  Target size: {size_mb} MB per segment")
            print(f"  Output folder: {output_dir}")
            
            result = subprocess.run(
                [
                    ffmpeg_path, "-i", input_file,
                    "-c", "copy",
                    "-map", "0",
                    "-f", "segment",
                    "-segment_size", str(size_bytes),
                    "-reset_timestamps", "1",
                    str(output_pattern)
                ],
                capture_output=True,
                text=True
            )
            
        elif split_choice == "3":
            # Split by number of parts
            num_parts = input(f"{Colors.CYAN}Enter number of parts (e.g., 4):{Colors.RESET} ").strip()
            if not num_parts or not num_parts.isdigit() or int(num_parts) < 2:
                print_error("Invalid input! Must be 2 or more.")
                return False
            
            # First, get video duration
            ffprobe = ffmpeg_path.replace("ffmpeg", "ffprobe")
            duration_result = subprocess.run(
                [
                    ffprobe, "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    input_file
                ],
                capture_output=True,
                text=True
            )
            
            if duration_result.returncode != 0:
                print_error("Could not get video duration!")
                return False
            
            total_duration = float(duration_result.stdout.strip())
            segment_duration = total_duration / int(num_parts)
            
            output_pattern = output_dir / f"{input_path.stem}_part%03d.mp4"
            
            print_info("Splitting video into equal parts...")
            print(f"  Input: {input_file}")
            print(f"  Total duration: {total_duration:.2f} seconds")
            print(f"  Parts: {num_parts}")
            print(f"  Duration per part: {segment_duration:.2f} seconds")
            print(f"  Output folder: {output_dir}")
            
            result = subprocess.run(
                [
                    ffmpeg_path, "-i", input_file,
                    "-c", "copy",
                    "-map", "0",
                    "-segment_time", str(segment_duration),
                    "-f", "segment",
                    "-reset_timestamps", "1",
                    str(output_pattern)
                ],
                capture_output=True,
                text=True
            )
        else:
            print_error("Invalid choice!")
            return False
        
        if result.returncode == 0:
            # Count created files
            parts = list(output_dir.glob(f"{input_path.stem}_part*.mp4"))
            total_size = sum(p.stat().st_size for p in parts) / (1024 * 1024)
            
            print_success(f"Video split complete!")
            print_success(f"Created {len(parts)} parts")
            print_success(f"Total size: {total_size:.2f} MB")
            print_success(f"Saved to: {output_dir}")
            
            # Show parts info
            print(f"\n{Colors.CYAN}Parts created:{Colors.RESET}")
            for i, part in enumerate(sorted(parts), 1):
                size = part.stat().st_size / (1024 * 1024)
                print(f"  {i}. {part.name} ({size:.2f} MB)")
            
            return True
        else:
            print_error("Split failed!")
            print(result.stderr[:500])
            return False
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def show_menu():
    """Display main menu"""
    print("\n" + "─"*60)
    print(f"{Colors.BOLD}Operations:{Colors.RESET}")
    print("─"*60)
    print(f"  {Colors.GREEN}1{Colors.RESET}. Get File Info")
    print(f"  {Colors.GREEN}2{Colors.RESET}. Convert to MP4")
    print(f"  {Colors.GREEN}3{Colors.RESET}. Convert to MP3")
    print(f"  {Colors.GREEN}4{Colors.RESET}. Extract Audio")
    print(f"  {Colors.GREEN}5{Colors.RESET}. Compress Video")
    print(f"  {Colors.GREEN}6{Colors.RESET}. Cut/Trim Video")
    print(f"  {Colors.GREEN}7{Colors.RESET}. Split Video")
    print(f"  {Colors.GREEN}8{Colors.RESET}. Select Different File")
    print(f"  {Colors.RED}0{Colors.RESET}. Exit")
    print("─"*60)


def main():
    """Main application loop"""
    print_header("FFmpeg Mini App - CLI Version")
    
    # Show system info
    os_name = platform.system()
    os_version = platform.release()
    arch = platform.machine()
    print_info(f"OS: {os_name} {os_version} ({arch})")
    print_info(f"Python: {sys.version.split()[0]}")
    
    # Check FFmpeg
    ffmpeg_path = check_ffmpeg()
    if not ffmpeg_path:
        return 1
    
    print("\n" + "─"*60)
    
    # Get input file
    current_file = None
    
    if len(sys.argv) > 1:
        # File provided as argument
        current_file = sys.argv[1]
        if not os.path.exists(current_file):
            print_error(f"File not found: {current_file}")
            current_file = None
    
    if not current_file:
        print(f"\n{Colors.CYAN}Enter path to video/audio file:{Colors.RESET}")
        print(f"{Colors.YELLOW}(or drag and drop the file here, then press Enter){Colors.RESET}")
        file_input = input("→ ").strip()
        
        # Handle drag-and-drop paths with spaces and special characters
        # Remove quotes and clean the path
        file_input = file_input.strip('"').strip("'").strip()
        
        # Handle escaped spaces from drag-and-drop
        if '\\ ' in file_input:
            file_input = file_input.replace('\\ ', ' ')
        
        if not file_input:
            print_error("No file path provided!")
            return 1
        
        if not os.path.exists(file_input):
            print_error(f"File not found: {file_input}")
            print_info("Make sure the file path is correct and the file exists")
            return 1
        
        current_file = file_input
    
    # Show file info
    file_name = os.path.basename(current_file)
    file_size = os.path.getsize(current_file) / (1024 * 1024)
    print_success(f"Loaded: {file_name} ({file_size:.2f} MB)")
    
    # Main loop
    while True:
        show_menu()
        
        choice = input(f"\n{Colors.CYAN}Select operation (0-8):{Colors.RESET} ").strip()
        
        if choice == "0":
            print_info("Goodbye!")
            break
        elif choice == "1":
            get_file_info(ffmpeg_path, current_file)
        elif choice == "2":
            convert_file(ffmpeg_path, current_file, "mp4")
        elif choice == "3":
            convert_file(ffmpeg_path, current_file, "mp3")
        elif choice == "4":
            extract_audio(ffmpeg_path, current_file)
        elif choice == "5":
            compress_video(ffmpeg_path, current_file)
        elif choice == "6":
            cut_video(ffmpeg_path, current_file)
        elif choice == "7":
            split_video(ffmpeg_path, current_file)
        elif choice == "8":
            file_input = input(f"\n{Colors.CYAN}Enter new file path:{Colors.RESET} ").strip().strip('"').strip("'")
            if os.path.exists(file_input):
                current_file = file_input
                file_name = os.path.basename(current_file)
                file_size = os.path.getsize(current_file) / (1024 * 1024)
                print_success(f"Loaded: {file_name} ({file_size:.2f} MB)")
            else:
                print_error("File not found!")
        else:
            print_warning("Invalid choice! Please select 0-8.")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted by user.{Colors.RESET}")
        sys.exit(0)

