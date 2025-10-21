#!/usr/bin/env python3
"""
Version management for FFmpeg Mini App
Handles versioning, changelog, and release management
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class VersionManager:
    def __init__(self):
        self.version_file = "version.json"
        self.changelog_file = "CHANGELOG.md"
        self.current_version = self.get_current_version()
    
    def get_current_version(self):
        """Get current version from version.json or default"""
        if os.path.exists(self.version_file):
            with open(self.version_file, 'r') as f:
                data = json.load(f)
                return data.get('version', '1.0.0')
        return '1.0.0'
    
    def get_version_info(self):
        """Get complete version information"""
        if os.path.exists(self.version_file):
            with open(self.version_file, 'r') as f:
                return json.load(f)
        
        return {
            'version': '1.0.0',
            'build': 1,
            'release_date': datetime.now().isoformat(),
            'features': [],
            'fixes': [],
            'notes': 'Initial release'
        }
    
    def update_version(self, version_type='patch', notes=''):
        """Update version number"""
        current = self.get_version_info()
        version_parts = current['version'].split('.')
        major, minor, patch = map(int, version_parts)
        
        if version_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif version_type == 'minor':
            minor += 1
            patch = 0
        elif version_type == 'patch':
            patch += 1
        
        new_version = f"{major}.{minor}.{patch}"
        
        version_info = {
            'version': new_version,
            'build': current['build'] + 1,
            'release_date': datetime.now().isoformat(),
            'features': current.get('features', []),
            'fixes': current.get('fixes', []),
            'notes': notes or f"Version {new_version} release"
        }
        
        with open(self.version_file, 'w') as f:
            json.dump(version_info, f, indent=2)
        
        self.current_version = new_version
        return new_version
    
    def add_feature(self, feature):
        """Add a new feature to the version"""
        version_info = self.get_version_info()
        if 'features' not in version_info:
            version_info['features'] = []
        version_info['features'].append(feature)
        
        with open(self.version_file, 'w') as f:
            json.dump(version_info, f, indent=2)
    
    def add_fix(self, fix):
        """Add a bug fix to the version"""
        version_info = self.get_version_info()
        if 'fixes' not in version_info:
            version_info['fixes'] = []
        version_info['fixes'].append(fix)
        
        with open(self.version_file, 'w') as f:
            json.dump(version_info, f, indent=2)
    
    def generate_changelog(self):
        """Generate changelog from version history"""
        version_info = self.get_version_info()
        
        changelog = f"""# FFmpeg Mini App - Changelog

## Version {version_info['version']} - {version_info['release_date'][:10]}

### Features
"""
        
        for feature in version_info.get('features', []):
            changelog += f"- {feature}\n"
        
        if version_info.get('fixes'):
            changelog += "\n### Bug Fixes\n"
            for fix in version_info['fixes']:
                changelog += f"- {fix}\n"
        
        changelog += f"\n### Notes\n{version_info.get('notes', '')}\n"
        
        with open(self.changelog_file, 'w') as f:
            f.write(changelog)
        
        return changelog
    
    def build_with_version(self):
        """Build executable with version information"""
        version_info = self.get_version_info()
        
        # Update version in the CLI app
        self.update_cli_version(version_info['version'])
        
        # Build executable
        print(f"🔨 Building version {version_info['version']}...")
        
        try:
            result = subprocess.run([
                'python3', '-m', 'PyInstaller',
                '--onefile',
                '--name', f"FFmpegMiniApp-v{version_info['version']}",
                '--console',
                '--clean',
                'ffmpeg_cli.py'
            ], check=True, capture_output=True, text=True)
            
            print("✅ Build successful!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            return False
    
    def update_cli_version(self, version):
        """Update version display in CLI app"""
        # This would update the version display in the CLI app
        # For now, we'll just print it
        print(f"📝 Version {version} ready for build")
    
    def create_release_package(self):
        """Create a complete release package"""
        version_info = self.get_version_info()
        version = version_info['version']
        
        # Create release directory
        release_dir = f"release-v{version}"
        os.makedirs(release_dir, exist_ok=True)
        
        # Copy executable
        if os.path.exists(f"dist/FFmpegMiniApp-v{version}"):
            subprocess.run(['cp', f"dist/FFmpegMiniApp-v{version}", f"{release_dir}/FFmpegMiniApp"])
        
        # Copy documentation
        docs = ['README.md', 'USAGE_GUIDE.md', 'BUILD_INSTRUCTIONS.md', 'DISTRIBUTION_PACKAGE.md']
        for doc in docs:
            if os.path.exists(doc):
                subprocess.run(['cp', doc, release_dir])
        
        # Create release notes
        with open(f"{release_dir}/RELEASE_NOTES.md", 'w') as f:
            f.write(f"""# FFmpeg Mini App v{version} - Release Notes

## What's New

### Features
""")
            for feature in version_info.get('features', []):
                f.write(f"- {feature}\n")
            
            if version_info.get('fixes'):
                f.write("\n### Bug Fixes\n")
                for fix in version_info['fixes']:
                    f.write(f"- {fix}\n")
            
            f.write(f"\n### Installation\n")
            f.write(f"1. Download the executable for your platform\n")
            f.write(f"2. Install FFmpeg on your system\n")
            f.write(f"3. Run the executable\n")
        
        print(f"📦 Release package created: {release_dir}")
        return release_dir

def main():
    """Main version management interface"""
    vm = VersionManager()
    
    print("🎬 FFmpeg Mini App - Version Manager")
    print("=" * 50)
    print(f"Current version: {vm.current_version}")
    print()
    
    print("Available commands:")
    print("1. Show current version")
    print("2. Update version (patch/minor/major)")
    print("3. Add feature")
    print("4. Add bug fix")
    print("5. Generate changelog")
    print("6. Build with version")
    print("7. Create release package")
    print("8. Show version history")
    
    choice = input("\nSelect option (1-8): ").strip()
    
    if choice == "1":
        version_info = vm.get_version_info()
        print(f"\n📋 Version Information:")
        print(f"  Version: {version_info['version']}")
        print(f"  Build: {version_info['build']}")
        print(f"  Release Date: {version_info['release_date']}")
        print(f"  Features: {len(version_info.get('features', []))}")
        print(f"  Fixes: {len(version_info.get('fixes', []))}")
    
    elif choice == "2":
        version_type = input("Version type (patch/minor/major): ").strip()
        notes = input("Release notes: ").strip()
        new_version = vm.update_version(version_type, notes)
        print(f"✅ Updated to version {new_version}")
    
    elif choice == "3":
        feature = input("New feature: ").strip()
        vm.add_feature(feature)
        print(f"✅ Added feature: {feature}")
    
    elif choice == "4":
        fix = input("Bug fix: ").strip()
        vm.add_fix(fix)
        print(f"✅ Added fix: {fix}")
    
    elif choice == "5":
        changelog = vm.generate_changelog()
        print("✅ Changelog generated")
        print(f"📄 Saved to: {vm.changelog_file}")
    
    elif choice == "6":
        if vm.build_with_version():
            print("✅ Build completed successfully")
        else:
            print("❌ Build failed")
    
    elif choice == "7":
        release_dir = vm.create_release_package()
        print(f"✅ Release package created: {release_dir}")
    
    elif choice == "8":
        version_info = vm.get_version_info()
        print(f"\n📚 Version History:")
        print(f"  Current: {version_info['version']} (Build {version_info['build']})")
        print(f"  Released: {version_info['release_date'][:10]}")
        if version_info.get('features'):
            print(f"  Features: {', '.join(version_info['features'])}")
        if version_info.get('fixes'):
            print(f"  Fixes: {', '.join(version_info['fixes'])}")
    
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
