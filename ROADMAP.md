# Roadmap 🗺️

A learning roadmap for growing this downloader from a working script into a
tested, packaged Python tool, while it keeps solving the real problem:
**getting songs that play reliably on a Sony car stereo from a USB drive.**

Each phase lists **tasks**, **what you'll learn**, and a **done when** checkpoint.
Work through them in order, one branch and PR per task.

---

## Phase 0: Project Hygiene 🧹

- [ ] Re-save `requirements.txt` as UTF-8 (it's currently UTF-16, which can break `pip install -r`)
- [ ] Remove `pytube`; `RegexMatchError` is imported from a different library than the one doing the downloading (`pytubefix`)
- [ ] Pin dependency versions in `requirements.txt`
- [ ] Add `pydub` to the README install step and document that **ffmpeg** is a system dependency
- [ ] Delete stale TODOs and the stray docstring between the imports

**You'll learn:** dependency management, text encodings, reproducible environments.
**Done when:** a fresh clone + `pip install -r requirements.txt` + README steps works first try.

---

## Phase 1: Correctness & Robustness 🛡️

- [ ] Replace the bare `except:` with specific exceptions; use `logging.exception()` so tracebacks aren't lost
- [ ] Make `load_urls` skip blank lines and `#` comments
- [ ] De-duplicate URLs
- [ ] Strip playlist/radio query params (`&list=…&start_radio=1&pp=…`), see `urllib.parse`
- [ ] Sanitize file names: Windows/FAT32-safe characters, optional ASCII-only mode, length cap
- [ ] Make `check_if_song_is_downloaded` compare against the *sanitized* name
- [ ] Pick the best audio stream (`order_by("abr")`) instead of `.first()`
- [ ] Configure logging at the very start of `main()`; decide what goes to console vs. file
- [ ] Print an end-of-run summary (`12 ok, 2 skipped, 1 failed`) and exit with a nonzero code on failures

**You'll learn:** exception design, `pathlib`, string handling, `urllib.parse`, `logging` configuration.
**Done when:** a messy input file (blanks, comments, duplicates, playlist links, weird titles) runs cleanly and every file plays on the car stereo.

---

## Phase 2: Structure 🏗️

- [ ] Split `main.py` into modules: `cli.py`, `sources.py`, `downloader.py`, `converter.py`, `naming.py`
- [ ] Have `download_single_song` return a result object (`@dataclass`: title, path, status, duration, error) instead of printing
- [ ] Use an `Enum` for statuses (`OK`, `SKIPPED`, `FAILED`)
- [ ] Add full type hints
- [ ] Use `pathlib.Path` everywhere instead of f-string paths
- [ ] Move magic values (`"192k"`, `44100`, the 50-char name limit) into constants or a config object

**You'll learn:** separation of concerns, dataclasses, enums, designing for testability.
**Done when:** each module has one clear job and `main()` reads like a short summary of the program.

---

## Phase 3: Testing & Tooling 🧪

- [ ] Add `pytest` tests for the pure functions: name sanitizing, URL parsing, `shorten_song_name`
- [ ] Test `load_urls` with the `tmp_path` fixture
- [ ] Mock `YouTube` with `unittest.mock` to test download logic without the network
- [ ] Add `ruff` (lint + format) and `mypy`
- [ ] Wire them into `pre-commit`
- [ ] Add a GitHub Actions workflow running lint, type check and tests on every PR

**You'll learn:** unit testing, fixtures, mocking, static analysis, CI.
**Done when:** every PR gets a green or red check automatically, and the tests run offline in seconds.

---

## Phase 4: Features for the Car 🚗

- [ ] ID3 tagging with `mutagen`: artist/title parsed from the video title, album art from the thumbnail
- [ ] `export` command: copy to the USB drive, warn if it isn't FAT32, add `01 - …` prefixes for play order, one folder per playlist
- [ ] Support whole playlist URLs (`pytubefix.Playlist`)
- [ ] `--dry-run` flag
- [ ] `--bitrate` option
- [ ] Retries with backoff for flaky network errors

**You'll learn:** binary metadata formats, file-system APIs, argparse subcommands (`add_subparsers`).
**Done when:** the stereo shows the correct artist/title and plays tracks in the intended order.

---

## Phase 5: Concurrency ⚡

- [ ] Parallel downloads with `ThreadPoolExecutor` + `as_completed`
- [ ] Measure: compare threads with `ProcessPoolExecutor` for the ffmpeg conversion step (use the existing timing/memory logging)
- [ ] Progress bar with `rich` or `tqdm`
- [ ] Thread-safe console/log output
- [ ] Graceful Ctrl+C: cancel pending work, clean up half-written temp files

**You'll learn:** the GIL, I/O-bound vs CPU-bound work, executors, graceful shutdown.
**Done when:** you can explain, with your own numbers, why you chose threads, processes, or both.

---

## Phase 6: Packaging 📦

- [ ] `pyproject.toml` with a `src/` layout
- [ ] Console-script entry point so `ytmp3 -f list.txt` works from anywhere after `pip install -e .`
- [ ] Semantic versioning, git tags, and a `CHANGELOG.md`
- [ ] *(Optional)* Publish to TestPyPI

**You'll learn:** how real Python packages are structured, built and distributed.
**Done when:** someone else can `pip install` it and run `ytmp3 --help`.

---

## Stretch Goals 🌟

- [ ] Replace `pydub` with direct `subprocess` calls to ffmpeg (avoids loading whole songs into memory)
- [ ] Config file support via `tomllib`
- [ ] An `asyncio` version to compare against the threaded one
