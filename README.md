# Bulk Video Downloader

A simple Python application with a **GUI (Tkinter)** to download videos in bulk using **FFmpeg**.

## Features
- Multi-threaded downloads for efficiency
- Progress tracking with a progress bar
- Supports URL input with filename and folder selection
- Log of completed and failed downloads

---

## Installation

### 1. Install Dependencies
Ensure you have **Python 3.10+** installed.

#### **Windows**
```sh
winget install ffmpeg
```

#### **Linux (Debian/Ubuntu-based)**
```sh
sudo apt update && sudo apt install -y python3-tk ffmpeg
```

#### **macOS**
```sh
brew install python-tk ffmpeg
```

Additionally, ensure you have the necessary Python modules installed:
```sh
pip install tkinter
```

---

## Running the Application
Once dependencies are installed, you can start the application by running:

```sh
python m3u8_video_downloader.py
```

---

## How to Use
1. Enter links in the following format:
   ```
   URL | Filename | Folder
   ```
   - **URL**: The direct link to the video file (e.g., `https://example.com/video.m3u8`).
   - you can get this links with: 
     m3u8 Sniffer extention - https://chromewebstore.google.com/detail/m3u8-sniffer-tv-find-and/akkncdpkjlfanomlnpmmolafofpnpjgn
   - **Filename**: The desired name for the downloaded file (without extension).
   - **Folder**: The directory where the video will be saved.

2. Click **Start Downloads** to begin.
3. Progress bars will update as downloads proceed.
4. Check the log for errors or successful downloads.
5. Click **Clear All** to reset inputs.

---

## Packaging as an Executable
If you want to distribute the app as an executable:

```sh
pip install pyinstaller
pyinstaller --onefile --windowed m3u8_video_downloader.py
```
- The standalone executable will be available in the `dist/` folder.

---

## License
MIT License. Feel free to modify and distribute.

---

## Author
Daniel Rubin

