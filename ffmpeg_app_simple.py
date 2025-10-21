#!/usr/bin/env python3
"""
FFmpeg Mini Application (Simplified Version - No Drag & Drop)
A cross-platform GUI application for basic FFmpeg operations
Works with standard tkinter only - no additional dependencies required
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import platform
import subprocess
import os
import shutil
from pathlib import Path
import threading


class FFmpegApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FFmpeg Mini App")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Variables
        self.current_file = None
        self.ffmpeg_path = None
        self.os_name = platform.system()
        
        # Setup UI
        self.setup_ui()
        
        # Check FFmpeg on startup
        self.check_ffmpeg()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="FFmpeg Mini App", 
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # System Info Frame
        info_frame = tk.Frame(self.root, bg="#ecf0f1", height=60)
        info_frame.pack(fill=tk.X, side=tk.TOP, padx=10, pady=5)
        info_frame.pack_propagate(False)
        
        self.os_label = tk.Label(
            info_frame,
            text=f"OS: {self.os_name} ({platform.machine()})",
            font=("Arial", 10),
            bg="#ecf0f1",
            anchor="w"
        )
        self.os_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.ffmpeg_status_label = tk.Label(
            info_frame,
            text="FFmpeg: Checking...",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="orange",
            anchor="w"
        )
        self.ffmpeg_status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Main Content Area
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # File Selection Area
        selection_frame = tk.Frame(main_frame, bg="#3498db", relief=tk.RIDGE, bd=3)
        selection_frame.pack(fill=tk.X, pady=10, padx=10)
        
        select_label = tk.Label(
            selection_frame,
            text="📁 Select Video/Audio File",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white"
        )
        select_label.pack(pady=10)
        
        browse_btn = tk.Button(
            selection_frame,
            text="Browse File",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#3498db",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.browse_file
        )
        browse_btn.pack(pady=10)
        
        # File Info Frame
        self.file_info_frame = tk.Frame(main_frame, bg="#ecf0f1", relief=tk.SUNKEN, bd=2)
        self.file_info_frame.pack(fill=tk.X, pady=10, padx=10)
        
        self.file_info_label = tk.Label(
            self.file_info_frame,
            text="No file selected",
            font=("Arial", 10),
            bg="#ecf0f1",
            anchor="w",
            justify=tk.LEFT,
            wraplength=700
        )
        self.file_info_label.pack(padx=10, pady=10)
        
        # Operations Frame
        operations_frame = tk.LabelFrame(
            main_frame,
            text="Operations",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=15,
            pady=10
        )
        operations_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)
        
        # Operation buttons in grid
        operations = [
            ("📋 Get File Info", self.get_file_info, "#3498db"),
            ("🎬 Convert to MP4", lambda: self.convert_file("mp4"), "#9b59b6"),
            ("🎵 Convert to MP3", lambda: self.convert_file("mp3"), "#e74c3c"),
            ("🔊 Extract Audio", self.extract_audio, "#f39c12"),
            ("📦 Compress Video", self.compress_video, "#16a085"),
            ("✂️ Cut/Trim Video", self.cut_video, "#27ae60"),
            ("🔪 Split Video", self.split_video, "#e67e22"),
        ]
        
        row, col = 0, 0
        for text, command, color in operations:
            btn = tk.Button(
                operations_frame,
                text=text,
                font=("Arial", 10, "bold"),
                bg=color,
                fg="white",
                padx=20,
                pady=12,
                cursor="hand2",
                command=command,
                relief=tk.RAISED,
                bd=3
            )
            btn.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Configure grid columns to expand equally
        for i in range(3):
            operations_frame.columnconfigure(i, weight=1)
        
        # Progress Frame
        progress_frame = tk.Frame(main_frame, bg="white")
        progress_frame.pack(fill=tk.X, pady=5, padx=10)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Ready",
            font=("Arial", 10, "bold"),
            bg="white",
            anchor="w"
        )
        self.progress_label.pack(fill=tk.X, padx=5)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=100
        )
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
    def check_ffmpeg(self):
        """Check if FFmpeg is installed on the system"""
        try:
            # Try to find ffmpeg
            ffmpeg_cmd = "ffmpeg"
            if self.os_name == "Windows":
                # Check common Windows locations
                common_paths = [
                    "ffmpeg.exe",
                    "C:\\ffmpeg\\bin\\ffmpeg.exe",
                    "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
                ]
                for path in common_paths:
                    if shutil.which(path) or os.path.exists(path):
                        ffmpeg_cmd = path
                        break
            
            # Test ffmpeg
            result = subprocess.run(
                [ffmpeg_cmd, "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                # Extract version
                version_line = result.stdout.split('\n')[0]
                self.ffmpeg_path = ffmpeg_cmd
                self.ffmpeg_status_label.config(
                    text=f"FFmpeg: ✓ Installed ({version_line.split()[2]})",
                    fg="green"
                )
                return True
            else:
                self.show_ffmpeg_not_found()
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            self.show_ffmpeg_not_found()
            return False
    
    def show_ffmpeg_not_found(self):
        """Show FFmpeg not found warning"""
        self.ffmpeg_status_label.config(
            text="FFmpeg: ✗ Not Found",
            fg="red"
        )
        
        message = (
            "FFmpeg is not installed or not found in PATH.\n\n"
            "Please install FFmpeg:\n"
            "• Windows: Download from ffmpeg.org\n"
            "• macOS: brew install ffmpeg\n"
            "• Linux: sudo apt install ffmpeg (Ubuntu/Debian)\n"
            "           sudo yum install ffmpeg (RedHat/CentOS)"
        )
        
        messagebox.showwarning("FFmpeg Not Found", message)
    
    def browse_file(self):
        """Open file browser dialog"""
        file_path = filedialog.askopenfilename(
            title="Select Video/Audio File",
            filetypes=[
                ("All Media Files", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.mp3 *.wav *.aac *.flac *.ogg"),
                ("Video Files", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
                ("Audio Files", "*.mp3 *.wav *.aac *.flac *.ogg"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """Load and display file information"""
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found!")
            return
        
        self.current_file = file_path
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        
        info_text = f"📄 File: {file_name}\n📊 Size: {file_size:.2f} MB\n📁 Path: {file_path}"
        self.file_info_label.config(text=info_text)
        self.progress_label.config(text=f"✅ Loaded: {file_name}")
    
    def run_ffmpeg_command(self, command, success_message, output_file=None):
        """Run FFmpeg command in a separate thread"""
        if not self.ffmpeg_path:
            messagebox.showerror("Error", "FFmpeg is not available!")
            return
        
        if not self.current_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        def execute():
            try:
                self.progress_label.config(text="⏳ Processing...")
                self.progress_bar.start()
                
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True
                )
                
                self.progress_bar.stop()
                
                if result.returncode == 0:
                    self.progress_label.config(text=f"✅ {success_message}")
                    
                    msg = success_message
                    if output_file and os.path.exists(output_file):
                        file_size = os.path.getsize(output_file) / (1024 * 1024)
                        msg += f"\n\nOutput size: {file_size:.2f} MB"
                    
                    messagebox.showinfo("Success", msg)
                else:
                    error_msg = result.stderr or "Unknown error"
                    self.progress_label.config(text="❌ Error occurred")
                    messagebox.showerror("Error", f"FFmpeg error:\n{error_msg[:500]}")
            
            except Exception as e:
                self.progress_bar.stop()
                self.progress_label.config(text="❌ Error occurred")
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        
        thread = threading.Thread(target=execute, daemon=True)
        thread.start()
    
    def get_file_info(self):
        """Get detailed file information using ffprobe"""
        if not self.current_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        try:
            ffprobe_cmd = self.ffmpeg_path.replace("ffmpeg", "ffprobe")
            result = subprocess.run(
                [ffprobe_cmd, self.current_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 or result.stderr:
                # ffprobe outputs to stderr by default
                info_window = tk.Toplevel(self.root)
                info_window.title("File Information")
                info_window.geometry("700x500")
                
                text_widget = tk.Text(info_window, wrap=tk.WORD, font=("Courier", 9))
                text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                scrollbar = tk.Scrollbar(text_widget)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                text_widget.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=text_widget.yview)
                
                text_widget.insert(tk.END, result.stderr)
                text_widget.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", "Could not get file information")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
    
    def convert_file(self, output_format):
        """Convert file to specified format"""
        if not self.current_file:
            return
        
        input_path = Path(self.current_file)
        output_path = input_path.parent / f"{input_path.stem}_converted.{output_format}"
        
        command = [
            self.ffmpeg_path,
            "-i", self.current_file,
            "-y",  # Overwrite output file
            str(output_path)
        ]
        
        self.run_ffmpeg_command(
            command,
            f"File converted to {output_format.upper()}!\nSaved to: {output_path}",
            str(output_path)
        )
    
    def extract_audio(self):
        """Extract audio from video file"""
        if not self.current_file:
            return
        
        input_path = Path(self.current_file)
        output_path = input_path.parent / f"{input_path.stem}_audio.mp3"
        
        command = [
            self.ffmpeg_path,
            "-i", self.current_file,
            "-vn",  # No video
            "-acodec", "libmp3lame",
            "-ab", "192k",
            "-y",
            str(output_path)
        ]
        
        self.run_ffmpeg_command(
            command,
            f"Audio extracted!\nSaved to: {output_path}",
            str(output_path)
        )
    
    def compress_video(self):
        """Compress video file"""
        if not self.current_file:
            return
        
        input_path = Path(self.current_file)
        output_path = input_path.parent / f"{input_path.stem}_compressed.mp4"
        
        command = [
            self.ffmpeg_path,
            "-i", self.current_file,
            "-vcodec", "libx264",
            "-crf", "28",  # Compression level (18-28 is good, higher = more compression)
            "-y",
            str(output_path)
        ]
        
        self.run_ffmpeg_command(
            command,
            f"Video compressed!\nSaved to: {output_path}",
            str(output_path)
        )
    
    def cut_video(self):
        """Cut/trim video with user input for start and end times"""
        if not self.current_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        # Create dialog for time input
        dialog = tk.Toplevel(self.root)
        dialog.title("Cut/Trim Video")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Start time (HH:MM:SS or seconds):", font=("Arial", 10)).pack(pady=5)
        start_entry = tk.Entry(dialog, font=("Arial", 10))
        start_entry.pack(pady=5)
        start_entry.insert(0, "00:00:00")
        
        tk.Label(dialog, text="Duration (HH:MM:SS or seconds):", font=("Arial", 10)).pack(pady=5)
        duration_entry = tk.Entry(dialog, font=("Arial", 10))
        duration_entry.pack(pady=5)
        duration_entry.insert(0, "00:00:10")
        
        def execute_cut():
            start = start_entry.get()
            duration = duration_entry.get()
            
            if not start or not duration:
                messagebox.showerror("Error", "Please fill in both fields!")
                return
            
            input_path = Path(self.current_file)
            output_path = input_path.parent / f"{input_path.stem}_cut.mp4"
            
            command = [
                self.ffmpeg_path,
                "-i", self.current_file,
                "-ss", start,
                "-t", duration,
                "-c", "copy",
                "-y",
                str(output_path)
            ]
            
            dialog.destroy()
            self.run_ffmpeg_command(
                command,
                f"Video trimmed!\nSaved to: {output_path}",
                str(output_path)
            )
        
        tk.Button(
            dialog,
            text="Cut Video",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=8,
            command=execute_cut
        ).pack(pady=15)
    
    def split_video(self):
        """Split video with user input for method and parameters"""
        if not self.current_file:
            messagebox.showerror("Error", "Please select a file first!")
            return
        
        # Create dialog for split options
        dialog = tk.Toplevel(self.root)
        dialog.title("Split Video")
        dialog.geometry("450x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog, 
            text="Split Video Into Multiple Parts", 
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Split method selection
        split_method = tk.StringVar(value="time")
        
        tk.Label(dialog, text="Select split method:", font=("Arial", 10)).pack(pady=5)
        
        method_frame = tk.Frame(dialog)
        method_frame.pack(pady=5)
        
        tk.Radiobutton(
            method_frame,
            text="By Time (equal duration segments)",
            variable=split_method,
            value="time",
            font=("Arial", 10)
        ).pack(anchor="w")
        
        tk.Radiobutton(
            method_frame,
            text="By Size (approximate MB per segment)",
            variable=split_method,
            value="size",
            font=("Arial", 10)
        ).pack(anchor="w")
        
        tk.Radiobutton(
            method_frame,
            text="By Number of Parts (equal parts)",
            variable=split_method,
            value="parts",
            font=("Arial", 10)
        ).pack(anchor="w")
        
        # Input field
        input_frame = tk.Frame(dialog)
        input_frame.pack(pady=15)
        
        tk.Label(input_frame, text="Enter value:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        value_entry = tk.Entry(input_frame, font=("Arial", 10), width=20)
        value_entry.pack(side=tk.LEFT, padx=5)
        value_entry.insert(0, "60")
        
        help_label = tk.Label(
            dialog,
            text="Time: HH:MM:SS or seconds (e.g., 60 or 00:01:00)\nSize: MB per segment (e.g., 10)\nParts: Number of parts (e.g., 4)",
            font=("Arial", 9),
            fg="gray",
            justify="left"
        )
        help_label.pack(pady=5)
        
        def execute_split():
            method = split_method.get()
            value = value_entry.get().strip()
            
            if not value:
                messagebox.showerror("Error", "Please enter a value!")
                return
            
            input_path = Path(self.current_file)
            output_dir = input_path.parent / f"{input_path.stem}_split"
            output_dir.mkdir(exist_ok=True)
            output_pattern = output_dir / f"{input_path.stem}_part%03d.mp4"
            
            try:
                if method == "time":
                    # Split by time duration
                    command = [
                        self.ffmpeg_path,
                        "-i", self.current_file,
                        "-c", "copy",
                        "-map", "0",
                        "-segment_time", value,
                        "-f", "segment",
                        "-reset_timestamps", "1",
                        str(output_pattern)
                    ]
                    
                elif method == "size":
                    # Split by size
                    if not value.isdigit():
                        messagebox.showerror("Error", "Size must be a number!")
                        return
                    
                    size_bytes = int(value) * 1024 * 1024
                    command = [
                        self.ffmpeg_path,
                        "-i", self.current_file,
                        "-c", "copy",
                        "-map", "0",
                        "-f", "segment",
                        "-segment_size", str(size_bytes),
                        "-reset_timestamps", "1",
                        str(output_pattern)
                    ]
                    
                elif method == "parts":
                    # Split by number of parts
                    if not value.isdigit() or int(value) < 2:
                        messagebox.showerror("Error", "Number of parts must be 2 or more!")
                        return
                    
                    # Get video duration first
                    ffprobe = self.ffmpeg_path.replace("ffmpeg", "ffprobe")
                    duration_result = subprocess.run(
                        [
                            ffprobe, "-v", "error",
                            "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1",
                            self.current_file
                        ],
                        capture_output=True,
                        text=True
                    )
                    
                    if duration_result.returncode != 0:
                        messagebox.showerror("Error", "Could not get video duration!")
                        return
                    
                    total_duration = float(duration_result.stdout.strip())
                    segment_duration = total_duration / int(value)
                    
                    command = [
                        self.ffmpeg_path,
                        "-i", self.current_file,
                        "-c", "copy",
                        "-map", "0",
                        "-segment_time", str(segment_duration),
                        "-f", "segment",
                        "-reset_timestamps", "1",
                        str(output_pattern)
                    ]
                
                dialog.destroy()
                
                # Execute in thread
                def run_split():
                    try:
                        self.progress_label.config(text="⏳ Splitting video...")
                        self.progress_bar.start()
                        
                        result = subprocess.run(command, capture_output=True, text=True)
                        
                        self.progress_bar.stop()
                        
                        if result.returncode == 0:
                            # Count created files
                            parts = list(output_dir.glob(f"{input_path.stem}_part*.mp4"))
                            total_size = sum(p.stat().st_size for p in parts) / (1024 * 1024)
                            
                            msg = f"Video split complete!\n\n"
                            msg += f"Created {len(parts)} parts\n"
                            msg += f"Total size: {total_size:.2f} MB\n"
                            msg += f"Saved to: {output_dir}"
                            
                            self.progress_label.config(text=f"✅ Split into {len(parts)} parts")
                            messagebox.showinfo("Success", msg)
                        else:
                            self.progress_label.config(text="❌ Split failed")
                            messagebox.showerror("Error", f"Split failed:\n{result.stderr[:500]}")
                    
                    except Exception as e:
                        self.progress_bar.stop()
                        self.progress_label.config(text="❌ Error occurred")
                        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
                
                thread = threading.Thread(target=run_split, daemon=True)
                thread.start()
                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        
        tk.Button(
            dialog,
            text="Split Video",
            font=("Arial", 11, "bold"),
            bg="#e67e22",
            fg="white",
            padx=20,
            pady=8,
            command=execute_split
        ).pack(pady=15)


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = FFmpegApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

