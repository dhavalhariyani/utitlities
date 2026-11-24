"""Shared helpers for the "All videos" listing tab used by the channel pages.

build_items()     turns yt-dlp rows into the compact records listing.js expects
listing_section() returns the HTML for the listing tab
assets()          returns (css, js) to inline into a page
write_videos_csv() writes the full listing as CSV
"""
import collections, csv, html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
GU = str.maketrans('૦૧૨૩૪૫૬૭૮૯', '0123456789')
DR = r'(?<!\d)(\d{1,2})\s*[/.\\-]\s*(\d{1,2})\s*[/.\\-]\s*((?:19|20)\d{2}|\d{2})(?!\d)'
KIND = {'videos': 'Video', 'streams': 'Live', 'shorts': 'Short'}


def secs(s):
    t = 0
    for x in (s or '0').split(':'):
        t = t * 60 + int(x)
    return t


def hm(s):
    h, m = divmod(int(s) // 60, 60)
    return f"{h}h {m:02d}m" if h else f"{m}m"


def rec_year(text):
    t = text.translate(GU)
    for d, m, y in re.findall(DR, t):
        y = int(y)
        y = y + 1900 if 50 < y < 100 else (y + 2000 if y < 100 else y)
        if 1 <= int(m) <= 12 and 1950 <= y <= 2030:
            return y
    ys = re.findall(r'(?<!\d)(19[5-9]\d|20[0-2]\d)(?!\d)', t)
    return int(ys[0]) if ys else None


def build_items(rows, event_label, singer_patterns, max_line_repeats=8):
    """rows: yt-dlp dicts with id,title,description,upload_date,duration_string,view_count,kind.
    event_label: {video_id: 'date · place'}; singer_patterns: [(name, regex-string)]."""
    pats = [(n, re.compile(p, re.I)) for n, p in singer_patterns]
    cnt = collections.Counter(l.strip() for r in rows for l in set((r['description'] or '').splitlines()))

    def clean(r):
        out = []
        for l in (r['description'] or '').splitlines():
            l = l.strip()
            if not l or l.startswith('#') or 'http' in l or cnt[l] > max_line_repeats or l in out:
                continue
            out.append(l)
        return ' · '.join(out)

    # newest upload first; n is the sort key for "newest/oldest upload"
    ordered = sorted(rows, key=lambda r: r.get('upload_date') or '', reverse=True)
    items = []
    for n, r in enumerate(ordered, 1):
        d = clean(r)
        text = r['title'] + ' ' + d
        items.append(dict(
            n=n, id=r['id'], t=' '.join(r['title'].split()), d=d[:400], dur=r.get('duration_string') or '',
            s=r.get('duration') or secs(r.get('duration_string')), up=r.get('upload_date') or '',
            v=r.get('view_count') or 0, k=KIND.get(r.get('kind'), 'Video'), y=rec_year(text),
            sg=[name for name, p in pats if p.search(text)], ev=event_label.get(r['id'], '')))
    return items


def listing_data_json(items, min_singer_count=2):
    c = collections.Counter(s for it in items for s in it['sg'])
    singers = [s for s, k in c.most_common() if k >= min_singer_count]
    years = sorted({it['y'] for it in items if it['y']})
    data = dict(items=items, singers=singers, years=years)
    return json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def listing_section(items, csv_href, hidden=False, extra_links=''):
    kinds = collections.Counter(it['k'] for it in items)
    parts = [f"{kinds['Video']} videos"]
    if kinds['Short']: parts.append(f"{kinds['Short']} short" + ('s' if kinds['Short'] != 1 else ''))
    if kinds['Live']: parts.append(f"{kinds['Live']} live recording" + ('s' if kinds['Live'] != 1 else ''))
    return f'''<section id="list" class="tab"{" hidden" if hidden else ""}>
<p class="sub">{", ".join(parts)}. Search covers titles and descriptions. Snapshot from November 2026. Download: <a href="{html.escape(csv_href)}">all videos (CSV)</a>{extra_links}</p>
<div class="filters">
<input id="q" type="search" placeholder="Search bhajan, place, singer… (Gujarati or English)">
<div class="row">
<select id="fs"><option value="">All singers</option></select>
<select id="fy"><option value="">Any recording year</option><option value="none">Year not given</option></select>
<select id="fk"><option value="">Videos, shorts &amp; live</option><option>Video</option><option>Short</option><option>Live</option></select>
<select id="fe"><option value="">In an event or not</option><option value="1">Part of an event</option><option value="0">Not in an event</option></select>
<select id="so"><option value="new">Newest upload first</option><option value="old">Oldest upload first</option><option value="rec">Recording year (oldest first)</option><option value="long">Longest first</option><option value="views">Most viewed</option></select>
</div></div>
<p id="count" class="sub"></p>
<ol id="res" class="res"></ol>
<button id="more" hidden>Show more</button>
</section>'''


def assets():
    css = open(os.path.join(HERE, 'listing.css'), encoding='utf-8').read()
    js = open(os.path.join(HERE, 'listing.js'), encoding='utf-8').read()
    return css, js


def write_videos_csv(path, items):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Type', 'Title', 'Duration', 'Uploaded', 'Views', 'Recording year (from text)', 'Singers named', 'Event', 'URL', 'Description (unique part)'])
        for it in items:
            up = f"{it['up'][:4]}-{it['up'][4:6]}-{it['up'][6:]}" if it['up'] else ''
            w.writerow([it['k'], it['t'], it['dur'], up, it['v'], it['y'] or '', '; '.join(it['sg']), it['ev'], 'https://youtu.be/' + it['id'], it['d']])
