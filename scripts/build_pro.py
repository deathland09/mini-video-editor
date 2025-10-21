#!/usr/bin/env python3
"""
Professional Build Script for FFmpeg Mini App
Advanced build system with configuration management
"""

import os
import sys
import json
import subprocess
import platform
import shutil
import time
from pathlib import Path
from datetime import datetime

class BuildProgress:
    """Enhanced progress tracking for professional builds"""
    
    def __init__(self):
        self.start_time = time.time()
        self.current_step = 0
        self.total_steps = 0
        self.step_start_time = 0
    
    def start_step(self, step_name, step_num, total_steps):
        """Start a new build step"""
        self.current_step = step_num
        self.total_steps = total_steps
        self.step_start_time = time.time()
        
        print(f"\n{'='*80}")
        print(f"📋 Step {step_num}/{total_steps}: {step_name}")
        print('='*80)
        print(f"⏰ Started: {time.strftime('%H:%M:%S')}")
    
    def log_action(self, message, status="info"):
        """Log an action with status"""
        elapsed = time.time() - self.start_time
        step_elapsed = time.time() - self.step_start_time
        
        icons = {
            "info": "ℹ️ ",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️ ",
            "working": "🔄",
            "progress": "📊"
        }
        
        icon = icons.get(status, "ℹ️ ")
        print(f"  {icon} [{elapsed:.1f}s] [{step_elapsed:.1f}s] {message}")
    
    def complete_step(self, success, message):
        """Complete the current step"""
        step_time = time.time() - self.step_start_time
        total_time = time.time() - self.start_time
        
        status_icon = "✅" if success else "❌"
        print(f"\n{status_icon} {message}")
        print(f"   Step time: {step_time:.1f}s | Total time: {total_time:.1f}s")
        
        return success

class ProfessionalBuildSystem:
    def __init__(self, config_file="build_config.json"):
        self.config = self.load_config(config_file)
        self.app_config = self.config["app"]
        self.build_config = self.config["build"]
        self.packaging_config = self.config["packaging"]
        
        # Map platform names to config keys
        system_name = platform.system().lower()
        if system_name == "darwin":
            self.current_os = "macos"
        elif system_name == "windows":
            self.current_os = "windows"
        else:
            self.current_os = "linux"
        
        self.arch = platform.machine()
        self.build_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Directories
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        self.release_dir = Path("release")
        self.assets_dir = Path("assets")
        
    def load_config(self, config_file):
        """Load build configuration"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Configuration file not found: {config_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {config_file}: {e}")
            sys.exit(1)
    
    def print_banner(self):
        """Print professional build banner"""
        print("=" * 80)
        print(f"🎬 {self.app_config['name']} - Professional Build System")
        print("=" * 80)
        print(f"📦 App: {self.app_config['name']} v{self.app_config['version']}")
        print(f"🖥️  Platform: {platform.system()} {self.arch}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        print(f"⏰ Build Time: {self.build_time}")
        print(f"📁 Working Directory: {os.getcwd()}")
        print(f"📄 Main File: {self.build_config['main_file']}")
        print("=" * 80)
    
    def clean_environment(self):
        """Clean build environment"""
        print("\n🧹 Cleaning build environment...")
        
        try:
            # Clean directories
            for dir_path in [self.build_dir, self.dist_dir, self.release_dir]:
                if dir_path.exists():
                    shutil.rmtree(dir_path)
                    print(f"  ✅ Cleaned {dir_path}")
            
            # Clean Python cache (simplified approach)
            import glob
            for cache_dir in glob.glob("**/__pycache__", recursive=True):
                try:
                    shutil.rmtree(cache_dir)
                    print(f"  ✅ Cleaned {cache_dir}")
                except Exception as e:
                    print(f"  ⚠️  Could not clean {cache_dir}: {e}")
            
            # Clean spec files
            for spec_file in Path(".").glob("*.spec"):
                try:
                    spec_file.unlink()
                    print(f"  ✅ Cleaned {spec_file}")
                except Exception as e:
                    print(f"  ⚠️  Could not clean {spec_file}: {e}")
            
            print("✅ Environment cleaned")
            return True
            
        except Exception as e:
            print(f"❌ Clean environment failed: {e}")
            return False
    
    def check_dependencies(self):
        """Check and install build dependencies"""
        print("\n📋 Checking dependencies...")
        
        required_packages = ["pyinstaller", "setuptools", "wheel"]
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"  ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"  ❌ {package} - missing")
        
        if missing_packages:
            print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "--upgrade"
                ] + missing_packages, check=True)
                print("✅ Dependencies installed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install dependencies: {e}")
                return False
        
        return True
    
    def create_optimized_spec(self):
        """Create optimized PyInstaller spec file"""
        print("\n📝 Creating optimized spec file...")
        
        excludes = self.build_config["excludes"]
        excludes_str = "', '".join(excludes)
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
# Generated by Professional Build System
# Build time: {self.build_time}

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['{excludes_str}'],
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
    name='{self.build_config["output_name"]}',
    debug=False,
    bootloader_ignore_signals=False,
    strip={str(self.build_config["strip"]).lower()},
    upx={str(self.build_config["upx"]).lower()},
    upx_exclude=[],
    runtime_tmpdir=None,
    console={str(self.build_config["console"]).lower()},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
        
        spec_file = f"{self.build_config['output_name']}.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        
        print(f"✅ Spec file created: {spec_file}")
        return spec_file
    
    def build_executable(self):
        """Build the executable with professional optimizations"""
        print("\n🔨 Building executable...")
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile" if self.build_config["onefile"] else "--onedir",
            "--name", self.build_config["output_name"],
            "--console" if self.build_config["console"] else "--windowed",
            "--clean",
            "--noconfirm",
            f"--optimize={self.build_config['optimize']}",
        ]
        
        # Add exclusions
        for exclude in self.build_config["excludes"]:
            cmd.extend(["--exclude-module", exclude])
        
        # Add main file
        cmd.append("src/main.py")
        
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
    
    def optimize_executable(self):
        """Apply post-build optimizations"""
        print("\n⚡ Applying optimizations...")
        
        exe_name = self.get_executable_name()
        exe_path = self.dist_dir / exe_name
        
        if not exe_path.exists():
            print(f"❌ Executable not found: {exe_path}")
            return False
        
        # Get file size
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"  📊 Original size: {size_mb:.2f} MB")
        
        # Apply UPX compression if enabled and available
        if self.config["optimization"]["compress"] and self.build_config["upx"]:
            try:
                upx_result = subprocess.run(["upx", "--version"], capture_output=True, text=True)
                if upx_result.returncode == 0:
                    print("  🗜️  Applying UPX compression...")
                    subprocess.run(["upx", "--best", str(exe_path)], check=True)
                    new_size = exe_path.stat().st_size / (1024 * 1024)
                    reduction = ((size_mb - new_size) / size_mb) * 100
                    print(f"  ✅ Compressed: {new_size:.2f} MB ({reduction:.1f}% reduction)")
                else:
                    print("  ⚠️  UPX not available, skipping compression")
            except:
                print("  ⚠️  UPX not available, skipping compression")
        
        return True
    
    def get_executable_name(self):
        """Get executable name based on platform"""
        base_name = self.build_config["output_name"]
        platform_config = self.config["platforms"][self.current_os]
        extension = platform_config["exe_extension"]
        return f"{base_name}{extension}"
    
    def run_tests(self):
        """Run comprehensive tests"""
        print("\n🧪 Running tests...")
        
        exe_name = self.get_executable_name()
        exe_path = self.dist_dir / exe_name
        
        if not exe_path.exists():
            print(f"❌ Executable not found: {exe_path}")
            return False
        
        tests = self.config["testing"]
        passed = 0
        total = 0
        
        # Test help command
        if tests["test_help"]:
            total += 1
            try:
                result = subprocess.run(
                    [str(exe_path), "--help"], 
                    capture_output=True, 
                    text=True, 
                    timeout=tests["timeout"]
                )
                if result.returncode == 0:
                    print("  ✅ Help command works")
                    passed += 1
                else:
                    print("  ❌ Help command failed")
            except Exception as e:
                print(f"  ❌ Help test failed: {e}")
        
        # Test startup
        if tests["test_startup"]:
            total += 1
            try:
                result = subprocess.run(
                    [str(exe_path)], 
                    input="\n", 
                    capture_output=True, 
                    text=True, 
                    timeout=tests["timeout"]
                )
                if "FFmpeg Mini App" in result.stdout:
                    print("  ✅ Application starts correctly")
                    passed += 1
                else:
                    print("  ❌ Application startup failed")
            except Exception as e:
                print(f"  ❌ Startup test failed: {e}")
        
        print(f"  📊 Tests: {passed}/{total} passed")
        return passed == total
    
    def create_release_package(self):
        """Create professional release package"""
        print("\n📦 Creating release package...")
        
        # Create release directory
        self.release_dir.mkdir(exist_ok=True)
        
        # Copy executable
        exe_name = self.get_executable_name()
        exe_path = self.dist_dir / exe_name
        
        if exe_path.exists():
            shutil.copy2(exe_path, self.release_dir / exe_name)
            print(f"  ✅ Copied executable: {exe_name}")
        else:
            print(f"  ❌ Executable not found: {exe_path}")
            return False
        
        # Copy included files
        for file_name in self.packaging_config["include_files"]:
            if os.path.exists(file_name):
                shutil.copy2(file_name, self.release_dir)
                print(f"  ✅ Copied: {file_name}")
            else:
                print(f"  ⚠️  File not found: {file_name}")
        
        # Create usage instructions
        self.create_usage_instructions()
        
        # Create build info
        self.create_build_info()
        
        return True
    
    def create_usage_instructions(self):
        """Create comprehensive usage instructions"""
        exe_name = self.get_executable_name()
        
        usage_content = f"""# {self.app_config['name']} v{self.app_config['version']} - Usage Instructions

## Quick Start

### Run the Application
```bash
# Windows
{exe_name}

# macOS/Linux
./{exe_name}
```

### With File
```bash
# Windows
{exe_name} video.mp4

# macOS/Linux
./{exe_name} video.mp4
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

- GitHub: {self.app_config['url']}
- Issues: {self.app_config['url']}/issues

---
Built on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Platform: {platform.system()} {self.arch}
Version: {self.app_config['version']}
"""
        
        with open(self.release_dir / "USAGE.md", "w") as f:
            f.write(usage_content)
        
        print("  ✅ Created usage instructions")
    
    def create_build_info(self):
        """Create build information file"""
        exe_name = self.get_executable_name()
        exe_path = self.release_dir / exe_name
        
        build_info = {
            "app": self.app_config,
            "build": {
                "version": self.app_config["version"],
                "build_date": datetime.now().isoformat(),
                "build_time": self.build_time,
                "platform": platform.system(),
                "architecture": self.arch,
                "python_version": sys.version,
                "executable_size_mb": exe_path.stat().st_size / (1024 * 1024) if exe_path.exists() else 0
            },
            "features": [
                "Drag-and-drop support",
                "All FFmpeg operations",
                "Video splitting",
                "Cross-platform",
                "Standalone executable"
            ]
        }
        
        with open(self.release_dir / "build_info.json", "w") as f:
            json.dump(build_info, f, indent=2)
        
        print("  ✅ Created build info")
    
    def create_installer_scripts(self):
        """Create platform-specific installer scripts"""
        print("\n📜 Creating installer scripts...")
        
        exe_name = self.get_executable_name()
        platform_config = self.config["platforms"][self.current_os]
        
        # Windows installer
        if self.current_os == "windows":
            installer_content = f"""@echo off
echo {self.app_config['name']} v{self.app_config['version']} - Windows Installer
echo ================================================

echo Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo FFmpeg not found!
    echo.
    echo Would you like to install FFmpeg automatically? (y/n)
    set /p response=
    if /i "%response%"=="y" (
        echo.
        echo Installing FFmpeg using Chocolatey...
        echo If Chocolatey is not installed, please install it first:
        echo   https://chocolatey.org/install
        echo.
        choco install ffmpeg -y
        if %errorlevel% neq 0 (
            echo.
            echo Failed to install FFmpeg automatically.
            echo Please install FFmpeg manually:
            echo   1. Download from: https://ffmpeg.org/download.html
            echo   2. Extract to C:\\ffmpeg
            echo   3. Add C:\\ffmpeg\\bin to your PATH
            echo.
            pause
            exit /b 1
        )
        echo FFmpeg installed successfully!
    ) else (
        echo FFmpeg is required to run this application.
        echo Please install FFmpeg manually and run this installer again.
        echo Download from: https://ffmpeg.org/download.html
        pause
        exit /b 1
    )
) else (
    echo FFmpeg found! Installation complete.
)

echo.
echo Usage:
echo   {exe_name}
echo   {exe_name} video.mp4
echo.
echo Features:
echo   - Convert videos (MP4, MP3, etc.)
echo   - Extract audio from videos
echo   - Compress videos
echo   - Cut/trim videos
echo   - Split videos by time/size
echo   - Fix broken/corrupted videos
echo.
pause
"""
            with open(self.release_dir / "install.bat", "w") as f:
                f.write(installer_content)
            print("  ✅ Created Windows installer")
        
        # Unix installer
        unix_installer = f"""#!/bin/bash
echo "{self.app_config['name']} v{self.app_config['version']} - Unix Installer"
echo "================================================"

# Function to detect package manager
detect_package_manager() {{
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
}}

# Function to install FFmpeg
install_ffmpeg() {{
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
}}

# Check if FFmpeg is already installed
echo "🔍 Checking FFmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg found: $(ffmpeg -version | head -n 1)"
    echo "✅ FFmpeg is already installed!"
else
    echo "❌ FFmpeg not found!"
    echo ""
    echo "🤖 Would you like to install FFmpeg automatically? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        if install_ffmpeg; then
            echo "✅ FFmpeg installed successfully!"
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
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 Usage:"
echo "  ./{exe_name}"
echo "  ./{exe_name} video.mp4"
echo ""
echo "📚 Features:"
echo "  • Convert videos (MP4, MP3, etc.)"
echo "  • Extract audio from videos"
echo "  • Compress videos"
echo "  • Cut/trim videos"
echo "  • Split videos by time/size"
echo "  • Fix broken/corrupted videos"
echo ""
echo "🎉 Enjoy using {self.app_config['name']}!"
"""
        
        with open(self.release_dir / "install.sh", "w") as f:
            f.write(unix_installer)
        os.chmod(self.release_dir / "install.sh", 0o755)
        print("  ✅ Created Unix installer")
        
        return True
    
    def create_distribution_archive(self):
        """Create distribution archive"""
        print("\n📦 Creating distribution archive...")
        
        archive_name = f"{self.app_config['name']}-v{self.app_config['version']}-{self.current_os}-{self.arch}"
        
        try:
            if self.current_os == "windows":
                shutil.make_archive(archive_name, 'zip', self.release_dir)
                print(f"  ✅ Created: {archive_name}.zip")
            else:
                shutil.make_archive(archive_name, 'gztar', self.release_dir)
                print(f"  ✅ Created: {archive_name}.tar.gz")
            
            return True
        except Exception as e:
            print(f"  ❌ Archive creation failed: {e}")
            return False
    
    def build(self):
        """Main build process with enhanced progress tracking"""
        self.print_banner()
        progress = BuildProgress()
        
        # Build steps
        steps = [
            ("Clean Environment", self.clean_environment),
            ("Check Dependencies", self.check_dependencies),
            ("Create Spec", self.create_optimized_spec),
            ("Build Executable", self.build_executable),
            ("Optimize", self.optimize_executable),
            ("Run Tests", self.run_tests),
            ("Create Package", self.create_release_package),
            ("Create Installers", self.create_installer_scripts),
            ("Create Archive", self.create_distribution_archive)
        ]
        
        success_count = 0
        total_steps = len(steps)
        
        for i, (step_name, step_func) in enumerate(steps, 1):
            progress.start_step(step_name, i, total_steps)
            
            try:
                success = step_func()
                if progress.complete_step(success, f"{step_name} completed"):
                    success_count += 1
                    progress.log_action(f"Step {i}/{total_steps} completed successfully", "success")
                else:
                    progress.log_action(f"Step {i}/{total_steps} failed", "error")
                    break
                    
            except Exception as e:
                progress.log_action(f"Step failed with error: {e}", "error")
                progress.complete_step(False, f"{step_name} failed with exception")
                break
        
        # Final summary
        total_time = time.time() - progress.start_time
        
        print(f"\n{'='*80}")
        if success_count == total_steps:
            print("🎉 PROFESSIONAL BUILD SUCCESSFUL!")
            print('='*80)
            print(f"📦 App: {self.app_config['name']} v{self.app_config['version']}")
            print(f"✅ All {success_count}/{total_steps} steps completed successfully")
            print(f"⏰ Total build time: {total_time:.1f} seconds")
            print(f"📁 Release: {self.release_dir}")
            print(f"📊 Executable: {self.dist_dir}")
            print(f"🖥️  Platform: {platform.system()} {self.arch}")
            
            # Show release contents
            if self.release_dir.exists():
                print(f"\n📁 Release Contents:")
                total_size = 0
                for item in sorted(self.release_dir.iterdir()):
                    if item.is_file():
                        size = item.stat().st_size / (1024 * 1024)
                        total_size += size
                        print(f"  📄 {item.name} ({size:.2f} MB)")
                    else:
                        print(f"  📁 {item.name}/")
                
                print(f"\n📊 Total Package Size: {total_size:.2f} MB")
            
            print(f"\n🎯 Next Steps:")
            print(f"  • Test executable: ./dist/FFmpegMiniApp --help")
            print(f"  • Check release package in: {self.release_dir}")
            print(f"  • Distribute to users (no Python required)")
            
        else:
            print("❌ PROFESSIONAL BUILD FAILED!")
            print('='*80)
            print(f"❌ {success_count}/{total_steps} steps completed successfully")
            print(f"⏰ Build time: {total_time:.1f} seconds")
            print(f"🔧 Check the error messages above for details")
        
        return success_count == total_steps

def main():
    """Main build process"""
    try:
        builder = ProfessionalBuildSystem()
        return builder.build()
    except KeyboardInterrupt:
        print("\n\n⚠️  Build interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Build failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
