from pytube.exceptions import RegexMatchError
from pytubefix import YouTube
import logging
import psutil
import os
import time

# TODO: Sanitize file names for iOS and Windows
# TODO: Speed Up with Concurrency
# TODO: Add arguments to be able to use it via the CLI
"""
    Use Python's concurrent.futures (ThreadPoolExecutor)
    to download multiple tracks at the same time.
"""

# TODO: If song is already in the folder, skip its downloading
# TODO: Sanitize the song's names

def parse_bytes_in_mb(value: float) -> float:
    return value / (1024 * 1024)

# def load_urls():
#     pass
#
# def download_single_song():
#     pass
#
# def main():
#     pass
#
# if __name__ == "__main__":
#     main()

overall_start = time.perf_counter()
cleaned_urls = []

# Read urls from a file
try:
    with open("songs_to_download.txt", "r") as f:
        for line in f.readlines():
            cleaned_urls.append(line.strip())
except FileNotFoundError:
    print("Error: songs_to_download.txt file not found in the current directory.")
    raise SystemExit
except Exception as e:
    print(e)
    raise SystemExit

# Initialize metrics
process = psutil.Process(os.getpid())
total_memory = 0
total_song_duration = 0

# Setup logging configuration
logging.basicConfig(
    filename='downloader.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("--- Batch download started ---")

# Download each song
for idx, url in enumerate(cleaned_urls):
    start_time = time.perf_counter()
    try:
        yt = YouTube(url)

        video_title = yt.title

        print(f'Downloading {video_title}')

        audio_stream = yt.streams.filter(only_audio=True).first()

        # TODO: Replace with your our class
        audio_stream.download(
            output_path='./songs_to_download',
            filename=f'{video_title}.mp3',
        )

        duration = time.perf_counter() - start_time
        memory_usage = parse_bytes_in_mb(value=process.memory_info().rss)

        msg = f"Success '{video_title}' downloaded in {duration:.2f}s | Memory usage - {memory_usage:.2f} MB"
        logging.info(msg)
        print(msg)
    except RegexMatchError:
        print("One of the songs was not found.")
    except:
        print("Something went wrong.")

# Calculate process time
overall_duration = time.perf_counter() - overall_start

# Log metrics data
print(f"All downloads finished in {overall_duration:.2f} seconds.")
logging.info(f"--- Batch download completed in {overall_duration} seconds. ---")

# Exit the program
exit()