import json, re, sys, collections, html, csv
sys.stdout.reconfigure(encoding='utf-8')
S = sys.argv[1]; OUT = sys.argv[2]
rows = json.load(open(S + '/all.json', encoding='utf-8'))
R = {i: r for i, r in enumerate(rows, 1)}
gu = str.maketrans('૦૧૨૩૪૫૬૭૮૯', '0123456789')

def secs(s):
    if not s: return 0
    p = [int(x) for x in s.split(':')]; t = 0
    for x in p: t = t * 60 + x
    return t

def rng(a, b): return list(range(a, b + 1))

# auto date groups
dated = collections.defaultdict(set)
for i, r in R.items():
    t = (r['title'] + ' ' + (r['description'] or '')).translate(gu)
    for d, m, y in re.findall(r'(?<!\d)(\d{1,2})\s*[-/.]\s*(\d{1,2})\s*[-/.]\s*((?:19|20)\d{2}|\d{2})(?!\d)', t):
        y = int(y); y = y + 1900 if 50 < y < 100 else (y + 2000 if y < 100 else y)
        if 1 <= int(m) <= 12 and 1 <= int(d) <= 31:
            dated[f'{y}-{int(m):02d}-{int(d):02d}'].add(i)

# (date/sort key, place, occasion/singers, indices, confidence note)
E = []
def ev(key, place, note, idx, conf='Confirmed'):
    E.append(dict(key=key, place=place, note=note, idx=sorted(set(idx)), conf=conf))

D = lambda k: dated[k]
ev('1980', 'Charan Boarding, Mandvi', 'Sonal Bij – Narayan Swami', [235, 255, 259, 266, 306, 328, 345])
ev('1981-12-28', 'Charan Boarding, Mandvi', 'Sonal Bij – Narayan Swami', D('1981-12-28'))
ev('1983-01-22', 'Charan Boarding, Mandvi', 'Sonal Bij – Narayan Swami', D('1983-01-22'))
ev('1984-01-19', 'Dwarka', 'Narayan Swami & Kandas Bapu', D('1984-01-19') | {897, 948, 996}, 'Parts 1-2 & "Bajrang Das Bapa ni Bandi" have no date, matched by place/singers')
ev('1985-11-10', 'Gitanjali, Bhuj', 'Veljibhai Ahir house vastu – Narayan Swami', D('1985-11-10'))
ev('1986-07-21', 'Narayan Ashram, Mandvi', 'Gurupunam – Narayan Swami', D('1986-07-21'))
ev('1987-05-16', 'Vadala', 'Narayan Swami, Jagmal Barot', D('1987-05-16'))
ev('1988-05-05', 'Vadala', 'Narayan Swami & Jagmal Barot (first jugalbandi)', D('1988-05-05'))
ev('1990-04-03', 'Faradi', 'Narayan Swami', D('1990-04-03'))
ev('1990-05-05', 'Bhanushali Nagar, Bhuj', 'Veljibhai Ahir house vastu – Narayan Swami', D('1990-05-05'))
ev('1991-03-02', 'Ramdarbar, Bhuj', 'Narayan Swami', D('1991-03-02'))
ev('1992-04-11', 'Ramgadh Lafra', 'Narayan Swami, Pranlal Vyas, Mina Patel, Amudan Gadhvi', D('1992-04-11') | {177, 183, 201, 208, 210}, 'Parts 01-05 say only "1992"; same title/singers')
ev('1992-05-02', 'Mota Bhadiya', 'Narayan Swami, Gahan Bharthi', D('1992-05-02'))
ev('1992-08-31', 'Makleshwar Mahadev, Meghpar-Borichi', 'Narayan Swami, Gahan Bharthi', D('1992-08-31'))
ev('1993', 'Desalpar', 'Narayan Swami & Laxman Barot', [958, 959, 960, 961, 962, 738])
ev('1993-07-03', 'Mandvi', 'Gurupunam – Narayan Swami, Devraj Gadhvi', D('1993-07-03'))
ev('1993-09-18', 'Bhuj', 'Narayan Swami, Devraj & Pradip Gadhvi', D('1993-09-18') | {50}, 'Part 03 says only "Bhuj 1993"')
ev('1994-01-23', 'Samanda', 'Narayan Swami, Niranjan Pandya, Samrathsinh Sodha', D('1994-01-23') | set(rng(31, 39)), 'Parts 14-22 say "Samanda 1994" only')
ev('1994-04-20', 'Ramgadh Lafra', 'Narayan Swami & Niranjan Pandya', D('1994-04-20'))
ev('1994-04-25', 'Bhojay', 'Narayan Swami, Laxman Barot', D('1994-04-25'))
ev('1995', 'Desalpar', 'Narayan Swami & Laxman Barot', rng(952, 957))
ev('1995-01-10', 'Mithapar', 'Sonal Bij – Kutchi santvani, Devraj Gadhvi, Jagmal Barot', D('1995-01-10'))
ev('1995-04-09', 'Lafra', 'Narayan Swami, Laxman Barot', D('1995-04-09'))
ev('1995-04-29', 'Koday, Mandvi', 'Narayan Swami & Laxman Barot', D('1995-04-29'))
ev('1995-06-06', 'Faradi', 'Narayan Swami, Yogeshpuri Goswami', D('1995-06-06'))
ev('1995-11-30', 'Faradi', 'Narayan Swami', D('1995-11-30'))
ev('1996', 'Kharoi', 'Narayan Swami & Niranjan Pandya', rng(914, 918))
ev('1996-01-01', 'Samanda', 'Narayan Swami, Khetshi Gadhvi, Yogeshpuri Goswami', D('1996-01-01'))
ev('1996-03-29', 'Lafra', 'Narayan Swami, Devraj Gadhvi', D('1996-03-29'))
ev('1997-01-25', 'Ghatkopar, Mumbai', 'Narayan Swami, Khetshi Gadhvi', D('1997-01-25') | set(rng(828, 832)) | {966}, 'Parts titled "Kandivali 1997" – description of Part-1 says Ghatkopar 1997; likely same program')
ev('1997-04-10', 'Ratadiya', 'Narayan Swami, Khetshi Gadhvi', D('1997-04-10'))
ev('1997-04-21', 'Antarjal', 'Narayan Swami, Arjangiri Bapu', D('1997-04-21'))
ev('1997-04-27', 'Ahmedabad', 'Narayan Swami & Laxman Barot', D('1997-04-27'))
ev('1997-10-27', 'Rajda Tekri', 'Moto Dero', [749, 750])
ev('1998-04-27', 'Bhuj', 'Veljibhai Ahir daughters\' wedding – Narayan Swami, Bhikhudan, Bhartiben Vyas', D('1998-04-27') | {186, 187}, '2 parts without date matched by title')
ev('1999-10-04', 'Pakadsar', 'Narayan Swami & Laxman Barot', D('1999-10-04'))
ev('2000-01-13', 'Dudhai', 'Narayan Swami, Shantilal Sadhu', D('2000-01-13'))
ev('2001-01-14', 'Kathda', 'Kutchi santvani – Sanga Bhagat, Khetshi Gadhvi', D('2001-01-14'))
ev('2003-02-06', 'Mota Ratadiya', 'Lok Dayro – Bhikhudan Gadhvi (Hansbai Mataji jayanti)', D('2003-02-06'))
ev('2003-05-10', 'Mota Bhadiya', 'Wedding – Laxman Barot, Punsi Gadhvi', D('2003-05-10'))
ev('2003-07-09', 'Nani Undoth', 'Vachhra Dada patotsav – Laxman Barot', D('2003-07-09'))
ev('2004', 'Mumbai', 'Sonal Bij – Devraj Gadhvi, Parsotam Puri, Jitudan Gadhvi', rng(815, 819) | {805} if False else rng(815, 819) + [805], 'Part-06 (no year) matched by singers')
ev('2004-01-26', 'Mota Ratadiya', 'Lok Dayro – Bhikhudan Gadhvi', D('2004-01-26'))
ev('2004-04-17', 'Antarjal', 'Laxman Barot & Parsotampuri Goswami', D('2004-04-17'))
ev('2005', 'Rajda Tekri, Mandvi', 'Laxman Barot, Devraj Gadhvi, Parsotam Puri (Katari)', [946, 965])
ev('2005', 'Rajda Tekri', 'Lok Dayro – Bhikhudan Gadhvi', rng(683, 685), 'Same place/year as the santvani above – may be the same night')
ev('2005', 'Bada', 'Program at Devraj Gadhvi\'s home – Niranjan Pandya, Laxman Barot, Parsotam Puri', [919, 920, 921, 923])
ev('2005', 'Mota Layja', 'Chodhari jugalbandi', rng(1008, 1013))
ev('2005-01-11', 'Mumbai', 'Sonal Bij – Laxman Barot, Parsotampuri Goswami', D('2005-01-11'))
ev('2005-01-12', 'Adipur', 'Sonal Bij – Laxman Barot, Devraj Gadhvi', D('2005-01-12') | {677})
ev('2005-12-14', 'Bada', 'Lok Dayro – Bhikhudan Gadhvi', D('2005-12-14'))
ev('2006', 'Mumbai', 'Sonal Bij – Laxman Barot, Devraj Gadhvi, Parsotam Puri', rng(898, 902) + [1016])
ev('2006-04-10', 'Nani Rayan', 'Dhoramnath Dada medo – Ramamandal', D('2006-04-10'))
ev('2006-05-12', 'Vinjan', 'Punsi Gadhvi, Jitugiri & Harsukhgiri Goswami', D('2006-05-12'))
ev('2006-12-22', 'Mumbai', 'Sonal Bij – Laxman Barot, Punsi Gadhvi', D('2006-12-22'))
ev('2007-10-07', 'Nani Undoth', 'Vachhra Dada medo – Kirtidan, Devraj Gadhvi', D('2007-10-07'))
ev('2008', 'Rajda Tekri', 'Laxman Barot, Jagmal Barot, Devraj, Punshi, Hari Gadhvi', rng(880, 887))
ev('2008-01-10', 'Adipur', 'Sonal Bij – Devraj Gadhvi, Kamshri Mataji', D('2008-01-10'))
ev('2008-01-11', 'Jamnagar', 'Sonal Bij – Laxman Barot, Devraj Gadhvi', D('2008-01-11'))
ev('2008-01-27', 'Kathda', 'Vajabhagat tithi – Devraj, Meghraj Naran, Khetshi', D('2008-01-27'))
ev('2008-02-18', 'Biru', 'Meldi Mataji patotsav', D('2008-02-18'))
ev('2008-03-22', 'Rampar-Abda', 'Hari Gadhvi, Meghraj Naran', D('2008-03-22'))
ev('2008-04-20', 'Gundiyali', 'Jagmal Barot, Parsotam Puri, Jayshri Mataji, Rasik Maraj', D('2008-04-20') | set(rng(490, 493)), 'Parts 3-6 have no date, matched by place/singers')
ev('2008-05-03', 'Khandiya (Patan)', 'Santvani', D('2008-05-03'))
ev('2008-05-04', 'Khandiya (Patan)', 'Dayro – Jaydev Gadhvi', D('2008-05-04'))
ev('2008-05-22', 'Azad Chowk', 'Kirtidan, Devraj Gadhvi', D('2008-05-22'))
ev('2008-05-24', 'Antarjal', 'Sailesh Maraj, Jitugiri, Kishor Vaghela', D('2008-05-24'))
ev('2008-06-03', 'Mota Bhadiya', 'Devraj, Hari Gadhvi, Meghraj Naran', D('2008-06-03'))
ev('2008-09-05', 'Babavadi, Mandvi', 'Devraj Gadhvi, Vijay Vaghela', D('2008-09-05'))
ev('2008-09-08', 'Nani Undoth', 'Devraj Gadhvi, Ramdas Gondaliya', rng(779, 783))
ev('2009', 'Undoth', 'Vachhra Dada – Sankar Marvada, Pradip, Hari Gadhvi', [461, 463, 464, 466, 467])
ev('2009', 'Nagalar', 'Nageshwar Mahadev – Devraj Gadhvi, Sonal Vyas', rng(545, 549))
ev('2009', 'Mota Bhadiya', 'Hanuman Mandir pran-pratishtha – Hari Gadhvi, Sailesh Maraj', rng(581, 584))
ev('2009', 'Kathda', 'Vaja Bhagat – Khetshi, Hari, Devraj Gadhvi', rng(833, 836))
ev('2009', 'Halapar', 'Ramdas Gondaliya, Parsotam Puri, Bhimsi Bhagat', rng(843, 846))
ev('2009', 'Pachotiya', 'Devraj, Hari, Punsi Gadhvi, Kishor Vaghela', rng(868, 873))
ev('2009-04-27', 'Mota Karodiya', 'Wedding – Devraj & Hari Gadhvi', D('2009-04-27'))
ev('2009-05-10', 'Buddhro', 'Bhimshi Bhagat, Isardan Gadhvi', D('2009-05-10'))
ev('2009-10-28', 'Narayan Swami Ashram, Mandvi', 'Bhagvat katha – Kirtidan, Nilesh Gadhvi', D('2009-10-28'))
ev('2010', 'Nani Rayan', 'Dhoramnath Dada medo – Sankar Marvada, Hari Gadhvi', rng(513, 515))
ev('2010', 'Kathda', 'Vaja Bhagat tithi – Kirtidan, Devraj, Khetshi', rng(823, 827))
ev('2010', 'Mota Karodiya', 'Momay Maa patotsav – Devraj Gadhvi, Laxman Barot', rng(853, 857))
ev('2019', 'Mota Ratadiya', 'Vachhra Dada medo – Vijay Gadhvi', rng(516, 519))
ev('2019', 'Kathda', 'Vajabhagat tithi', [470, 472, 473, 475, 479])
ev('2020-01-15', 'Kathda', 'Vajabhagat tithi', [407, 409, 413, 417, 421], '4 videos say "Kathda 2020" only')
# year unknown, place known
U = '~'
ev(U, 'Desalpar', 'Narayan Swami & Amarnathji Bapu', [185, 200, 206, 213, 220])
ev(U, 'Nagor, Bhuj', 'At Veljibhai Ahir\'s – Narayan Swami, Samrathsinh Sodha', [203, 236])
ev(U, 'Mulund (Brahmandeshwar), Mumbai', 'Narayan Swami & Kandas Bapu', [925, 949, 950, 951, 998])
ev(U, 'Hingariya', 'Kutchi santvani – Khetshi, Devraj, Punshi, Hari Gadhvi, Kamshri Mataji', [401, 406, 414, 416, 422, 424, 425, 428, 434, 436, 439, 442, 445, 447, 450])
ev(U, 'Miyani', 'Devshwar Mahadev patotsav – Aaradhi vani, Meghrajji Dada', [398, 404, 411, 418, 423, 427, 430, 432, 435, 438, 440, 444, 446, 448])
ev(U, 'Miyani', 'Devraj, Punsi, Hari Gadhvi, Jiviben Kapdi', rng(858, 862))
ev(U, 'Mandvi', 'Juni santvani – Narayan Swami, Kandas Bapu, Pravindan Gadhvi', rng(612, 627))
ev(U, 'Kathda', 'Vachhra Dada medo', rng(607, 611))
ev(U, 'Lodai', 'Mekaran Dada patotsav', rng(642, 646))
ev(U, 'Koday', 'Bhagvat katha santvani – Jagmal Barot, Punshi Gadhvi', rng(658, 661))
ev(U, 'Luni', 'Narayan Swami, Gahan Bharti', rng(662, 666))
ev(U, 'Bharapar (Hajal Dada)', 'Narayan Swami, Laxman Barot', rng(674, 676))
ev(U, 'Koday (Koteshwar Mahadev)', 'Jagmal Barot, Punshi Gadhvi, Parsotam Puri', rng(697, 701))
ev(U, 'Nana Ratadiya', 'Sonal Sangar, Ketan Devadiya and others', rng(708, 713))
ev(U, 'Nani Undoth (Nagnath Mahadev)', 'Laxman Barot, Rajesh Gadhvi', rng(728, 733))
ev(U, 'Antarjal', 'Ramamandal', rng(756, 761))
ev(U, 'Bedli', 'Narayan Swami, Kandas Bapu', rng(769, 773))
ev(U, 'Nani Rayan', 'Dhoramnath Dada – Karsan Sagthiya, Vijay Vaghela', rng(774, 778))
ev(U, 'Nani Rayan', 'Stage program – Kandas Bapu, Narayan Swami', [707, 412], 'Matched by place/singers only')
ev(U, 'Jogninar', 'Laxman Barot', rng(796, 800))
ev(U, 'Rajda Tekri', 'Aaradhi santvani', rng(888, 892))
ev(U, 'Biru', 'Aaradhi santvani', rng(893, 896))
ev(U, 'Pachotiya', 'Moto Dero, Nano Dero', rng(907, 909))
ev(U, 'Sekhadiya', 'Moto Dero, Kamshri Mataji', [910, 911])
ev(U, 'Bhujpar', 'Moto Dero, Pranlal Vyas', [748, 786, 202], 'Matched by place only')
ev(U, 'Adipur', 'Goswami samaj samuh lagna – Laxman Barot, Kirtidan, Yogeshpuri', rng(531, 537))
ev(U, 'Devaliya', 'Narayan Swami, Khetshi Gadhvi', [158, 165, 169, 217])
ev(U, 'Pithora Pir, Bhuj', 'Antim santvani (last program) – Narayan Swami', rng(993, 995))
# place unknown – numbered parts of one program
ev(U, '(place not given)', '"Jaher Santvani" – Narayan Swami', rng(787, 795), 'Part series, no place/date')
ev(U, '(place not given)', '"Jabri Jugalbandhi" – Narayan Swami & Niranjan Pandya', rng(936, 942), 'Part series, no place/date')
ev(U, '(place not given)', 'Live santvani – Kirtidan Gadhvi', rng(926, 935), 'Part series, no place/date')
ev(U, '(place not given)', '"Alakh no Aaradh" – Narayan Swami', rng(735, 737), 'Part series, no place/date')
ev(U, '(place not given)', '"Aasu Akhadima Aani" – Narayan Swami, Khetshi Gadhvi', rng(585, 588), 'Part series, no place/date')

used = set(i for e in E for i in e['idx'])
dup = [i for i, c in collections.Counter(i for e in E for i in e['idx']).items() if c > 1]
print('videos grouped', len(used), 'events', len(E), 'dups', dup)
print('dated not used:', sorted(i for k, v in dated.items() for i in v if i not in used))

for e in E:
    vids = []
    for i in e['idx']:
        r = R[i]
        vids.append(dict(id=r['id'], title=r['title'], dur=r['duration_string'], up=r['upload_date']))
    def partno(v):
        t = v['title'].translate(gu)
        m = re.search(r'(?:Part|ભાગ)\s*-?\s*(\d+)', t, re.I) or re.match(r'\s*(\d{1,2})\b', t)
        return int(m.group(1)) if m else 99
    vids.sort(key=lambda v: (partno(v), v['up']))
    e['videos'] = vids
    e['secs'] = sum(secs(v['dur']) for v in vids)

E.sort(key=lambda e: (e['key'] == U, e['key'], e['place']))
json.dump(E, open(OUT + '/events.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(OUT + '/events.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Event date', 'Place', 'Program / singers', 'Note', 'Part order', 'Video title', 'Duration', 'URL'])
    for e in E:
        for n, v in enumerate(e['videos'], 1):
            w.writerow([e['key'] if e['key'] != U else 'unknown', e['place'], e['note'], '' if e['conf'] == 'Confirmed' else e['conf'], n, v['title'], v['dur'], 'https://youtu.be/' + v['id']])
print('total secs', sum(e['secs'] for e in E) / 3600)
