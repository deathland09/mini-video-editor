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
import time
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
    """Convert file to specified format with progress tracking"""
    
    input_path = Path(input_file)
    output_path = input_path.parent / f"{input_path.stem}_converted.{output_format}"
    
    print_info(f"Converting to {output_format.upper()}...")
    print(f"  Input: {input_file}")
    print(f"  Output: {output_path}")
    
    # Get input file size for progress estimation
    input_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
    print_info(f"Input file size: {input_size:.2f} MB")
    
    print_info("Starting conversion process...")
    start_time = time.time()
    
    try:
        # Use FFmpeg with progress output
        cmd = [
            ffmpeg_path, "-i", input_file, 
            "-y",  # Overwrite output file
            "-progress", "pipe:1",  # Output progress to stdout
            str(output_path)
        ]
        
        print_info("FFmpeg command: " + " ".join(cmd))
        print_info("Conversion in progress...")
        
        # Run FFmpeg with real-time progress
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Monitor progress
        progress_started = False
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            
            if output:
                # Parse FFmpeg progress output
                if "out_time_ms=" in output:
                    if not progress_started:
                        print_info("Conversion progress started...")
                        progress_started = True
                    
                    # Extract time information
                    try:
                        time_str = output.split("out_time_ms=")[1].split()[0]
                        time_ms = int(time_str)
                        time_seconds = time_ms / 1000000.0
                        
                        # Show progress every 5 seconds
                        if int(time_seconds) % 5 == 0 and int(time_seconds) > 0:
                            elapsed = time.time() - start_time
                            print_info(f"Progress: {time_seconds:.1f}s processed (elapsed: {elapsed:.1f}s)")
                    except:
                        pass
        
        # Wait for process to complete
        return_code = process.wait()
        
        if return_code == 0:
            end_time = time.time()
            conversion_time = end_time - start_time
            
            if os.path.exists(output_path):
                output_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print_success(f"Conversion complete!")
                print_success(f"  Output size: {output_size:.2f} MB")
                print_success(f"  Conversion time: {conversion_time:.1f} seconds")
                print_success(f"  Saved to: {output_path}")
                
                # Show compression ratio
                if input_size > 0:
                    ratio = (output_size / input_size) * 100
                    print_info(f"  Size ratio: {ratio:.1f}% of original")
                
                return True
            else:
                print_error("Output file was not created!")
                return False
        else:
            # Get error details
            stderr_output = process.stderr.read()
            print_error(f"Conversion failed with return code: {return_code}")
            if stderr_output:
                print_error("Error details:")
                print(stderr_output[-500:])  # Last 500 characters
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def extract_audio(ffmpeg_path, input_file):
    """Extract audio from video with progress tracking"""
    
    input_path = Path(input_file)
    output_path = input_path.parent / f"{input_path.stem}_audio.mp3"
    
    print_info("Extracting audio...")
    print(f"  Input: {input_file}")
    print(f"  Output: {output_path}")
    
    # Get input file size for progress estimation
    input_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
    print_info(f"Input file size: {input_size:.2f} MB")
    
    print_info("Starting audio extraction...")
    start_time = time.time()
    
    try:
        # Use FFmpeg with progress output
        cmd = [
            ffmpeg_path, "-i", input_file, 
            "-vn",  # No video
            "-acodec", "libmp3lame", 
            "-ab", "192k", 
            "-y",  # Overwrite output file
            "-progress", "pipe:1",  # Output progress to stdout
            str(output_path)
        ]
        
        print_info("FFmpeg command: " + " ".join(cmd))
        print_info("Audio extraction in progress...")
        
        # Run FFmpeg with real-time progress
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Monitor progress
        progress_started = False
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            
            if output:
                # Parse FFmpeg progress output
                if "out_time_ms=" in output:
                    if not progress_started:
                        print_info("Audio extraction progress started...")
                        progress_started = True
                    
                    # Extract time information
                    try:
                        time_str = output.split("out_time_ms=")[1].split()[0]
                        time_ms = int(time_str)
                        time_seconds = time_ms / 1000000.0
                        
                        # Show progress every 5 seconds
                        if int(time_seconds) % 5 == 0 and int(time_seconds) > 0:
                            elapsed = time.time() - start_time
                            print_info(f"Progress: {time_seconds:.1f}s processed (elapsed: {elapsed:.1f}s)")
                    except:
                        pass
        
        # Wait for process to complete
        return_code = process.wait()
        
        if return_code == 0:
            end_time = time.time()
            extraction_time = end_time - start_time
            
            if os.path.exists(output_path):
                output_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print_success(f"Audio extraction complete!")
                print_success(f"  Output size: {output_size:.2f} MB")
                print_success(f"  Extraction time: {extraction_time:.1f} seconds")
                print_success(f"  Saved to: {output_path}")
                
                # Show compression ratio
                if input_size > 0:
                    ratio = (output_size / input_size) * 100
                    print_info(f"  Size ratio: {ratio:.1f}% of original")
                
                return True
            else:
                print_error("Output file was not created!")
                return False
        else:
            # Get error details
            stderr_output = process.stderr.read()
            print_error(f"Audio extraction failed with return code: {return_code}")
            if stderr_output:
                print_error("Error details:")
                print(stderr_output[-500:])  # Last 500 characters
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
            
            print_info("Starting video splitting...")
            start_time = time.time()
            
            # Use FFmpeg with progress output
            cmd = [
                ffmpeg_path, "-i", input_file,
                "-c", "copy",
                "-map", "0",
                "-segment_time", segment_time,
                "-f", "segment",
                "-reset_timestamps", "1",
                "-progress", "pipe:1",  # Output progress to stdout
                str(output_pattern)
            ]
            
            print_info("FFmpeg command: " + " ".join(cmd))
            print_info("Video splitting in progress...")
            
            # Run FFmpeg with real-time progress
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor progress
            progress_started = False
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                
                if output:
                    # Parse FFmpeg progress output
                    if "out_time_ms=" in output:
                        if not progress_started:
                            print_info("Video splitting progress started...")
                            progress_started = True
                        
                        # Extract time information
                        try:
                            time_str = output.split("out_time_ms=")[1].split()[0]
                            time_ms = int(time_str)
                            time_seconds = time_ms / 1000000.0
                            
                            # Show progress every 5 seconds
                            if int(time_seconds) % 5 == 0 and int(time_seconds) > 0:
                                elapsed = time.time() - start_time
                                print_info(f"Progress: {time_seconds:.1f}s processed (elapsed: {elapsed:.1f}s)")
                        except:
                            pass
            
            # Wait for process to complete
            result = type('obj', (object,), {'returncode': process.wait()})()
            
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
            
            print_info("Starting video splitting by size...")
            start_time = time.time()
            
            # Use FFmpeg with progress output
            cmd = [
                ffmpeg_path, "-i", input_file,
                "-c", "copy",
                "-map", "0",
                "-f", "segment",
                "-segment_size", str(size_bytes),
                "-reset_timestamps", "1",
                "-progress", "pipe:1",  # Output progress to stdout
                str(output_pattern)
            ]
            
            print_info("FFmpeg command: " + " ".join(cmd))
            print_info("Video splitting in progress...")
            
            # Run FFmpeg with real-time progress
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor progress
            progress_started = False
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                
                if output:
                    # Parse FFmpeg progress output
                    if "out_time_ms=" in output:
                        if not progress_started:
                            print_info("Video splitting progress started...")
                            progress_started = True
                        
                        # Extract time information
                        try:
                            time_str = output.split("out_time_ms=")[1].split()[0]
                            time_ms = int(time_str)
                            time_seconds = time_ms / 1000000.0
                            
                            # Show progress every 5 seconds
                            if int(time_seconds) % 5 == 0 and int(time_seconds) > 0:
                                elapsed = time.time() - start_time
                                print_info(f"Progress: {time_seconds:.1f}s processed (elapsed: {elapsed:.1f}s)")
                        except:
                            pass
            
            # Wait for process to complete
            result = type('obj', (object,), {'returncode': process.wait()})()
            
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
            
            print_info("Starting video splitting into equal parts...")
            start_time = time.time()
            
            # Use FFmpeg with progress output
            cmd = [
                ffmpeg_path, "-i", input_file,
                "-c", "copy",
                "-map", "0",
                "-segment_time", str(segment_duration),
                "-f", "segment",
                "-reset_timestamps", "1",
                "-progress", "pipe:1",  # Output progress to stdout
                str(output_pattern)
            ]
            
            print_info("FFmpeg command: " + " ".join(cmd))
            print_info("Video splitting in progress...")
            
            # Run FFmpeg with real-time progress
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor progress
            progress_started = False
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                
                if output:
                    # Parse FFmpeg progress output
                    if "out_time_ms=" in output:
                        if not progress_started:
                            print_info("Video splitting progress started...")
                            progress_started = True
                        
                        # Extract time information
                        try:
                            time_str = output.split("out_time_ms=")[1].split()[0]
                            time_ms = int(time_str)
                            time_seconds = time_ms / 1000000.0
                            
                            # Show progress every 5 seconds
                            if int(time_seconds) % 5 == 0 and int(time_seconds) > 0:
                                elapsed = time.time() - start_time
                                print_info(f"Progress: {time_seconds:.1f}s processed (elapsed: {elapsed:.1f}s)")
                        except:
                            pass
            
            # Wait for process to complete
            result = type('obj', (object,), {'returncode': process.wait()})()
        else:
            print_error("Invalid choice!")
            return False
        
        if result.returncode == 0:
            end_time = time.time()
            splitting_time = end_time - start_time
            
            # Count created files
            parts = list(output_dir.glob(f"{input_path.stem}_part*.mp4"))
            total_size = sum(p.stat().st_size for p in parts) / (1024 * 1024)
            
            print_success(f"Video split complete!")
            print_success(f"  Created {len(parts)} parts")
            print_success(f"  Total size: {total_size:.2f} MB")
            print_success(f"  Splitting time: {splitting_time:.1f} seconds")
            print_success(f"  Saved to: {output_dir}")
            
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


def fix_broken_video(ffmpeg_path, input_file):
    """Fix broken/corrupted video files"""
    print("\n" + "─"*60)
    print(f"{Colors.CYAN}Fix Broken Video{Colors.RESET}")
    print("─"*60)
    
    input_path = Path(input_file)
    output_path = input_path.parent / f"{input_path.stem}_fixed.mp4"
    
    print_info("Attempting to fix broken video...")
    print(f"  Input: {input_file}")
    print(f"  Output: {output_path}")
    
    # Get input file size for progress estimation
    input_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
    print_info(f"Input file size: {input_size:.2f} MB")
    
    print_info("Starting video repair process...")
    start_time = time.time()
    
    try:
        # Use FFmpeg with error correction and progress output
        cmd = [
            ffmpeg_path, "-i", input_file,
            "-c", "copy",  # Copy streams without re-encoding
            "-map", "0",   # Map all streams
            "-ignore_errors",  # Ignore errors and continue
            "-y",  # Overwrite output file
            "-progress", "pipe:1",  # Output progress to stdout
            str(output_path)
        ]
        
        print_info("FFmpeg command: " + " ".join(cmd))
        print_info("Video repair in progress...")
        
        # Run FFmpeg with real-time progress
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Monitor progress
        progress_started = False
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            
            if output:
                # Parse FFmpeg progress output
                if "out_time_ms=" in output:
                    if not progress_started:
                        print_info("Video repair progress started...")
                        progress_started = True
                    
                    # Extract time information
                    try:
                        time_str = output.split("out_time_ms=")[1].split()[0]
                        time_ms = int(time_str)
                        time_seconds = time_ms / 1000000.0
                        
                        # Show progress every 5 seconds
                        if int(time_seconds) % 5 == 0 and int(time_seconds) > 0:
                            elapsed = time.time() - start_time
                            print_info(f"Progress: {time_seconds:.1f}s processed (elapsed: {elapsed:.1f}s)")
                    except:
                        pass
        
        # Wait for process to complete
        return_code = process.wait()
        
        if return_code == 0:
            end_time = time.time()
            repair_time = end_time - start_time
            
            if os.path.exists(output_path):
                output_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print_success(f"Video repair complete!")
                print_success(f"  Output size: {output_size:.2f} MB")
                print_success(f"  Repair time: {repair_time:.1f} seconds")
                print_success(f"  Saved to: {output_path}")
                
                # Show size comparison
                if input_size > 0:
                    ratio = (output_size / input_size) * 100
                    print_info(f"  Size ratio: {ratio:.1f}% of original")
                
                return True
            else:
                print_error("Output file was not created!")
                return False
        else:
            # Get error details
            stderr_output = process.stderr.read()
            print_error(f"Video repair failed with return code: {return_code}")
            if stderr_output:
                print_error("Error details:")
                print(stderr_output[-500:])  # Last 500 characters
            
            # Try alternative repair method
            print_info("Trying alternative repair method...")
            return try_alternative_repair(ffmpeg_path, input_file, output_path)
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def try_alternative_repair(ffmpeg_path, input_file, output_path):
    """Try alternative repair methods for severely corrupted videos"""
    print_info("Attempting alternative repair with re-encoding...")
    
    try:
        # Alternative method: re-encode with error correction
        cmd = [
            ffmpeg_path, "-i", input_file,
            "-c:v", "libx264",  # Re-encode video
            "-c:a", "aac",       # Re-encode audio
            "-crf", "23",        # Good quality
            "-preset", "fast",   # Fast encoding
            "-ignore_errors",    # Ignore errors
            "-y",  # Overwrite output file
            "-progress", "pipe:1",  # Output progress to stdout
            str(output_path)
        ]
        
        print_info("Alternative FFmpeg command: " + " ".join(cmd))
        print_info("Alternative repair in progress...")
        
        # Run FFmpeg with real-time progress
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Monitor progress
        progress_started = False
        start_time = time.time()
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            
            if output:
                # Parse FFmpeg progress output
                if "out_time_ms=" in output:
                    if not progress_started:
                        print_info("Alternative repair progress started...")
                        progress_started = True
                    
                    # Extract time information
                    try:
                        time_str = output.split("out_time_ms=")[1].split()[0]
                        time_ms = int(time_str)
                        time_seconds = time_ms / 1000000.0
                        
                        # Show progress every 10 seconds (re-encoding is slower)
                        if int(time_seconds) % 10 == 0 and int(time_seconds) > 0:
                            elapsed = time.time() - start_time
                            print_info(f"Progress: {time_seconds:.1f}s processed (elapsed: {elapsed:.1f}s)")
                    except:
                        pass
        
        # Wait for process to complete
        return_code = process.wait()
        
        if return_code == 0 and os.path.exists(output_path):
            end_time = time.time()
            repair_time = end_time - start_time
            output_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            
            print_success(f"Alternative repair successful!")
            print_success(f"  Output size: {output_size:.2f} MB")
            print_success(f"  Repair time: {repair_time:.1f} seconds")
            print_success(f"  Saved to: {output_path}")
            print_warning("Note: Video was re-encoded, quality may be slightly reduced")
            
            return True
        else:
            print_error("Alternative repair also failed!")
            stderr_output = process.stderr.read()
            if stderr_output:
                print_error("Error details:")
                print(stderr_output[-500:])
            return False
            
    except Exception as e:
        print_error(f"Alternative repair error: {e}")
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
    print(f"  {Colors.YELLOW}8{Colors.RESET}. Fix Broken Video")
    print(f"  {Colors.GREEN}9{Colors.RESET}. Select Different File")
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
        
        choice = input(f"\n{Colors.CYAN}Select operation (0-9):{Colors.RESET} ").strip()
        
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
            fix_broken_video(ffmpeg_path, current_file)
        elif choice == "9":
            file_input = input(f"\n{Colors.CYAN}Enter new file path:{Colors.RESET} ").strip().strip('"').strip("'")
            if os.path.exists(file_input):
                current_file = file_input
                file_name = os.path.basename(current_file)
                file_size = os.path.getsize(current_file) / (1024 * 1024)
                print_success(f"Loaded: {file_name} ({file_size:.2f} MB)")
            else:
                print_error("File not found!")
        else:
            print_warning("Invalid choice! Please select 0-9.")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.RESET}")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted by user.{Colors.RESET}")
        sys.exit(0)

