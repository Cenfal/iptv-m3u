# iptv-m3u

A curated M3U playlist for IPTV players.

## Playlist

**File:** `playlist.m3u`

### Channels

| Channel | Group | HLS Stream URL |
|---------|-------|----------------|
| Al Mayadeen English | News | https://mdnlv.cdn.octivid.com/almdn/smil:mpegts.stream.smil/playlist.m3u8 |
| Al Manar | News | https://manar.live/iptv/playlist.m3u8 |

## Usage

Load `playlist.m3u` in any IPTV player that supports the M3U/HLS format (e.g. VLC, Kodi, TiviMate, IPTV Smarters).

## How to extract or refresh HLS URLs

Live stream URLs occasionally change. Use `extract_hls.py` to automatically
extract the current HLS `.m3u8` endpoints from each channel's live page and
write a fresh `playlist.m3u`.

### Prerequisites

```bash
pip install yt-dlp
```

### Run

```bash
python3 extract_hls.py
```

The script calls `yt-dlp -g <live-page-url>` for each channel, which tells
yt-dlp to print the resolved direct media URL instead of downloading the
stream. The resolved URLs are written back to `playlist.m3u`.

### Manual extraction with yt-dlp

```bash
# Print the HLS URL for any live stream page
yt-dlp -g https://english.almayadeen.net/live
yt-dlp -g https://www.almanar.com.lb/live/
```

### Manual extraction with browser DevTools

1. Open the live stream page in Chrome or Firefox.
2. Open **DevTools** → **Network** tab (press `F12`).
3. Filter requests by **Media** or type `.m3u8` in the search box.
4. Reload the page; you will see one or more `.m3u8` requests appear.
5. Right-click the request → **Copy URL**.

> **Note:** Stream URLs may require specific `Referer` or `User-Agent` headers.
> If playback fails in your IPTV player, try adding:
> `#EXTVLCOPT:http-referrer=<live-page-url>`
> on the line immediately before the stream URL in `playlist.m3u`.