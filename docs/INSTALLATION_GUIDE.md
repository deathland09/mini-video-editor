# 🎬 FFmpeg Mini App - Installation Guide

## 📋 Overview

The FFmpeg Mini App is a **standalone executable** that doesn't require Python installation. However, it does require **FFmpeg** to be installed on your system for video processing.

## 🚀 Quick Installation

### Option 1: Automatic Installation (Recommended)

The app includes automatic dependency installation:

#### **macOS/Linux:**
```bash
# Run the installer
./install.sh

# Or install dependencies separately
./install_dependencies.sh
```

#### **Windows:**
```cmd
# Run the installer
install.bat

# Or install dependencies separately
install_dependencies.bat
```

### Option 2: Manual Installation

If automatic installation fails, you can install FFmpeg manually:

## 🖥️ Platform-Specific Installation

### **macOS**

#### Using Homebrew (Recommended):
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install FFmpeg
brew install ffmpeg
```

#### Using MacPorts:
```bash
sudo port install ffmpeg
```

### **Windows**

#### Using Chocolatey (Recommended):
```powershell
# Install Chocolatey (if not already installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install FFmpeg
choco install ffmpeg
```

#### Manual Installation:
1. Download FFmpeg from: https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your PATH environment variable

### **Linux**

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### CentOS/RHEL:
```bash
sudo yum install ffmpeg
# or for newer versions:
sudo dnf install ffmpeg
```

#### Fedora:
```bash
sudo dnf install ffmpeg
```

#### Arch Linux:
```bash
sudo pacman -S ffmpeg
```

#### OpenSUSE:
```bash
sudo zypper install ffmpeg
```

## 🔧 Verification

After installation, verify FFmpeg is working:

```bash
ffmpeg -version
```

You should see FFmpeg version information.

## 📦 App Installation

### **Download the App**

1. Download the latest release from the GitHub repository
2. Extract the archive to your desired location

### **Run the App**

#### **macOS/Linux:**
```bash
# Make executable
chmod +x FFmpegMiniApp

# Run the app
./FFmpegMiniApp

# Or with a specific file
./FFmpegMiniApp video.mp4
```

#### **Windows:**
```cmd
# Run the app
FFmpegMiniApp.exe

# Or with a specific file
FFmpegMiniApp.exe video.mp4
```

## 🎯 Features

Once installed, the app provides:

- ✅ **Convert videos** (MP4, MP3, etc.)
- ✅ **Extract audio** from videos
- ✅ **Compress videos** for smaller file sizes
- ✅ **Cut/trim videos** to specific segments
- ✅ **Split videos** by time, size, or number of parts
- ✅ **Fix broken/corrupted videos** (NEW!)
- ✅ **Drag-and-drop support** for easy file selection
- ✅ **Cross-platform** (Windows, macOS, Linux)

## 🆘 Troubleshooting

### **FFmpeg Not Found Error**

If you get "FFmpeg not found" error:

1. **Check installation:**
   ```bash
   ffmpeg -version
   ```

2. **Verify PATH:**
   - Make sure FFmpeg is in your system PATH
   - Restart your terminal/command prompt

3. **Reinstall FFmpeg:**
   - Use the automatic installer: `./install_dependencies.sh` (Linux/macOS) or `install_dependencies.bat` (Windows)
   - Or follow the manual installation steps above

### **Permission Denied (Linux/macOS)**

If you get permission errors:

```bash
# Make the app executable
chmod +x FFmpegMiniApp

# Make the installer executable
chmod +x install.sh
chmod +x install_dependencies.sh
```

### **Windows Defender Warning**

Windows might show a security warning for the executable:

1. Click "More info"
2. Click "Run anyway"
3. Or add the app to Windows Defender exclusions

## 📚 Additional Resources

- **FFmpeg Documentation:** https://ffmpeg.org/documentation.html
- **Homebrew:** https://brew.sh/
- **Chocolatey:** https://chocolatey.org/
- **GitHub Repository:** [Your Repository URL]

## 🎉 Ready to Use!

Once FFmpeg is installed, you can start using the FFmpeg Mini App immediately. The app will guide you through all available operations with an interactive menu.

---

**Need help?** Check the [Usage Guide](USAGE_GUIDE.md) or open an issue on GitHub.
