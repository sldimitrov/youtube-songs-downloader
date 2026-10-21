import argparse

from pytube.exceptions import RegexMatchError
from pytubefix import YouTube
import logging
import psutil
import os
from pydub import AudioSegment
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

    # 1. Download the raw audio stream. YouTube serves AAC (.m4a) or Opus (.webm),
    # never real MP3, so keep the real extension instead of pretending it's .mp3
    audio_stream = yt.streams.filter(only_audio=True).first()
    temp_file = audio_stream.download(
        output_path=output_path,
        filename=f"temp_{video_title}.{audio_stream.subtype}",
    )

    # 2. Convert and export strictly to car-friendly MP3 (44.1 kHz, stereo, 192k CBR)
    final_path = os.path.join(output_path, f"{video_title}.mp3")
    try:
        sound = AudioSegment.from_file(temp_file)
        sound.export(
            final_path,
            format="mp3",
            bitrate="192k",
            parameters=[
                "-ar", "44100",  # Forces CD-quality sample rate for older head units
                "-ac", "2",
                "-id3v2_version", "3",  # Car stereos often choke on ffmpeg's default ID3v2.4 tags
                "-write_id3v1", "1",
            ]
        )
    except Exception as e:
        print(f"Error converting audio for {video_title}: {e}")
        logging.error(f"Conversion error for {video_title}: {e}")
    finally:
        # 3. Clean up the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

    duration = time.perf_counter() - start_time
    memory_usage = parse_bytes_in_mb(value=process.memory_info().rss)

    msg = f"Success '{shorten_song_name(song_name=video_title)}' downloaded & converted in {duration:.2f}s | Memory usage - {memory_usage:.2f} MB"
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