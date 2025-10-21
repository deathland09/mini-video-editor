#!/usr/bin/env python3
"""
Test script to verify FFmpeg Mini App setup
Checks all requirements without launching the GUI
"""

import sys
import platform
import subprocess
import shutil

def print_status(message, status):
    """Print colored status message"""
    colors = {
        'success': '\033[92m✓\033[0m',  # Green
        'error': '\033[91m✗\033[0m',    # Red
        'warning': '\033[93m⚠\033[0m',  # Yellow
        'info': '\033[94mℹ\033[0m',     # Blue
    }
    symbol = colors.get(status, colors['info'])
    print(f"{symbol} {message}")

def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 7:
        print_status(f"Python {version_str}", 'success')
        return True
    else:
        print_status(f"Python {version_str} (requires 3.7+)", 'error')
        return False

def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter
        print_status("Tkinter (GUI library)", 'success')
        return True
    except ImportError:
        print_status("Tkinter (GUI library) - Not installed", 'error')
        return False

def check_tkinterdnd2():
    """Check if tkinterdnd2 is available (optional)"""
    try:
        import tkinterdnd2
        print_status("tkinterdnd2 (Drag & Drop support)", 'success')
        return True
    except ImportError:
        print_status("tkinterdnd2 (Optional - for drag & drop)", 'warning')
        print("  → You can still use ffmpeg_app_simple.py without it")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed and get version"""
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
            print_status(f"FFmpeg {version}", 'success')
            
            # Also check for ffprobe
            try:
                subprocess.run(["ffprobe", "-version"], capture_output=True, timeout=5)
                print_status("FFprobe (info tool)", 'success')
            except:
                print_status("FFprobe (info tool) - Not found", 'warning')
            
            return True
        else:
            print_status("FFmpeg - Not working properly", 'error')
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_status("FFmpeg - Not installed", 'error')
        print("\n  Installation instructions:")
        os_name = platform.system()
        if os_name == "Darwin":
            print("  → macOS: brew install ffmpeg")
        elif os_name == "Linux":
            print("  → Ubuntu/Debian: sudo apt install ffmpeg")
            print("  → RedHat/CentOS: sudo yum install ffmpeg")
        elif os_name == "Windows":
            print("  → Windows: Download from ffmpeg.org")
        return False

def check_files():
    """Check if application files exist"""
    import os
    files = {
        'ffmpeg_app_simple.py': 'Simplified app (recommended)',
        'ffmpeg_app.py': 'Full app with drag & drop',
        'requirements.txt': 'Dependencies file',
    }
    
    all_exist = True
    for filename, description in files.items():
        if os.path.exists(filename):
            print_status(f"{filename} - {description}", 'success')
        else:
            print_status(f"{filename} - {description}", 'error')
            all_exist = False
    
    return all_exist

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("FFmpeg Mini App - Setup Verification")
    print("="*60 + "\n")
    
    # System Info
    print("📋 System Information:")
    print(f"  OS: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"  Python: {sys.version.split()[0]}")
    print()
    
    # Run checks
    print("🔍 Checking Requirements:\n")
    
    checks = {
        'Python 3.7+': check_python_version(),
        'Tkinter': check_tkinter(),
        'tkinterdnd2 (optional)': check_tkinterdnd2(),
        'FFmpeg': check_ffmpeg(),
        'Application Files': check_files(),
    }
    
    print("\n" + "="*60)
    
    # Summary
    required_checks = ['Python 3.7+', 'Tkinter', 'FFmpeg', 'Application Files']
    all_required_passed = all(checks[k] for k in required_checks)
    
    if all_required_passed:
        print_status("All required components are installed!", 'success')
        print("\n✅ You're ready to go!")
        print("\nTo run the application:")
        print("  → python3 ffmpeg_app_simple.py   (Recommended)")
        
        if checks['tkinterdnd2 (optional)']:
            print("  → python3 ffmpeg_app.py          (With drag & drop)")
        else:
            print("\nTo enable drag & drop:")
            print("  → pip install tkinterdnd2")
            print("  → python3 ffmpeg_app.py")
    else:
        print_status("Some required components are missing!", 'error')
        print("\n❌ Please install missing components before running the app.")
        return 1
    
    print("\n" + "="*60 + "\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())

