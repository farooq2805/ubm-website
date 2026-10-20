(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  // Mobile menu
  var toggle = $(".menu-toggle"), nav = $("#nav");
  if (toggle && nav) toggle.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });

  // Reveal on scroll
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (es) {
    es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
  }, { rootMargin: "0px 0px -60px 0px" }) : null;
  $$(".reveal").forEach(function (el, i) {
    el.style.transitionDelay = (i % 4) * 70 + "ms";
    io ? io.observe(el) : el.classList.add("in");
  });

  // Count-up
  $$("[data-count]").forEach(function (el) {
    var end = +el.getAttribute("data-count"), start = end > 1000 ? end - 40 : 0, t0 = null;
    var run = function (ts) { if (!t0) t0 = ts; var p = Math.min((ts - t0) / 1400, 1);
      el.textContent = Math.round(start + (end - start) * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(run); };
    requestAnimationFrame(run);
  });

  // Card spotlight
  document.addEventListener("pointermove", function (ev) {
    var c = ev.target.closest && ev.target.closest(".card"); if (!c) return;
    var r = c.getBoundingClientRect();
    c.style.setProperty("--mx", ev.clientX - r.left + "px"); c.style.setProperty("--my", ev.clientY - r.top + "px");
  });

  // Space planner
  var PLAN = {
    classroom: { name: "classroom", sol: "Smart Classroom Solutions",
      s: [["Display", "65\" interactive flat panel"], ["Sharing", "Wireless BYOD presentation"], ["Audio", "Built-in panel speakers"], ["Extras", "Document camera, teacher training"]],
      m: [["Display", "75–86\" interactive flat panel or interactive projector"], ["Sharing", "Wireless presentation for teacher + students"], ["Audio", "Wall speakers with amplifier"], ["Extras", "Document camera, lecture-capture ready cabling, training"]],
      l: [["Display", "High-brightness laser projector, 120\"+ screen"], ["Sharing", "Wireless presentation + lectern input"], ["Audio", "Voice-lift microphone and distributed speakers"], ["Control", "One-touch control panel at lectern"]],
      brands: ["Epson", "BenQ", "ViewSonic", "Bose Professional"], hint: "Most schools start with medium rooms of 30–45 students." },
    boardroom: { name: "boardroom", sol: "Boardroom & Meeting Room AV",
      s: [["Display", "55–65\" display"], ["Conferencing", "All-in-one video bar"], ["Sharing", "One-click wireless presentation"], ["Control", "Teams/Zoom room controller"]],
      m: [["Display", "75–86\" display or dual displays"], ["Camera", "Auto-framing PTZ camera"], ["Audio", "Ceiling microphone + conferencing loudspeakers"], ["Sharing", "Wireless BYOD + HDMI/USB-C table box"]],
      l: [["Display", "Video wall or laser projection + confidence monitors"], ["Camera", "Dual cameras with speaker tracking"], ["Audio", "Beamforming ceiling mics, DSP, Bose Professional speakers"], ["Signal", "Matrix switching, extenders, touch control"]],
      brands: ["Bose Professional", "ATEN", "Liberty AV", "BenQ", "ViewSonic"], hint: "Audio is the #1 driver of meeting quality — we design it first." },
    auditorium: { name: "auditorium", sol: "Auditorium AV & Sound",
      s: [["Display", "Laser projector, 150\" screen"], ["Audio", "Left/right loudspeakers + subwoofer"], ["Mics", "Lectern + 2 wireless mics"], ["Mixing", "Compact digital mixer"]],
      m: [["Display", "High-brightness laser projector or LED screen"], ["Audio", "Main + fill loudspeakers designed for even coverage"], ["Mics", "Lectern, wireless handheld and lapel set"], ["Control", "Digital mixer, stage box, presets for common events"]],
      l: [["Display", "LED wall or edge-blended projection"], ["Audio", "Line-array or distributed system with balcony fills"], ["Stage", "Stage boxes, monitors, choir/instrument mics"], ["Control", "Central control for audio, video and lighting"]],
      brands: ["Bose Professional", "Epson", "TOA", "Liberty AV"], hint: "We model coverage so the last row hears as clearly as the first." },
    lobby: { name: "lobby / retail space", sol: "Video Wall Solutions",
      s: [["Display", "2×2 narrow-bezel LCD video wall"], ["Content", "Media player with scheduling"], ["Audio", "Zoned background music"], ["Mounting", "Wall-mount, service access"]],
      m: [["Display", "3×3 LCD wall or fine-pitch LED"], ["Processing", "Video wall processor with layouts"], ["Audio", "Zoned background music"], ["Distribution", "Content routed from any source"]],
      l: [["Display", "Large fine-pitch LED or laser projection mapping"], ["Processing", "Multi-window processor"], ["Distribution", "AV-over-IP to multiple walls/floors"], ["Control", "Tablet control of layouts and content"]],
      brands: ["Epson", "ViewSonic", "BenQ", "TOA"], hint: "Viewing distance decides LCD vs LED — we'll calculate it for you." },
    campus: { name: "campus / building", sol: "AV over IP & Media Distribution",
      s: [["Distribution", "HDMI matrix for a few rooms"], ["Audio", "Zoned PA and paging"], ["Control", "Central scheduler"], ["Support", "Preventive maintenance plan"]],
      m: [["Distribution", "AV-over-IP encoders/decoders"], ["Audio", "Zoned PA + background music"], ["Signage", "Displays across common areas"], ["Support", "AMC with on-site service"]],
      l: [["Distribution", "Scalable AV-over-IP across buildings"], ["Audio", "Campus-wide PA with emergency paging"], ["Rooms", "Standardised small/medium/large room designs"], ["Control", "Centralised monitoring and control"]],
      brands: ["Liberty AV", "ATEN", "TOA", "Bose Professional"], hint: "Standardised room designs make multi-site roll-outs faster and cheaper." }
  };
  var SIZE = { s: "Small", m: "Medium", l: "Large" };
  var state = { space: "classroom", size: "m" };
  function renderPlan() {
    var p = PLAN[state.space]; if (!p || !$("#pl-list")) return;
    $("#pl-title").textContent = SIZE[state.size] + " " + p.name;
    $("#pl-list").innerHTML = p[state.size].map(function (r, i) { return '<li style="animation-delay:' + i * 60 + 'ms"><b>' + r[0] + "</b><span>" + r[1] + "</span></li>"; }).join("");
    $("#pl-brands").innerHTML = p.brands.map(function (b) { return "<span>" + b + "</span>"; }).join("");
    $("#pl-hint").textContent = p.hint;
    var msg = "Planner: " + SIZE[state.size] + " " + p.name + " — " + p[state.size].map(function (r) { return r[0] + ": " + r[1]; }).join("; ");
    $("#pl-cta").href = "contact/?solution=" + encodeURIComponent(p.sol) + "&plan=" + encodeURIComponent(msg) + "#enquiry";
  }
  $$(".seg").forEach(function (g) {
    g.addEventListener("click", function (ev) {
      var b = ev.target.closest("button"); if (!b) return;
      $$("button", g).forEach(function (x) { x.classList.remove("on"); }); b.classList.add("on");
      state[g.getAttribute("data-group")] = b.getAttribute("data-v"); renderPlan();
    });
  });
  renderPlan();

  // Prefill enquiry from URL (?solution=…&plan=…)
  var qs = new URLSearchParams(location.search);
  var sol = qs.get("solution"), plan = qs.get("plan");
  if (sol && $("#f-sol")) $$("#f-sol option").forEach(function (o) {
    if (o.textContent === sol || o.textContent.toLowerCase().replace(/[^a-z]+/g, "-").indexOf(sol.split("-")[0]) === 0) o.selected = true;
  });
  if (plan && $("#f-msg")) $("#f-msg").value = plan;

  // Lead form: POST to configured endpoint, else hand off to WhatsApp / email
  $$("[data-ubm-form]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var bad = $$("[required]", form).filter(function (i) { return !i.value.trim() || (i.type === "email" && !/^\S+@\S+\.\S+$/.test(i.value)); });
      $$("[required]", form).forEach(function (i) { i.style.borderColor = ""; });
      if (bad.length) { bad.forEach(function (i) { i.style.borderColor = "#c0392b"; }); bad[0].focus(); return; }
      var data = {}; new FormData(form).forEach(function (v, k) { data[k] = v; });
      data.page = location.pathname; data.source = document.referrer || "direct";
      var ok = $(".form-ok", form);
      var done = function () { ok.style.display = "block"; form.querySelector("button[type=submit]").disabled = true;
        if (window.gtag) gtag("event", "generate_lead", { form_role: data.role, solution: data.solution }); };
      var cfg = window.UBM || {};
      if (cfg.endpoint) {
        fetch(cfg.endpoint, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) })
          .then(done).catch(function () { handoff(data, cfg); done(); });
      } else { handoff(data, cfg); done(); }
    });
  });
  function handoff(d, cfg) {
    var lines = ["New AV enquiry (website)", "Role: " + d.role, "Name: " + d.name, "Organisation: " + d.company, "Phone: " + d.phone,
      "Email: " + d.email, "Solution: " + (d.solution || "Not sure"), "City: " + d.city, "Rooms: " + d.rooms, "Timeline: " + d.timeline, "Details: " + d.message];
    window.open("https://wa.me/" + cfg.wa + "?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
  }
})();
