# Sonal Audio Old Bhajan – event finder

Groups the videos on the [Sonal Audio Old Bhajan](https://www.youtube.com/@SONALAUDIOOLDBHAJAN) YouTube channel into single-night programs, using only video titles and descriptions. No video was watched or listened to.

- **All events:** 118 events covering 650 of the channel's 1,016 videos (snapshot from November 2026).
- **Per-singer tabs:** Kandas Bapu and Laxman Barot. Each tab lists every video that names the singer, shows the full multi-part events those videos belong to, and keeps hashtag-only matches in a separate group.

## How the grouping works

1. If a title or description has a date (e.g. `23-1-1994`), every video with the same date forms one event.
2. Videos without a date are grouped by hand when they form a numbered `Part-N` series with the same place and singers.
3. Groups that rest on weaker clues are marked with ⚠ on the page.
4. Left out on purpose: long compilation series that span many nights (Rambhav Bhajan 1–32, Madhurvani 1–33, Junu Sambharnu, Surili Santvani), single bhajans split into parts, and standalone clips.

## Files

- `index.html`: the page
- `data/events.csv`, `data/events.json`: all events, one row per video, in part order
- `data/kandas-bapu.csv`, `data/laxman-barot.csv`: per-singer lists. The `Match` column says whether the video names the singer, is part of the same event, or has the hashtag only.
- `scripts/build.py`: builds `events.json`/`events.csv` from the channel metadata (manual event rules are inside)
- `scripts/page.py`: builds `index.html` and the per-singer CSVs. To add a singer, add an entry to `PEOPLE`.

## Regenerating

```
yt-dlp --flat-playlist -j "https://www.youtube.com/@SONALAUDIOOLDBHAJAN/videos" > flat.jsonl
# fetch full metadata for each video (yt-dlp --skip-download -j), merge into all.json
python scripts/build.py <dir-with-all.json> <output-dir>
python scripts/page.py <dir-with-all.json>    # run inside the output dir
```

The manual rules in `build.py` refer to videos by their position in the channel's upload list, so check them again after the channel adds videos.
