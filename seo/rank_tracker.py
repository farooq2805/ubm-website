#!/usr/bin/env python3
"""Weekly rank + AI Overview (GEO) tracker for UBM.

Uses the Apify Google Search Scraper (Google India, English). Needs APIFY_TOKEN in the environment.

  APIFY_TOKEN=... python3 seo/rank_tracker.py            # all P1 + P2 keywords
  APIFY_TOKEN=... python3 seo/rank_tracker.py --all      # every keyword in keywords.csv

Appends to reports/rankings.csv and writes reports/rankings-latest.md with:
  - UBM organic position (top 30) per keyword
  - whether a Google AI Overview appears, and whether ubm.co.in is cited in it
  - the top 3 competitors ranking for that keyword
"""
import csv, json, os, sys, datetime, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "ubm.co.in"
ACTOR = "https://api.apify.com/v2/acts/apify~google-search-scraper/run-sync-get-dataset-items?token={}&timeout=280"
DIRECTORIES = ("justdial.com", "indiamart.com", "tradeindia.com", "google.com", "youtube.com", "instagram.com", "linkedin.com", "facebook.com")


def host(u):
    return u.split("/")[2].removeprefix("www.") if "//" in u else u


def main():
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("APIFY_TOKEN not set — add it as a GitHub Actions secret or export it locally.")
    rows = list(csv.DictReader(open(ROOT / "seo/keywords.csv")))
    if "--all" not in sys.argv:
        rows = [r for r in rows if r["priority"] in ("P1", "P2")]
    payload = {"queries": "\n".join(r["keyword"] for r in rows), "countryCode": "in", "languageCode": "en",
               "resultsPerPage": 30, "maxPagesPerQuery": 1, "mobileResults": False}
    req = urllib.request.Request(ACTOR.format(token), data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        items = json.load(r)
    today = datetime.date.today().isoformat()
    by_kw = {i["searchQuery"]["term"].lower(): i for i in items}
    out_rows, md = [], [f"# Rankings & AI Overview citations — {today}", "", "Google India · English · desktop · top 30", "",
                       "| Keyword | Target page | UBM position | AI Overview | UBM cited in AIO | Top competitors |", "|---|---|---:|:-:|:-:|---|"]
    ranked = cited = 0
    for r in rows:
        it = by_kw.get(r["keyword"].lower(), {})
        org = it.get("organicResults") or []
        pos = next((o.get("position") for o in org if DOMAIN in o.get("url", "")), None)
        aio = it.get("aiOverview") or {}
        aio_src = [host(s.get("url", "")) for s in (aio.get("sources") or [])]
        is_cited = any(DOMAIN in s for s in aio_src)
        comps = [h for h in (host(o.get("url", "")) for o in org) if DOMAIN not in h and not h.endswith(DIRECTORIES)]
        comps = list(dict.fromkeys(comps))[:3]
        ranked += pos is not None; cited += is_cited
        out_rows.append([today, r["keyword"], r["priority"], r["target_page"], pos or "", "yes" if aio else "no", "yes" if is_cited else "no", "|".join(comps)])
        md.append(f"| {r['keyword']} | `{r['target_page']}` | {pos or '—'} | {'✅' if aio else '—'} | {'✅' if is_cited else '—'} | {', '.join(comps)} |")
    md[2] += f" · UBM ranks for **{ranked}/{len(rows)}** · cited in **{cited}** AI Overviews"
    (ROOT / "reports").mkdir(exist_ok=True)
    hist = ROOT / "reports/rankings.csv"
    new = not hist.exists()
    with open(hist, "a", newline="") as f:
        w = csv.writer(f)
        if new: w.writerow(["date", "keyword", "priority", "target_page", "ubm_position", "ai_overview", "ubm_cited_in_aio", "top_competitors"])
        w.writerows(out_rows)
    (ROOT / "reports/rankings-latest.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[:3]))


if __name__ == "__main__":
    main()
