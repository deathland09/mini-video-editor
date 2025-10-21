# FFmpeg Mini App - Build Instructions

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
# Add to PATH: C:\ffmpeg\bin

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
