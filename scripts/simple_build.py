#!/usr/bin/env python3
"""
Simple build script for FFmpeg Mini App with detailed process status
"""

import os
import sys
import subprocess
import platform
import time
import shutil
from pathlib import Path

# Ensure Windows console handles Unicode safely
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')  # type: ignore[attr-defined]
except Exception:
    pass

class ProcessStatus:
    """Handle process status display"""
    
    def __init__(self):
        self.start_time = time.time()
        self.current_step = 0
        self.total_steps = 0
    
    def show_header(self, title, step_num, total_steps):
        """Show step header"""
        self.current_step = step_num
        self.total_steps = total_steps
        print(f"\n{'='*80}")
        print(f"📋 Step {step_num}/{total_steps}: {title}")
        print('='*80)
    
    def show_progress(self, message, status="info"):
        """Show progress message"""
        elapsed = time.time() - self.start_time
        elapsed_str = f"[{elapsed:.1f}s]"
        
        icons = {
            "info": "ℹ️ ",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️ ",
            "working": "🔄"
        }
        
        icon = icons.get(status, "ℹ️ ")
        print(f"  {icon} {elapsed_str} {message}")
    
    def show_summary(self, success, message):
        """Show step summary"""
        elapsed = time.time() - self.start_time
        status_icon = "✅" if success else "❌"
        print(f"\n{status_icon} {message} ({elapsed:.1f}s)")
        return success

def clean_environment(status):
    """Clean build environment with detailed status"""
    status.show_header("Clean Environment", 1, 3)
    
    try:
        # Clean directories
        dirs_to_clean = ["build", "dist", "release"]
        status.show_progress("Scanning for directories to clean...")
        
        for dir_name in dirs_to_clean:
            if os.path.exists(dir_name):
                status.show_progress(f"Removing directory: {dir_name}", "working")
                shutil.rmtree(dir_name)
                status.show_progress(f"Removed directory: {dir_name}", "success")
            else:
                status.show_progress(f"Directory not found: {dir_name}", "info")
        
        # Clean spec files
        status.show_progress("Scanning for .spec files...")
        spec_files = list(Path(".").glob("*.spec"))
        
        if spec_files:
            for spec_file in spec_files:
                status.show_progress(f"Removing spec file: {spec_file}", "working")
                spec_file.unlink()
                status.show_progress(f"Removed spec file: {spec_file}", "success")
        else:
            status.show_progress("No .spec files found to clean", "info")
        
        return status.show_summary(True, "Environment cleaned successfully")
        
    except Exception as e:
        status.show_progress(f"Error during cleanup: {e}", "error")
        return status.show_summary(False, "Environment cleanup failed")

def check_dependencies(status):
    """Check dependencies with detailed status"""
    status.show_header("Check Dependencies", 2, 3)
    
    try:
        status.show_progress("Checking for PyInstaller...")
        
        try:
            import PyInstaller
            version = PyInstaller.__version__
            status.show_progress(f"PyInstaller found (version: {version})", "success")
            return status.show_summary(True, "All dependencies satisfied")
            
        except ImportError:
            status.show_progress("PyInstaller not found", "warning")
            status.show_progress("Installing PyInstaller via pip...", "working")
            
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "pyinstaller"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                status.show_progress("PyInstaller installation completed", "success")
                
                # Verify installation
                import PyInstaller
                version = PyInstaller.__version__
                status.show_progress(f"PyInstaller installed successfully (version: {version})", "success")
                return status.show_summary(True, "Dependencies installed and verified")
                
            except subprocess.CalledProcessError as e:
                status.show_progress(f"Installation failed: {e}", "error")
                if e.stderr:
                    status.show_progress(f"Error details: {e.stderr[:200]}", "error")
                return status.show_summary(False, "Failed to install dependencies")
                
    except Exception as e:
        status.show_progress(f"Unexpected error: {e}", "error")
        return status.show_summary(False, "Dependency check failed")

def build_executable(status):
    """Build the executable with detailed status"""
    status.show_header("Build Executable", 3, 3)
    
    try:
        # Check if main file exists
        main_file = "src/main.py"
        if not os.path.exists(main_file):
            status.show_progress(f"Main file not found: {main_file}", "error")
            return status.show_summary(False, "Build failed - main file missing")
        
        status.show_progress(f"Found main file: {main_file}", "success")
        
        # Prepare build command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name", "FFmpegMiniApp",
            "--console",
            "--clean",
            "--noconfirm",
            main_file
        ]
        
        status.show_progress("Preparing PyInstaller command...")
        status.show_progress(f"Command: {' '.join(cmd)}", "info")
        
        # Start build process
        status.show_progress("Starting PyInstaller build process...", "working")
        build_start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd, 
                check=True, 
                capture_output=True, 
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            build_time = time.time() - build_start_time
            status.show_progress(f"PyInstaller build completed in {build_time:.1f}s", "success")
            
            # Check if executable was created
            is_windows = platform.system() == "Windows"
            exe_name = "FFmpegMiniApp.exe" if is_windows else "FFmpegMiniApp"
            exe_path = os.path.join("dist", exe_name)
            
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                status.show_progress(f"Executable created: {exe_path} ({file_size:.2f} MB)", "success")
                status.exe_name = exe_name  # Store for final summary
                return status.show_summary(True, "Build completed successfully")
            else:
                status.show_progress(f"Executable not found at: {exe_path}", "error")
                return status.show_summary(False, "Build failed - executable not created")
                
        except subprocess.TimeoutExpired:
            status.show_progress("Build process timed out (5 minutes)", "error")
            return status.show_summary(False, "Build failed - timeout")
            
        except subprocess.CalledProcessError as e:
            status.show_progress(f"PyInstaller failed with exit code: {e.returncode}", "error")
            if e.stderr:
                status.show_progress(f"Error output: {e.stderr[:300]}", "error")
            if e.stdout:
                status.show_progress(f"Build output: {e.stdout[:300]}", "info")
            return status.show_summary(False, "Build failed - PyInstaller error")
            
    except Exception as e:
        status.show_progress(f"Unexpected error: {e}", "error")
        return status.show_summary(False, "Build failed - unexpected error")

def main():
    """Main build process with detailed status tracking"""
    status = ProcessStatus()
    
    print("🎬 FFmpeg Mini App - Enhanced Build System")
    print("=" * 80)
    print(f"🖥️  Platform: {platform.system()} {platform.machine()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"⏰ Build started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Build steps with detailed status
    steps = [
        ("Clean Environment", clean_environment),
        ("Check Dependencies", check_dependencies),
        ("Build Executable", build_executable)
    ]
    
    success_count = 0
    total_time = 0
    
    for step_name, step_func in steps:
        step_start_time = time.time()
        
        try:
            success = step_func(status)
            step_time = time.time() - step_start_time
            
            if success:
                success_count += 1
                status.show_progress(f"Step '{step_name}' completed successfully", "success")
            else:
                status.show_progress(f"Step '{step_name}' failed", "error")
                break
                
        except Exception as e:
            step_time = time.time() - step_start_time
            status.show_progress(f"Step '{step_name}' failed with error: {e}", "error")
            break
        
        total_time = time.time() - status.start_time
    
    # Final summary
    print(f"\n{'='*80}")
    if success_count == len(steps):
        print("🎉 BUILD SUCCESSFUL!")
        print('='*80)
        print(f"✅ All {success_count}/{len(steps)} steps completed successfully")
        print(f"⏰ Total build time: {total_time:.1f} seconds")
        
        # Get executable name based on platform
        is_windows = platform.system() == "Windows"
        exe_name = "FFmpegMiniApp.exe" if is_windows else "FFmpegMiniApp"
        exe_path = f"dist/{exe_name}"
        
        # Check if executable actually exists
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"📦 Executable location: {exe_path} ({file_size:.2f} MB)")
        else:
            print(f"📦 Executable location: {exe_path}")
        
        print(f"🎯 Ready to use!")
        
        # Show next steps
        print(f"\n📋 Next Steps:")
        if is_windows:
            print(f"  • Test the executable: dist\\{exe_name} --help")
            print(f"  • Or double-click: dist\\{exe_name}")
        else:
            print(f"  • Test the executable: ./dist/{exe_name} --help")
        print(f"  • Copy to desired location")
        print(f"  • Share with others (no Python required)")
        
    else:
        print("❌ BUILD FAILED!")
        print('='*80)
        print(f"❌ {success_count}/{len(steps)} steps completed successfully")
        print(f"⏰ Build time: {total_time:.1f} seconds")
        print(f"🔧 Check the error messages above for details")
    
    return success_count == len(steps)

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
