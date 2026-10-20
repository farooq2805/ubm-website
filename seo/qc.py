#!/usr/bin/env python3
"""Visual + technical QC for every built page (desktop 1440px and mobile 390px).

  python3 -m http.server 8765 -d docs &   # serve the build
  python3 seo/qc.py                       # writes reports/qc-latest.md, exit 1 on failures

Checks: text contrast on buttons/links/headings (WCAG AA 4.5:1, 3:1 for large text),
horizontal overflow, broken internal links, images without alt, missing/duplicate
<title> and meta description, title/description length.
"""
import asyncio, re, sys, glob, os, collections
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get("QC_BASE", "http://localhost:8765")
CHROME = os.environ.get("QC_CHROME", "/opt/pw-browsers/chromium")

JS = r"""() => {
 const lum = c => { const m = c.match(/[\d.]+/g); if (!m) return null; const [r,g,b,a] = m.map(Number);
   if (a === 0) return null; return [r,g,b].map(v => { v/=255; return v<=.03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4) }).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0) };
 const bg = el => { while (el) { const cs = getComputedStyle(el); const c = cs.backgroundColor; const m = c.match(/[\d.]+/g);
   if (cs.backgroundImage !== 'none' && !/gradient/.test(cs.backgroundImage)) return null;
   if (/gradient/.test(cs.backgroundImage)) { const g = cs.backgroundImage.match(/rgba?\([^)]+\)/); if (g) return g[0]; }
   if (m && (m.length < 4 || +m[3] > .5)) return c; el = el.parentElement } return 'rgb(255,255,255)' };
 const bad = [];
 document.querySelectorAll('a.btn, button, .btn, h1, h2, h3, .chip, .quick2 a, .filters button, .nav a').forEach(el => {
   const r = el.getBoundingClientRect(); if (!r.width || !r.height || getComputedStyle(el).visibility === 'hidden') return;
   if (el.closest('.loader,[hidden],.space,.path,.cta-band,.page-hero,.hero,.mosaic,.numbers,.planner-out,.fact,.aside-card.dark,.partner-badge')) return;  // white text on photo/dark overlays
   const b = bg(el); if (!b) return; const L1 = lum(getComputedStyle(el).color), L2 = lum(b); if (L1 == null || L2 == null) return;
   const ratio = (Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);
   const big = parseFloat(getComputedStyle(el).fontSize) >= 24 || (parseFloat(getComputedStyle(el).fontSize) >= 18.6 && +getComputedStyle(el).fontWeight >= 700);
   if (ratio < (big ? 3 : 4.5)) bad.push(`${el.tagName.toLowerCase()}.${(el.className||'').toString().split(' ')[0]} "${el.textContent.trim().slice(0,40)}" contrast ${ratio.toFixed(2)}`);
 });
 const over = document.documentElement.scrollWidth > innerWidth + 1;
 const noalt = [...document.images].filter(i => !i.hasAttribute('alt')).length;
 return {bad: [...new Set(bad)].slice(0, 12), over, noalt};
}"""

async def main():
    pages = sorted("/" + str(Path(f).relative_to(ROOT / "docs").parent).replace(".", "").strip("/") + "/" for f in glob.glob(str(ROOT / "docs/**/index.html"), recursive=True))
    pages = [p.replace("//", "/") for p in pages]
    issues = collections.defaultdict(list); titles = collections.Counter(); descs = collections.Counter()
    known = set(pages)
    for p in pages:  # static checks
        h = (ROOT / "docs" / p.strip("/") / "index.html").read_text()
        t = re.search(r"<title>(.*?)</title>", h); d = re.search(r'<meta name="description" content="([^"]*)"', h)
        if not t: issues[p].append("missing <title>")
        else:
            titles[t.group(1)] += 1
            if len(t.group(1)) > 65: issues[p].append(f"title {len(t.group(1))} chars (>65)")
        if not d: issues[p].append("missing meta description")
        else:
            descs[d.group(1)] += 1
            if not 110 <= len(d.group(1)) <= 165: issues[p].append(f"description {len(d.group(1))} chars")
        depth = p.strip("/").count("/") + (1 if p.strip("/") else 0)
        for href in re.findall(r'href="(\.\./[^"#?]*|\./[^"#?]*|[a-z][a-z0-9-]*/[^"#?]*)"', h):
            if href.startswith(("http", "mailto", "tel")): continue
            parts = (p.strip("/").split("/") if p.strip("/") else [])
            for seg in href.split("/"):
                if seg == "..": parts = parts[:-1]
                elif seg not in (".", ""): parts.append(seg)
            target = "/" + "/".join(parts) + ("/" if parts else "")
            if href.endswith((".css", ".js", ".png", ".svg", ".txt", ".xml")): continue
            if target not in known: issues[p].append(f"broken link {href}")
    for t, c in titles.items():
        if c > 1: issues["(site)"].append(f"duplicate title x{c}: {t}")
    for d, c in descs.items():
        if c > 1: issues["(site)"].append(f"duplicate description x{c}: {d[:60]}")
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=CHROME)
        for w, label in ((1440, "desktop"), (390, "mobile")):
            pg = await b.new_page(viewport={"width": w, "height": 900})
            for p in pages:
                await pg.goto(BASE + p, wait_until="domcontentloaded"); await pg.wait_for_timeout(150)
                r = await pg.evaluate(JS)
                for x in r["bad"]: issues[p].append(f"[{label}] low contrast: {x}")
                if r["over"]: issues[p].append(f"[{label}] horizontal overflow")
                if r["noalt"]: issues[p].append(f"[{label}] {r['noalt']} image(s) without alt")
            await pg.close()
        await b.close()
    n = sum(len(v) for v in issues.values())
    out = [f"# QC report", "", f"Pages checked: {len(pages)} at 1440px and 390px · Issues: **{n}**", ""]
    for p, v in sorted(issues.items()):
        out.append(f"## {p}"); out += [f"- {x}" for x in sorted(set(v))]; out.append("")
    (ROOT / "reports").mkdir(exist_ok=True); (ROOT / "reports/qc-latest.md").write_text("\n".join(out))
    print("\n".join(out[:3])); return n

if __name__ == "__main__":
    sys.exit(1 if asyncio.run(main()) else 0)
