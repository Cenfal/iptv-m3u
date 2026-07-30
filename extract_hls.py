#!/usr/bin/env python3
"""
extract_hls.py – Extract HLS stream URLs from live TV web pages and
                 update playlist.m3u automatically.

Requirements:
    pip install yt-dlp

Usage:
    python3 extract_hls.py
"""

import subprocess
import sys
import re

# Channels whose HLS URLs we want to resolve.
# Each entry maps a channel name to the web page that hosts the live player.
CHANNELS = [
    {
        "name": "Al Mayadeen English",
        "tvg_id": "AlMayadeen.English",
        "tvg_logo": "https://english.almayadeen.net/images/logo.png",
        "group": "News",
        "page_url": "https://english.almayadeen.net/live",
    },
    {
        "name": "Al Manar",
        "tvg_id": "AlManar",
        "tvg_logo": "https://www.almanar.com.lb/framework/assets/images/logo-tech.png",
        "group": "News",
        "page_url": "https://www.almanar.com.lb/live/",
    },
]

PLAYLIST_FILE = "playlist.m3u"
EXTRACTION_TIMEOUT = 60  # seconds to wait for yt-dlp per channel


def extract_hls_url(page_url: str) -> str | None:
    """
    Use yt-dlp to extract the best direct HLS (.m3u8) stream URL from a
    live-stream web page.

    yt-dlp is invoked with:
      -g           print the direct media URL instead of downloading
      --no-warnings suppress non-critical warnings
      -f best      request the best available quality

    Returns the URL string on success, or None on failure.
    """
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--no-warnings",
        "-g",
        "-f", "best",
        page_url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=EXTRACTION_TIMEOUT)
        if result.returncode == 0:
            url = result.stdout.strip().splitlines()[0]
            if url:
                return url
        print(f"  [yt-dlp] stderr: {result.stderr.strip()}", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print(f"  [yt-dlp] timed out for {page_url}", file=sys.stderr)
    except FileNotFoundError:
        print("  yt-dlp not found. Install it with: pip install yt-dlp", file=sys.stderr)
    return None


def build_playlist(channels: list[dict]) -> str:
    """Build an EXTM3U playlist string from a list of channel dicts."""
    lines = ["#EXTM3U"]
    for ch in channels:
        extinf = (
            f'#EXTINF:-1 tvg-id="{ch["tvg_id"]}" '
            f'tvg-name="{ch["name"]}" '
            f'tvg-logo="{ch["tvg_logo"]}" '
            f'group-title="{ch["group"]}",{ch["name"]}'
        )
        lines.append(extinf)
        lines.append(ch["stream_url"])
    lines.append("")  # trailing newline
    return "\n".join(lines)


def main() -> None:
    resolved = []

    for ch in CHANNELS:
        print(f"Extracting HLS URL for: {ch['name']} ({ch['page_url']})")
        hls_url = extract_hls_url(ch["page_url"])

        if hls_url:
            print(f"  -> {hls_url}")
            resolved.append({**ch, "stream_url": hls_url})
        else:
            # Fall back to the web page URL so the playlist stays valid.
            print(f"  -> extraction failed, using page URL as fallback")
            resolved.append({**ch, "stream_url": ch["page_url"]})

    playlist_content = build_playlist(resolved)

    with open(PLAYLIST_FILE, "w") as f:
        f.write(playlist_content)

    print(f"\nPlaylist written to {PLAYLIST_FILE}")
    print(playlist_content)


if __name__ == "__main__":
    main()
