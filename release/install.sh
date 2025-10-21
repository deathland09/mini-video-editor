#!/bin/bash
echo "FFmpegMiniApp v1.0.0 - Unix Installer"
echo "================================================"

echo "Checking FFmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg found: $(ffmpeg -version | head -n 1)"
else
    echo "❌ FFmpeg not found!"
    echo "Please install FFmpeg:"
    echo "  macOS: brew install ffmpeg"
    echo "  Ubuntu: sudo apt install ffmpeg"
    echo "  CentOS: sudo yum install ffmpeg"
    exit 1
fi

echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  ./FFmpegMiniApp"
echo "  ./FFmpegMiniApp video.mp4"
