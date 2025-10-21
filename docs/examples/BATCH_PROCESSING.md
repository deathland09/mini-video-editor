# 🔄 Batch Processing Examples

Examples for processing multiple files efficiently.

## Convert All Videos to MP4
```bash
#!/bin/bash
# Convert all MOV files to MP4

for file in *.mov; do
    if [ -f "$file" ]; then
        echo "Converting $file..."
        python3 src/mini_ffmpeg.py convert "$file" "${file%.mov}.mp4"
    fi
done

echo "All MOV files converted to MP4!"
```

## Extract Audio from All Videos
```bash
#!/bin/bash
# Extract audio from all video files

for file in *.mp4 *.mov *.avi; do
    if [ -f "$file" ]; then
        echo "Extracting audio from $file..."
        python3 src/mini_ffmpeg.py extract-audio "$file" "${file%.*}.mp3"
    fi
done

echo "Audio extracted from all videos!"
```

## Split All Long Videos
```bash
#!/bin/bash
# Split all videos longer than 5 minutes into 2-minute segments

for file in *.mp4 *.mov *.avi; do
    if [ -f "$file" ]; then
        echo "Processing $file..."
        
        # Get duration (this is a simplified example)
        # In practice, you'd need to parse the info output
        python3 src/mini_ffmpeg.py split "$file" "${file%.*}_part_%03d.mp4" --time 120
    fi
done

echo "All long videos split into 2-minute segments!"
```

## Process by File Size
```bash
#!/bin/bash
# Process files larger than 100MB

for file in *.mp4 *.mov *.avi; do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        if [ "$size" -gt 104857600 ]; then  # 100MB in bytes
            echo "Processing large file: $file ($(($size / 1048576))MB)"
            python3 src/mini_ffmpeg.py split "$file" "${file%.*}_part_%03d.mp4" --time 300
        fi
    fi
done
```

## Convert and Compress
```bash
#!/bin/bash
# Convert and compress videos

for file in *.mov *.avi; do
    if [ -f "$file" ]; then
        echo "Converting and compressing $file..."
        python3 src/mini_ffmpeg.py convert "$file" "${file%.*}.mp4" --vcodec libx264 --acodec aac
    fi
done

echo "All videos converted and compressed!"
```

## Create Thumbnails (using FFmpeg directly)
```bash
#!/bin/bash
# Create thumbnails for all videos

for file in *.mp4 *.mov *.avi; do
    if [ -f "$file" ]; then
        echo "Creating thumbnail for $file..."
        ffmpeg -i "$file" -ss 00:00:01 -vframes 1 "${file%.*}_thumb.jpg"
    fi
done

echo "Thumbnails created for all videos!"
```

## Organize by Date
```bash
#!/bin/bash
# Process files and organize by creation date

for file in *.mp4 *.mov *.avi; do
    if [ -f "$file" ]; then
        # Get creation date
        date=$(stat -f "%Sm" -t "%Y-%m-%d" "$file" 2>/dev/null || stat -c "%y" "$file" | cut -d' ' -f1)
        
        # Create directory if it doesn't exist
        mkdir -p "processed/$date"
        
        # Process file
        echo "Processing $file for date $date..."
        python3 src/mini_ffmpeg.py convert "$file" "processed/$date/${file%.*}.mp4"
    fi
done

echo "Files organized by date!"
```

## Quality Control
```bash
#!/bin/bash
# Check all videos and report issues

echo "Checking video files..."

for file in *.mp4 *.mov *.avi; do
    if [ -f "$file" ]; then
        echo "Checking $file..."
        
        # Get file info
        info=$(python3 src/mini_ffmpeg.py info "$file" 2>/dev/null)
        
        if [ $? -eq 0 ]; then
            echo "✅ $file - OK"
        else
            echo "❌ $file - Issues detected"
        fi
    fi
done

echo "Quality check complete!"
```

## Backup Before Processing
```bash
#!/bin/bash
# Create backup before batch processing

backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"

echo "Creating backup in $backup_dir..."

# Copy all video files
cp *.mp4 *.mov *.avi "$backup_dir/" 2>/dev/null

echo "Backup created. Starting batch processing..."

# Your batch processing commands here
for file in *.mp4 *.mov *.avi; do
    if [ -f "$file" ]; then
        echo "Processing $file..."
        python3 src/mini_ffmpeg.py convert "$file" "${file%.*}_processed.mp4"
    fi
done

echo "Batch processing complete!"
```

## Progress Tracking
```bash
#!/bin/bash
# Process files with progress tracking

files=($(ls *.mp4 *.mov *.avi 2>/dev/null))
total=${#files[@]}
current=0

for file in "${files[@]}"; do
    current=$((current + 1))
    echo "[$current/$total] Processing $file..."
    
    python3 src/mini_ffmpeg.py convert "$file" "${file%.*}_processed.mp4"
    
    echo "Progress: $((current * 100 / total))%"
done

echo "All files processed!"
```
