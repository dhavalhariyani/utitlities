# Kandas Bapu channels

Pages for two YouTube channels that mostly carry Kandas Bapu's santvani:

- [Raju Mokaria](https://www.youtube.com/@RajuMokaria9974075477): `raju-mokaria/`
- [Naran Valani](https://www.youtube.com/@naranvalani6626): `naran-valani/`

Each page has two tabs:

- **All videos:** every upload (videos, shorts, live), searchable across title and description, with filters for singer, recording year, type and event membership. You can sort by upload date, recording year, length or views.
- **Single-night events:** recordings grouped into one program, using the same method as `sonal-audio-events`. A group needs a shared date, a shared place, or a numbered part series with matching content. Groups resting on weaker clues are marked ⚠.

Most uploads on these channels are single bhajans with no date or place, so far fewer videos fall into events than on Sonal Audio. That's why the full listing is the main view.

Snapshot: November 2026 (Raju Mokaria 690 uploads, Naran Valani 474; 3 Naran Valani uploads were unavailable when fetched).

## Files

```
index.html                  hub page linking both channels
raju-mokaria/index.html     channel page
raju-mokaria/data/          raju-videos.csv (every upload), raju-events.csv
naran-valani/...            same for Naran Valani
scripts/channel_page.py     builds a channel page; event rules live in EVENTS
../_shared/                 listing code (listing.js, listing.css, listing_data.py) shared with sonal-audio-events
```

"Singers named" and "recording year" come from pattern matching on the title and description text. They're hints, not verified credits.

## Regenerating

1. Fetch the uploads: `yt-dlp --flat-playlist -j https://www.youtube.com/<handle>/videos` (and `/streams`, `/shorts`).
2. Fetch full metadata for each video: `yt-dlp --skip-download -j`.
3. Save as `all.json`, newest first, with a `kind` field (`videos`, `streams` or `shorts`).
4. Run `python scripts/channel_page.py raju <dir-with-all.json> raju-mokaria`.

The event rules refer to positions in that list, so re-check them after re-fetching.
