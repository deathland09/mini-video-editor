# What's New - Split Video Feature! 🎉

## ⭐ New Feature Added: Split Video

I've added a powerful **Split Video** feature to all three versions of the FFmpeg Mini App!

---

## 🆕 What's New

### Split Video Feature
Split your videos into multiple smaller segments using three different methods:

1. **By Time** ⏱️
   - Split into segments of equal duration
   - Example: Split a 10-minute video into 2-minute chunks
   - Input: Seconds (60) or HH:MM:SS (00:01:00)

2. **By Size** 📦
   - Split into segments of approximately equal file size
   - Example: Create 25 MB chunks for email attachments
   - Input: Size in MB (25, 50, 100)

3. **By Number of Parts** 🔢
   - Split into a specific number of equal parts
   - Example: Divide a video into exactly 4 parts
   - Input: Number of parts (2, 3, 4, 5, etc.)

---

## 📍 Where to Find It

### CLI Version (`ffmpeg_cli.py`)
- **Option 7** in the main menu
- "Select Different File" moved to **Option 8**

```
Select operation (0-8): 7
```

### Simple GUI (`ffmpeg_app_simple.py`)
- New **"🔪 Split Video"** button (orange color)
- Located in the operations grid

### Full GUI (`ffmpeg_app.py`)
- New **"Split Video"** button
- Same functionality as simple GUI

---

## 🎯 Use Cases

### Email Attachments
Split large videos into 25 MB chunks for email:
```
Method: By Size
Value: 25
```

### Social Media
Create 15-second clips for Instagram Stories:
```
Method: By Time
Value: 15
```

### Video Series
Divide a tutorial into equal parts:
```
Method: By Number of Parts
Value: 5
```

### Platform Limits
Meet upload size restrictions:
```
Method: By Size
Value: 50
```

---

## 📁 Output

Split videos are organized in a new folder:

```
original_video.mp4
original_video_split/
  ├── original_video_part000.mp4
  ├── original_video_part001.mp4
  ├── original_video_part002.mp4
  └── original_video_part003.mp4
```

---

## ⚡ Features

✅ **Fast** - Uses FFmpeg's segment muxer with `-c copy` (no re-encoding)  
✅ **Lossless** - No quality loss (copies streams directly)  
✅ **Smart** - Automatically calculates segment durations  
✅ **Organized** - Creates separate folder for segments  
✅ **Informative** - Shows all created parts with sizes  

---

## 🚀 Try It Now!

### CLI Version:
```bash
python3 ffmpeg_cli.py onboarding2.mp4
# Select option 7
# Choose split method
# Enter value
```

### GUI Version:
```bash
python3 ffmpeg_app_simple.py
# Load file
# Click "🔪 Split Video"
# Select method and enter value
```

---

## 📚 Complete Documentation

For detailed instructions and examples, see:
- **SPLIT_VIDEO_GUIDE.md** - Complete guide with examples
- **START_HERE.md** - Updated quick start
- **FINAL_README.md** - Updated feature list

---

## 🔧 Technical Details

### FFmpeg Commands

**By Time:**
```bash
ffmpeg -i input.mp4 -c copy -map 0 -segment_time 60 -f segment -reset_timestamps 1 output_%03d.mp4
```

**By Size:**
```bash
ffmpeg -i input.mp4 -c copy -map 0 -f segment -segment_size 10485760 -reset_timestamps 1 output_%03d.mp4
```

**By Parts:**
```bash
# Calculate: duration / parts
ffmpeg -i input.mp4 -c copy -map 0 -segment_time <calculated> -f segment -reset_timestamps 1 output_%03d.mp4
```

---

## 📊 Updated Operation Counts

| Version | Operations | New Count |
|---------|------------|-----------|
| CLI | 6 → **7** | ✅ Added Split |
| Simple GUI | 6 → **7** | ✅ Added Split |
| Full GUI | 5 → **6** | ✅ Added Split |

---

## 💡 Examples

### Example 1: Split 100 MB video for email (25 MB limit)
```
Input: video.mp4 (100 MB)
Method: By Size
Value: 20

Output:
  video_split/
    ├── video_part000.mp4 (20 MB)
    ├── video_part001.mp4 (20 MB)
    ├── video_part002.mp4 (20 MB)
    ├── video_part003.mp4 (20 MB)
    └── video_part004.mp4 (20 MB)
```

### Example 2: Create 30-second clips
```
Input: long_video.mp4 (5 minutes)
Method: By Time
Value: 30

Output: 10 clips of 30 seconds each
```

### Example 3: Divide into 3 equal parts
```
Input: tutorial.mp4 (15 minutes)
Method: By Number of Parts
Value: 3

Output: 3 parts of 5 minutes each
```

---

## 🎉 Enjoy the New Feature!

All three versions have been updated with this powerful new capability. The split feature uses FFmpeg's native segment muxer for fast, lossless splitting without re-encoding.

**Ready to try it?**
```bash
python3 ffmpeg_cli.py
```

Happy splitting! 🎬✂️



