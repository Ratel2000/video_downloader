import os
import re
import subprocess
import tkinter as tk
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor


class VideoDownloaderApp:
    def __init__(self, root):
    	self.root = root
        self.root.title("Bulk Video Downloader")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # Setup layout
        self.setup_ui()

        # Executor for managing download threads
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.progress_bars = {}

    def setup_ui(self):
        # Links Entry (Multi-line for multiple links, expandable)
        self.links_label = tk.Label(self.root, text="Enter Links format { URL | Filename | Folder }:")
        self.links_label.pack(anchor="w", padx=5)

        self.links_entry = tk.Text(self.root, height=15, wrap="word")
        self.links_entry.pack(fill="both", expand=True, padx=5, pady=5)

        # Download log (Expandable)
        self.log_label = tk.Label(self.root, text="Download Log")
        self.log_label.pack(anchor="w", padx=5)

        self.log_text = tk.Text(self.root, height=10, state="disabled", wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Progress bars
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=5, pady=5)

        self.download_button = tk.Button(button_frame, text="Start Downloads", command=self.start_downloads)
        self.download_button.pack(side="left", padx=5)

        self.clear_button = tk.Button(button_frame, text="Clear All", command=self.clear_all)
        self.clear_button.pack(side="left", padx=5)

    def add_progress_bar(self, label_text):
        frame = tk.Frame(self.progress_frame)
        frame.pack(fill="x", padx=5, pady=2)

        label = tk.Label(frame, text=label_text[:30] + "..." if len(label_text) > 30 else label_text)
        label.pack(side="left")

        progress = ttk.Progressbar(frame, length=200, mode="determinate")
        progress.pack(side="left", padx=5)

        self.progress_bars[label_text] = progress

    def start_downloads(self):
        # Parse links from the multi-line text entry
        links = self.links_entry.get("1.0", tk.END).strip().splitlines()
        for line in links:
            try:
                url, filename, folder = map(str.strip, line.split("|"))
                self.add_progress_bar(filename)
                self.executor.submit(self.download_video, url, filename, folder)
            except ValueError:
                self.log_text.config(state="normal")
                self.log_text.insert(tk.END, f"Invalid format in line: {line}\n")
                self.log_text.config(state="disabled")

    def download_video(self, url, filename, folder):
        filename = self.sanitize_filename(filename)

        # Create folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        output_path = os.path.join(folder, f"{filename}.mp4")

        # Extract video duration for progress calculation
        duration = self.get_video_duration(url)
        if duration is None:
            self.update_log(f"Failed to retrieve duration for {url}")
            return

        # Run FFmpeg command and capture progress
        ffmpeg_command = ["ffmpeg", "-i", url, "-c", "copy", "-bsf:a", "aac_adtstoasc", output_path]
        process = subprocess.Popen(ffmpeg_command, stderr=subprocess.PIPE, universal_newlines=True)

        for line in process.stderr:
            if "time=" in line:
                elapsed_time = self.get_elapsed_time(line)
                if elapsed_time:
                    progress = int((elapsed_time / duration) * 100)
                    self.update_progress(filename, progress)

        process.wait()

        if process.returncode == 0:
            self.update_log(f"Download completed for: {filename}")
            self.update_progress(filename, 100)
        else:
            self.update_log(f"Error downloading {url}")

    def get_video_duration(self, url):
        try:
            ffprobe_command = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                               "default=noprint_wrappers=1:nokey=1", url]
            result = subprocess.run(ffprobe_command, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except subprocess.CalledProcessError:
            return None

    def get_elapsed_time(self, line):
        match = re.search(r"time=(\d+:\d+:\d+\.\d+)", line)
        if match:
            time_str = match.group(1)
            hours, minutes, seconds = map(float, time_str.split(':'))
            return hours * 3600 + minutes * 60 + seconds
        return None

    def update_log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")

    def update_progress(self, filename, value):
        progress_bar = self.progress_bars.get(filename)
        if progress_bar:
            progress_bar["value"] = value

    def clear_all(self):
        self.progress_frame.destroy()
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.links_entry.delete("1.0", tk.END)
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state="disabled")
        self.progress_bars.clear()

    @staticmethod
    def sanitize_filename(filename):
        return re.sub(r'[<>:"/\\|?*]', '_', filename)


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
