import json, html, re, sys, csv
S = sys.argv[1]
rows = json.load(open(S + '/all.json', encoding='utf-8'))
E = json.load(open('events.json', encoding='utf-8'))
ev_of = {v['id']: e for e in E for v in e['videos']}
def secs(s):
    t = 0
    for x in (s or '0').split(':'): t = t * 60 + int(x)
    return t
def hm(s):
    h, m = divmod(s // 60, 60)
    return f"{h}h {m:02d}m" if h else f"{m}m"
esc = html.escape
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '_shared'))
from listing_data import thumb_li
def li(v):
    dur = v.get('duration_string') or v.get('dur') or ''
    return thumb_li(v['id'], ' '.join(v['title'].split()), dur)
def card(e):
    k = 'Date unknown' if e['key'] == '~' else e['key']
    note = '' if e['conf'] == 'Confirmed' else f'<p class="flag">⚠ {esc(e["conf"])}</p>'
    s = esc((k + ' ' + e['place'] + ' ' + e['note']).lower())
    return (f'<details class="ev" data-s="{s}"><summary><span class="dt">{k}</span><span class="pl">{esc(e["place"])}</span>'
            f'<span class="meta">{len(e["videos"])} videos · {hm(e["secs"])}</span><span class="nt">{esc(e["note"])}</span></summary>'
            f'{note}<ol>{"".join(li(v) for v in e["videos"])}</ol></details>')

PEOPLE = [
    ('kandas', 'Kandas Bapu', 'kandasbapu', 'kandas-bapu.csv',
     re.compile(r'k+a+n+a?d+a+s|કાનદાસ|કાંનદાસ|કાનાદાસ', re.I)),
    ('laxman', 'Laxman Barot', 'laxmanbarot', 'laxman-barot.csv',
     re.compile(r'la?xa?man\s*barot|lakshman\s*barot|લક્ષ્?મણ\s*(?:બારોટ|બાપુ)|બારોટજી', re.I)),
]

def person(key, name, tag, csvname, pat):
    main = []; tagonly = []
    for r in rows:
        d = r['description'] or ''
        body = '\n'.join(l for l in d.splitlines() if not l.strip().startswith('#'))
        tags = '\n'.join(l for l in d.splitlines() if l.strip().startswith('#'))
        if pat.search(r['title']) or pat.search(body): main.append(r)
        elif pat.search(tags.replace('#' + tag, ' ' + name + ' ').replace('#', ' ')) or ('#' + tag) in tags.lower(): tagonly.append(r)
    kev = []; seen = set()
    for r in main:
        e = ev_of.get(r['id'])
        if e and id(e) not in seen: seen.add(id(e)); kev.append(e)
    kev.sort(key=lambda e: (e['key'] == '~', e['key'], e['place']))
    ingroup = {v['id'] for e in kev for v in e['videos']}
    single = [r for r in main if r['id'] not in ingroup]
    main_ids = {r['id'] for r in main}
    kcount = len(main); kevvids = sum(len(e['videos']) for e in kev)
    tag_secs = sum(secs(r['duration_string']) for r in tagonly)
    sec = f'''<section id="{key}" class="tab" hidden><h2>{name}</h2>
<p class="sub">{kcount} videos name {name} in the title or description. {kcount - len(single)} of them belong to {len(kev)} multi-part events, which are shown in full below ({kevvids} videos in those events). The other {len(single)} are single uploads.</p>
<h3>Events with {name} ({len(kev)})</h3>{"".join(card(e) for e in kev)}
<h3>Single videos ({len(single)})</h3><div class="ev plain"><ol>{"".join(li(r) for r in single)}</ol></div>
<h3>Hashtag only</h3>
<details class="ev"><summary><span class="dt">Tag only</span><span class="pl">#{tag} in tags only ({len(tagonly)})</span><span class="meta">{hm(tag_secs)}</span><span class="nt">These videos have the hashtag in their tags but don't name {name} in the title or description. The channel adds such tags to many videos as standard tags, so most of these probably don't feature this singer.</span></summary><ol>{"".join(li(r) for r in tagonly)}</ol></details>
</section>'''
    with open(csvname, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Match', 'Event date', 'Place', 'Video title', 'Duration', 'URL'])
        for r in main:
            e = ev_of.get(r['id'])
            w.writerow(['Named in title/description', (e['key'] if e['key'] != '~' else 'unknown') if e else '', e['place'] if e else '', r['title'], r['duration_string'], 'https://youtu.be/' + r['id']])
        for e in kev:
            for v in e['videos']:
                if v['id'] not in main_ids:
                    w.writerow(['Same event, not named in this part', e['key'] if e['key'] != '~' else 'unknown', e['place'], v['title'], v['dur'], 'https://youtu.be/' + v['id']])
        for r in tagonly:
            w.writerow(['Hashtag only', '', '', r['title'], r['duration_string'], 'https://youtu.be/' + r['id']])
    print(name, kcount, 'events', len(kev), 'event-vids', kevvids, 'single', len(single), 'tagonly', len(tagonly))
    return kcount, sec

psecs = [(k, n) + person(k, n, t, c, p) for k, n, t, c, p in PEOPLE]
cards = ''.join(card(e) for e in E)
tot = sum(len(e['videos']) for e in E)

# ---- "All videos" listing tab (shared with the Kandas Bapu channel pages) ----
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '_shared'))
from listing_data import build_items, listing_data_json, listing_section, assets, write_videos_csv
SONAL_SINGERS = [
    ('Narayan Swami', r'નારાયણ ?(?:સ્વામી|બાપુ|બાપૂ)|નારાયણસ્વામી|narayan ?(?:swami|bapu)|narayanswami'),
    ('Kandas Bapu', r'k+a+n+a?d+a+s|કાનદાસ|કાંનદાસ|કાનાદાસ'),
    ('Laxman Barot', r'la?xa?man\s*barot|lakshman\s*barot|લક્ષ્?મણ\s*(?:બારોટ|બાપુ)|બારોટજી'),
    ('Niranjan Pandya', r'નિરંજન|niranjan'),
    ('Khetshi Gadhvi', r'ખેત[શસ]ી|khet[sh]+i'),
    ('Devraj Gadhvi', r'દેવરાજ|devraj|dervraj|moto dero|મોટો ડેરો'),
    ('Jagmal Barot', r'જગમાલ|jagmal'),
    ('Pranlal Vyas', r'પ્રાણલાલ|pranlal'),
    ('Bhikhudan Gadhvi', r'ભીખુદાન|bhikhudan'),
    ('Kirtidan Gadhvi', r'કિર્તીદાન|કીર્તિદાન|kirtidan'),
    ('Hari Gadhvi', r'હરિ ગઢવી|હરી ગઢવી|hari gadhvi'),
    ('Punshi Gadhvi', r'પુ[ંન]શી|punsh?i'),
    ('Meghraj Naran', r'મેઘરાજ|meghraj|megraj'),
    ('Parsotam Puri', r'પરસો[ત્]*તમ|parsot+am|parsotm'),
    ('Samrathsinh Sodha', r'સમરથ|samrath'),
    ('Arjangiri Bapu', r'અરજણ ?ગ[ીિ]રી|arjan ?giri'),
    ('Gahan Bharti', r'ગહન|gahan'),
    ('Shantilal Sadhu', r'શાંતિલાલ|shantilal'),
    ('Kamshri Mataji', r'કમશ્રી|kamas?h?ri'),
    ('Yogeshpuri Goswami', r'યોગેશ|yoges'),
    ('Sankar Marvada', r'શંકર મારવાડા|sankar marvada'),
    ('Bhartiben Vyas', r'ભારતીબેન|bhartiben'),
]
L_ROWS = json.load(open(S + '/sonal/all_listing.json', encoding='utf-8'))
L_LABELS = {v['id']: ('Date unknown' if e['key'] == '~' else e['key']) + ' · ' + e['place'] for e in E for v in e['videos']}
L_ITEMS = build_items(L_ROWS, L_LABELS, SONAL_SINGERS)
L_CSS, L_JS = assets()
write_videos_csv('data/sonal-videos.csv', L_ITEMS)

css = L_CSS + '''
:root{--bg:#faf8f4;--fg:#222;--mut:#6b6560;--card:#fff;--line:#e6e0d8;--acc:#a0461e;--flag:#8a5a00}
@media (prefers-color-scheme:dark){:root{--bg:#171513;--fg:#eee;--mut:#a39c94;--card:#211e1b;--line:#38332e;--acc:#e48a5c;--flag:#e0b35a}}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,"Noto Sans Gujarati",sans-serif}
main{max-width:960px;margin:0 auto;padding:24px 16px}h1{margin:0 0 12px;font-size:1.5rem}h2{font-size:1.25rem;margin:8px 0 4px}
h3{font-size:1rem;margin:20px 0 8px;color:var(--mut)}.sub{color:var(--mut);margin:0 0 16px}
nav{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 16px}nav button{padding:8px 14px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--fg);font:inherit;cursor:pointer}
nav button.on{background:var(--acc);border-color:var(--acc);color:#fff}
#qe{width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);font-size:15px;margin-bottom:16px}
.ev{background:var(--card);border:1px solid var(--line);border-radius:10px;margin:0 0 8px}.plain ol{padding-top:12px}
summary{cursor:pointer;padding:10px 14px;display:grid;grid-template-columns:110px 1fr auto;gap:2px 12px;align-items:baseline}
.dt{font-weight:600;color:var(--acc);font-variant-numeric:tabular-nums}.pl{font-weight:600}.meta{color:var(--mut);font-size:13px;white-space:nowrap}
.nt{grid-column:2/4;color:var(--mut);font-size:13px}ol{margin:0;padding:0 14px 12px 40px}li{margin:3px 0}a{color:var(--fg)}a:hover{color:var(--acc)}
.d{color:var(--mut);font-size:12px;font-variant-numeric:tabular-nums}.flag{margin:0 14px 6px;color:var(--flag);font-size:13px}
[hidden]{display:none!important}
@media (max-width:600px){summary{grid-template-columns:1fr auto}.pl{grid-column:1/3}.nt{grid-column:1/3}}
'''
js = '''
document.getElementById('qe').addEventListener('input',e=>{const q=e.target.value.toLowerCase();document.querySelectorAll('#all .ev').forEach(d=>d.style.display=d.dataset.s.includes(q)||d.textContent.toLowerCase().includes(q)?'':'none')});
''' + L_JS  # listing.js also handles the tab buttons and #hash
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sonal Audio Events</title><style>{css}</style></head><body><main><h1>Sonal Audio Old Bhajan – single-night events</h1>
<nav><button data-t="all" class="on">All events ({len(E)})</button><button data-t="list">All videos ({len(L_ITEMS)})</button>{"".join(f'<button data-t="{k}">{n} ({c})</button>' for k, n, c, s in psecs)}</nav>
<section id="all" class="tab"><p class="sub">{len(E)} events · {tot} videos grouped from titles &amp; descriptions of 1,016 channel videos. Click an event to see its parts in order. Download: <a href="data/events.csv">events.csv</a> · <a href="data/kandas-bapu.csv">kandas-bapu.csv</a> · <a href="data/laxman-barot.csv">laxman-barot.csv</a> · <a href="data/events.json">events.json</a></p>
<input id="qe" placeholder="Filter by year, place or singer (e.g. 1994, Samanda, Laxman)">{cards}</section>
{listing_section(L_ITEMS, "data/sonal-videos.csv", hidden=True)}
{"".join(s for k, n, c, s in psecs)}</main><script>const DATA={listing_data_json(L_ITEMS)};</script><script>{js}</script></body></html>'''
open('index.html', 'w', encoding='utf-8').write(page)

