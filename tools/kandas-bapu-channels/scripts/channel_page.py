"""Build a channel page: single-night events + full searchable listing.

Usage: python channel_page.py <channel-key> <dir-with-all.json> <output-dir>
all.json = list of {id,title,description,upload_date,duration_string,duration,view_count,kind}
in channel order (newest first), as fetched with yt-dlp. Event rules below refer to
1-based positions in that list, so re-check them after re-fetching.
"""
import json, re, sys, html, csv, collections, os

KEY, SRC, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
rows = json.load(open(os.path.join(SRC, 'all.json'), encoding='utf-8'))
R = {i: r for i, r in enumerate(rows, 1)}
gu = str.maketrans('૦૧૨૩૪૫૬૭૮૯', '0123456789')

CHANNELS = {
    'naran': dict(name='Naran Valani', handle='@naranvalani6626'),
    'raju': dict(name='Raju Mokaria', handle='@RajuMokaria9974075477'),
}
# (date or year or '~', place, program / singers, [positions], note-or-None)
EVENTS = {
    'naran': [
        ('~', '(place not given)', 'Prachin santvani – Kandas Bapu, parts 1–3', [218, 217, 216], 'Part series; no place or date given'),
        ('~', 'Kutch', 'Kandas Bapu & Jagmal Barot jugalbandi (Katari)', [378, 455], 'Both descriptions say "this program is from Kutch"; may be the same night'),
    ],
    'raju': [
        ('1968-05-01', '(place not given)', 'Kandas Bapu', [239, 246, 657], None),
        ('1975-12-18', 'Kalyan (Shilphata)', 'Kandas Bapu', [245, 252, 395], 'One part says Datt Mandir Kalyan, one says Hanuman Mandir'),
        ('1977-05-23', 'Amar Metro Cinema, Mumbai', 'Kandas Bapu', [351, 366, 262, 77], 'Part titled "1977 Amar Metro Cinema" has the year only'),
        ('1981-10-20', '(place not given)', 'Kandas Bapu', [180, 181], None),
        ('1982-09-02', 'Ranavav, Porbandar (Samatbhai Sisodiya\'s vadi)', 'Kandas Bapu', [241, 242, 240], 'One part says only "1982, Ranavav"'),
        ('~', 'Pajod', 'Kandas Bapu (tabla: Rudchand Bagli)', [40, 79, 476, 533, 558], 'Matched by place only; may include the 13‑9‑1982 Pajod program'),
        ('1983-04-07', 'Parabdham', 'Kandas Bapu', [497, 528, 532, 3], 'One part says "Parabdham 1983" only'),
        ('1983-09-03', 'Ghatkopar, Mumbai', 'Kandas Bapu', [217, 200, 199, 198, 213, 37, 89, 680], '3 videos say only "1983 Mumbai/Ghatkopar"'),
        ('1987-05-14', 'Mumbai', 'Kandas Bapu – Savaram Bapa ni vani', [209, 210], None),
        ('1987-08-14', 'Bhatiya Vadi, Ghatkopar, Mumbai', 'Kandas Bapu', [433, 686, 18, 30], '2 videos say only "Ghatkopar 1987" or "Bhatiya Vadi"'),
        ('1990-02-04', 'Surendranagar', 'Kandas Bapu, Jagmal Barot', [211, 203, 205, 204, 202, 197, 201], None),
        ('1990-03-03', 'Jetpur', 'Kandas Bapu', [587, 461], None),
        ('1993', 'Ranavav, Porbandar (Samatbhai Sisodiya\'s vadi)', 'Kandas Bapu', [176, 177, 184, 185], 'Year only'),
        ('1993', 'Jalaram Bapa Mandir, Kalyan', 'Kandas Bapu, parts 1–3', [292, 291, 290], 'Year only'),
        ('1993', 'Kandas Bapu Ashram (Shivpuri Dham), Dwarka', 'Kandas Bapu, Lalitaben Ghodadra, Karshan Sagathiya', [312, 308, 309, 310, 34, 155, 182, 183, 311, 688], 'Year only – may be more than one program in 1993'),
        ('1996', 'Kandas Bapu Ashram, Dwarka', 'Savra Mandap mahotsav – Jagmal Barot, Lalitaben, Karshan Sagathiya, Niranjan Pandya', [153, 152, 188, 190, 191], 'Year only; one festival'),
        ('2002-08-10', 'Ramdevji Mandir, Dwarka', 'Shravan sud bij – Jagdish Bapu Kapadi', [141, 142], None),
        ('2006-04-06', 'Ramdevji Mandir, Dwarka', 'Ram Navmi – Jagdish Bapu Kapadi', [143, 132], 'One title says 6‑4‑2007 but its description says 6‑4‑2006'),
        ('2007-03-27', 'Ramdevpir Mandir, Dwarka', 'Ram Navmi – Jagdish Bapu Kapadi', [158, 163], None),
        ('2007-04-02', '(place not given)', 'Jagdish Bapu Kapadi', [137, 138], None),
        ('2018-04-15', 'Porbandar', 'Ramesh Giri Bapu, Vijaybhai Mokaria', [225, 641, 642], None),
        ('2019-11-01', 'Kandas Bapu Ashram, Dwarka', 'Labh Pancham – Jitugiri Bapu', [478, 644], None),
        ('2022-10-29', 'Degam, Porbandar', 'Kandas Bapu\'s 28th nirvan tithi (Labh Pancham) – Samatbhai Sisodiya', [36, 129], None),
        ('~', 'Devaliya', 'Kandas Bapu', [299, 300], 'Matched by place only'),
        ('~', 'Valsad', 'Kandas Bapu', [115, 523], 'Matched by place only'),
        ('~', '(place not given)', 'Kandas Bapu – same recording in parts 1–2', [390, 425], 'Same song list in both descriptions'),
        ('~', '(place not given)', 'Kandas Bapu – "Santone santpana", parts 1–2', [554, 555], None),
        ('~', '(place not given)', 'Kandas Bapu – "Suno Hanumana / Kaikay taro Bharatji", parts 1–2', [575, 574], None),
        ('~', '(place not given)', 'Kandas Bapu – "Gagan gadh ramva halo", parts 1–2', [583, 582], None),
    ],
}

SINGERS = [
    ('Kandas Bapu', r'k+a+n+a?d+a+s|ksndas|કાનદાસ|કાંનદાસ|કાનાદાસ|કાન દાસ'),
    ('Narayan Swami', r'નારાયણ ?(?:સ્વામી|બાપુ)|narayan ?(?:swami|bapu)'),
    ('Jagmal Barot', r'જગમાલ|jagmal'),
    ('Jagdish Bapu Kapadi', r'જગદીશ બાપુ|jagadish|jagdish'),
    ('Laxman Barot', r'la?xa?man\s*barot|લક્ષ્?મણ\s*(?:બારોટ|બાપુ)'),
    ('Karshan Sagathiya', r'કરશન\S* \S*\s*સાગઠ|karas?han\S*\s*sag'),
    ('Lalitaben Ghodadra', r'લલ[િી]તા|lalita'),
    ('Samatbhai Sisodiya', r'સામત ?ભાઈ|સિસોદ|samat ?bhai|sisod'),
    ('Niranjan Pandya', r'નિરંજન|niranjan'),
    ('Mepa Bhagat', r'મેપા|mepa'),
    ('Arjangiri Bapu', r'અરજણ ?ગ[ીિ]રી|arjan ?giri'),
    ('Sevadas Bapu', r'સેવાદાસ|sevadas'),
    ('Ramdas Virdas', r'રામદાસ વીરદાસ|ramdas virdas'),
    ('Harbham Gadhvi', r'હરભમ|harbham'),
    ('Mula Bhagat', r'મુળા ભગત|mula bhagat'),
    ('Abha Bhagat', r'એભા|abha bhagat'),
    ('Shantiram Bapu', r'શાંતિ ?રામ|shanti ?ram'),
    ('Vijay Mokaria', r'વિજય\S* મોકરીયા|vijay\S* mokaria'),
    ('Ramesh Giri Bapu', r'રમેશ ?ગ[ીિ]રી|ramesh ?giri'),
]
SINGERS = [(n, re.compile(p, re.I)) for n, p in SINGERS]

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '_shared'))
from listing_data import build_items, listing_data_json, listing_section, assets, write_videos_csv, secs, hm

events = []
ev_of = {}
for key, place, note, idx, conf in EVENTS[KEY]:
    vids = [R[i] for i in idx]
    e = dict(key=key, place=place, note=note, conf=conf, ids=[v['id'] for v in vids],
             secs=sum(secs(v['duration_string']) for v in vids))
    events.append(e)
    for v in vids: ev_of[v['id']] = e
events.sort(key=lambda e: (e['key'] == '~', e['key'], e['place']))

labels = {vid: ('Date unknown' if e['key'] == '~' else e['key']) + ' · ' + e['place'] for vid, e in ev_of.items()}
items = build_items(rows, labels, [(n, p.pattern) for n, p in SINGERS])
ch = CHANNELS[KEY]
esc = html.escape
grouped = sum(len(e['ids']) for e in events)
byid = {it['id']: it for it in items}

def li(it):
    return f'<li><a href="https://youtu.be/{it["id"]}" target="_blank" rel="noopener">{esc(it["t"])}</a> <span class="d">{it["dur"]}</span></li>'
def card(e):
    k = 'Date unknown' if e['key'] == '~' else e['key']
    flag = f'<p class="flag">⚠ {esc(e["conf"])}</p>' if e['conf'] else ''
    return (f'<details class="ev"><summary><span class="dt">{k}</span><span class="pl">{esc(e["place"])}</span>'
            f'<span class="meta">{len(e["ids"])} videos · {hm(e["secs"])}</span><span class="nt">{esc(e["note"])}</span></summary>'
            f'{flag}<ol>{"".join(li(byid[i]) for i in e["ids"])}</ol></details>')

css, js = assets()
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(ch["name"])} – Events</title><style>{css}</style></head><body><main>
<p class="crumb"><a href="../">← Kandas Bapu channels</a></p>
<h1>{esc(ch["name"])} <a class="yt" href="https://www.youtube.com/{ch["handle"]}" target="_blank" rel="noopener">YouTube ↗</a></h1>
<nav><button data-t="list" class="on">All videos ({len(items)})</button><button data-t="events">Single-night events ({len(events)})</button></nav>
{listing_section(items, f"data/{KEY}-videos.csv", extra_links=f' · <a href="data/{KEY}-events.csv">events (CSV)</a>')}
<section id="events" class="tab" hidden>
<p class="sub">{len(events)} events covering {grouped} of {len(items)} videos. Most uploads on this channel are single bhajans with no date or place, so only recordings whose title or description gives a date, place or part number could be grouped. Groups marked ⚠ rest on weaker clues.</p>
{"".join(card(e) for e in events)}
</section>
</main>
<script>const DATA={listing_data_json(items)};</script><script>{js}</script></body></html>'''
os.makedirs(os.path.join(OUT, 'data'), exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)
write_videos_csv(os.path.join(OUT, 'data', f'{KEY}-videos.csv'), items)
with open(os.path.join(OUT, 'data', f'{KEY}-events.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Event date', 'Place', 'Program / singers', 'Note', 'Part order', 'Video title', 'Duration', 'URL'])
    for e in events:
        for n, vid in enumerate(e['ids'], 1):
            it = byid[vid]
            w.writerow(['unknown' if e['key'] == '~' else e['key'], e['place'], e['note'], e['conf'] or '', n, it['t'], it['dur'], 'https://youtu.be/' + vid])
print(ch['name'], 'items', len(items), 'events', len(events), 'grouped', grouped)
