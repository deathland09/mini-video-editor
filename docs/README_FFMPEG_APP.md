# FFmpeg Mini Application

A cross-platform GUI application built with Python3 for basic FFmpeg operations.

## Features

✅ **Cross-Platform**: Works on Windows, macOS, and Linux  
✅ **Auto-Detection**: Automatically detects OS and checks for FFmpeg installation  
✅ **Drag & Drop**: Drag video/audio files directly into the application  
✅ **File Browser**: Alternative file selection through browse button  
✅ **Multiple Operations**:
  - Get file information
  - Convert to MP4
  - Convert to MP3  
  - Extract audio from video
  - Compress video files

## Prerequisites

1. **Python 3.7 or higher**
   ```bash
   python3 --version
   ```

2. **FFmpeg installed on your system**
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   
   **Windows:**
   - Download from: https://ffmpeg.org/download.html
   - Add to PATH or place in `C:\ffmpeg\bin\`

## Installation

1. **Install required Python package:**
   ```bash
   pip install tkinterdnd2
   ```
   
   Or use the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```bash
   python3 ffmpeg_app.py
   ```
   
   Or make it executable (macOS/Linux):
   ```bash
   chmod +x ffmpeg_app.py
   ./ffmpeg_app.py
   ```

2. **Using the application:**
   - The app will automatically check if FFmpeg is installed
   - Drag and drop a video/audio file into the blue drop zone, OR
   - Click "Browse File" to select a file
   - Choose an operation from the available buttons
   - Processed files will be saved in the same directory as the source file

## Operations Explained

- **Get Info**: Display detailed information about the media file
- **Convert to MP4**: Convert any video format to MP4
- **Convert to MP3**: Convert any audio/video file to MP3 audio
- **Extract Audio**: Extract audio track from video as MP3
- **Compress Video**: Compress video file to reduce size (using H.264)

## Supported File Formats

**Video:** MP4, AVI, MKV, MOV, WMV, FLV, WebM  
**Audio:** MP3, WAV, AAC, FLAC, OGG

## Troubleshooting

**"FFmpeg Not Found" error:**
- Make sure FFmpeg is installed
- On Windows, FFmpeg should be in PATH or in `C:\ffmpeg\bin\`
- Run `ffmpeg -version` in terminal to verify installation

**Drag and drop not working:**
- Make sure `tkinterdnd2` is installed: `pip install tkinterdnd2`
- You can still use the "Browse File" button as an alternative

**Operations fail:**
- Check that the input file is not corrupted
- Ensure you have write permissions in the output directory
- Check FFmpeg is properly installed

## Building Standalone Executable (Optional)

You can create a standalone executable using PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name "FFmpeg-App" ffmpeg_app.py
```

The executable will be in the `dist` folder.

## License

Free to use and modify.

## Notes

- Output files are saved with suffix: `_converted`, `_audio`, or `_compressed`
- Processing large files may take time - the progress bar will indicate activity
- The application runs FFmpeg commands in the background

