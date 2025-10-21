# ⚡ Quick Start Guide

Get up and running with FFmpeg Mini App in minutes!

## 🚀 5-Minute Setup

### Step 1: Install FFmpeg
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Step 2: Get the App
```bash
# Clone repository
git clone https://github.com/yourusername/ffmpeg-mini-app.git
cd ffmpeg-mini-app

# Or download executable
# Windows: FFmpegMiniApp.exe
# macOS: FFmpegMiniApp
# Linux: FFmpegMiniApp
```

### Step 3: Test It Works
```bash
# Python version
python3 src/mini_ffmpeg.py --help

# Executable version
./FFmpegMiniApp --help
```

## 🎯 Common Tasks

### Get Video Info
```bash
python3 src/mini_ffmpeg.py info video.mp4
```

### Convert Video
```bash
python3 src/mini_ffmpeg.py convert input.mov output.mp4
```

### Trim Video
```bash
python3 src/mini_ffmpeg.py trim input.mp4 output.mp4 --start 10 --duration 30
```

### Extract Audio
```bash
python3 src/mini_ffmpeg.py extract-audio video.mp4 audio.mp3
```

### Split Video
```bash
python3 src/mini_ffmpeg.py split video.mp4 part-%03d.mp4 --time 60
```

## 🔨 Build Executable

```bash
# Build for current platform
python3 scripts/build.py

# Result: dist/FFmpegMiniApp
```

## 📚 Next Steps

- Read the [Complete Usage Guide](USAGE_GUIDE.md)
- Check out [Examples](examples/)
- View [Project Structure](PROJECT_STRUCTURE.md)

## 🆘 Need Help?

- Check [Troubleshooting](USAGE_GUIDE.md#troubleshooting)
- Create an [Issue](https://github.com/yourusername/ffmpeg-mini-app/issues)
- Read the [Full Documentation](USAGE_GUIDE.md)

---

**Ready to go! Start processing your videos! 🎬**