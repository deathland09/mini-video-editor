#!/usr/bin/env python3
"""
Debug build script to identify issues
"""

import sys
import traceback

def main():
    """Debug the build process"""
    print("🔍 Debugging build process...")
    
    try:
        # Test imports
        print("Testing imports...")
        import os
        import sys
        import subprocess
        import platform
        import shutil
        from pathlib import Path
        from datetime import datetime
        print("✅ Basic imports successful")
        
        # Test build script import
        print("Testing build script import...")
        sys.path.insert(0, 'scripts')
        from build_pro import ProfessionalBuildSystem
        print("✅ Build script import successful")
        
        # Test build system initialization
        print("Testing build system initialization...")
        builder = ProfessionalBuildSystem()
        print("✅ Build system initialization successful")
        
        # Test clean environment
        print("Testing clean environment...")
        result = builder.clean_environment()
        print(f"✅ Clean environment result: {result}")
        
        print("🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
