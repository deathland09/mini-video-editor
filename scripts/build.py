#!/usr/bin/env python3
"""
Professional Build System for FFmpeg Mini App
Creates optimized, cross-platform executables with proper packaging
"""

import os
import sys
import subprocess
import platform
import shutil
import json
from pathlib import Path
from datetime import datetime

class ProfessionalBuilder:
    def __init__(self):
        self.app_name = "FFmpegMiniApp"
        self.main_file = "src/main.py"
        self.current_os = platform.system()
        self.arch = platform.machine()
        self.version = self.get_version()
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        self.release_dir = Path("release")
        
    def get_version(self):
        """Get version from package info"""
        try:
            with open("src/__init__.py", "r") as f:
                for line in f:
                    if line.startswith("__version__"):
                        return line.split("=")[1].strip().strip('"').strip("'")
        except:
            pass
        return "1.0.0"
    
    def clean_build(self):
        """Clean previous build artifacts"""
        print("🧹 Cleaning previous builds...")
        
        dirs_to_clean = [self.build_dir, self.dist_dir, self.release_dir]
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"  ✅ Cleaned {dir_path}")
        
        # Clean Python cache
        for root, dirs, files in os.walk("."):
            for dir_name in dirs:
                if dir_name == "__pycache__":
                    shutil.rmtree(os.path.join(root, dir_name))
        
        print("✅ Build environment cleaned")
    
    def check_requirements(self):
        """Check and install required packages"""
        print("📋 Checking build requirements...")
        
        requirements = ["pyinstaller", "setuptools", "wheel"]
        missing = []
        
        for req in requirements:
            try:
                __import__(req)
                print(f"  ✅ {req}")
            except ImportError:
                missing.append(req)
                print(f"  ❌ {req} - missing")
        
        if missing:
            print(f"\n📦 Installing missing packages: {', '.join(missing)}")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "--upgrade"
                ] + missing, check=True)
                print("✅ All requirements installed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install requirements: {e}")
                return False
        
        return True
    
    def create_spec_file(self):
        """Create optimized PyInstaller spec file"""
        print("📝 Creating optimized spec file...")
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{self.main_file}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'tkinter', 'matplotlib', 'numpy', 'pandas', 'scipy',
        'PIL', 'cv2', 'tensorflow', 'torch', 'sklearn'
    ],
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
    name='{self.app_name}',
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
        
        spec_file = f"{self.app_name}.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        
        print(f"✅ Spec file created: {spec_file}")
        return spec_file
    
    def build_executable(self):
        """Build the executable with optimizations"""
        print("🔨 Building optimized executable...")
        
        # Build command with optimizations
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name", self.app_name,
            "--console",
            "--clean",
            "--noconfirm",
            "--optimize", "2",
            "--strip",
            "--noupx" if self.current_os == "Darwin" else "--upx-dir",  # UPX issues on macOS
            "src/main.py"
        ]
        
        # Add OS-specific optimizations
        if self.current_os == "Windows":
            cmd.extend(["--add-data", "README.md;.", "--add-data", "LICENSE;."])
        else:
            cmd.extend(["--add-data", "README.md:.", "--add-data", "LICENSE:."])
        
        print(f"  Command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ Build successful!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr[:500]}")
            return False
    
    def create_release_package(self):
        """Create professional release package"""
        print("📦 Creating release package...")
        
        # Create release directory
        self.release_dir.mkdir(exist_ok=True)
        
        # Copy executable
        exe_name = f"{self.app_name}.exe" if self.current_os == "Windows" else self.app_name
        exe_path = self.dist_dir / exe_name
        
        if exe_path.exists():
            shutil.copy2(exe_path, self.release_dir / exe_name)
            print(f"  ✅ Copied executable: {exe_name}")
        else:
            print(f"  ❌ Executable not found: {exe_path}")
            return False
        
        # Copy documentation
        docs_to_copy = [
            "README.md",
            "LICENSE",
            "requirements.txt"
        ]
        
        for doc in docs_to_copy:
            if os.path.exists(doc):
                shutil.copy2(doc, self.release_dir)
                print(f"  ✅ Copied: {doc}")
        
        # Create usage instructions
        usage_content = f"""# FFmpeg Mini App v{self.version} - Usage Instructions

## Quick Start

### Run the Application
```bash
# Windows
{self.app_name}.exe

# macOS/Linux
./{self.app_name}
```

### With File
```bash
# Windows
{self.app_name}.exe video.mp4

# macOS/Linux
./{self.app_name} video.mp4
```

## Features

✅ **Drag-and-Drop Support** - Drag files into terminal
✅ **All FFmpeg Operations** - Convert, trim, split, extract audio
✅ **Split Video** - By time, size, or number of parts
✅ **Cross-Platform** - Works on Windows, macOS, Linux
✅ **No Dependencies** - Standalone executable

## Requirements

- FFmpeg must be installed on your system
- No Python installation required

## Installation

1. Download the executable for your platform
2. Install FFmpeg on your system
3. Run the executable

## Support

- GitHub: https://github.com/yourusername/ffmpeg-mini-app
- Issues: https://github.com/yourusername/ffmpeg-mini-app/issues

---
Built on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Platform: {self.current_os} {self.arch}
"""
        
        with open(self.release_dir / "USAGE.md", "w") as f:
            f.write(usage_content)
        
        print(f"  ✅ Created usage instructions")
        
        # Create build info
        build_info = {
            "version": self.version,
            "build_date": datetime.now().isoformat(),
            "platform": self.current_os,
            "architecture": self.arch,
            "python_version": sys.version,
            "executable_size": os.path.getsize(self.release_dir / exe_name) if (self.release_dir / exe_name).exists() else 0
        }
        
        with open(self.release_dir / "build_info.json", "w") as f:
            json.dump(build_info, f, indent=2)
        
        print(f"  ✅ Created build info")
        
        return True
    
    def create_installer_scripts(self):
        """Create platform-specific installer scripts"""
        print("📜 Creating installer scripts...")
        
        # Windows installer
        if self.current_os == "Windows":
            installer_content = f"""@echo off
echo FFmpeg Mini App v{self.version} - Windows Installer
echo ================================================

echo Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo FFmpeg not found! Please install FFmpeg first.
    echo Download from: https://ffmpeg.org/download.html
    pause
    exit /b 1
)

echo FFmpeg found! Installation complete.
echo.
echo Usage:
echo   {self.app_name}.exe
echo   {self.app_name}.exe video.mp4
echo.
pause
"""
            with open(self.release_dir / "install.bat", "w") as f:
                f.write(installer_content)
            print("  ✅ Created Windows installer")
        
        # Unix installer
        unix_installer = f"""#!/bin/bash
echo "FFmpeg Mini App v{self.version} - Unix Installer"
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
echo "  ./{self.app_name}"
echo "  ./{self.app_name} video.mp4"
"""
        
        with open(self.release_dir / "install.sh", "w") as f:
            f.write(unix_installer)
        os.chmod(self.release_dir / "install.sh", 0o755)
        print("  ✅ Created Unix installer")
    
    def optimize_executable(self):
        """Apply post-build optimizations"""
        print("⚡ Applying optimizations...")
        
        exe_name = f"{self.app_name}.exe" if self.current_os == "Windows" else self.app_name
        exe_path = self.dist_dir / exe_name
        
        if not exe_path.exists():
            print("  ❌ Executable not found for optimization")
            return False
        
        # Get file size
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"  📊 Executable size: {size_mb:.2f} MB")
        
        # Apply UPX compression if available (except on macOS)
        if self.current_os != "Darwin":
            try:
                upx_result = subprocess.run(["upx", "--version"], capture_output=True, text=True)
                if upx_result.returncode == 0:
                    print("  🗜️  Applying UPX compression...")
                    subprocess.run(["upx", "--best", str(exe_path)], check=True)
                    new_size = exe_path.stat().st_size / (1024 * 1024)
                    reduction = ((size_mb - new_size) / size_mb) * 100
                    print(f"  ✅ Compressed: {new_size:.2f} MB ({reduction:.1f}% reduction)")
            except:
                print("  ⚠️  UPX not available, skipping compression")
        
        return True
    
    def run_tests(self):
        """Run basic functionality tests"""
        print("🧪 Running build tests...")
        
        exe_name = f"{self.app_name}.exe" if self.current_os == "Windows" else self.app_name
        exe_path = self.dist_dir / exe_name
        
        if not exe_path.exists():
            print("  ❌ Executable not found for testing")
            return False
        
        try:
            # Test help command
            result = subprocess.run([str(exe_path), "--help"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("  ✅ Help command works")
            else:
                print("  ❌ Help command failed")
                return False
            
            # Test version info
            result = subprocess.run([str(exe_path)], input="\n", capture_output=True, text=True, timeout=5)
            if "FFmpeg Mini App" in result.stdout:
                print("  ✅ Application starts correctly")
            else:
                print("  ❌ Application startup failed")
                return False
            
            print("  ✅ All tests passed")
            return True
            
        except Exception as e:
            print(f"  ❌ Test failed: {e}")
            return False
    
    def create_distribution_archive(self):
        """Create distribution archive"""
        print("📦 Creating distribution archive...")
        
        archive_name = f"{self.app_name}-v{self.version}-{self.current_os.lower()}-{self.arch}"
        
        try:
            if self.current_os == "Windows":
                # Create ZIP archive
                shutil.make_archive(archive_name, 'zip', self.release_dir)
                print(f"  ✅ Created: {archive_name}.zip")
            else:
                # Create TAR.GZ archive
                shutil.make_archive(archive_name, 'gztar', self.release_dir)
                print(f"  ✅ Created: {archive_name}.tar.gz")
            
            return True
        except Exception as e:
            print(f"  ❌ Archive creation failed: {e}")
            return False
    
    def build(self):
        """Main build process"""
        print_header("Professional Build System")
        print(f"🎯 Building {self.app_name} v{self.version}")
        print(f"🖥️  Platform: {self.current_os} {self.arch}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        print()
        
        # Build steps
        steps = [
            ("Clean", self.clean_build),
            ("Requirements", self.check_requirements),
            ("Spec File", self.create_spec_file),
            ("Build", self.build_executable),
            ("Optimize", self.optimize_executable),
            ("Test", self.run_tests),
            ("Package", self.create_release_package),
            ("Installers", self.create_installer_scripts),
            ("Archive", self.create_distribution_archive)
        ]
        
        for step_name, step_func in steps:
            print(f"\n{'='*60}")
            print(f"📋 Step: {step_name}")
            print('='*60)
            
            try:
                if not step_func():
                    print(f"❌ {step_name} failed!")
                    return False
            except Exception as e:
                print(f"❌ {step_name} failed with error: {e}")
                return False
        
        # Success summary
        print(f"\n{'='*60}")
        print("🎉 BUILD SUCCESSFUL!")
        print('='*60)
        print(f"📦 Release package: {self.release_dir}")
        print(f"📊 Executable: {self.dist_dir}")
        print(f"🎯 Version: {self.version}")
        print(f"🖥️  Platform: {self.current_os} {self.arch}")
        
        # Show release contents
        if self.release_dir.exists():
            print(f"\n📁 Release contents:")
            for item in self.release_dir.iterdir():
                size = item.stat().st_size / (1024 * 1024) if item.is_file() else 0
                print(f"  📄 {item.name} ({size:.2f} MB)" if item.is_file() else f"  📁 {item.name}/")
        
        return True

def print_header(text):
    """Print colored header"""
    print(f"\n{'='*60}")
    print(f"🎬 {text}")
    print('='*60)

def main():
    """Main build process"""
    builder = ProfessionalBuilder()
    return builder.build()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Build interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Build failed with error: {e}")
        sys.exit(1)