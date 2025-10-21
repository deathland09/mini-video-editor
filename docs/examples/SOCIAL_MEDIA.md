# 📱 Social Media Examples

Examples for preparing videos for different social media platforms.

## Instagram Stories (15 seconds)
```bash
# Trim to 15 seconds
python3 src/mini_ffmpeg.py trim video.mp4 instagram_story.mp4 --start 0 --duration 15

# Split into 15-second clips
python3 src/mini_ffmpeg.py split video.mp4 story_%03d.mp4 --time 15
```

## Instagram Reels (30-90 seconds)
```bash
# Trim to 30 seconds
python3 src/mini_ffmpeg.py trim video.mp4 reel.mp4 --start 0 --duration 30

# Trim to 60 seconds
python3 src/mini_ffmpeg.py trim video.mp4 reel.mp4 --start 0 --duration 60
```

## TikTok (15-60 seconds)
```bash
# Trim to 30 seconds for TikTok
python3 src/mini_ffmpeg.py trim video.mp4 tiktok.mp4 --start 0 --duration 30

# Split into 30-second clips
python3 src/mini_ffmpeg.py split video.mp4 tiktok_%03d.mp4 --time 30
```

## YouTube Shorts (60 seconds)
```bash
# Trim to 60 seconds
python3 src/mini_ffmpeg.py trim video.mp4 youtube_short.mp4 --start 0 --duration 60

# Split into 60-second segments
python3 src/mini_ffmpeg.py split video.mp4 short_%03d.mp4 --time 60
```

## Twitter/X (2 minutes 20 seconds)
```bash
# Trim to 2:20
python3 src/mini_ffmpeg.py trim video.mp4 twitter.mp4 --start 0 --duration 140
```

## Facebook (3 minutes)
```bash
# Trim to 3 minutes
python3 src/mini_ffmpeg.py trim video.mp4 facebook.mp4 --start 0 --duration 180
```

## Batch Processing for Multiple Platforms
```bash
#!/bin/bash
# Process video for all platforms

input="original_video.mp4"

# Instagram Story (15s)
python3 src/mini_ffmpeg.py trim "$input" "instagram_story.mp4" --start 0 --duration 15

# Instagram Reel (30s)
python3 src/mini_ffmpeg.py trim "$input" "instagram_reel.mp4" --start 0 --duration 30

# TikTok (30s)
python3 src/mini_ffmpeg.py trim "$input" "tiktok.mp4" --start 0 --duration 30

# YouTube Short (60s)
python3 src/mini_ffmpeg.py trim "$input" "youtube_short.mp4" --start 0 --duration 60

# Twitter (2:20)
python3 src/mini_ffmpeg.py trim "$input" "twitter.mp4" --start 0 --duration 140

# Facebook (3:00)
python3 src/mini_ffmpeg.py trim "$input" "facebook.mp4" --start 0 --duration 180

echo "All social media versions created!"
```
