# Split Video Feature - User Guide

## Overview

The **Split Video** feature allows you to divide a single video file into multiple smaller segments. This is useful for:

- Sharing large videos on platforms with size limits
- Creating video chapters or parts
- Processing videos in smaller chunks
- Uploading videos with better reliability

## Available in All Versions

✅ **CLI Version** (`ffmpeg_cli.py`) - Option 7  
✅ **Simple GUI** (`ffmpeg_app_simple.py`) - "🔪 Split Video" button  
✅ **Full GUI** (`ffmpeg_app.py`) - "Split Video" button

---

## Three Splitting Methods

### 1. Split by Time Duration ⏱️

Split your video into segments of equal duration.

**CLI Example:**
```
Select operation: 7
Select split method: 1
Enter segment duration: 60
```
This creates segments of 60 seconds each.

**Input formats:**
- Seconds: `60`, `120`, `300`
- Time format: `00:01:00`, `00:02:00`, `00:05:00`

**Use case:** Create 1-minute clips from a long video

---

### 2. Split by File Size 📦

Split your video into segments of approximately equal file size.

**CLI Example:**
```
Select operation: 7
Select split method: 2
Enter target size: 10
```
This creates segments of approximately 10 MB each.

**Input format:**
- Size in MB: `10`, `25`, `50`, `100`

**Use case:** Split video to meet email attachment limits (e.g., 25 MB)

**Note:** Sizes are approximate due to video encoding. FFmpeg uses the `-c copy` codec which doesn't re-encode, so splits happen at keyframes.

---

### 3. Split by Number of Parts 🔢

Split your video into a specific number of equal parts.

**CLI Example:**
```
Select operation: 7
Select split method: 3
Enter number of parts: 4
```
This creates exactly 4 equal parts.

**Input format:**
- Number (must be 2 or more): `2`, `3`, `4`, `5`

**Use case:** Divide a 10-minute video into 4 equal 2.5-minute parts

**How it works:**
1. The app gets the total video duration using ffprobe
2. Calculates segment duration: `total_duration / num_parts`
3. Splits the video into equal time segments

---

## Output

### File Organization

Split videos are saved in a new folder:
```
original_video.mp4
original_video_split/
  ├── original_video_part000.mp4
  ├── original_video_part001.mp4
  ├── original_video_part002.mp4
  └── original_video_part003.mp4
```

### File Naming

- Pattern: `{original_name}_part{number}.mp4`
- Numbers are zero-padded (001, 002, 003...)
- Always outputs as MP4 format

---

## CLI Version Usage

### Step-by-Step Example

```bash
$ python3 ffmpeg_cli.py video.mp4

Select operation (0-8): 7

────────────────────────────────────────────────────────────
Split Video
────────────────────────────────────────────────────────────

Split by:
  1. Time (equal duration segments)
  2. Size (approximate file size)
  3. Number of parts

Select split method (1-3): 1

Enter segment duration (HH:MM:SS or seconds): 120

ℹ Splitting video by time...
  Input: video.mp4
  Segment duration: 120
  Output folder: /path/to/video_split

✓ Video split complete!
✓ Created 5 parts
✓ Total size: 45.23 MB
✓ Saved to: /path/to/video_split

Parts created:
  1. video_part000.mp4 (8.54 MB)
  2. video_part001.mp4 (9.12 MB)
  3. video_part002.mp4 (9.45 MB)
  4. video_part003.mp4 (9.01 MB)
  5. video_part004.mp4 (9.11 MB)
```

---

## GUI Version Usage

### Simple GUI (`ffmpeg_app_simple.py`)

1. **Load your video** using "Browse File"
2. **Click** "🔪 Split Video" button
3. **Select split method** via radio buttons:
   - ○ By Time (equal duration segments)
   - ○ By Size (approximate MB per segment)
   - ○ By Number of Parts (equal parts)
4. **Enter value** in the input field
5. **Click** "Split Video" button
6. **Wait** for processing (progress bar shows activity)
7. **See results** in success popup

### Full GUI (`ffmpeg_app.py`)

Same as Simple GUI, with the added benefit of drag-and-drop file selection.

---

## Real-World Examples

### Example 1: Email-Friendly Segments
**Goal:** Split a 100 MB video for email (25 MB limit)

```
Method: By Size
Value: 20
Result: 5 segments, each ~20 MB
```

### Example 2: Social Media Stories
**Goal:** Create 15-second clips for Instagram Stories

```
Method: By Time
Value: 15
Result: Multiple 15-second clips
```

### Example 3: Video Series
**Goal:** Divide a 30-minute tutorial into 5 equal parts

```
Method: By Number of Parts
Value: 5
Result: 5 parts, each 6 minutes
```

### Example 4: Chapter Breaks
**Goal:** Split at 5-minute intervals for YouTube chapters

```
Method: By Time
Value: 300 (or 00:05:00)
Result: 5-minute segments
```

---

## Technical Details

### FFmpeg Commands Used

**Split by Time:**
```bash
ffmpeg -i input.mp4 -c copy -map 0 -segment_time 60 \
  -f segment -reset_timestamps 1 output_part%03d.mp4
```

**Split by Size:**
```bash
ffmpeg -i input.mp4 -c copy -map 0 -f segment \
  -segment_size 10485760 -reset_timestamps 1 output_part%03d.mp4
```

**Split by Parts (calculated):**
```bash
# First: Get duration with ffprobe
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 input.mp4

# Then: Split with calculated segment_time
ffmpeg -i input.mp4 -c copy -map 0 -segment_time <calculated> \
  -f segment -reset_timestamps 1 output_part%03d.mp4
```

### Key FFmpeg Options

- `-c copy`: Copy codec (no re-encoding, fast and lossless)
- `-map 0`: Include all streams (video, audio, subtitles)
- `-f segment`: Use segment muxer
- `-segment_time`: Duration per segment
- `-segment_size`: Size per segment in bytes
- `-reset_timestamps 1`: Reset timestamps for each segment

---

## Tips & Best Practices

### ✅ Do's

- **Use "By Size"** for upload limits (email, messaging apps)
- **Use "By Time"** for consistent viewing experience
- **Use "By Parts"** when you need exact number of segments
- **Keep originals** - the app creates new files, doesn't modify originals
- **Test first** with a small segment to verify output

### ⚠️ Don'ts

- **Don't split very small videos** (< 5 seconds) - may not work as expected
- **Don't use tiny segments** (< 2 seconds) - may cause issues
- **Don't expect exact sizes** with "By Size" - they're approximate
- **Don't interrupt** the process - let FFmpeg finish

---

## Troubleshooting

### Issue: "Could not get video duration"
**Solution:** Make sure ffprobe is installed (comes with FFmpeg)

### Issue: Segments are not exact size
**Solution:** This is normal with `-c copy` (no re-encoding). Split happens at keyframes. For exact sizes, you'd need to re-encode (slower).

### Issue: Some segments are slightly different lengths
**Solution:** This is expected, especially with "By Parts" - last segment may be shorter.

### Issue: No audio in segments
**Solution:** Check original video has audio. Use `-map 0` flag (already included).

### Issue: Split takes a long time
**Solution:** Splitting with `-c copy` should be fast. If slow, check disk space and system resources.

---

## Advanced: Custom Splits

For more control, you can edit the split commands in the source code:

### Add Custom Codec
Change `-c copy` to `-c:v libx264 -crf 23` for re-encoding

### Adjust Split Points
Modify `-segment_time` calculation for custom timing

### Change Output Format
Change `%03d` to `%04d` for more segments (e.g., over 999)

---

## Summary

| Method | Input | Best For | Speed |
|--------|-------|----------|-------|
| **By Time** | Seconds or HH:MM:SS | Consistent segments | ⚡ Fast |
| **By Size** | MB per segment | Size limits | ⚡ Fast |
| **By Parts** | Number of parts | Fixed number of files | ⚡ Fast |

All methods use `-c copy` for fast, lossless splitting without re-encoding!

---

**Ready to split?** Try it now:
```bash
python3 ffmpeg_cli.py your_video.mp4
# Select option 7 for Split Video
```

Or use the GUI for a visual interface! 🎬



