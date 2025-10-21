#!/usr/bin/env python3
"""
Build script for creating cross-platform FFmpeg Mini App executables
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

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
        "src/mini_ffmpeg.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main build process"""
    print("🎬 FFmpeg Mini App - Cross Platform Builder")
    print("=" * 50)
    
    # Check current platform
    current_os = platform.system()
    print(f"🖥️  Current platform: {current_os}")
    print()
    
    # Check requirements
    if not check_requirements():
        return False
    
    print()
    
    # Build the executable
    if build_executable():
        print()
        print("✅ Build complete!")
        print()
        print("📁 Output files:")
        print("  • dist/FFmpegMiniApp - Executable")
        print()
        print("🚀 Usage:")
        print("  ./dist/FFmpegMiniApp --help")
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
