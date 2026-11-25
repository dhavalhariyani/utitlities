"""Builds data/kandas-all.json + .csv and the "Kandas Bapu - all found" tab of index.html.

Input: list of {id, t, ch, dur} (video id, title, channel, seconds), built from YouTube searches,
the upload lists of channels that carry his bhajans, and the playlists on the Playlists tab.
A video is kept when its title names Kandas Bapu (English or Gujarati spelling).
Events (single-night groups) come from a second file: [{d, p, n, conf, ch, v:[video ids]}].
Usage (inside tools/sonal-audio-events): python scripts/found.py videos.json events.json
"""
import collections, csv, json, re, sys
V = json.load(open(sys.argv[1], encoding='utf-8'))
EVS = json.load(open(sys.argv[2], encoding='utf-8'))
cnt = collections.Counter(v['ch'] for v in V)
chans = [c for c, _ in cnt.most_common()]
ix = {c: i for i, c in enumerate(chans)}
V.sort(key=lambda v: (ix[v['ch']], v['t']))
pos = {v['id']: i for i, v in enumerate(V)}
vev = {}
def partno(v):
    m = re.match(r'\s*[\(\[]?\s*(?:part\s*[-:]?\s*)?(\d{1,3})', v['t'].translate(str.maketrans('૦૧૨૩૪૫૬૭૮૯', '0123456789')), re.I)
    return int(m.group(1)) if m else 999
EVS.sort(key=lambda e: (e['d'] == '~', e['d'], e['p']))
E = []
for i, e in enumerate(EVS):
    ids = sorted(e['v'], key=lambda x: (partno(V[pos[x]]), V[pos[x]]['t']))
    for x in ids: vev[x] = i
    E.append([e['d'], e['p'], e['n'], e['conf'], [pos[x] for x in ids]])
nev = sum(len(e[4]) for e in E)
json.dump(dict(c=chans, v=[[v['id'], v['t'], ix[v['ch']], v['dur'], vev.get(v['id'], -1)] for v in V], e=E),
          open('data/kandas-all.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
with open('data/kandas-all.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Channel', 'Title', 'Duration (s)', 'URL'])
    for v in V:
        w.writerow([v['ch'], v['t'], v['dur'], 'https://youtu.be/' + v['id']])
hrs = round(sum(v['dur'] for v in V) / 3600)
section = f'''<section id="found" class="tab" hidden>
<p class="sub">{len(E)} single-night events group {nev} of the {len(V):,} videos; the rest are standalone clips, because their titles name no place, date or program. {len(V):,} videos (about {hrs:,} hours) from {len(chans)} channels whose title names Kandas Bapu. Found by searching YouTube in English and Gujarati, then reading the full upload lists of the channels that carry his bhajans, and the playlists on the Playlists tab. The same recording is often uploaded by several channels, so expect repeats. Titles only, nothing was listened to. Snapshot from November 2026. Download: <a href="data/kandas-all.csv">kandas-all.csv</a></p>
<div class="pfilters"><input id="fq" type="search" placeholder="Search title or channel (Gujarati or English)">
<select id="fv"><option value="ev">Events ({len(E)})</option><option value="all">All videos</option><option value="solo">Not in an event</option></select>
<select id="fc"><option value="">All channels</option></select>
<select id="fo"><option value="ch">By channel</option><option value="long">Longest first</option><option value="az">A-Z</option></select></div>
<p id="fcount" class="sub"></p><div id="fev"></div><ol id="fres"></ol><button id="fmore" hidden>Show more</button></section>'''
h = open('index.html', encoding='utf-8').read()
h = re.sub(r'<section id="found".*?</section>', '', h, flags=re.S)
h = re.sub(r'<script id="fnd">.*?</script>', '', h, flags=re.S)
h = re.sub(r'<button data-t="found">.*?</button>', '', h)
h = h.replace('</nav>', f'<button data-t="found">Kandas Bapu – all found ({len(V):,})</button></nav>', 1)
h = h.replace('</main>', section + '</main>', 1)
js = open('../_shared/found.js', encoding='utf-8').read()
h = h.replace('</body>', f'<script id="fnd">window.FOUND_URL="data/kandas-all.json";{js}</script></body>', 1)
css = open('../_shared/listing.css', encoding='utf-8').read()
h = re.sub(r'<style id="pcss">.*?</style>', '', h, flags=re.S)
h = h.replace('</head>', f'<style id="pcss">{css[css.index(".pfilters"):]}</style></head>', 1)
open('index.html', 'w', encoding='utf-8').write(h)
print(len(V), 'videos', len(chans), 'channels', hrs, 'hours', len(E), 'events', nev, 'in events')
