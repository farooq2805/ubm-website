(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var num = function (id) { var v = parseFloat(($(id) || {}).value); return isFinite(v) ? v : 0; };
  var r1 = function (v) { return Math.round(v * 10) / 10; };
  var r0 = function (v) { return Math.round(v).toLocaleString("en-IN"); };
  var IN = 39.3701;
  function cta(id, text) {
    var a = $(id + "-cta"); if (!a) return;
    a.href = "../../contact/?plan=" + encodeURIComponent("AV calculator result: " + text) + "#enquiry";
  }
  function show(id, rows, summary) {
    $(id + "-out").innerHTML = rows.map(function (r) { return '<div class="res"><span>' + r[0] + "</span><strong>" + r[1] + "</strong></div>"; }).join("");
    cta(id, summary);
  }
  var SIZES = [55, 65, 75, 86, 98, 110, 120, 135, 150, 180, 200];

  // 1. Display size from farthest viewer (4-6-8 rule)
  function screen() {
    var d = num("s-dist"), k = num("s-type"), ar = $("s-ar").value === "16:10" ? [16, 10] : [16, 9];
    if (!d) return;
    var h = d / k, w = h * ar[0] / ar[1], diag = Math.sqrt(w * w + h * h) * IN;
    var pick = SIZES.filter(function (s) { return s >= diag; })[0];
    var rec = pick ? (pick <= 98 ? pick + '" flat panel' : pick + '" projection screen or LED wall') : "LED wall or large projection";
    show("s", [["Minimum image height", r1(h * 100) + " cm"], ["Minimum image width", r1(w * 100) + " cm"], ["Minimum diagonal", r0(diag) + '"'], ["Recommended", rec]],
      "Farthest viewer " + d + " m, content factor " + k + ", needs at least " + r0(diag) + "\" diagonal; recommended " + rec);
  }
  // 2. Projector brightness
  function lumens() {
    var diag = num("l-diag") / IN, gain = num("l-gain") || 1, nits = num("l-amb");
    if (!diag) return;
    var w = diag * 16 / Math.sqrt(337), h = diag * 9 / Math.sqrt(337), area = w * h;
    var lm = nits * area * Math.PI / gain, rec = lm * 1.3;
    show("l", [["Screen area", r1(area) + " m²"], ["Lumens needed", r0(lm) + " lm"], ["Recommended (30% headroom)", r0(Math.ceil(rec / 500) * 500) + " lm"]],
      num("l-diag") + "\" screen, target " + nits + " nits, gain " + gain + " needs about " + r0(Math.ceil(rec / 500) * 500) + " lumens");
  }
  // 3. Throw distance
  function throwd() {
    var diag = num("t-diag") / IN, tr = num("t-ratio");
    if (!diag || !tr) return;
    var w = diag * 16 / Math.sqrt(337), d = w * tr;
    show("t", [["Image width", r1(w) + " m"], ["Lens-to-screen distance", r1(d) + " m"], ["Projector type", tr < 0.4 ? "Ultra short throw" : tr < 1 ? "Short throw" : "Standard throw"]],
      num("t-diag") + "\" image at throw ratio " + tr + " needs the projector about " + r1(d) + " m from the screen");
  }
  // 4. LED wall
  function led() {
    var W = num("v-w"), H = num("v-h"), p = num("v-pitch");
    if (!W || !H || !p) return;
    var px = Math.round(W * 1000 / p), py = Math.round(H * 1000 / p);
    var label = px >= 3840 ? "4K or higher" : px >= 1920 ? "Full HD or higher" : "Below Full HD";
    show("v", [["Resolution", px + " × " + py + " px (" + label + ")"], ["Minimum viewing distance", r1(p) + " m"], ["Comfortable viewing distance", r1(p * 2.5) + " to " + r1(p * 3.5) + " m"], ["Wall area", r1(W * H) + " m²"]],
      "LED wall " + W + " × " + H + " m at P" + p + " gives " + px + "×" + py + " px, best viewed from " + r1(p * 2.5) + " m");
  }
  // 5. Ceiling speakers
  function spk() {
    var L = num("c-len"), Wd = num("c-wid"), ch = num("c-height"), ear = num("c-ear"), disp = num("c-disp"), lay = num("c-layout");
    if (!L || !Wd || ch <= ear) return;
    var dia = 2 * (ch - ear) * Math.tan(disp / 2 * Math.PI / 180), sp = dia * lay;
    var nx = Math.max(1, Math.ceil(L / sp)), ny = Math.max(1, Math.ceil(Wd / sp));
    show("c", [["Coverage circle at ear height", r1(dia) + " m diameter"], ["Speaker spacing", r1(sp) + " m"], ["Layout", nx + " × " + ny + " grid"], ["Speakers needed", String(nx * ny)]],
      "Room " + L + "×" + Wd + " m, ceiling " + ch + " m: about " + (nx * ny) + " ceiling speakers in a " + nx + "×" + ny + " grid");
  }
  // 6. Amplifier for 70V / 100V line
  function amp() {
    var n = num("a-n"), tap = num("a-tap");
    if (!n || !tap) return;
    var load = n * tap, need = load * 1.25, std = [60, 120, 240, 360, 480, 650, 1000, 1500, 2000];
    var pick = std.filter(function (s) { return s >= need; })[0];
    show("a", [["Total speaker load", r0(load) + " W"], ["With 25% headroom", r0(need) + " W"], ["Suggested amplifier", pick ? pick + " W (70V/100V)" : "Split across multiple amplifiers or zones"]],
      n + " speakers at " + tap + " W tap: " + r0(load) + " W load, suggested amplifier " + (pick ? pick + " W" : "multiple amps"));
  }
  var map = { s: screen, l: lumens, t: throwd, v: led, c: spk, a: amp };
  Object.keys(map).forEach(function (k) {
    var f = document.querySelector('[data-calc="' + k + '"]'); if (!f) return;
    f.addEventListener("input", map[k]); f.addEventListener("change", map[k]); map[k]();
  });
  // tabs
  var tabs = document.querySelectorAll(".calc-tabs button");
  tabs.forEach(function (b) {
    b.addEventListener("click", function () {
      tabs.forEach(function (x) { x.setAttribute("aria-selected", x === b ? "true" : "false"); });
      document.querySelectorAll(".calc").forEach(function (c) { c.hidden = c.id !== b.getAttribute("aria-controls"); });
      if (history.replaceState) history.replaceState(null, "", "#" + b.getAttribute("aria-controls"));
    });
  });
  var h = location.hash.slice(1), start = document.querySelector('.calc-tabs [aria-controls="' + h + '"]');
  if (start) start.click();
})();
(function () {
  "use strict";
  // ---- 1) Drag sliders next to every number input ----
  var RANGE = { "s-dist": [2, 40, 0.5], "l-diag": [50, 300, 5], "l-gain": [0.6, 2.5, 0.1], "t-diag": [50, 300, 5], "t-ratio": [0.25, 3, 0.05],
    "v-w": [1, 20, 0.25], "v-h": [0.5, 10, 0.25], "c-len": [3, 50, 0.5], "c-wid": [3, 40, 0.5], "c-height": [2.4, 8, 0.1], "a-n": [1, 120, 1] };
  Object.keys(RANGE).forEach(function (id) {
    var inp = document.getElementById(id); if (!inp) return;
    var r = document.createElement("input"); r.type = "range"; r.className = "rng";
    r.min = RANGE[id][0]; r.max = RANGE[id][1]; r.step = RANGE[id][2]; r.value = inp.value; r.setAttribute("aria-label", inp.parentNode.firstChild.textContent);
    var wrap = document.createElement("div"); wrap.className = "rng-wrap"; inp.parentNode.insertBefore(wrap, inp); wrap.appendChild(r); wrap.appendChild(inp);
    var paint = function () { var p = (r.value - r.min) / (r.max - r.min) * 100; r.style.background = "linear-gradient(90deg,#1f4fb8 " + p + "%,#dce7fd " + p + "%)"; };
    r.addEventListener("input", function () { inp.value = r.value; paint(); inp.dispatchEvent(new Event("input", { bubbles: true })); });
    inp.addEventListener("input", function () { r.value = inp.value; paint(); });
    paint();
  });

  // ---- 2) Live visuals ----
  var $ = function (id) { return document.getElementById(id); };
  var v = function (id) { var x = parseFloat(($(id) || {}).value); return isFinite(x) ? x : 0; };
  var IN = 39.3701, clamp = function (x, a, b) { return Math.max(a, Math.min(b, x)); };
  var svg = function (w, h, body) { return '<svg viewBox="0 0 ' + w + " " + h + '" xmlns="http://www.w3.org/2000/svg">' + body + "</svg>"; };
  var T = function (x, y, s, o) { return '<text x="' + x + '" y="' + y + '" fill="' + ((o && o.c) || "#dfe8fb") + '" font-size="' + ((o && o.z) || 11) + '" font-family="Archivo,sans-serif" font-weight="' + ((o && o.w) || 600) + '" text-anchor="' + ((o && o.a) || "middle") + '">' + s + "</text>"; };
  var person = function (x, y, s, c) { s = s || 1; c = c || "#9fd0ff"; return '<g fill="' + c + '"><circle cx="' + x + '" cy="' + (y - 34 * s) + '" r="' + 6 * s + '"/><rect x="' + (x - 7 * s) + '" y="' + (y - 27 * s) + '" width="' + 14 * s + '" height="' + 22 * s + '" rx="' + 5 * s + '"/><rect x="' + (x - 6 * s) + '" y="' + (y - 7 * s) + '" width="' + 12 * s + '" height="' + 7 * s + '" rx="2"/></g>'; };

  var VIZ = {
    s: function () {
      var d = v("s-dist"), k = v("s-type"), h = d / k, ar = $("s-ar").value === "16:10" ? 1.6 : 16 / 9, diag = Math.sqrt(Math.pow(h * ar, 2) + h * h) * IN;
      var sc = 300 / Math.max(d + 1, 6), sx = 40, fy = 150, sh = clamp(h * sc, 8, 120), vx = sx + d * sc;
      return svg(380, 180, '<rect x="0" y="0" width="380" height="180" rx="12" fill="#0f2c6e"/>' +
        '<line x1="20" y1="' + fy + '" x2="360" y2="' + fy + '" stroke="#3b5ba8" stroke-width="2"/>' +
        '<rect x="' + (sx - 6) + '" y="' + (fy - 30 - sh) + '" width="8" height="' + sh + '" rx="2" fill="#9fd0ff"><animate attributeName="opacity" values=".7;1;.7" dur="2.4s" repeatCount="indefinite"/></rect>' +
        '<path d="M' + (sx + 2) + ' ' + (fy - 30 - sh) + ' L' + vx + ' ' + (fy - 34) + ' L' + (sx + 2) + ' ' + (fy - 30) + 'Z" fill="rgba(159,208,255,.15)"/>' +
        person(vx, fy, 1) + '<line x1="' + sx + '" y1="' + (fy + 14) + '" x2="' + vx + '" y2="' + (fy + 14) + '" stroke="#9fd0ff" stroke-dasharray="4 3"/>' +
        T((sx + vx) / 2, fy + 28, d + " m to the last row") + T(sx + 14, fy - 38 - sh, Math.round(diag) + '" screen', { a: "start", c: "#fff", z: 13, w: 800 }));
    },
    l: function () {
      var amb = v("l-amb"), diag = v("l-diag") / IN, gain = v("l-gain") || 1, w = diag * 16 / Math.sqrt(337), hh = diag * 9 / Math.sqrt(337), lm = amb * w * hh * Math.PI / gain * 1.3;
      var suns = amb >= 350 ? 3 : amb >= 220 ? 2 : amb >= 120 ? 1 : 0, glow = clamp(lm / 9000, .25, 1);
      var bulbs = ""; for (var i = 0; i < suns; i++) bulbs += '<circle cx="' + (300 + i * 24) + '" cy="30" r="8" fill="#ffd166"/><circle cx="' + (300 + i * 24) + '" cy="30" r="13" fill="none" stroke="#ffd166" stroke-opacity=".4"/>';
      var meter = clamp(lm / 12000, .05, 1) * 300;
      return svg(380, 180, '<rect width="380" height="180" rx="12" fill="' + (suns ? "#1d3d84" : "#0a1f52") + '"/>' + bulbs +
        '<rect x="70" y="30" width="200" height="112" rx="4" fill="#fff" fill-opacity="' + glow + '"/><rect x="70" y="30" width="200" height="112" rx="4" fill="none" stroke="#9fd0ff"/>' +
        T(170, 92, Math.round(lm / 100) * 100 + " lm", { c: "#0f2c6e", z: 18, w: 800 }) +
        '<rect x="40" y="158" width="300" height="8" rx="4" fill="#2b4c96"/><rect x="40" y="158" width="' + meter + '" height="8" rx="4" fill="#9fd0ff"/>' + T(40, 152, "Brightness needed", { a: "start", z: 10 }));
    },
    t: function () {
      var diag = v("t-diag") / IN, tr = v("t-ratio"), w = diag * 16 / Math.sqrt(337), d = w * tr;
      var sc = 280 / Math.max(d, w, 2), sw = clamp(w * sc, 20, 150), px = 340 - d * sc;
      return svg(380, 180, '<rect width="380" height="180" rx="12" fill="#0f2c6e"/>' + T(190, 20, "Top view", { z: 10, c: "#9fb3da" }) +
        '<path d="M' + (px + 16) + ' 90 L340 ' + (90 - sw / 2) + ' L340 ' + (90 + sw / 2) + 'Z" fill="rgba(159,208,255,.22)"><animate attributeName="fill-opacity" values=".6;1;.6" dur="2s" repeatCount="indefinite"/></path>' +
        '<rect x="' + (px - 6) + '" y="80" width="24" height="20" rx="4" fill="#fff"/><circle cx="' + (px + 16) + '" cy="90" r="4" fill="#9fd0ff"/>' +
        '<rect x="340" y="' + (90 - sw / 2) + '" width="6" height="' + sw + '" fill="#9fd0ff"/>' +
        '<line x1="' + px + '" y1="150" x2="340" y2="150" stroke="#9fd0ff" stroke-dasharray="4 3"/>' + T((px + 340) / 2, 166, (Math.round(d * 10) / 10) + " m throw", { c: "#fff", z: 12, w: 800 }) +
        T(358, 90 - sw / 2 - 6, (Math.round(w * 10) / 10) + " m", { z: 10 }));
    },
    v: function () {
      var W = v("v-w"), H = v("v-h"), p = v("v-pitch"), cw = 0.5, nx = Math.max(1, Math.round(W / cw)), ny = Math.max(1, Math.round(H / cw));
      var maxW = 330, maxH = 130, sc = Math.min(maxW / W, maxH / H), tw = W * sc, th = H * sc, x0 = (380 - tw) / 2, y0 = 18, g = "";
      for (var i = 0; i < nx; i++) for (var j = 0; j < ny; j++) {
        var hue = 205 + ((i * 7 + j * 11) % 40);
        g += '<rect x="' + (x0 + i * tw / nx + .5) + '" y="' + (y0 + j * th / ny + .5) + '" width="' + (tw / nx - 1) + '" height="' + (th / ny - 1) + '" fill="hsl(' + hue + ',70%,' + (35 + ((i + j) % 3) * 8) + '%)"/>';
      }
      var px = Math.round(W * 1000 / p), py = Math.round(H * 1000 / p);
      return svg(380, 180, '<rect width="380" height="180" rx="12" fill="#0a1f52"/><g><animate attributeName="opacity" values=".85;1;.85" dur="3s" repeatCount="indefinite"/>' + g + "</g>" +
        T(190, 168, px + " × " + py + " px · " + (nx * ny) + " cabinets (500 mm)", { c: "#fff", z: 12, w: 800 }));
    },
    c: function () {
      var L = v("c-len"), Wd = v("c-wid"), ch = v("c-height"), ear = v("c-ear"), disp = v("c-disp"), lay = v("c-layout");
      if (ch <= ear) return "";
      var dia = 2 * (ch - ear) * Math.tan(disp / 2 * Math.PI / 180), sp = dia * lay, nx = Math.max(1, Math.ceil(L / sp)), ny = Math.max(1, Math.ceil(Wd / sp));
      var sc = Math.min(330 / L, 140 / Wd), rw = L * sc, rh = Wd * sc, x0 = (380 - rw) / 2, y0 = 14, g = "";
      for (var i = 0; i < nx; i++) for (var j = 0; j < ny; j++) {
        var cx = x0 + (i + .5) * rw / nx, cy = y0 + (j + .5) * rh / ny;
        g += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (dia / 2 * sc) + '" fill="rgba(159,208,255,.16)" stroke="rgba(159,208,255,.5)"/><circle cx="' + cx + '" cy="' + cy + '" r="4" fill="#fff"/>';
      }
      return svg(380, 180, '<rect width="380" height="180" rx="12" fill="#0f2c6e"/><defs><clipPath id="room"><rect x="' + x0 + '" y="' + y0 + '" width="' + rw + '" height="' + rh + '"/></clipPath></defs>' +
        '<g clip-path="url(#room)">' + g + '</g><rect x="' + x0 + '" y="' + y0 + '" width="' + rw + '" height="' + rh + '" fill="none" stroke="#9fd0ff" stroke-width="2"/>' +
        T(190, 172, (nx * ny) + " speakers · " + L + " × " + Wd + " m room", { c: "#fff", z: 12, w: 800 }));
    },
    a: function () {
      var n = v("a-n"), tap = v("a-tap"), load = n * tap, std = [60, 120, 240, 360, 480, 650, 1000, 1500, 2000], need = load * 1.25, amp = std.filter(function (s) { return s >= need; })[0] || need;
      var icons = "", shown = Math.min(n, 40);
      for (var i = 0; i < shown; i++) icons += '<rect x="' + (24 + (i % 20) * 16.5) + '" y="' + (22 + Math.floor(i / 20) * 22) + '" width="12" height="16" rx="3" fill="#9fd0ff"/><circle cx="' + (30 + (i % 20) * 16.5) + '" cy="' + (32 + Math.floor(i / 20) * 22) + '" r="3" fill="#0f2c6e"/>';
      var lw = clamp(load / amp, 0, 1) * 330, hw = clamp(need / amp, 0, 1) * 330;
      return svg(380, 180, '<rect width="380" height="180" rx="12" fill="#0f2c6e"/>' + icons + (n > 40 ? T(350, 80, "+" + (n - 40), { z: 11 }) : "") +
        '<rect x="24" y="112" width="330" height="18" rx="9" fill="#2b4c96"/><rect x="24" y="112" width="' + hw + '" height="18" rx="9" fill="rgba(159,208,255,.4)"/><rect x="24" y="112" width="' + lw + '" height="18" rx="9" fill="#9fd0ff"/>' +
        T(24, 104, "Speaker load " + Math.round(load) + " W", { a: "start", z: 10 }) + T(354, 104, "Amplifier " + Math.round(amp) + " W", { a: "end", z: 10 }) +
        T(190, 160, Math.round(load / amp * 100) + "% of amplifier capacity used", { c: "#fff", z: 12, w: 800 }));
    }
  };
  Object.keys(VIZ).forEach(function (k) {
    var f = document.querySelector('[data-calc="' + k + '"]'), box = $(k + "-viz"); if (!f || !box) return;
    var draw = function () { box.innerHTML = VIZ[k](); };
    f.addEventListener("input", draw); f.addEventListener("change", draw); draw();
  });
})();
