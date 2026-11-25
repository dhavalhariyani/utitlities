(function () {
  var $ = function (id) { return document.getElementById(id); };
  var P, byId = {}, PAGE = 40, shown = PAGE, started = false;
  // data is fetched the first time the Playlists tab is opened
  function start() {
    if (started) return; started = true;
    $('pcount').textContent = 'Loading playlists…';
    fetch(window.PL_URL).then(function (r) { return r.json(); }).then(function (d) { P = d; init(); })
      .catch(function () { $('pcount').textContent = 'Could not load playlists.'; });
  }
  document.querySelectorAll('nav button[data-t="playlists"]').forEach(function (b) { b.addEventListener('click', start); });
  if (location.hash === '#playlists') start();
  function init() {
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var fmt = function (s) { var h = Math.floor(s / 3600), m = Math.round((s % 3600) / 60); return h ? h + 'h ' + (m < 10 ? '0' : '') + m + 'm' : m + 'm'; };
  var mk = function (id, opts) { opts.forEach(function (o) { var e = document.createElement('option'); e.textContent = o; $(id).appendChild(e); }); };
  var cnt = function (f) { var m = {}; P.forEach(function (p) { [].concat(f(p)).forEach(function (k) { m[k] = (m[k] || 0) + 1; }); }); return Object.keys(m).sort(function (a, b) { return m[b] - m[a]; }); };
  mk('pc', cnt(function (p) { return p.ch; })); mk('pa', cnt(function (p) { return p.a; }));
  P.forEach(function (p) { p._s = (p.t + ' ' + p.ch + ' ' + p.a.join(' ') + ' ' + p.v.map(function (v) { return v[1]; }).join(' ')).toLowerCase(); });
  function vids(p) {
    return p.v.map(function (v) {
      var u = 'https://www.youtube.com/watch?v=' + v[0] + '&list=' + p.id;
      return '<li class="vt"><img class="tn" src="https://i.ytimg.com/vi/' + v[0] + '/mqdefault.jpg" alt="" width="96" height="54" loading="lazy" decoding="async"><span><a href="' + u + '" target="_blank" rel="noopener">' + esc(v[1]) + '</a> <span class="d">' + (v[2] ? fmt(v[2]).replace(/^0m$/, '') : '') + '</span></span></li>';
    }).join('');
  }
  function run(reset) {
    if (reset) shown = PAGE;
    var words = $('pq').value.trim().toLowerCase().split(/\s+/).filter(Boolean), c = $('pc').value, a = $('pa').value, so = $('ps').value;
    var cur = P.filter(function (p) {
      if (c && p.ch !== c) return false;
      if (a && p.a.indexOf(a) < 0) return false;
      for (var i = 0; i < words.length; i++) if (p._s.indexOf(words[i]) < 0) return false;
      return true;
    });
    cur.sort({ big: function (x, y) { return y.s - x.s; }, num: function (x, y) { return y.v.length - x.v.length; }, az: function (x, y) { return x.t.localeCompare(y.t); }, ch: function (x, y) { return x.ch.localeCompare(y.ch) || y.s - x.s; } }[so]);
    var vc = cur.reduce(function (n, p) { return n + p.v.length; }, 0);
    $('pcount').textContent = cur.length + ' of ' + P.length + ' playlists · ' + vc.toLocaleString() + ' videos';
    $('pres').innerHTML = cur.slice(0, shown).map(function (p) {
      return '<details class="ev" data-i="' + p.id + '"><summary><span class="dt">' + esc(p.ch) + '</span><span class="pl">' + esc(p.t) + '</span><span class="meta">' + p.v.length + ' videos · ' + fmt(p.s) + '</span>' +
        '<span class="nt">' + (p.a.length ? p.a.map(function (s) { return '<span class="chip">' + esc(s) + '</span>'; }).join(' ') + ' · ' : '') + '<a href="https://www.youtube.com/playlist?list=' + p.id + '" target="_blank" rel="noopener">open on YouTube</a></span></summary><ol></ol></details>';
    }).join('');
    $('pmore').hidden = cur.length <= shown;
  }
  P.forEach(function (p) { byId[p.id] = p; });
  $('pres').addEventListener('toggle', function (e) {
    var d = e.target; if (!d.open || d.dataset.f) return; d.dataset.f = 1;
    d.querySelector('ol').innerHTML = vids(byId[d.dataset.i]);
  }, true);
  ['pq', 'pc', 'pa', 'ps'].forEach(function (id) { $(id).addEventListener(id === 'pq' ? 'input' : 'change', function () { run(true); }); });
  $('pmore').onclick = function () { shown += PAGE * 2; run(false); };
  run(true);
  }
})();
