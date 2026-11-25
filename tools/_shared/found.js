(function () {
  var $ = function (id) { return document.getElementById(id); };
  var D, items, PAGE = 60, shown = PAGE, started = false;
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var dur = function (s) { if (!s) return ''; var h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60; return (h ? h + ':' + (m < 10 ? '0' : '') : '') + m + ':' + (x < 10 ? '0' : '') + x; };
  function start() {
    if (started) return; started = true; $('fcount').textContent = 'Loading…';
    fetch(window.FOUND_URL).then(function (r) { return r.json(); }).then(function (d) { D = d; init(); })
      .catch(function () { $('fcount').textContent = 'Could not load the list.'; });
  }
  document.querySelectorAll('nav button[data-t="found"]').forEach(function (b) { b.addEventListener('click', start); });
  if (location.hash === '#found') start();
  function init() {
    items = D.v.map(function (v) { return { id: v[0], t: v[1], c: D.c[v[2]], s: v[3], e: v[4], _s: (v[1] + ' ' + D.c[v[2]]).toLowerCase() }; });
    var cnt = {}; items.forEach(function (i) { cnt[i.c] = (cnt[i.c] || 0) + 1; });
    Object.keys(cnt).sort(function (a, b) { return cnt[b] - cnt[a]; }).forEach(function (c) { var o = document.createElement('option'); o.value = c; o.textContent = c + ' (' + cnt[c] + ')'; $('fc').appendChild(o); });
    ['fq', 'fc', 'fo', 'fv'].forEach(function (id) { $(id).addEventListener(id === 'fq' ? 'input' : 'change', function () { run(true); }); });
    $('fmore').onclick = function () { shown += PAGE * 2; run(false); };
    run(true);
  }
  function li(i) {
    var u = 'https://youtu.be/' + i.id;
    return '<li class="vt"><img class="tn" src="https://i.ytimg.com/vi/' + i.id + '/mqdefault.jpg" alt="" width="96" height="54" loading="lazy" decoding="async"><span><a href="' + u + '" target="_blank" rel="noopener">' + esc(i.t) + '</a> <span class="d">' + dur(i.s) + '</span><br><span class="d">' + esc(i.c) + '</span></span></li>';
  }
  function events(w, c) {
    var out = [], n = 0, vn = 0;
    D.e.forEach(function (e) {
      var vs = e[4].map(function (ix) { return items[ix]; });
      if (c && !vs.some(function (i) { return i.c === c; })) return;
      if (w.length && !w.every(function (k) { return (e[0] + ' ' + e[1] + ' ' + e[2] + ' ' + vs.map(function (i) { return i._s; }).join(' ')).toLowerCase().indexOf(k) >= 0; })) return;
      n++; vn += vs.length;
      var tot = vs.reduce(function (a, i) { return a + i.s; }, 0), chs = {}; vs.forEach(function (i) { chs[i.c] = 1; });
      var flag = e[3] === 'Confirmed' ? '' : '<p class="flag">⚠ ' + esc(e[3]) + '</p>';
      out.push('<details class="ev"><summary><span class="dt">' + (e[0] === '~' ? 'Date unknown' : esc(e[0])) + '</span><span class="pl">' + esc([e[1], e[2]].filter(Boolean).join(' · ') || '(place not given)') + '</span><span class="meta">' + vs.length + ' videos · ' + Math.round(tot / 60) + 'm</span><span class="nt">' + esc(Object.keys(chs).join(', ')) + '</span></summary>' + flag + '<ol>' + vs.map(li).join('') + '</ol></details>');
    });
    $('fev').innerHTML = out.join('');
    $('fcount').textContent = n + ' events · ' + vn + ' videos. Click an event to see its parts.';
  }
  function run(reset) {
    var view = $('fv').value;
    $('fev').hidden = view !== 'ev'; $('fres').hidden = view === 'ev'; $('fmore').hidden = true; $('fo').hidden = view === 'ev';
    if (view === 'ev') { events($('fq').value.trim().toLowerCase().split(/\s+/).filter(Boolean), $('fc').value); return; }
    if (reset) shown = PAGE;
    var w = $('fq').value.trim().toLowerCase().split(/\s+/).filter(Boolean), c = $('fc').value, o = $('fo').value;
    var cur = items.filter(function (i) { if (c && i.c !== c) return false; if (view === 'solo' && i.e >= 0) return false; for (var k = 0; k < w.length; k++) if (i._s.indexOf(w[k]) < 0) return false; return true; });
    if (o === 'long') cur = cur.slice().sort(function (a, b) { return b.s - a.s; });
    else if (o === 'az') cur = cur.slice().sort(function (a, b) { return a.t.localeCompare(b.t); });
    var tot = cur.reduce(function (n, i) { return n + i.s; }, 0);
    $('fcount').textContent = cur.length.toLocaleString() + ' of ' + items.length.toLocaleString() + ' videos · ' + Math.round(tot / 3600).toLocaleString() + ' hours';
    $('fres').innerHTML = cur.slice(0, shown).map(li).join('');
    $('fmore').hidden = cur.length <= shown;
  }
})();
