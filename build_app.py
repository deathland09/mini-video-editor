#!/usr/bin/env python3
"""
Build script for creating cross-platform FFmpeg Mini App executables
Creates standalone apps for Windows and macOS
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_requirements():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller found")
        return True
    except ImportError:
        print("❌ PyInstaller not found")
        print("Installing PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("✅ PyInstaller installed")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def create_spec_file():
    """Create PyInstaller spec file for the app"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['ffmpeg_cli.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FFmpegMiniApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('ffmpeg_app.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created PyInstaller spec file")

def build_executable():
    """Build the executable"""
    print("🔨 Building FFmpeg Mini App executable...")
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "FFmpegMiniApp",
        "--console",
        "--clean",
        "ffmpeg_cli.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_installer_script():
    """Create installer script for the app"""
    installer_content = '''#!/bin/bash
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
        python3 ffmpeg_cli.py
        ;;
    2)
        echo "🔨 Building executable..."
        python3 build_app.py
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
'''
    
    with open('install.sh', 'w') as f:
        f.write(installer_content)
    
    os.chmod('install.sh', 0o755)
    print("✅ Created installer script")

def create_build_instructions():
    """Create build instructions for different platforms"""
    instructions = '''# FFmpeg Mini App - Build Instructions

## 🎯 Cross-Platform Executable Build

This guide shows how to create standalone executables for Windows and macOS.

---

## 📋 Prerequisites

### All Platforms:
- Python 3.7 or higher
- FFmpeg installed and in PATH
- PyInstaller (will be installed automatically)

### Platform-Specific:

#### macOS:
```bash
# Install FFmpeg
brew install ffmpeg

# Install Python (if not already installed)
brew install python3
```

#### Windows:
```bash
# Install FFmpeg
# Download from: https://ffmpeg.org/download.html
# Add to PATH: C:\\ffmpeg\\bin

# Install Python
# Download from: https://python.org
```

#### Linux:
```bash
# Install FFmpeg
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # RedHat/CentOS

# Install Python
sudo apt install python3 python3-pip  # Ubuntu/Debian
```

---

## 🔨 Building Executables

### Automatic Build:
```bash
python3 build_app.py
```

### Manual Build:
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --name FFmpegMiniApp --console ffmpeg_cli.py
```

---

## 📦 Output Files

After building, you'll find:

### macOS:
- `dist/FFmpegMiniApp` - Executable for macOS
- `FFmpegMiniApp.app` - macOS app bundle (if created)

### Windows:
- `dist/FFmpegMiniApp.exe` - Windows executable

### Linux:
- `dist/FFmpegMiniApp` - Linux executable

---

## 🚀 Usage

### Run Executable:
```bash
# macOS/Linux
./FFmpegMiniApp

# Windows
FFmpegMiniApp.exe

# With file
./FFmpegMiniApp video.mp4
```

### Features:
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ No Python installation required
- ✅ No dependencies needed
- ✅ All FFmpeg operations included
- ✅ Split video feature included

---

## 📁 File Structure

```
video-editor/
├── ffmpeg_cli.py          # Main application
├── build_app.py           # Build script
├── install.sh             # Installer script
├── dist/                  # Built executables
│   └── FFmpegMiniApp      # Executable
├── build/                 # Build files
└── FFmpegMiniApp.spec     # PyInstaller spec
```

---

## 🎯 Distribution

### For End Users:
1. **Download the executable** for their platform
2. **Install FFmpeg** on their system
3. **Run the executable** - no Python needed!

### For Developers:
1. **Clone the repository**
2. **Run build script**: `python3 build_app.py`
3. **Distribute the executable**

---

## 🔧 Troubleshooting

### Build Issues:
- **PyInstaller not found**: Run `pip install pyinstaller`
- **FFmpeg not found**: Install FFmpeg and add to PATH
- **Permission denied**: Use `chmod +x` on Unix systems

### Runtime Issues:
- **FFmpeg not found**: Install FFmpeg on target system
- **File not found**: Check file paths and permissions
- **Slow startup**: Normal for first run (extraction)

---

## 📊 File Sizes

Typical executable sizes:
- **macOS**: ~15-20 MB
- **Windows**: ~15-20 MB  
- **Linux**: ~15-20 MB

The executable includes Python runtime and all dependencies.

---

## 🎉 Success!

Your cross-platform FFmpeg Mini App is ready!

**Features included:**
- ✅ Get file information
- ✅ Convert video formats
- ✅ Extract audio
- ✅ Compress videos
- ✅ Cut/trim videos
- ✅ **Split videos** (by time, size, or parts)
- ✅ Cross-platform compatibility

**Ready to distribute!** 🚀
'''
    
    with open('BUILD_INSTRUCTIONS.md', 'w') as f:
        f.write(instructions)
    
    print("✅ Created build instructions")

def main():
    """Main build process"""
    print("🎬 FFmpeg Mini App - Cross Platform Builder")
    print("=" * 50)
    print()
    
    # Check current platform
    current_os = platform.system()
    print(f"🖥️  Current platform: {current_os}")
    print()
    
    # Check requirements
    if not check_requirements():
        return False
    
    print()
    
    # Create spec file
    create_spec_file()
    
    # Create installer script
    create_installer_script()
    
    # Create build instructions
    create_build_instructions()
    
    print()
    print("🔨 Building executable...")
    
    # Build the executable
    if build_executable():
        print()
        print("✅ Build complete!")
        print()
        print("📁 Output files:")
        print("  • dist/FFmpegMiniApp - Executable")
        print("  • install.sh - Installer script")
        print("  • BUILD_INSTRUCTIONS.md - Build guide")
        print()
        print("🚀 Usage:")
        print("  ./dist/FFmpegMiniApp")
        print("  ./dist/FFmpegMiniApp video.mp4")
        print()
        print("📦 Distribution:")
        print("  • Copy the executable to any system")
        print("  • Ensure FFmpeg is installed on target system")
        print("  • Run the executable - no Python needed!")
        print()
        print("🎉 Cross-platform FFmpeg Mini App ready!")
        
        return True
    else:
        print("❌ Build failed!")
        return False

if __name__ == "__main__":
    main()
