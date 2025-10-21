#!/usr/bin/env python3
"""
Progress utilities for build system
"""

import sys
import time
import threading
from typing import Optional

class ProgressBar:
    """Simple progress bar for long operations"""
    
    def __init__(self, total: int, desc: str = "Progress", width: int = 50):
        self.total = total
        self.current = 0
        self.desc = desc
        self.width = width
        self.start_time = time.time()
        self.last_update = 0
        self.update_interval = 0.1  # Update every 100ms
        
    def update(self, n: int = 1, desc: Optional[str] = None):
        """Update progress by n steps"""
        self.current = min(self.current + n, self.total)
        
        if desc:
            self.desc = desc
            
        # Only update if enough time has passed
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            self._display()
            self.last_update = current_time
    
    def set_progress(self, current: int, desc: Optional[str] = None):
        """Set absolute progress"""
        self.current = min(current, self.total)
        
        if desc:
            self.desc = desc
            
        self._display()
    
    def _display(self):
        """Display the progress bar"""
        if self.total == 0:
            percent = 0
        else:
            percent = self.current / self.total
        
        filled = int(self.width * percent)
        bar = '█' * filled + '░' * (self.width - filled)
        
        elapsed = time.time() - self.start_time
        
        if self.current == 0:
            eta = "?s"
        else:
            eta_seconds = (elapsed / self.current) * (self.total - self.current)
            eta = f"{eta_seconds:.0f}s"
        
        print(f"\r{self.desc}: |{bar}| {self.current}/{self.total} ({percent:.1%}) [{elapsed:.1f}s<{eta}]", 
              end='', flush=True)
    
    def finish(self, desc: Optional[str] = None):
        """Finish the progress bar"""
        self.current = self.total
        if desc:
            self.desc = desc
        self._display()
        print()  # New line

class Spinner:
    """Simple spinner for indeterminate progress"""
    
    def __init__(self, desc: str = "Working"):
        self.desc = desc
        self.spinning = False
        self.thread = None
        self.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    def start(self):
        """Start the spinner"""
        self.spinning = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self, desc: Optional[str] = None):
        """Stop the spinner"""
        self.spinning = False
        if self.thread:
            self.thread.join()
        
        if desc:
            print(f"\r✅ {desc}")
        else:
            print("\r✅ Done")
    
    def _spin(self):
        """Spin animation"""
        i = 0
        while self.spinning:
            print(f"\r{self.frames[i % len(self.frames)]} {self.desc}", end='', flush=True)
            time.sleep(0.1)
            i += 1

def show_build_progress(step_name: str, duration: float = 0):
    """Show build progress for a specific step"""
    if duration > 0:
        # Known duration - use progress bar
        steps = int(duration * 10)  # 10 updates per second
        progress = ProgressBar(steps, f"Building {step_name}")
        
        for i in range(steps):
            progress.update()
            time.sleep(0.1)
        
        progress.finish(f"Built {step_name}")
    else:
        # Unknown duration - use spinner
        spinner = Spinner(f"Building {step_name}")
        spinner.start()
        
        # Simulate work
        time.sleep(1)
        
        spinner.stop(f"Built {step_name}")

if __name__ == "__main__":
    # Test the progress utilities
    print("Testing Progress Bar:")
    progress = ProgressBar(100, "Test Progress")
    for i in range(101):
        progress.update()
        time.sleep(0.02)
    
    print("\nTesting Spinner:")
    spinner = Spinner("Test Spinner")
    spinner.start()
    time.sleep(3)
    spinner.stop("Test Complete")
