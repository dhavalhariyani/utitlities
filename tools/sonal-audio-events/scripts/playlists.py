"""Builds data/playlists.json + data/playlists.csv and the Playlists tab of index.html.

Input: selected.json (already filtered and de-duplicated; each video once per playlist) = list of {id, t, ch, a, s, v:[[video_id, title, seconds]]} (see README).
Usage (run inside tools/sonal-audio-events): python scripts/playlists.py selected.json
Re-running replaces the tab if it is already in index.html.
"""
import csv, json, re, sys
src = sys.argv[1]
P = json.load(open(src, encoding='utf-8'))
ORDER = {'Narayan Swami': 0, 'Kandas Bapu': 1, 'Laxman Barot': 2, 'Ramdas Gondaliya': 3}
for p in P: p['a'] = sorted(p['a'], key=ORDER.get)
P.sort(key=lambda p: (-len(p['a']), p['ch'], -p['s']))
json.dump(P, open('data/playlists.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
with open('data/playlists.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f); w.writerow(['Channel', 'Playlist', 'Artists named', 'Videos', 'Hours', 'URL'])
    for p in P: w.writerow([p['ch'], p['t'], '; '.join(p['a']), len(p['v']), round(p['s'] / 3600, 1), 'https://www.youtube.com/playlist?list=' + p['id']])
nv = sum(len(p['v']) for p in P); nc = len({p['ch'] for p in P})
section = f'''<section id="playlists" class="tab" hidden>
<p class="sub">{len(P)} YouTube playlists ({nv:,} videos) from {nc} channels that name Narayan Swami, Kandas Bapu, Laxman Barot or Ramdas Gondaliya. A playlist is included when the artist is in its title or in at least 3 of its videos' titles (or 40%). Artist tags are matched from titles only. Many playlists on the big studio channels are whole programs. Snapshot from November 2026. Download: <a href="data/playlists.csv">playlists.csv</a></p>
<div class="pfilters"><input id="pq" type="search" placeholder="Search playlist or video title, place, year…">
<select id="pc"><option value="">All channels</option></select><select id="pa"><option value="">All artists</option></select>
<select id="ps"><option value="big">Longest first</option><option value="num">Most videos first</option><option value="az">A–Z</option><option value="ch">By channel</option></select></div>
<p id="pcount" class="sub"></p><div id="pres"></div><button id="pmore" hidden>Show more</button></section>'''
h = open('index.html', encoding='utf-8').read()
h = re.sub(r'<section id="playlists".*?</section>', '', h, flags=re.S)
h = re.sub(r'<script id="plj">.*?</script>', '', h, flags=re.S)
h = re.sub(r'<button data-t="playlists">.*?</button>', '', h)
h = h.replace('</nav>', f'<button data-t="playlists">Playlists ({len(P)})</button></nav>', 1)
h = h.replace('</main>', section + '</main>', 1)
js = open('../_shared/playlists.js', encoding='utf-8').read()
css = open('../_shared/listing.css', encoding='utf-8').read()
pcss = css[css.index('.pfilters'):]
h = re.sub(r'<style id="pcss">.*?</style>', '', h, flags=re.S)
h = h.replace('</head>', f'<style id="pcss">{pcss}</style></head>', 1)
h = h.replace('</body>', f'<script id="plj">window.PL_URL="data/playlists.json";{js}</script></body>', 1)
open('index.html', 'w', encoding='utf-8').write(h)
print(len(P), 'playlists', nv, 'videos', nc, 'channels')
