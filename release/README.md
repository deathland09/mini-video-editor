# 🎬 FFmpeg Mini App

A lightweight, cross-platform FFmpeg wrapper that provides essential video/audio processing capabilities through a simple command-line interface.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Cross Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/yourusername/ffmpeg-mini-app)

## ✨ Features

- 🎯 **Simple CLI** - Easy-to-use command-line interface
- 🌍 **Cross-Platform** - Works on Windows, macOS, and Linux
- 📦 **Standalone Executables** - No Python installation required for end users
- ⚡ **Fast Processing** - Direct FFmpeg integration with stream copying
- 🔧 **Essential Operations** - All common video/audio tasks covered

## 🚀 Quick Start

### Option 1: Python CLI (For Developers)

```bash
# Clone the repository
git clone https://github.com/deathland09/mini-video-editor
cd ffmpeg-mini-app

# Install dependencies
pip install -r requirements.txt

# Use the CLI
python3 src/main.py --help
```

### Option 2: Standalone Executable (For End Users)

```bash
# Download the executable for your platform
# Windows: FFmpegMiniApp.exe
# macOS: FFmpegMiniApp
# Linux: FFmpegMiniApp

# Make executable (Unix systems)
chmod +x FFmpegMiniApp

# Run
./FFmpegMiniApp --help
```

## 📋 Prerequisites

- **FFmpeg** must be installed on your system
- **Python 3.7+** (for CLI usage or building executables)

### Installing FFmpeg

#### macOS
```bash
brew install ffmpeg
```

#### Windows
Download from [FFmpeg.org](https://ffmpeg.org/download.html) and add to PATH

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Linux (RedHat/CentOS)
```bash
sudo yum install ffmpeg
```

## 🎯 Usage

### Get File Information
```bash
# Python CLI
python3 src/main.py info video.mp4

# Executable
./FFmpegMiniApp info video.mp4
```

### Convert Video/Audio
```bash
# Convert MOV to MP4
python3 src/main.py convert input.mov output.mp4

# Convert with specific codecs
python3 src/main.py convert input.avi output.mp4 --vcodec libx264 --acodec aac
```

### Trim/Cut Video
```bash
# Trim from 10 seconds, duration 30 seconds
python3 src/main.py trim input.mp4 output.mp4 --start 10 --duration 30

# Trim with stream copy (faster, no re-encoding)
python3 src/main.py trim input.mp4 output.mp4 --start 10 --duration 30 --copy
```

### Extract Audio
```bash
# Extract audio to MP3
python3 src/main.py extract-audio video.mp4 audio.mp3

# Extract with custom bitrate
python3 src/main.py extract-audio video.mp4 audio.mp3 --bitrate 320k
```

### Split Video
```bash
# Split into 60-second segments
python3 src/main.py split video.mp4 part-%03d.mp4 --time 60

# Split into 30-second segments
python3 src/main.py split long_video.mp4 segment-%03d.mp4 --time 30
```

## 🔨 Building Executables

### Simple Build (Recommended)
```bash
# Build for current platform
python3 build.py
```

### Professional Build
```bash
# Advanced build with optimizations
python3 scripts/build_pro.py
```

### Manual Build
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --name FFmpegMiniApp --console src/main.py
```

### Cross-Platform Building

To create executables for different platforms:

1. **Windows**: Build on Windows machine
2. **macOS**: Build on macOS machine  
3. **Linux**: Build on Linux machine

The executable will be created in the `dist/` directory.

## 📁 Project Structure

```
ffmpeg-mini-app/
├── src/                          # Source code
│   ├── __init__.py               # Package initialization
│   └── main.py                   # Main CLI application
├── scripts/                       # Build and utility scripts
│   ├── build.py                  # Basic build script
│   └── build_pro.py              # Professional build system
├── docs/                         # Documentation
│   ├── README.md                 # Documentation index
│   ├── USAGE_GUIDE.md            # Complete usage guide
│   ├── QUICK_START.md            # Quick start guide
│   ├── BUILD_SYSTEM.md           # Build system guide
│   ├── PROJECT_STRUCTURE.md     # Structure documentation
│   └── examples/                 # Usage examples
│       ├── SOCIAL_MEDIA.md       # Social media examples
│       └── BATCH_PROCESSING.md   # Batch processing examples
├── __test__/                     # Test files (git ignored)
│   ├── test_drag_drop.py         # Drag-and-drop tests
│   ├── test_setup.py             # Environment tests
│   ├── demo_split.py             # Demo scripts
│   └── README.md                 # Test documentation
├── .github/workflows/             # CI/CD automation
│   └── build.yml                 # Automated builds
├── README.md                     # Main documentation
├── LICENSE                       # MIT License
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
└── .gitignore                    # Git ignore rules
```

## 📚 Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running in 5 minutes
- **[Complete Usage Guide](docs/USAGE_GUIDE.md)** - Comprehensive documentation
- **[Build System](docs/BUILD_SYSTEM.md)** - Professional build system
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Repository organization
- **[Examples](docs/examples/)** - Practical usage examples
  - [Social Media Examples](docs/examples/SOCIAL_MEDIA.md) - Instagram, TikTok, YouTube
  - [Batch Processing](docs/examples/BATCH_PROCESSING.md) - Process multiple files

## 🎬 Examples

### Video Processing Workflow
```bash
# 1. Get video information
python3 src/main.py info input.mov

# 2. Convert to MP4
python3 src/main.py convert input.mov output.mp4

# 3. Trim to 2 minutes
python3 src/main.py trim output.mp4 trimmed.mp4 --start 0 --duration 120

# 4. Extract audio
python3 src/main.py extract-audio trimmed.mp4 audio.mp3

# 5. Split into segments
python3 src/main.py split trimmed.mp4 part-%03d.mp4 --time 30
```

### Batch Processing
```bash
# Process multiple files
for file in *.mov; do
    python3 src/main.py convert "$file" "${file%.mov}.mp4"
done
```

## 🔧 Advanced Usage

### Custom Codecs
```bash
# Use specific video codec
python3 src/main.py convert input.mp4 output.mp4 --vcodec libx265

# Use specific audio codec
python3 src/main.py convert input.mp4 output.mp4 --acodec libmp3lame
```

### Time Format Support
```bash
# Use HH:MM:SS format
python3 src/main.py trim video.mp4 output.mp4 --start 00:01:30 --duration 00:02:00

# Use seconds
python3 src/main.py trim video.mp4 output.mp4 --start 90 --duration 120
```

## 📦 Distribution

### For End Users
1. Download the executable for your platform
2. Install FFmpeg on your system
3. Run the executable - no Python needed!

### For Developers
1. Clone the repository
2. Install Python dependencies
3. Use the CLI directly or build executables

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FFmpeg](https://ffmpeg.org/) - The powerful multimedia framework
- [PyInstaller](https://pyinstaller.org/) - For creating standalone executables

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/ffmpeg-mini-app/issues) page
2. Create a new issue with detailed information
3. Include your operating system and FFmpeg version

## 🎯 Roadmap

- [ ] GUI version with drag-and-drop
- [ ] Batch processing interface
- [ ] Video compression presets
- [ ] Audio normalization
- [ ] Subtitle extraction
- [ ] Video thumbnail generation

---

**Made with ❤️ for the open-source community**
