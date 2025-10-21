# 🎬 FFmpeg Mini App v1.0.0

## 🎉 What's New

- ✨ Initial release of FFmpeg Mini App
- 🎯 Simple CLI interface for common video/audio operations
- 🌍 Cross-platform support (Windows, macOS, Linux)
- 📦 Standalone executables - no Python required for end users

## 🚀 Features

- **Get File Info** - View detailed media information
- **Convert** - Convert between video/audio formats
- **Trim** - Cut video/audio with precise timing
- **Extract Audio** - Extract audio tracks from video
- **Split Video** - Split videos into segments by time

## 📦 Downloads

### Windows
- `FFmpegMiniApp.exe` - Windows executable

### macOS
- `FFmpegMiniApp` - macOS executable (Intel + Apple Silicon)

### Linux
- `FFmpegMiniApp` - Linux executable

## 🔧 Installation

1. **Download** the executable for your platform
2. **Install FFmpeg** on your system:
   - macOS: `brew install ffmpeg`
   - Windows: Download from [FFmpeg.org](https://ffmpeg.org/download.html)
   - Linux: `sudo apt install ffmpeg`
3. **Run** the executable

## 🎯 Quick Start

```bash
# Get help
./FFmpegMiniApp --help

# Get file information
./FFmpegMiniApp info video.mp4

# Convert video
./FFmpegMiniApp convert input.mov output.mp4

# Trim video
./FFmpegMiniApp trim input.mp4 output.mp4 --start 10 --duration 30

# Extract audio
./FFmpegMiniApp extract-audio video.mp4 audio.mp3

# Split video
./FFmpegMiniApp split video.mp4 part-%03d.mp4 --time 60
```

## 📋 Requirements

- FFmpeg installed on your system
- No Python installation required (for executables)

## 🐛 Bug Reports

If you encounter any issues, please:
1. Check that FFmpeg is installed and in your PATH
2. Create an issue with your operating system and FFmpeg version
3. Include the command you were trying to run

## 🙏 Acknowledgments

- [FFmpeg](https://ffmpeg.org/) - The powerful multimedia framework
- [PyInstaller](https://pyinstaller.org/) - For creating standalone executables

---

**Full Changelog**: https://github.com/yourusername/ffmpeg-mini-app/compare/v0.1.0...v1.0.0
