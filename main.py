import argparse

from pytube.exceptions import RegexMatchError
from pytubefix import YouTube
import logging
import psutil
import os
import time

# TODO: Sanitize file names for iOS and Windows
# TODO: Sanitize the song's names

# TODO: Speed Up with Concurrency
# TODO: Add arguments to be able to use it via the CLI
"""
    Use Python's concurrent.futures (ThreadPoolExecutor)
    to download multiple tracks at the same time.
"""

def shorten_song_name(song_name: str) -> str:
    if len(song_name) > 50:
        return f"{song_name[:50]}..."
    return song_name


def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description="Download YouTube songs to MP3 from a text file.")

    parser.add_argument(
        "-f", "--file",
        type=str,
        default="songs_to_download.txt",
        help="Path to the text file containing YouTube URLs (default: songs_to_download.txt)"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default="./downloaded_songs",
        help="Path to the directory where the downloaded songs will be saved (default: ./downloaded_songs)"
    )

    return parser.parse_args()


def parse_bytes_in_mb(value: float) -> float:
    return value / (1024 * 1024)


def load_urls(path: str) -> list:
    urls = []

    try:
        with open(path, "r") as f:
            for line in f.readlines():
                urls.append(line.strip())
    except FileNotFoundError:
        print(f"Error: {path} file not found in the current directory.")
        raise SystemExit
    except Exception as e:
        print(e)
        raise SystemExit

    if len(urls) == 0:
        print(f"The file '{path}' is empty.")
        raise SystemExit

    return urls


def check_if_song_is_downloaded(song_name: str, output_path: str) -> bool:
    if os.path.exists(f"{output_path}/{song_name}.mp3"):
        return True
    return False


def download_single_song(url: str, process: psutil.Process, output_path: str) -> None:
    start_time = time.perf_counter()
    yt = YouTube(url)
    video_title = yt.title

    if check_if_song_is_downloaded(video_title, output_path=output_path):
        logging.info(f"Skipping {video_title}")
        print(f"Skipping '{video_title}', because it's already downloaded.")
        return

    print(f'Downloading {shorten_song_name(song_name=video_title)}')

    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(
        output_path=f'{output_path}',
        filename=f'{video_title}.mp3',
    )

    duration = time.perf_counter() - start_time
    memory_usage = parse_bytes_in_mb(value=process.memory_info().rss)

    msg = f"Success '{shorten_song_name(song_name=video_title)}' downloaded in {duration:.2f}s | Memory usage - {memory_usage:.2f} MB"
    logging.info(msg)
    print(msg)


def main():
    args = parse_arguments()
    overall_start = time.perf_counter()

    # Read urls from a file
    cleaned_urls = load_urls(args.file)

    # Initialize metrics
    process = psutil.Process(os.getpid())

    # Setup logging configuration
    logging.basicConfig(
        filename='downloader.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.info("--- Batch download started ---")

    # Download each song
    for idx, url in enumerate(cleaned_urls):
        try:
            download_single_song(url=url, process=process, output_path=args.output)
        except RegexMatchError:
            print("One of the songs was not found.")
        except:
            print("Something went wrong.")

    # Calculate process time
    overall_duration = time.perf_counter() - overall_start

    # Log metrics data
    print(f"Process finished in {overall_duration:.2f} seconds.")
    logging.info(f"--- Batch download completed in {overall_duration:.2f} seconds. ---")


if __name__ == "__main__":
    main()