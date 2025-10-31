@echo off
setlocal enableextensions enabledelayedexpansion

echo FFmpeg Mini App - Dependency Installer
echo ======================================
echo.

echo Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo FFmpeg found! Installation complete.
    echo.
    echo You can now run the FFmpeg Mini App!
    exit /b 0
)

echo FFmpeg not found.
echo Checking for Chocolatey...
choco -v >nul 2>&1
if %errorlevel% equ 0 (
    echo Chocolatey detected. Installing FFmpeg non-interactively...
    choco install ffmpeg -y >nul 2>&1
    if %errorlevel% equ 0 (
        echo FFmpeg installed successfully via Chocolatey.
        echo Verifying installation...
        ffmpeg -version >nul 2>&1
        if %errorlevel% equ 0 (
            echo FFmpeg is now available. You can run the FFmpeg Mini App.
            exit /b 0
        ) else (
            echo Verification failed. Please ensure FFmpeg is on your PATH.
            exit /b 1
        )
    ) else (
        echo Chocolatey install failed.
        echo Please install FFmpeg manually:
        echo   1. Download from: https://ffmpeg.org/download.html
        echo   2. Extract to C:\ffmpeg
        echo   3. Add C:\ffmpeg\bin to your PATH
        exit /b 1
    )
) else (
    echo Chocolatey not found.
    echo Please install FFmpeg manually:
    echo   1. Download from: https://ffmpeg.org/download.html
    echo   2. Extract to C:\ffmpeg
    echo   3. Add C:\ffmpeg\bin to your PATH
    exit /b 1
)

endlocal
