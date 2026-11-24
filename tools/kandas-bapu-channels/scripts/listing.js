(function () {
  var $ = function (id) { return document.getElementById(id); };
  var items = DATA.items, PAGE = 60, shown = PAGE;
  // tabs
  var show = function (t) {
    document.querySelectorAll('nav button').forEach(function (b) { b.classList.toggle('on', b.dataset.t === t); });
    document.querySelectorAll('section.tab').forEach(function (s) { s.hidden = s.id !== t; });
    try { history.replaceState(null, '', '#' + t); } catch (e) {}
  };
  document.querySelectorAll('nav button').forEach(function (b) { b.onclick = function () { show(b.dataset.t); }; });
  if (location.hash === '#events') show('events');
  // filter options
  DATA.singers.forEach(function (s) { var o = document.createElement('option'); o.textContent = s; $('fs').appendChild(o); });
  DATA.years.forEach(function (y) { var o = document.createElement('option'); o.textContent = y; $('fy').appendChild(o); });
  // search index: lower-case title + description + singers + event
  items.forEach(function (it) { it._s = (it.t + ' ' + it.d + ' ' + it.sg.join(' ') + ' ' + it.ev).toLowerCase(); });
  var esc = function (s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var hl = function (s, words) {
    var h = esc(s);
    words.forEach(function (w) {
      if (!w) return;
      var re = new RegExp('(' + esc(w).replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
      h = h.replace(re, '<mark>$1</mark>');
    });
    return h;
  };
  var fmtUp = function (u) { return u ? u.slice(0, 4) + '-' + u.slice(4, 6) + '-' + u.slice(6) : ''; };
  var current = [];
  function run(reset) {
    if (reset) shown = PAGE;
    var q = $('q').value.trim().toLowerCase(), words = q.split(/\s+/).filter(Boolean);
    var fs = $('fs').value, fy = $('fy').value, fk = $('fk').value, fe = $('fe').value, so = $('so').value;
    current = items.filter(function (it) {
      if (fs && it.sg.indexOf(fs) < 0) return false;
      if (fy === 'none' ? it.y : (fy && String(it.y) !== fy)) return false;
      if (fk && it.k !== fk) return false;
      if (fe === '1' && !it.ev) return false;
      if (fe === '0' && it.ev) return false;
      for (var i = 0; i < words.length; i++) if (it._s.indexOf(words[i]) < 0) return false;
      return true;
    });
    var cmp = {
      new: function (a, b) { return a.n - b.n; },
      old: function (a, b) { return b.n - a.n; },
      rec: function (a, b) { return (a.y || 9999) - (b.y || 9999) || a.n - b.n; },
      long: function (a, b) { return b.s - a.s; },
      views: function (a, b) { return b.v - a.v; }
    }[so];
    current.sort(cmp);
    var tot = current.reduce(function (s, it) { return s + (it.s || 0); }, 0), h = Math.floor(tot / 3600);
    $('count').textContent = current.length + ' of ' + items.length + ' videos · ' + h + 'h ' + Math.round((tot % 3600) / 60) + 'm total';
    $('res').innerHTML = current.slice(0, shown).map(function (it) {
      var chips = it.sg.map(function (s) { return '<span class="chip">' + esc(s) + '</span>'; }).join('');
      if (it.ev) chips += '<span class="chip e">Event: ' + esc(it.ev) + '</span>';
      return '<li><a class="t" href="https://youtu.be/' + it.id + '" target="_blank" rel="noopener">' + hl(it.t, words) + '</a>' +
        '<div class="m"><span>' + it.k + '</span><span>' + esc(it.dur) + '</span><span>uploaded ' + fmtUp(it.up) + '</span>' +
        (it.y ? '<span>recorded ' + it.y + '</span>' : '') + '<span>' + it.v.toLocaleString() + ' views</span>' + chips + '</div>' +
        (it.d ? '<div class="x">' + hl(it.d, words) + '</div>' : '') + '</li>';
    }).join('');
    $('more').hidden = current.length <= shown;
  }
  ['q', 'fs', 'fy', 'fk', 'fe', 'so'].forEach(function (id) { $(id).addEventListener(id === 'q' ? 'input' : 'change', function () { run(true); }); });
  $('more').onclick = function () { shown += PAGE * 2; run(false); };
  run(true);
})();
