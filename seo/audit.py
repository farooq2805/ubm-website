#!/usr/bin/env python3
"""SEO + AEO + GEO audit for the UBM site. Standard library only.

  python3 seo/audit.py docs                     # audit the local build
  python3 seo/audit.py https://www.ubm.co.in    # audit the live site (reads /sitemap.xml)

Writes reports/audit-YYYY-MM-DD.md and reports/audit-latest.json. Exit code 1 if any page scores below 70.
"""
import json, re, sys, datetime, urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "UBM-SEO-Audit/1.0 (+https://www.ubm.co.in)"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""; self.meta = {}; self.canonical = ""; self.h1 = []; self.h2 = 0
        self.imgs_no_alt = 0; self.links = []; self.ld = []; self.text = []
        self._in = None; self._buf = ""; self._skip = 0; self.answer_block = False

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag in ("script", "style"):
            self._skip += 1
            if tag == "script" and a.get("type") == "application/ld+json":
                self._in = "ld"; self._buf = ""
        elif tag == "title": self._in = "title"; self._buf = ""
        elif tag == "h1": self._in = "h1"; self._buf = ""
        elif tag == "h2": self.h2 += 1
        elif tag == "meta" and (a.get("name") or a.get("property")): self.meta[(a.get("name") or a.get("property")).lower()] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical": self.canonical = a.get("href", "")
        elif tag == "img" and not a.get("alt"): self.imgs_no_alt += 1
        elif tag == "a" and a.get("href"): self.links.append(a["href"])
        if "answer" in (a.get("class") or "").split(): self.answer_block = True

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip = max(0, self._skip - 1)
            if self._in == "ld":
                try: self.ld.append(json.loads(self._buf))
                except Exception: self.ld.append({"@type": "INVALID_JSON"})
                self._in = None
        elif tag == "title" and self._in == "title": self.title = self._buf.strip(); self._in = None
        elif tag == "h1" and self._in == "h1": self.h1.append(self._buf.strip()); self._in = None

    def handle_data(self, d):
        if self._in: self._buf += d
        if not self._skip: self.text.append(d)


def ld_types(ld):
    out = set()
    for block in ld:
        for node in (block.get("@graph", [block]) if isinstance(block, dict) else []):
            t = node.get("@type")
            out.update(t if isinstance(t, list) else [t])
    return out


def score_page(url, html):
    p = Page(); p.feed(html)
    words = len(re.findall(r"\w+", " ".join(p.text)))
    types = ld_types(p.ld)
    desc = p.meta.get("description", "")
    issues, s = [], 100
    def bad(pts, msg): nonlocal s; s -= pts; issues.append(msg)
    if not p.title: bad(15, "Missing <title>")
    elif not 30 <= len(p.title) <= 65: bad(4, f"Title length {len(p.title)} (aim 30–65)")
    if not desc: bad(12, "Missing meta description")
    elif not 110 <= len(desc) <= 165: bad(3, f"Meta description length {len(desc)} (aim 110–165)")
    if len(p.h1) != 1: bad(8, f"{len(p.h1)} <h1> tags (need exactly 1)")
    if not p.canonical: bad(8, "Missing canonical")
    if p.imgs_no_alt: bad(min(6, p.imgs_no_alt * 2), f"{p.imgs_no_alt} image(s) without alt")
    if "noindex" in p.meta.get("robots", ""): issues.append("NOTE: page is noindex (expected on staging only)")
    if not p.meta.get("og:title"): bad(3, "Missing Open Graph tags")
    # AEO: direct answers + FAQ markup
    if not ({"Organization", "LocalBusiness"} & types): bad(6, "No Organization/LocalBusiness schema")
    if "INVALID_JSON" in types: bad(10, "Invalid JSON-LD")
    is_home = url.rstrip("/").endswith(("docs", ".in")) or url.endswith("index.html") and url.count("/") <= 2
    if not is_home and "BreadcrumbList" not in types: bad(3, "No BreadcrumbList schema")
    if "FAQPage" not in types: bad(4, "No FAQPage schema (AEO)")
    if not p.answer_block: bad(4, "No direct-answer block near top (AEO/GEO)")
    if p.h2 < 2: bad(3, "Fewer than 2 <h2> sections")
    if words < 300: bad(6, f"Thin content: {words} words")
    return {"url": url, "score": max(s, 0), "title": p.title, "words": words, "schema": sorted(t for t in types if t), "issues": issues, "links": p.links}


def fetch(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def collect(target):
    pages = []
    if target.startswith("http"):
        base = target.rstrip("/")
        locs = re.findall(r"<loc>(.*?)</loc>", fetch(base + "/sitemap.xml"))
        # sitemap URLs point at production; audit the target host instead (e.g. the GitHub Pages preview)
        locs = [re.sub(r"^https?://[^/]+", base, u) for u in locs]
        for u in locs:
            try: pages.append((u, fetch(u)))
            except Exception as ex: pages.append((u, f"<title></title><!-- fetch error {ex} -->"))
        extras = {}
        for f in ("robots.txt", "llms.txt", "sitemap.xml"):
            try: extras[f] = len(fetch(base + "/" + f)) > 20
            except Exception: extras[f] = False
    else:
        d = Path(target)
        for f in sorted(d.rglob("index.html")):
            pages.append((str(f.relative_to(d)), f.read_text(encoding="utf-8")))
        extras = {f: (d / f).exists() for f in ("robots.txt", "llms.txt", "sitemap.xml")}
        # internal link check
        known = {str(f.parent.relative_to(d)).replace(".", "") for f in d.rglob("index.html")}
        extras["_known"] = known
    return pages, extras


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "docs")
    pages, extras = collect(target)
    results = [score_page(u, h) for u, h in pages]
    avg = round(sum(r["score"] for r in results) / max(len(results), 1), 1)
    today = datetime.date.today().isoformat()
    lines = [f"# SEO / AEO / GEO audit — {today}", "", f"Target: `{target}` · Pages: {len(results)} · **Average score: {avg}/100**", "",
             "## Site-level (GEO / crawlability)", ""]
    for f in ("robots.txt", "sitemap.xml", "llms.txt"):
        lines.append(f"- {'✅' if extras.get(f) else '❌'} `{f}`")
    lines += ["", "## Pages (lowest first)", "", "| Score | Page | Words | Schema | Top issues |", "|---:|---|---:|---|---|"]
    for r in sorted(results, key=lambda r: r["score"]):
        lines.append(f"| {r['score']} | {r['url']} | {r['words']} | {', '.join(r['schema'])} | {'; '.join(r['issues'][:3]) or '—'} |")
    out = ROOT / "reports"; out.mkdir(exist_ok=True)
    (out / f"audit-{today}.md").write_text("\n".join(lines) + "\n")
    (out / "audit-latest.json").write_text(json.dumps({"date": today, "target": target, "average": avg,
        "site": {k: v for k, v in extras.items() if not k.startswith("_")}, "pages": [{k: v for k, v in r.items() if k != "links"} for r in results]}, indent=1))
    print("\n".join(lines[:12])); print(f"... full report: reports/audit-{today}.md")
    sys.exit(1 if any(r["score"] < 70 for r in results) else 0)


if __name__ == "__main__":
    main()
