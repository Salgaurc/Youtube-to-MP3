# YouTube to MP3 Downloader

A simple Python desktop application that downloads YouTube videos and converts them to MP3 format.

## Features
- Download YouTube videos by URL
- Automatically convert videos to MP3
- Easy-to-use interface (built with Tkinter)
- Lightweight and fast
- Works with playlists
- Cross-platform: macOS and Windows

## Download (no Python required)

Pre-built Windows executables are generated automatically on every push, via GitHub Actions.

1. Go to the **Actions** tab of this repository
2. Open the latest successful **"Build Windows EXE"** run
3. Download the **YouTube-to-MP3-Windows** artifact at the bottom of the page
4. Unzip it — run `YouTube-to-MP3.exe` directly, no installation needed

## Requirements (running from source)
- Python 3.9+
- [ffmpeg](https://ffmpeg.org/download.html) installed and available on your system PATH
- Dependencies listed in `requirements.txt`

## Installation (running from source)

1. Clone this repository:
```bash
   git clone https://github.com/YOUR-USERNAME/youtube-to-mp3.git
   cd youtube-to-mp3
```

2. Create and activate a virtual environment:
```bash
   python3 -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

## Usage

1. Run the app:
```bash
   python main.py
```

2. Enter a YouTube URL into the input field.

3. Choose a save location.

4. The app will download and convert the video to MP3, saving it locally.

## Building it yourself

- **macOS**: `pyinstaller --onefile --windowed --name "YouTube-to-MP3" main.py`
- **Windows**: handled automatically by the `.github/workflows/build-windows.yml` workflow — it downloads a static `ffmpeg.exe`, bundles it with the app, and produces a single-file executable as a build artifact.

## Contributing
Feel free to fork this project, open issues, or submit pull requests.
