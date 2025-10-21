@echo off
REM Installation script for FFmpeg Mini App (Windows)

echo ======================================
echo FFmpeg Mini App - Installation Script
echo ======================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)

echo OK: Python found
python --version

REM Install dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo OK: Dependencies installed successfully

REM Check FFmpeg
echo.
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: FFmpeg is not installed or not in PATH!
    echo.
    echo Please install FFmpeg:
    echo   1. Download from https://ffmpeg.org/download.html
    echo   2. Extract to C:\ffmpeg
    echo   3. Add C:\ffmpeg\bin to your PATH
    echo.
) else (
    echo OK: FFmpeg found
    ffmpeg -version 2>&1 | findstr "ffmpeg version"
)

echo.
echo ======================================
echo Installation complete!
echo ======================================
echo.
echo To run the application:
echo   python ffmpeg_app.py
echo.
pause

