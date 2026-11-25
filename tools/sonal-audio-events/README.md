# Sonal Audio Old Bhajan – event finder

Groups the videos on the [Sonal Audio Old Bhajan](https://www.youtube.com/@SONALAUDIOOLDBHAJAN) YouTube channel into single-night programs, using only video titles and descriptions. No video was watched or listened to.

- **All events:** 118 events covering 650 of the channel's 1,016 videos (snapshot from November 2026).
- **All videos:** every upload (1,016 videos and 1 short), searchable across title and description, with filters for singer, recording year, type and event membership, and sorting by upload date, recording year, length or views. This tab uses the shared code in `tools/_shared/`.
- **Per-singer tabs:** Kandas Bapu and Laxman Barot. Each tab lists every video that names the singer, shows the full multi-part events those videos belong to, and keeps hashtag-only matches in a separate group.

- **Playlists:** 492 YouTube playlists (17,304 videos) from the big studio channels that name Narayan Swami, Kandas Bapu, Laxman Barot or Ramdas Gondaliya. Loaded from `data/playlists.json` when the tab opens.
- **Kandas Bapu – all found:** 2,982 videos from 215 channels whose title names him, with 35 single-night events built from shared dates, places, numbered series and program playlists (weaker groups marked ⚠). The rest are standalone clips. Loaded from `data/kandas-all.json`.

## How the grouping works

1. If a title or description has a date (e.g. `23-1-1994`), every video with the same date forms one event.
2. Videos without a date are grouped by hand when they form a numbered `Part-N` series with the same place and singers.
3. Groups that rest on weaker clues are marked with ⚠ on the page.
4. Left out on purpose: long compilation series that span many nights (Rambhav Bhajan 1–32, Madhurvani 1–33, Junu Sambharnu, Surili Santvani), single bhajans split into parts, and standalone clips.

## Files

- `index.html`: the page
- `data/events.csv`, `data/events.json`: all events, one row per video, in part order
- `data/sonal-videos.csv`: every upload, with type, upload date, views, recording year and singers found in the text, and its event if any
- `data/kandas-bapu.csv`, `data/laxman-barot.csv`: per-singer lists. The `Match` column says whether the video names the singer, is part of the same event, or has the hashtag only.
- `scripts/build.py`: builds `events.json`/`events.csv` from the channel metadata (manual event rules are inside)
- `scripts/playlists.py`, `scripts/found.py`: build the Playlists and Kandas Bapu tabs from crawled YouTube data (input formats are in each script's docstring); they patch `index.html` in place
- `scripts/page.py`: builds `index.html` and the per-singer CSVs. To add a singer, add an entry to `PEOPLE`.

## Regenerating

```
yt-dlp --flat-playlist -j "https://www.youtube.com/@SONALAUDIOOLDBHAJAN/videos" > flat.jsonl
# fetch full metadata for each video (yt-dlp --skip-download -j), merge into all.json
python scripts/build.py <dir-with-all.json> <output-dir>
# also save every upload (videos + shorts, with a "kind" field) as <dir>/sonal/all_listing.json
python scripts/page.py <dir-with-all.json>    # run inside this folder, with events.json copied next to it
```

The manual rules in `build.py` refer to videos by their position in the channel's upload list, so check them again after the channel adds videos.
