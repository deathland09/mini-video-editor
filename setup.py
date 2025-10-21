#!/usr/bin/env python3
"""
Setup script for FFmpeg Mini App
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ffmpeg-mini-app",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A lightweight, cross-platform FFmpeg wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ffmpeg-mini-app",
    packages=find_packages(),
    py_modules=["src.mini_ffmpeg"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ffmpeg-mini=src.mini_ffmpeg:main",
        ],
    },
    keywords="ffmpeg video audio cli cross-platform",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ffmpeg-mini-app/issues",
        "Source": "https://github.com/yourusername/ffmpeg-mini-app",
    },
)