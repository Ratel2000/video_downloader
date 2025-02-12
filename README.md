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
pip install -r requirements.txt
winget install ffmpeg
```

#### **Linux (Debian/Ubuntu-based)**
```sh
sudo apt update && sudo apt install -y python3-tk ffmpeg
pip install -r requirements.txt
```

#### **macOS**
```sh
brew install python-tk ffmpeg
pip install -r requirements.txt
```

---

## Running the Application
Once dependencies are installed, you can start the application by running:

```sh
python main.py
```

---

## How to Use
1. Enter links in the following format:
   ```
   URL | Filename | Folder
   ```
2. Click **Start Downloads** to begin.
3. Progress bars will update as downloads proceed.
4. Check the log for errors or successful downloads.
5. Click **Clear All** to reset inputs.

---

## Packaging as an Executable
If you want to distribute the app as an executable:

```sh
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```
- The standalone executable will be available in the `dist/` folder.

---


## License
MIT License. Feel free to modify and distribute.

---

## Author
[Daniel Rubin]

