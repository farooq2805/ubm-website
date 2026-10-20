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
