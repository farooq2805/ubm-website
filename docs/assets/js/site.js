(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var desktop = matchMedia("(min-width: 1100px)");

  // Mobile menu: full-screen drawer, body scroll locked while open
  var toggle = $(".menu-toggle"), nav = $("#nav");
  function setMenu(open) {
    if (!nav) return;
    nav.classList.toggle("open", open);
    document.body.classList.toggle("nav-open", open && !desktop.matches);
    if (toggle) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
  }
  if (toggle) toggle.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") setMenu(false); });
  if (nav) nav.addEventListener("click", function (ev) { if (ev.target.closest("a")) setMenu(false); });
  desktop.addEventListener && desktop.addEventListener("change", function () { setMenu(false); });

  // Dropdowns: tap to expand on mobile; hover/focus handles desktop
  $$(".dd > button").forEach(function (b) {
    b.addEventListener("click", function () {
      var dd = b.parentNode, open = !dd.classList.contains("open");
      $$(".dd.open").forEach(function (d) { if (d !== dd) { d.classList.remove("open"); $("button", d).setAttribute("aria-expanded", "false"); } });
      dd.classList.toggle("open", open);
      b.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function (ev) {
    if (desktop.matches && !ev.target.closest(".dd")) $$(".dd.open").forEach(function (d) { d.classList.remove("open"); $("button", d).setAttribute("aria-expanded", "false"); });
  });

  // Prefill enquiry from URL (?solution=…&plan=…)
  var qs = new URLSearchParams(location.search);
  var sol = qs.get("solution"), plan = qs.get("plan");
  if (sol && $("#f-sol")) $$("#f-sol option").forEach(function (o) {
    if (o.textContent === sol || o.textContent.toLowerCase().replace(/[^a-z]+/g, "-").indexOf(sol.split("-")[0]) === 0) o.selected = true;
  });
  if (plan && $("#f-msg")) $("#f-msg").value = plan;

  // Lead form: POST to configured endpoint, else hand off to WhatsApp
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
    var f = [["Role", d.role], ["Name", d.name], ["Organisation", d.company], ["Phone", d.phone], ["Email", d.email], ["Need", d.need],
      ["Solution", d.solution], ["City", d.city], ["Rooms", d.rooms], ["Timeline", d.timeline], ["Details", d.message], ["Page", d.page]];
    var lines = ["New AV enquiry (website)"].concat(f.filter(function (x) { return x[1]; }).map(function (x) { return x[0] + ": " + x[1]; }));
    window.open("https://wa.me/" + cfg.wa + "?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
  }

  // Blog topic filters
  var list = document.getElementById("bloglist");
  if (list) $$(".filters button").forEach(function (b) {
    b.addEventListener("click", function () {
      $$(".filters button").forEach(function (x) { x.classList.toggle("on", x === b); });
      var f = b.getAttribute("data-filter");
      list.classList.toggle("filtered", f !== "all");
      $$(".pcard", list).forEach(function (c) { c.hidden = f !== "all" && c.getAttribute("data-cat") !== f; });
    });
  });
})();
