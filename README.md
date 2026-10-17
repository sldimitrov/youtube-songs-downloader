# YouTube MP3 Downloader 🎵

A lightweight CLI tool built in Python to batch download YouTube audio as `.mp3` files from a text file containing video URLs.

## Features ✨

* **Batch Processing:** Reads multiple URLs from a text file.
* **Skip Existing Downloads:** Automatically checks if a song is already downloaded to prevent re-downloading.
* **CLI Customization:** Choose custom input files and output directories using command-line arguments.
* **Performance & Memory Logging:** Tracks total processing time and memory usage per download (`psutil`).
* **Error Handling & Logging:** Logs successes, skipped files, and errors to `downloader.log`.

---

## Installation ⚙️

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sldimitrov/youtube-songs-downloader.git
   cd youtube-songs-downloader
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # On macOS/Linux
   # or
   .\.venv\Scripts\activate       # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install pytubefix psutil
   ```

---

## Usage 🚀

1. Create a text file containing your YouTube links (one per line):
   ```text
   # songs_to_download.txt
   https://www.youtube.com/watch?v=EXAMPLE1
   https://www.youtube.com/watch?v=EXAMPLE2
   ```

2. Run the script using default settings (`songs_to_download.txt` -> `./downloaded_songs`):
   ```bash
   python main.py
   ```

### Command Line Options 🛠️

| Argument | Short | Default | Description |
| :--- | :--- | :--- | :--- |
| `--file` | `-f` | `songs_to_download.txt` | Path to the text file containing YouTube links. |
| `--output` | `-o` | `./downloaded_songs` | Folder path where downloaded `.mp3` files will be saved. |

**Examples:**

```bash
# Custom input file
python main.py -f my_playlist.txt

# Custom input file and custom output folder
python main.py -f my_playlist.txt -o ./my_music
```

---

## Roadmap 🗺️

- [ ] Filename sanitization for OS compatibility (Windows/iOS)
- [ ] Concurrent downloads using `concurrent.futures.ThreadPoolExecutor`
- [ ] ID3 metadata and album art tagging