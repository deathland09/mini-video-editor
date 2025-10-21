#!/bin/bash
# FFmpeg Mini App - Cross Platform Installer

echo "🎬 FFmpeg Mini App - Cross Platform Installer"
echo "=============================================="
echo ""

# Check OS
OS_NAME=$(uname -s)
case $OS_NAME in
    Darwin*)
        echo "🍎 Detected: macOS"
        PLATFORM="macos"
        ;;
    Linux*)
        echo "🐧 Detected: Linux"
        PLATFORM="linux"
        ;;
    CYGWIN*|MINGW*|MSYS*)
        echo "🪟 Detected: Windows"
        PLATFORM="windows"
        ;;
    *)
        echo "❓ Unknown OS: $OS_NAME"
        PLATFORM="unknown"
        ;;
esac

echo ""
echo "📋 Prerequisites Check:"
echo "======================="

# Check Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3: $(python3 --version)"
else
    echo "❌ Python3 not found!"
    echo "Please install Python 3.7+ from python.org"
    exit 1
fi

# Check FFmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg: $(ffmpeg -version | head -n 1)"
else
    echo "⚠️  FFmpeg not found!"
    echo ""
    echo "Please install FFmpeg:"
    if [ "$PLATFORM" = "macos" ]; then
        echo "  brew install ffmpeg"
    elif [ "$PLATFORM" = "linux" ]; then
        echo "  sudo apt install ffmpeg  # Ubuntu/Debian"
        echo "  sudo yum install ffmpeg  # RedHat/CentOS"
    else
        echo "  Download from: https://ffmpeg.org/download.html"
    fi
    echo ""
fi

echo ""
echo "🚀 Installation Options:"
echo "========================"
echo "1. Run Python version (requires Python + FFmpeg)"
echo "2. Build standalone executable (requires PyInstaller)"
echo "3. Download pre-built executable (if available)"
echo ""

read -p "Select option (1-3): " choice

case $choice in
    1)
        echo "🐍 Running Python version..."
        python3 src/main.py
        ;;
    2)
        echo "🔨 Building executable..."
        python3 build.py
        ;;
    3)
        echo "📥 Downloading pre-built executable..."
        echo "Check the releases section for pre-built executables"
        ;;
    *)
        echo "❌ Invalid choice!"
        exit 1
        ;;
esac
