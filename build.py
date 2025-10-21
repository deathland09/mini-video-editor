#!/usr/bin/env python3
"""
FFmpeg Mini App - Build Entry Point
Enhanced build system with process status tracking
"""

import sys
import subprocess
import time
from pathlib import Path

def show_build_options():
    """Show build options"""
    print("🎬 FFmpeg Mini App - Build System")
    print("=" * 60)
    print("Choose your build option:")
    print()
    print("1. 🚀 Quick Build (Recommended)")
    print("   • Fast, reliable build with detailed status")
    print("   • Perfect for development and testing")
    print()
    print("2. 🔨 Professional Build")
    print("   • Full optimizations and release packaging")
    print("   • Complete with installers and documentation")
    print()
    print("3. 🎯 Enhanced Build Menu")
    print("   • Interactive menu with all options")
    print("   • Build, test, clean, and status check")
    print()
    print("4. 📊 Build Status Check")
    print("   • Check environment and dependencies")
    print()
    print("0. ❌ Exit")
    print()

def run_quick_build():
    """Run the enhanced quick build"""
    print("🚀 Starting Enhanced Quick Build...")
    print("=" * 50)
    
    build_script = Path("simple_build.py")
    if not build_script.exists():
        print("❌ Enhanced build script not found!")
        print("Please ensure simple_build.py exists")
        return False
    
    print("📁 Using: simple_build.py (with enhanced status tracking)")
    print("⏰ Started:", time.strftime('%H:%M:%S'))
    print()
    
    try:
        start_time = time.time()
        result = subprocess.run([
            sys.executable, str(build_script)
        ], check=True)
        
        build_time = time.time() - start_time
        print(f"\n✅ Build completed successfully in {build_time:.1f} seconds!")
        print("📦 Check the 'dist/' directory for your executable")
        print("🎯 Ready to use!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with exit code: {e.returncode}")
        print("🔧 Check the error messages above for details")
        return False
    except Exception as e:
        print(f"\n❌ Build failed with error: {e}")
        return False

def run_professional_build():
    """Run the professional build"""
    print("🔨 Starting Professional Build...")
    print("=" * 50)
    
    # Check if config exists
    config_file = Path("build_config.json")
    if not config_file.exists():
        print("❌ Build configuration not found!")
        print("Please ensure build_config.json exists")
        return False
    
    pro_build_script = Path("scripts/build_pro.py")
    if not pro_build_script.exists():
        print("❌ Professional build script not found!")
        print("Please ensure scripts/build_pro.py exists")
        return False
    
    print("📁 Using: scripts/build_pro.py")
    print("⚙️  Config: build_config.json")
    print("⏰ Started:", time.strftime('%H:%M:%S'))
    print()
    
    try:
        start_time = time.time()
        result = subprocess.run([
            sys.executable, str(pro_build_script)
        ], check=True)
        
        build_time = time.time() - start_time
        print(f"\n✅ Professional build completed in {build_time:.1f} seconds!")
        print("📦 Check the 'release/' directory for your complete package")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Professional build failed with exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Professional build failed with error: {e}")
        return False

def run_enhanced_menu():
    """Run the enhanced build menu"""
    enhanced_script = Path("build_enhanced.py")
    if not enhanced_script.exists():
        print("❌ Enhanced build menu not found!")
        print("Please ensure build_enhanced.py exists")
        return False
    
    try:
        result = subprocess.run([
            sys.executable, str(enhanced_script)
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Enhanced menu failed with exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Enhanced menu failed with error: {e}")
        return False

def check_build_status():
    """Check build environment status"""
    print("📊 Build Environment Status")
    print("=" * 50)
    
    import platform
    
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
    
    # Check build scripts
    scripts = [
        ("simple_build.py", "Enhanced Quick Build"),
        ("scripts/build_pro.py", "Professional Build"),
        ("build_enhanced.py", "Enhanced Menu"),
        ("build_config.json", "Build Configuration")
    ]
    
    for script, description in scripts:
        script_path = Path(script)
        if script_path.exists():
            print(f"📜 {description}: {script} ✅")
        else:
            print(f"📜 {description}: {script} ❌")
    
    print("\n📊 Status check complete!")

def main():
    """Main build system with interactive menu"""
    while True:
        show_build_options()
        
        try:
            choice = input("Enter your choice (0-4): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                run_quick_build()
            elif choice == "2":
                run_professional_build()
            elif choice == "3":
                run_enhanced_menu()
            elif choice == "4":
                check_build_status()
            else:
                print("❌ Invalid choice. Please enter 0-4.")
            
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
