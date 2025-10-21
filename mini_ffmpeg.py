#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from shutil import which

def find_ffmpeg():
    path = which("ffmpeg")
    if not path:
        print("❌ FFmpeg not found. Please install ffmpeg or add it to PATH.")
        sys.exit(1)
    return path

def run_ffmpeg(args):
    print("▶ Running:", " ".join(args))
    process = subprocess.Popen(args, stderr=subprocess.PIPE, text=True)
    for line in process.stderr:
        sys.stdout.write(line)
    process.wait()
    if process.returncode == 0:
        print("✅ Done.")
    else:
        print("❌ FFmpeg exited with code", process.returncode)
        sys.exit(process.returncode)

def info(file):
    if not os.path.exists(file):
        print("❌ File not found:", file)
        sys.exit(1)
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", file]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("❌ ffprobe failed:", result.stderr)
        sys.exit(1)
    data = json.loads(result.stdout)
    print(json.dumps(data, indent=2))

def convert(input_file, output_file, vcodec, acodec):
    ffmpeg = find_ffmpeg()
    cmd = [
        ffmpeg, "-y", "-i", input_file,
        "-c:v", vcodec,
        "-c:a", acodec,
        output_file
    ]
    run_ffmpeg(cmd)

def trim(input_file, output_file, start, duration, copy=False):
    ffmpeg = find_ffmpeg()
    cmd = [
        ffmpeg, "-y", "-ss", str(start), "-t", str(duration),
        "-i", input_file
    ]
    if copy:
        cmd += ["-c", "copy"]
    cmd += [output_file]
    run_ffmpeg(cmd)

def extract_audio(input_file, output_file, bitrate="192k"):
    ffmpeg = find_ffmpeg()
    cmd = [
        ffmpeg, "-y", "-i", input_file,
        "-vn", "-acodec", "mp3", "-b:a", bitrate,
        output_file
    ]
    run_ffmpeg(cmd)

def split_video(input_file, out_pattern, segment_time):
    ffmpeg = find_ffmpeg()
    cmd = [
        ffmpeg, "-y", "-i", input_file,
        "-c", "copy",
        "-map", "0",
        "-f", "segment",
        "-segment_time", str(segment_time),
        "-reset_timestamps", "1",
        out_pattern
    ]
    run_ffmpeg(cmd)

def main():
    parser = argparse.ArgumentParser(description="Mini FFmpeg CLI (Python version)")
    subparsers = parser.add_subparsers(dest="command")

    # info
    p_info = subparsers.add_parser("info", help="Show media info")
    p_info.add_argument("file")

    # convert
    p_convert = subparsers.add_parser("convert", help="Convert file")
    p_convert.add_argument("input")
    p_convert.add_argument("output")
    p_convert.add_argument("--vcodec", default="copy", help="Video codec (default: copy)")
    p_convert.add_argument("--acodec", default="copy", help="Audio codec (default: copy)")

    # trim
    p_trim = subparsers.add_parser("trim", help="Trim video/audio")
    p_trim.add_argument("input")
    p_trim.add_argument("output")
    p_trim.add_argument("--start", required=True, help="Start time (seconds or HH:MM:SS)")
    p_trim.add_argument("--duration", required=True, help="Duration (seconds or HH:MM:SS)")
    p_trim.add_argument("--copy", action="store_true", help="Use stream copy (no re-encode)")

    # extract-audio
    p_audio = subparsers.add_parser("extract-audio", help="Extract audio track")
    p_audio.add_argument("input")
    p_audio.add_argument("output")
    p_audio.add_argument("--bitrate", default="192k")

    # split
    p_split = subparsers.add_parser("split", help="Split by duration")
    p_split.add_argument("input")
    p_split.add_argument("pattern", help="Output pattern, e.g. part-%03d.mp4")
    p_split.add_argument("--time", required=True, type=int, help="Segment time in seconds")

    args = parser.parse_args()

    if args.command == "info":
        info(args.file)
    elif args.command == "convert":
        convert(args.input, args.output, args.vcodec, args.acodec)
    elif args.command == "trim":
        trim(args.input, args.output, args.start, args.duration, args.copy)
    elif args.command == "extract-audio":
        extract_audio(args.input, args.output, args.bitrate)
    elif args.command == "split":
        split_video(args.input, args.pattern, args.time)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3