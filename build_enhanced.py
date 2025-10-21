#!/usr/bin/env python3
"""
Enhanced Build Script for FFmpeg Mini App
Combines simple reliability with professional features
"""

import sys
import subprocess
import platform
import time
from pathlib import Path

def show_build_menu():
    """Show build options menu"""
    print("🎬 FFmpeg Mini App - Enhanced Build System")
    print("=" * 60)
    print("Choose your build option:")
    print()
    print("1. 🚀 Quick Build (Recommended)")
    print("   • Fast, reliable build")
    print("   • Basic optimizations")
    print("   • Perfect for development")
    print()
    print("2. 🔨 Professional Build")
    print("   • Full optimizations")
    print("   • Release packaging")
    print("   • Cross-platform installers")
    print()
    print("3. 🧪 Test Build")
    print("   • Build and test executable")
    print("   • Verify functionality")
    print()
    print("4. 📊 Build Status")
    print("   • Check build environment")
    print("   • Verify dependencies")
    print()
    print("5. 🧹 Clean Only")
    print("   • Clean build artifacts")
    print("   • Reset environment")
    print()
    print("0. ❌ Exit")
    print()

def run_quick_build():
    """Run the quick build"""
    print("🚀 Starting Quick Build...")
    print("=" * 40)
    
    try:
        result = subprocess.run([
            sys.executable, "simple_build.py"
        ], check=True)
        
        print("\n✅ Quick build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Quick build failed with exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Quick build failed with error: {e}")
        return False

def run_professional_build():
    """Run the professional build"""
    print("🔨 Starting Professional Build...")
    print("=" * 40)
    
    # Check if config exists
    if not Path("build_config.json").exists():
        print("❌ Build configuration not found!")
        print("Please ensure build_config.json exists")
        return False
    
    try:
        result = subprocess.run([
            sys.executable, "scripts/build_pro.py"
        ], check=True)
        
        print("\n✅ Professional build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Professional build failed with exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Professional build failed with error: {e}")
        return False

def run_test_build():
    """Run build and test"""
    print("🧪 Starting Test Build...")
    print("=" * 40)
    
    # First build
    print("Step 1: Building executable...")
    if not run_quick_build():
        return False
    
    # Then test
    print("\nStep 2: Testing executable...")
    exe_name = "FFmpegMiniApp.exe" if platform.system() == "Windows" else "FFmpegMiniApp"
    exe_path = Path("dist") / exe_name
    
    if not exe_path.exists():
        print(f"❌ Executable not found: {exe_path}")
        return False
    
    try:
        # Test help command
        print("Testing help command...")
        result = subprocess.run([
            str(exe_path), "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Help command works")
        else:
            print("❌ Help command failed")
            return False
        
        # Test startup
        print("Testing application startup...")
        result = subprocess.run([
            str(exe_path)
        ], input="\n", capture_output=True, text=True, timeout=5)
        
        if "FFmpeg Mini App" in result.stdout:
            print("✅ Application starts correctly")
        else:
            print("❌ Application startup failed")
            return False
        
        print("\n✅ All tests passed!")
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def check_build_status():
    """Check build environment status"""
    print("📊 Build Environment Status")
    print("=" * 40)
    
    # Check Python
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Check platform
    print(f"🖥️  Platform: {platform.system()} {platform.machine()}")
    
    # Check main file
    main_file = Path("src/main.py")
    if main_file.exists():
        size = main_file.stat().st_size / 1024  # KB
        print(f"📄 Main file: {main_file} ({size:.1f} KB) ✅")
    else:
        print(f"📄 Main file: {main_file} ❌")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print(f"🔧 PyInstaller: {PyInstaller.__version__} ✅")
    except ImportError:
        print("🔧 PyInstaller: Not installed ❌")
    
    # Check build directories
    dirs = ["build", "dist", "release"]
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"📁 {dir_name}/: Exists ✅")
        else:
            print(f"📁 {dir_name}/: Not found ℹ️ ")
    
    # Check config
    config_file = Path("build_config.json")
    if config_file.exists():
        print(f"⚙️  Config: {config_file} ✅")
    else:
        print(f"⚙️  Config: {config_file} ❌")
    
    print("\n📊 Status check complete!")

def clean_build():
    """Clean build artifacts"""
    print("🧹 Cleaning Build Environment...")
    print("=" * 40)
    
    import shutil
    
    dirs_to_clean = ["build", "dist", "release"]
    cleaned_count = 0
    
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Cleaned {dir_name}/")
                cleaned_count += 1
            except Exception as e:
                print(f"❌ Failed to clean {dir_name}/: {e}")
        else:
            print(f"ℹ️  {dir_name}/ not found")
    
    # Clean spec files
    spec_count = 0
    for spec_file in Path(".").glob("*.spec"):
        try:
            spec_file.unlink()
            print(f"✅ Cleaned {spec_file}")
            spec_count += 1
        except Exception as e:
            print(f"❌ Failed to clean {spec_file}: {e}")
    
    if not spec_count:
        print("ℹ️  No .spec files found")
    
    print(f"\n🧹 Cleanup complete! Removed {cleaned_count} directories and {spec_count} spec files.")

def main():
    """Main enhanced build system"""
    while True:
        show_build_menu()
        
        try:
            choice = input("Enter your choice (0-5): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                run_quick_build()
            elif choice == "2":
                run_professional_build()
            elif choice == "3":
                run_test_build()
            elif choice == "4":
                check_build_status()
            elif choice == "5":
                clean_build()
            else:
                print("❌ Invalid choice. Please enter 0-5.")
            
            if choice in ["1", "2", "3"]:
                input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Build interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
