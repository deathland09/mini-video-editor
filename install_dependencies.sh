#!/bin/bash
# FFmpeg Mini App - Dependency Installer
# This script automatically installs FFmpeg on various platforms

echo "🎬 FFmpeg Mini App - Dependency Installer"
echo "=========================================="

# Function to detect package manager
detect_package_manager() {
    if command -v brew &> /dev/null; then
        echo "brew"
    elif command -v apt &> /dev/null; then
        echo "apt"
    elif command -v yum &> /dev/null; then
        echo "yum"
    elif command -v dnf &> /dev/null; then
        echo "dnf"
    elif command -v pacman &> /dev/null; then
        echo "pacman"
    elif command -v zypper &> /dev/null; then
        echo "zypper"
    else
        echo "unknown"
    fi
}

# Function to install FFmpeg
install_ffmpeg() {
    local pkg_manager=$(detect_package_manager)
    
    echo "🔍 Detected package manager: $pkg_manager"
    echo "📦 Installing FFmpeg..."
    
    case $pkg_manager in
        "brew")
            if command -v brew &> /dev/null; then
                brew install ffmpeg
            else
                echo "❌ Homebrew not found. Please install Homebrew first:"
                echo "   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                return 1
            fi
            ;;
        "apt")
            sudo apt update
            sudo apt install -y ffmpeg
            ;;
        "yum")
            sudo yum install -y ffmpeg
            ;;
        "dnf")
            sudo dnf install -y ffmpeg
            ;;
        "pacman")
            sudo pacman -S --noconfirm ffmpeg
            ;;
        "zypper")
            sudo zypper install -y ffmpeg
            ;;
        *)
            echo "❌ Unsupported package manager: $pkg_manager"
            echo "Please install FFmpeg manually:"
            echo "  Download from: https://ffmpeg.org/download.html"
            return 1
            ;;
    esac
}

# Check if FFmpeg is already installed
echo "🔍 Checking FFmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg found: $(ffmpeg -version | head -n 1)"
    echo "✅ FFmpeg is already installed!"
    exit 0
fi

echo "❌ FFmpeg not found!"
echo ""
echo "🤖 Would you like to install FFmpeg automatically? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    if install_ffmpeg; then
        echo "✅ FFmpeg installed successfully!"
        echo ""
        echo "🎉 You can now run the FFmpeg Mini App!"
    else
        echo "❌ Failed to install FFmpeg automatically."
        echo "Please install FFmpeg manually:"
        echo "  macOS: brew install ffmpeg"
        echo "  Ubuntu/Debian: sudo apt install ffmpeg"
        echo "  CentOS/RHEL: sudo yum install ffmpeg"
        echo "  Fedora: sudo dnf install ffmpeg"
        echo "  Arch: sudo pacman -S ffmpeg"
        echo "  OpenSUSE: sudo zypper install ffmpeg"
        exit 1
    fi
else
    echo "❌ FFmpeg is required to run this application."
    echo "Please install FFmpeg manually and run this installer again."
    exit 1
fi
