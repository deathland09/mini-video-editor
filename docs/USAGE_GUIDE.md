# 📖 FFmpeg Mini App - Complete Usage Guide

This comprehensive guide covers all aspects of using the FFmpeg Mini App.

## 🎯 Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Command Reference](#command-reference)
4. [Examples](#examples)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)
7. [Development](#development)

## 📦 Installation

### Prerequisites

- **FFmpeg** must be installed on your system
- **Python 3.7+** (for CLI usage or building executables)

### Installing FFmpeg

#### macOS
```bash
brew install ffmpeg
```

#### Windows
1. Download from [FFmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your PATH

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Linux (RedHat/CentOS)
```bash
sudo yum install ffmpeg
```

### Installation Methods

#### Method 1: Python Package
```bash
# Clone repository
git clone https://github.com/yourusername/ffmpeg-mini-app.git
cd ffmpeg-mini-app

# Install dependencies
pip install -r requirements.txt

# Use CLI
python3 src/mini_ffmpeg.py --help
```

#### Method 2: Standalone Executable
```bash
# Download executable for your platform
# Windows: FFmpegMiniApp.exe
# macOS: FFmpegMiniApp
# Linux: FFmpegMiniApp

# Make executable (Unix systems)
chmod +x FFmpegMiniApp

# Run
./FFmpegMiniApp --help
```

## 🚀 Basic Usage

### Command Structure
```bash
python3 src/mini_ffmpeg.py <command> [options] <input> [output]
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `info` | Show media information | `info video.mp4` |
| `convert` | Convert between formats | `convert input.mov output.mp4` |
| `trim` | Cut/trim video/audio | `trim input.mp4 output.mp4 --start 10 --duration 30` |
| `extract-audio` | Extract audio track | `extract-audio video.mp4 audio.mp3` |
| `split` | Split video into segments | `split video.mp4 part-%03d.mp4 --time 60` |

## 📋 Command Reference

### `info` - Get Media Information

Shows detailed information about media files.

```bash
python3 src/mini_ffmpeg.py info <file>
```

**Example:**
```bash
python3 src/mini_ffmpeg.py info video.mp4
```

**Output:**
```json
{
  "format": {
    "filename": "video.mp4",
    "duration": "120.5",
    "size": "10485760"
  },
  "streams": [
    {
      "codec_name": "h264",
      "codec_type": "video"
    }
  ]
}
```

### `convert` - Convert Media Files

Convert between different video/audio formats.

```bash
python3 src/mini_ffmpeg.py convert <input> <output> [--vcodec <codec>] [--acodec <codec>]
```

**Options:**
- `--vcodec <codec>` - Video codec (default: copy)
- `--acodec <codec>` - Audio codec (default: copy)

**Examples:**
```bash
# Convert MOV to MP4 (stream copy - fast)
python3 src/mini_ffmpeg.py convert input.mov output.mp4

# Convert with re-encoding
python3 src/mini_ffmpeg.py convert input.avi output.mp4 --vcodec libx264 --acodec aac

# Convert to different format
python3 src/mini_ffmpeg.py convert video.mp4 audio.mp3 --acodec mp3
```

### `trim` - Cut/Trim Media

Cut or trim video/audio files.

```bash
python3 src/mini_ffmpeg.py trim <input> <output> --start <time> --duration <time> [--copy]
```

**Options:**
- `--start <time>` - Start time (seconds or HH:MM:SS)
- `--duration <time>` - Duration (seconds or HH:MM:SS)
- `--copy` - Use stream copy (faster, no re-encoding)

**Examples:**
```bash
# Trim from 10 seconds, duration 30 seconds
python3 src/mini_ffmpeg.py trim input.mp4 output.mp4 --start 10 --duration 30

# Trim with stream copy (faster)
python3 src/mini_ffmpeg.py trim input.mp4 output.mp4 --start 10 --duration 30 --copy

# Trim using time format
python3 src/mini_ffmpeg.py trim input.mp4 output.mp4 --start 00:01:30 --duration 00:02:00
```

### `extract-audio` - Extract Audio

Extract audio track from video files.

```bash
python3 src/mini_ffmpeg.py extract-audio <input> <output> [--bitrate <rate>]
```

**Options:**
- `--bitrate <rate>` - Audio bitrate (default: 192k)

**Examples:**
```bash
# Extract audio to MP3
python3 src/mini_ffmpeg.py extract-audio video.mp4 audio.mp3

# Extract with custom bitrate
python3 src/mini_ffmpeg.py extract-audio video.mp4 audio.mp3 --bitrate 320k

# Extract to different format
python3 src/mini_ffmpeg.py extract-audio video.mp4 audio.wav
```

### `split` - Split Video

Split video into multiple segments.

```bash
python3 src/mini_ffmpeg.py split <input> <pattern> --time <seconds>
```

**Parameters:**
- `<pattern>` - Output pattern (e.g., `part-%03d.mp4`)
- `--time <seconds>` - Duration per segment in seconds

**Examples:**
```bash
# Split into 60-second segments
python3 src/mini_ffmpeg.py split video.mp4 part-%03d.mp4 --time 60

# Split into 30-second segments
python3 src/mini_ffmpeg.py split long_video.mp4 segment-%03d.mp4 --time 30

# Split into 2-minute segments
python3 src/mini_ffmpeg.py split video.mp4 chunk-%03d.mp4 --time 120
```

## 🎬 Examples

### Complete Video Processing Workflow

```bash
# 1. Get video information
python3 src/mini_ffmpeg.py info input.mov

# 2. Convert to MP4
python3 src/mini_ffmpeg.py convert input.mov output.mp4

# 3. Trim to 2 minutes
python3 src/mini_ffmpeg.py trim output.mp4 trimmed.mp4 --start 0 --duration 120

# 4. Extract audio
python3 src/mini_ffmpeg.py extract-audio trimmed.mp4 audio.mp3

# 5. Split into segments
python3 src/mini_ffmpeg.py split trimmed.mp4 part-%03d.mp4 --time 30
```

### Batch Processing

```bash
# Convert all MOV files to MP4
for file in *.mov; do
    python3 src/mini_ffmpeg.py convert "$file" "${file%.mov}.mp4"
done

# Extract audio from all videos
for file in *.mp4; do
    python3 src/mini_ffmpeg.py extract-audio "$file" "${file%.mp4}.mp3"
done
```

### Social Media Preparation

```bash
# Split long video into 60-second clips for Instagram
python3 src/mini_ffmpeg.py split tutorial.mp4 instagram_%03d.mp4 --time 60

# Trim to 30 seconds for TikTok
python3 src/mini_ffmpeg.py trim video.mp4 tiktok.mp4 --start 0 --duration 30
```

## 🔧 Advanced Usage

### Custom Codecs

```bash
# Use H.265 for better compression
python3 src/mini_ffmpeg.py convert input.mp4 output.mp4 --vcodec libx265

# Use specific audio codec
python3 src/mini_ffmpeg.py convert input.mp4 output.mp4 --acodec libmp3lame

# Convert to WebM
python3 src/mini_ffmpeg.py convert input.mp4 output.webm --vcodec libvpx --acodec libvorbis
```

### Time Format Support

```bash
# Use HH:MM:SS format
python3 src/mini_ffmpeg.py trim video.mp4 output.mp4 --start 00:01:30 --duration 00:02:00

# Use seconds
python3 src/mini_ffmpeg.py trim video.mp4 output.mp4 --start 90 --duration 120

# Mix formats
python3 src/mini_ffmpeg.py trim video.mp4 output.mp4 --start 00:01:30 --duration 60
```

### Output Patterns

```bash
# Numbered segments
python3 src/mini_ffmpeg.py split video.mp4 part-%03d.mp4 --time 60
# Creates: part-000.mp4, part-001.mp4, part-002.mp4

# Custom naming
python3 src/mini_ffmpeg.py split video.mp4 segment_%02d.mp4 --time 60
# Creates: segment_00.mp4, segment_01.mp4, segment_02.mp4
```

## 🔨 Building Executables

### Automatic Build
```bash
python3 scripts/build.py
```

### Manual Build
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --name FFmpegMiniApp --console src/mini_ffmpeg.py
```

### Cross-Platform Building

To create executables for different platforms:

1. **Windows**: Build on Windows machine
2. **macOS**: Build on macOS machine
3. **Linux**: Build on Linux machine

## 🧪 Testing

### Run Tests
```bash
cd __test__

# Test environment setup
python3 test_setup.py

# Test drag-and-drop functionality
python3 test_drag_drop.py

# Demo video splitting
python3 demo_split.py
```

## 🐛 Troubleshooting

### Common Issues

#### "FFmpeg not found"
```bash
# Check if FFmpeg is installed
ffmpeg -version

# Install FFmpeg
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: Download from ffmpeg.org
```

#### "File not found"
```bash
# Check file path
ls -la video.mp4

# Use absolute path
python3 src/mini_ffmpeg.py info /full/path/to/video.mp4
```

#### "Permission denied"
```bash
# Make executable (Unix systems)
chmod +x FFmpegMiniApp

# Check file permissions
ls -la FFmpegMiniApp
```

### Performance Tips

1. **Use stream copy** for faster operations:
   ```bash
   python3 src/mini_ffmpeg.py trim input.mp4 output.mp4 --start 10 --duration 30 --copy
   ```

2. **Split large files** for easier handling:
   ```bash
   python3 src/mini_ffmpeg.py split large_video.mp4 part-%03d.mp4 --time 300
   ```

3. **Convert to efficient formats**:
   ```bash
   python3 src/mini_ffmpeg.py convert input.avi output.mp4 --vcodec libx264
   ```

## 🚀 Development

### Project Structure
```
ffmpeg-mini-app/
├── src/                          # Source code
│   ├── __init__.py               # Package initialization
│   └── mini_ffmpeg.py            # Main CLI application
├── scripts/                       # Build scripts
│   └── build.py                  # Cross-platform builder
├── docs/                         # Documentation
├── __test__/                     # Test files
└── README.md                     # Main documentation
```

### Adding New Features

1. **Modify source code** in `src/mini_ffmpeg.py`
2. **Add tests** in `__test__/` directory
3. **Update documentation** in `docs/`
4. **Test build** with `python3 scripts/build.py`

### Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

---

**For more information, see the main [README.md](../README.md) file.**
