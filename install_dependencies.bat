@echo off
echo FFmpeg Mini App - Dependency Installer
echo ======================================

echo Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo FFmpeg not found!
    echo.
    echo Would you like to install FFmpeg automatically? (y/n)
    set /p response=
    if /i "%response%"=="y" (
        echo.
        echo Installing FFmpeg using Chocolatey...
        echo If Chocolatey is not installed, please install it first:
        echo   https://chocolatey.org/install
        echo.
        choco install ffmpeg -y
        if %errorlevel% neq 0 (
            echo.
            echo Failed to install FFmpeg automatically.
            echo Please install FFmpeg manually:
            echo   1. Download from: https://ffmpeg.org/download.html
            echo   2. Extract to C:\ffmpeg
            echo   3. Add C:\ffmpeg\bin to your PATH
            echo.
            pause
            exit /b 1
        )
        echo FFmpeg installed successfully!
        echo.
        echo You can now run the FFmpeg Mini App!
    ) else (
        echo FFmpeg is required to run this application.
        echo Please install FFmpeg manually and run this installer again.
        echo Download from: https://ffmpeg.org/download.html
        pause
        exit /b 1
    )
) else (
    echo FFmpeg found! Installation complete.
    echo.
    echo You can now run the FFmpeg Mini App!
)

echo.
pause
