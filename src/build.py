#!/usr/bin/env python3
"""Static site generator for the UBM website.

Usage:  python3 src/build.py            -> staging build (noindex) into docs/
        UBM_ENV=production python3 src/build.py  -> indexable production build
"""
import html, json, os, re, shutil, datetime
from pathlib import Path
from content import SITE, ICONS, SERVICES, SOLUTIONS, INDUSTRIES, BRANDS, GENERAL_FAQS, IMG, HERO_SLIDES, U
from blog import POSTS
from blog_more import MORE_POSTS
from blog_india import INDIA_POSTS
from industry_stories import STORIES
from meta import META
POSTS = sorted(POSTS + MORE_POSTS + INDIA_POSTS, key=lambda p: p["date"], reverse=True)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
PROD = os.environ.get("UBM_ENV") == "production"
BASE = SITE["prod_url"]
TODAY = datetime.date.today().isoformat()
SOL = {s["slug"]: s for s in SOLUTIONS}
IND = {i["slug"]: i for i in INDUSTRIES}
BR = {b["slug"]: b for b in BRANDS}
LOGO_BASE = "https://www.ubm.co.in/asset/img/"
pages = []  # (path, priority) for sitemap
META_LOG = []
CONTACT_FAQ = [("Where is UBM's office?", 'B-101, Sarvodaya Bldg No. 11, Khernagar Service Road, off Western Express Highway, Bandra (East), Mumbai 400051.'), ('How can I contact UBM?', 'Call 022 2647 5639 or +91 98202 93108 (also WhatsApp), or email connect@ubm.co.in or balraj@ubm.co.in.'), ('How quickly does UBM respond to enquiries?', 'UBM aims to respond to every project enquiry within one working day.')]
ABOUT_FAQ = [('When was UBM founded?', 'UBM, Universal Business Machines, was founded in Mumbai in 1997.'), ('What makes UBM a value-added distributor?', 'Beyond supplying products, UBM provides design, consultation, installation, maintenance, service and training to dealers and organisations.')]
HUBS = {'solutions': ('UBM, a Mumbai-based value-added pro AV distributor since 1997, designs, supplies, installs and supports six solution families: smart classrooms, boardroom and meeting room AV, video walls, auditorium sound and AV, AV over IP and media distribution, and public address systems.', [('Which AV solutions does UBM provide?', 'Smart classrooms, boardroom and meeting room AV, video walls, auditorium sound and AV, AV over IP and media distribution, and public address systems.'), ('Does UBM install the systems it supplies?', 'Yes. UBM provides design, consultation, installation, maintenance, service and training.')]), 'industries': ('UBM delivers professional AV for education, corporate, hospitality, places of worship, stadiums and sports venues, home theatre and retail, from its Mumbai base since 1997, directly and through dealer partners across India.', [('Which industries does UBM serve?', 'Education, corporate, hospitality, places of worship, stadiums and sports venues, home theatre and retail.'), ('Does UBM work outside Mumbai?', 'Yes. UBM supports customers across India directly and through its dealer and integrator network.')]), 'brands': ('UBM (Universal Business Machines), a Mumbai-based value-added AV distributor since 1997, supplies Epson, Bose Professional, ATEN, Liberty AV Solutions, ViewSonic, BenQ and TOA to dealers, system integrators and organisations across India.', [('Which brands does UBM distribute?', 'Epson, Bose Professional, ATEN, Liberty AV Solutions, ViewSonic, BenQ and TOA.'), ('Can dealers buy from UBM?', 'Yes. UBM supplies dealers and system integrators and supports them with design, training and after-sales service.')]), 'blog': ('The UBM blog publishes practical, vendor-neutral guides on smart classrooms, interactive displays, video walls, boardroom AV, AV over IP, projectors and public address systems, written from UBM’s experience as a Mumbai pro AV distributor since 1997.', [('Who writes the UBM guides?', 'The UBM Solutions Team, pro AV professionals and system designers at Universal Business Machines, Mumbai.'), ('Can I ask UBM a question about my project?', 'Yes. Use the contact form, call 022 2647 5639 or WhatsApp +91 98202 93108.')])}

e = html.escape


def rel(depth):
    return "../" * depth if depth else "./"


def md(text, r):
    out, ul = [], False
    for block in text.strip().split("\n"):
        line = block.rstrip()
        line_html = e(line, quote=False)
        line_html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line_html)
        line_html = re.sub(r"\[(.+?)\]\(/(.*?)\)", lambda m: f'<a href="{r}{m.group(2)}">{m.group(1)}</a>', line_html)
        if line.startswith("- "):
            if not ul:
                out.append("<ul>"); ul = True
            out.append(f"<li>{line_html[2:]}</li>"); continue
        if ul:
            out.append("</ul>"); ul = False
        if not line:
            continue
        if line.startswith("## "):
            t = line_html[3:]; out.append(f'<h2 id="{slugify(line[3:])}">{t}</h2>')
        elif line.startswith("### "):
            out.append(f"<h3>{line_html[4:]}</h3>")
        elif line.startswith("> "):
            out.append(f'<p class="pull">{line_html[5:]}</p>')
        else:
            out.append(f"<p>{line_html}</p>")
    if ul:
        out.append("</ul>")
    return "\n".join(out)


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ------------------------------------------------------------------ schema
def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": ["Organization", "LocalBusiness"],
        "@id": BASE + "/#org",
        "name": SITE["legal"], "alternateName": "UBM",
        "url": BASE + "/", "logo": BASE + "/assets/img/ubm-logo-trim.png",
        "foundingDate": str(SITE["founded"]),
        "description": "Mumbai-based value-added distributor of professional audio-visual (pro AV) solutions since 1997, Epson, Bose Professional, ATEN, Liberty AV Solutions, ViewSonic, BenQ and TOA, with design, consultation, installation, maintenance, service and training.",
        "telephone": [SITE["phone_tel"], SITE["mobile_tel"]], "email": [SITE["email"], SITE["email2"]],
        "address": {"@type": "PostalAddress", "streetAddress": SITE["street"], "addressLocality": SITE["city"],
                    "addressRegion": SITE["region"], "postalCode": SITE["postcode"], "addressCountry": "IN"},
        "geo": {"@type": "GeoCoordinates", "latitude": 19.0593, "longitude": 72.8460},
        "areaServed": {"@type": "Country", "name": "India"},
        "sameAs": SITE["profiles"],
        "slogan": "Value-added pro AV distribution since 1997",
        "brand": [{"@type": "Brand", "name": x["name"]} for x in BRANDS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Professional AV solutions", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": BASE + "/solutions/" + s["slug"] + "/"}} for s in SOLUTIONS]},
        "knowsAbout": ["Pro AV distribution", "Smart classroom solutions", "Boardroom AV", "Video walls",
                       "Auditorium sound systems", "AV over IP", "Public address systems", "Projectors", "Interactive flat panels"],
        "contactPoint": [{"@type": "ContactPoint", "telephone": SITE["phone_tel"], "email": SITE["email"], "contactType": "customer service", "areaServed": "IN", "availableLanguage": ["English", "Hindi", "Marathi"]},
                         {"@type": "ContactPoint", "telephone": SITE["mobile_tel"], "email": SITE["email2"], "contactType": "sales", "areaServed": "IN", "availableLanguage": ["English", "Hindi", "Marathi"]}],
    }


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def crumbs_schema(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + p}
                                for i, (n, p) in enumerate(trail)]}


# ------------------------------------------------------------------ chrome
def nav(r, active):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{r}{href}"{cur}>{label}</a>'
    sol = "".join(f'<a href="{r}solutions/{s["slug"]}/">{e(s["name"])}<small>{e(s["kw"].capitalize())}</small></a>' for s in SOLUTIONS)
    ind = "".join(f'<a href="{r}industries/{i["slug"]}/">{e(i["name"])}</a>' for i in INDUSTRIES)
    br = "".join(f'<a href="{r}{b["slug"]}/">{e(b["name"])}</a>' for b in BRANDS)
    return f'''<nav class="nav" id="nav" aria-label="Main">
  <div class="dd"><button type="button">Solutions</button><div class="dd-menu">{sol}<a href="{r}solutions/"><b>All solutions →</b></a></div></div>
  <div class="dd"><button type="button">Industries</button><div class="dd-menu">{ind}</div></div>
  <div class="dd"><button type="button">Brands</button><div class="dd-menu">{br}<a href="{r}brands/"><b>All brands →</b></a></div></div>
  {a("dealer-partners/", "Partners", "partners")}
  {a("about-us/", "About", "about")}
  {a("blog/", "Blog", "blog")}
  {a("contact/", "Contact", "contact")}
</nav>'''


WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.7c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.7 10.7 0 1 1 16 26.7zm5.9-8c-.3-.2-1.9-1-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.8 8.8 0 0 1-4.4-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.6 3.6 0 0 0-1.1 2.7 6.3 6.3 0 0 0 1.3 3.3 14.4 14.4 0 0 0 5.5 4.9c2 .9 2.8 1 3.9.8a3.3 3.3 0 0 0 2.1-1.5 2.7 2.7 0 0 0 .2-1.5c0-.2-.3-.3-.6-.5z"/></svg>'


def page(path, title, desc, body, active="", schemas=(), depth=None, priority="0.7", og_type="website"):
    if depth is None:
        depth = path.count("/")
    r = rel(depth)
    if path in META:
        title, desc = META[path]
    canonical = BASE + "/" + path
    robots = "index,follow,max-image-preview:large" if PROD else "noindex,nofollow"
    ga = ""
    if SITE["ga4_id"]:
        ga = f'''<script async src="https://www.googletagmanager.com/gtag/js?id={SITE["ga4_id"]}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{SITE["ga4_id"]}');</script>'''
    gsc = f'<meta name="google-site-verification" content="{SITE["gsc_verification"]}">' if SITE["gsc_verification"] else ""
    webpage = {"@context": "https://schema.org", "@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": title,
               "description": desc, "inLanguage": "en-IN", "isPartOf": {"@type": "WebSite", "name": "UBM - Universal Business Machines", "url": BASE + "/"},
               "publisher": {"@id": BASE + "/#org"}, "datePublished": "2026-10-01", "dateModified": TODAY,
               "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".story-lede", ".lead"]}}
    schemas = tuple(schemas) + (webpage,)
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (org_schema(),) + tuple(schemas))
    intro_js = ""
    wa_msg = "Hi UBM, I'd like to discuss an AV project."
    doc = f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:site_name" content="UBM, Universal Business Machines"><meta property="og:locale" content="en_IN">
<meta property="og:image" content="{BASE}/assets/img/og-image.png"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f2c6e">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="author" content="UBM - Universal Business Machines">
<meta property="article:modified_time" content="{TODAY}">{intro_js}
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/site.css">
{gsc}{ga}
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <div class="tb-left"><span><b>Since 1997</b> · Value-added Pro AV distribution</span><a href="tel:{SITE["phone_tel"]}">{SITE["phone_display"]}</a><a href="tel:{SITE["mobile_tel"]}">{SITE["mobile_display"]}</a><a href="mailto:{SITE["email"]}">{SITE["email"]}</a><a href="mailto:{SITE["email2"]}">{SITE["email2"]}</a></div>
  <div class="tb-right"><a href="{r}dealer-partners/">Dealer &amp; integrator programme →</a></div>
</div></div>
<header class="site-header"><div class="wrap">
  <a class="brand" href="{r}" aria-label="UBM, Universal Business Machines home"><img src="{r}assets/img/ubm-logo-trim.png" alt="UBM, Universal Business Machines" width="208" height="45"></a>
  {nav(r, active)}
  <div class="header-cta">
    <a class="btn btn-ghost" href="tel:{SITE["phone_tel"]}">Call us</a>
    <a class="btn btn-coral" href="{r}contact/#enquiry">Consult now</a>
    <button class="menu-toggle" aria-label="Open menu" aria-controls="nav" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</div></header>
<main id="main">
{body}
</main>
{footer(r)}
<a class="wa" href="https://wa.me/{SITE["whatsapp"]}?text={e(wa_msg).replace(" ", "%20")}" target="_blank" rel="noopener" aria-label="Chat with UBM on WhatsApp">{WA_SVG}</a>
<div class="mobile-cta"><a href="tel:{SITE["phone_tel"]}">Call UBM</a><a href="{r}contact/#enquiry">Get a proposal</a></div>
<script>window.UBM={{endpoint:{json.dumps(SITE["form_endpoint"])},wa:{json.dumps(SITE["whatsapp"])},email:{json.dumps(SITE["email"])}}};</script>
<script src="{r}assets/js/site.js" defer></script>
</body>
</html>'''
    dest = OUT / path / "index.html" if path and not path.endswith(".html") else OUT / (path or "index.html")
    if path == "":
        dest = OUT / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    if path != "404.html":
        pages.append((path, priority))
        META_LOG.append((path, title, desc))


def footer(r):
    sol = "".join(f'<li><a href="{r}solutions/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SOLUTIONS)
    ind = "".join(f'<li><a href="{r}industries/{i["slug"]}/">{e(i["name"])}</a></li>' for i in INDUSTRIES)
    br = "".join(f'<li><a href="{r}{b["slug"]}/">{e(b["name"])}</a></li>' for b in BRANDS)
    return f'''<footer class="site-footer"><div class="wrap">
  <div class="cols">
    <div><span class="foot-logo"><img src="{r}assets/img/ubm-logo-trim.png" alt="UBM" width="158" height="34"></span>
      <p>Value-added distributor of professional audio-visual technology since 1997. Design, consultation, installation, maintenance, service and training, from Mumbai, for India.</p></div>
    <div><h4>Solutions</h4><ul>{sol}</ul></div>
    <div><h4>Industries</h4><ul>{ind}</ul></div>
    <div><h4>Brands</h4><ul>{br}</ul></div>
    <div><h4>Contact</h4><ul>
      <li>{e(SITE["street"])}, {SITE["city"]} {SITE["postcode"]}</li>
      <li><a href="tel:{SITE["phone_tel"]}">{SITE["phone_display"]}</a></li>
      <li><a href="https://wa.me/{SITE["whatsapp"]}">WhatsApp {SITE["mobile_display"]}</a></li>
      <li><a href="tel:{SITE["mobile_tel"]}">Mobile {SITE["mobile_display"]}</a></li>
      <li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
      <li><a href="mailto:{SITE["email2"]}">{SITE["email2"]}</a></li>
      <li><a href="{r}careers/">Careers</a> · <a href="{r}faq/">FAQ</a> · <a href="{r}blog/">Blog</a></li></ul></div>
  </div>
  <div class="foot-bottom"><span>© {datetime.date.today().year} Universal Business Machines. All rights reserved. Last updated {TODAY}.</span><span><a href="{r}editorial-policy/">Editorial policy</a> · <a href="{r}privacy-policy/">Privacy policy</a></span><span>Brand names and logos are trademarks of their respective owners.</span></div>
</div></footer>'''



def logo_tile(r, b):
    cls = "logo-tile epson" if b["slug"] == "epson" else "logo-tile"
    return f'''<a class="{cls}" href="{r}{b["slug"]}/" title="{e(b["name"])}"><img src="{LOGO_BASE}{b["logo"]}" alt="{e(b["name"])} logo" loading="lazy" height="34" onerror="this.replaceWith(Object.assign(document.createElement('span'),{{className:'fallback',textContent:'{e(b["name"])}'}}))"></a>'''


def faq_block(faqs, title="Frequently asked questions"):
    items = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)
    return f'<div class="faq"><h2>{e(title)}</h2>{items}</div>'


def hub_extra(answer, faqs):
    return f'<section class="alt"><div class="wrap content"><article class="prose"><h2>How UBM helps</h2><p class="story-lede">{e(answer)}</p></article></div></section><section><div class="wrap">{faq_block(faqs)}</div></section>'



def enquiry_form(r, preset=""):
    opts = "".join(f'<option{" selected" if s["name"] == preset else ""}>{e(s["name"])}</option>' for s in SOLUTIONS)
    return f'''<form class="form-card" id="enquiry" data-ubm-form novalidate>
  <h3>Tell us about your project</h3><p class="muted">Takes under a minute. We reply within one working day.</p>
  <div class="field full"><label>I am a</label><div class="chips">
    <label><input type="radio" name="role" value="End customer" checked><span>End customer</span></label>
    <label><input type="radio" name="role" value="Dealer / Integrator"><span>Dealer / Integrator</span></label>
    <label><input type="radio" name="role" value="Consultant / Architect"><span>Consultant / Architect</span></label></div></div>
  <div class="form-grid" style="margin-top:16px">
    <div class="field"><label for="f-name">Full name *</label><input id="f-name" name="name" required autocomplete="name"></div>
    <div class="field"><label for="f-company">Organisation *</label><input id="f-company" name="company" required autocomplete="organization"></div>
    <div class="field"><label for="f-phone">Phone / WhatsApp *</label><input id="f-phone" name="phone" type="tel" required autocomplete="tel"></div>
    <div class="field"><label for="f-email">Work email *</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
    <div class="field"><label for="f-sol">Solution</label><select id="f-sol" name="solution"><option value="">Not sure yet</option>{opts}<option>Product supply only</option></select></div>
    <div class="field"><label for="f-city">City</label><input id="f-city" name="city" autocomplete="address-level2"></div>
    <div class="field"><label for="f-rooms">Number of rooms / sites</label><select id="f-rooms" name="rooms"><option>1</option><option>2–5</option><option>6–20</option><option>20+</option></select></div>
    <div class="field"><label for="f-time">Timeline</label><select id="f-time" name="timeline"><option>Within 1 month</option><option>1–3 months</option><option>3–6 months</option><option>Just exploring</option></select></div>
    <div class="field full"><label for="f-msg">Project details</label><textarea id="f-msg" name="message" placeholder="Room sizes, current setup, what you want to achieve…"></textarea></div>
  </div>
  <button class="btn btn-navy" type="submit" style="margin-top:18px;width:100%">Send enquiry →</button>
  <p class="form-note">By submitting you agree to be contacted by UBM about your enquiry. We never share your details.</p>
  <div class="form-ok" role="status">Thank you, your enquiry is ready. A UBM specialist will be in touch shortly.</div>
</form>'''


# ------------------------------------------------------------------ pages
def page_hero(r, trail, h1, intro, eyebrow="", actions=True, img=None):
    c = ' <span>/</span> '.join([f'<a href="{r}">Home</a>'] + [f'<a href="{r}{p}">{e(n)}</a>' for n, p in trail[:-1]] + [e(trail[-1][0])])
    act = f'''<div class="hero-actions"><a class="btn btn-coral" href="{r}contact/#enquiry">Get a free consultation</a><a class="btn btn-ghost" href="https://wa.me/{SITE["whatsapp"]}" target="_blank" rel="noopener">WhatsApp an expert</a></div>''' if actions else ""
    eb = f'<div class="eyebrow">{e(eyebrow)}</div>' if eyebrow else ""
    if img is None:
        key = trail[-1][1].strip("/").split("/")[-1]
        HUB = {"solutions": "auditorium-av-solutions", "industries": "corporate", "brands": "epson", "blog": "blog", "about-us": "about",
               "dealer-partners": "partners", "contact": "contact", "careers": "about", "faq": "about2"}
        img = IMG.get(HUB.get(key, key))
    bg = f'<img src="{U(img, 1800)}" alt="" fetchpriority="high">' if img else ""
    return f'''<section class="page-hero">{bg}<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">{c}</nav>{eb}<h1>{e(h1)}</h1><p class="lead">{e(intro)}</p>{act}</div></section>'''


def cta_band(r, h="Planning an AV project?", p="Tell us about your space. A UBM specialist will respond within one working day with ideas, options and a clear proposal."):
    return f'''<section><div class="wrap"><div class="cta-band reveal"><img src="{U(IMG["cta"], 1600)}" alt="" loading="lazy"><div><div class="eyebrow">Talk to a specialist</div><h2>{e(h)}</h2><p>{e(p)}</p></div>
<div class="actions"><a class="btn btn-coral" href="{r}contact/#enquiry">Get a proposal</a><a class="btn btn-ghost" href="tel:{SITE["phone_tel"]}">{SITE["phone_display"]}</a></div></div></div></section>'''


def convert_strip(r, topic):
    return f'''<div class="convert"><div><b>Need {e(topic)} for your site?</b><span>Free consultation. Proposal within one working day.</span></div><div class="btns"><a class="btn btn-coral" href="{r}contact/#enquiry">Get a proposal</a><a class="btn btn-ghost" href="https://wa.me/{SITE["whatsapp"]}" target="_blank" rel="noopener">WhatsApp us</a></div></div>'''


def lead_section(r, topic, preset=""):
    return f'''<section class="alt" id="enquiry-section"><div class="wrap form-wrap">
 <div><p class="kicker">Talk to a UBM specialist</p><h2>Get a proposal for {e(topic)}</h2>
  <p class="lead">Tell us about your space. We reply within one working day with options, brands and a clear, itemised proposal.</p>
  <ul class="checks"><li><strong>Free consultation</strong>Vendor-neutral advice from AV specialists in Mumbai</li><li><strong>One accountable partner</strong>Design, supply, installation, service and training</li><li><strong>Trusted since 1997</strong>{len(BRANDS)} global brands, pan-India support</li></ul>
  <p style="margin-top:20px"><a class="link-arrow" href="tel:{SITE["phone_tel"]}">Prefer to talk? Call {SITE["phone_display"]}</a></p></div>
 {enquiry_form(r, preset)}
</div></section>'''


def sol_card(r, s):
    return f'''<a class="pcard reveal" href="{r}solutions/{s["slug"]}/"><div class="ph"><img src="{U(IMG[s["slug"]], 900)}" alt="{e(s["name"])}" loading="lazy"><span class="chip">Solution</span></div><div class="bd"><span class="ic-b">{ICONS[s["icon"]]}</span><h3>{e(s["name"])}</h3><p>{e(s["intro"])}</p><span class="link-arrow">Explore solution</span></div></a>'''


def ind_card(r, i):
    return f'''<a class="pcard reveal" href="{r}industries/{i["slug"]}/"><div class="ph"><img src="{U(IMG[i["slug"]], 900)}" alt="AV for {e(i["name"])}" loading="lazy"><span class="chip">Industry</span></div><div class="bd"><span class="ic-b">{ICONS[i["icon"]]}</span><h3>{e(i["name"])}</h3><p>{e(i["intro"])}</p><span class="link-arrow">See how we help</span></div></a>'''


def brand_card(r, b):
    return f'''<a class="pcard reveal" href="{r}{b["slug"]}/"><div class="ph"><img src="{U(IMG[b["slug"]], 900)}" alt="{e(b["name"])} products" loading="lazy"><span class="chip">{e(b["name"])}</span></div><div class="bd"><h3>{e(b["name"])}</h3><p>{e(b["intro"])}</p><span class="link-arrow">View range</span></div></a>'''


def post_card(r, p):
    return f'''<a class="pcard post reveal" data-cat="{e(p["cat"])}" href="{r}blog/{p["slug"]}/"><div class="ph"><img src="{U(IMG.get(p["slug"], IMG["blog"]), 900)}" alt="" loading="lazy"><span class="chip">{e(p["cat"])}</span></div><div class="bd"><span class="mono">{p["read"]} min read · {p["date"]}</span><h3 style="margin-top:10px">{e(p["title"])}</h3><p>{e(p["desc"])}</p><span class="link-arrow">Read guide</span></div></a>'''


def blog_filters():
    cats = sorted({p["cat"] for p in POSTS})
    btns = "".join(f'<button type="button" data-filter="{e(c)}">{e(c)}</button>' for c in cats)
    return f'<div class="filters" role="toolbar" aria-label="Filter posts by topic"><button type="button" class="on" data-filter="all">All posts</button>{btns}</div>'


def marquee(r):
    tiles = "".join(logo_tile(r, b) for b in BRANDS)
    return f'<div class="marquee"><div class="label">Global brands we distribute</div><div class="marquee-track">{tiles}{tiles}</div></div>'


STAT_IC = {
    "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>',
    "grid": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
    "map": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/></svg>',
}


def build_home():
    r = rel(0)
    slides = "".join(f'<div class="hero-slide{" on" if n == 0 else ""}" data-cap="{e(t)}"><img src="{U(pid, 2000)}" alt="{e(t)}" {"fetchpriority=high" if n == 0 else "loading=lazy"}></div>' for n, (pid, t, _) in enumerate(HERO_SLIDES))
    dots = "".join(f'<button type="button" aria-label="Show slide {n + 1}"{" class=on" if n == 0 else ""}></button>' for n in range(len(HERO_SLIDES)))
    sols = "".join(sol_card(r, s) for s in SOLUTIONS)
    spaces = "".join(f'''<a class="space" href="{r}industries/{i["slug"]}/"><img src="{U(IMG[i["slug"]], 800)}" alt="AV solutions for {e(i["name"])}" loading="lazy"><div class="cap"><small>{e(i["name"])}</small><h3>{e(i["h1"])}</h3><p>{e(i["intro"])}</p></div></a>''' for i in INDUSTRIES)
    svcs = "".join(f'<div class="card svc reveal"><span class="num">0{n + 1}</span><div class="icon">{ICONS[k]}</div><h3>{t}</h3><p>{e(d)}</p></div>' for n, (k, t, d) in enumerate(SERVICES))
    posts = "".join(post_card(r, p) for p in POSTS[:3])
    years = datetime.date.today().year - SITE["founded"]
    reel = [("35336", "LED and video walls", "solutions/video-wall-solutions/"), ("11942", "Stage and auditorium AV", "solutions/auditorium-av-solutions/"), ("32591", "Event sound and lighting", "solutions/auditorium-av-solutions/")]
    reel_js = json.dumps([{"src": f"https://assets.mixkit.co/videos/{v}/{v}-720.mp4", "cap": c, "href": h} for v, c, h in reel])
    body = f'''
<section class="hero2" aria-label="Introduction"><div class="wrap hero2-grid">
 <div class="hero2-copy">
  <p class="pill"><span class="dot"></span>Value-added AV distributor, Mumbai, since 1997</p>
  <h1>Classrooms, boardrooms and halls that just work.</h1>
  <p class="lead">UBM designs, supplies, installs and services complete audio-visual systems for India's schools, offices, hotels and venues. One accountable partner, from first drawing to years after handover.</p>
  <div class="hero-actions"><a class="btn btn-coral" href="contact/#enquiry">Get a free proposal</a><a class="btn btn-ghost" href="https://wa.me/{SITE["whatsapp"]}?text=Hi%20UBM%2C%20I%20need%20help%20with%20an%20AV%20project" target="_blank" rel="noopener">WhatsApp us now</a></div>
  <div class="quick2"><span>What do you need?</span>{"".join(f'<a href="contact/?solution={sl}#enquiry">{n}</a>' for sl, n in [("smart-classroom-solutions", "Smart classroom"), ("video-wall-solutions", "Video wall"), ("boardroom-meeting-room-av-solutions", "Boardroom"), ("auditorium-av-solutions", "Auditorium sound"), ("public-address-pa-systems", "PA system")])}</div>
  <div class="brandline"><span>Brands we supply</span><b>Epson</b><b>Bose Professional</b><b>BenQ</b><b>ViewSonic</b><b>ATEN</b><b>TOA</b></div>
 </div>
 <div class="mosaic" aria-hidden="true">
  <figure class="m1"><img src="{U(IMG["education"], 900)}" alt="" fetchpriority="high"><figcaption>Smart classrooms</figcaption></figure>
  <figure class="m2"><img src="{U(IMG["boardroom-meeting-room-av-solutions"], 700)}" alt=""><figcaption>Boardrooms</figcaption></figure>
  <figure class="m3"><img src="{U(IMG["auditorium-av-solutions"], 700)}" alt=""><figcaption>Auditoriums</figcaption></figure>
  <div class="float f1"><strong>{years} years</strong><span>of pro AV in India</span></div>
  <div class="float f2"><span class="ok"></span><div><strong>Proposal in 1 working day</strong><span>Free consultation</span></div></div>
 </div>
</div></section>

<section id="about"><div class="wrap partner">
 <div class="partner-media reveal"><img src="{U(IMG["about"], 1100)}" alt="UBM team with clients in a conference room" loading="lazy"><div class="partner-badge"><strong>{years} years</strong><span>of professional AV across India, since 1997</span></div></div>
 <div class="reveal"><p class="kicker">About UBM</p><h2>Your partner in professional AV excellence</h2>
  <p class="lead">Universal Business Machines is a Mumbai-based value-added distributor of professional audio-visual technology. Since 1997 our system designers and AV specialists have helped dealers, integrators and organisations choose, deploy and support systems that perform for years.</p>
  <div class="pillars">
   <div class="pillar"><span class="icon">{ICONS["shield"]}</span><div><h3>Expertise and experience</h3><p>Nearly three decades of designing and supplying AV for Indian spaces.</p></div></div>
   <div class="pillar"><span class="icon">{ICONS["handshake"]}</span><div><h3>Client and partner centric</h3><p>Vendor-neutral advice for end customers, and design support for dealers.</p></div></div>
   <div class="pillar"><span class="icon">{ICONS["service"]}</span><div><h3>Commitment to service</h3><p>Installation, training and maintenance from a team you can reach.</p></div></div>
  </div>
  <div class="hero-actions" style="margin-top:0"><a class="btn btn-blue" href="about-us/">Read more about UBM</a><a class="btn btn-ghost" href="contact/#enquiry">Consult now</a></div></div>
</div></section>

<section class="alt"><div class="wrap">
 <div class="sec-head"><div><div class="eyebrow">What we deliver</div><h2>We deliver turnkey AV solutions</h2><p class="lead">From a single huddle room to an entire campus, designed around the people who use it and the people who maintain it.</p></div><a class="btn btn-ghost" href="solutions/">All solutions →</a></div>
 <div class="grid g3 m-swipe">{sols}</div>
</div></section>

<section class="numbers" aria-label="UBM in numbers"><div class="wrap">
 <div><strong data-count="{years}">{years}</strong><span>Years in professional AV</span></div>
 <div><strong data-count="{len(BRANDS)}">{len(BRANDS)}</strong><span>Global brands distributed</span></div>
 <div><strong data-count="{len(INDUSTRIES)}">{len(INDUSTRIES)}</strong><span>Industries served</span></div>
 <div><strong data-count="6">6</strong><span>End-to-end services</span></div>
</div></section>

<section><div class="wrap">
 <div class="sec-head center"><div><div class="eyebrow">Our services</div><h2>From consultation to long-term support</h2><p class="lead">From the first drawing to years after handover, UBM stays with the project.</p></div></div>
 <div class="grid g3 m-tiles">{svcs}</div>
</div></section>

<section class="alt"><div class="wrap">
 <div class="sec-head"><div><div class="eyebrow">Specialised spaces</div><h2>AV designed for the way your sector works</h2></div><div class="car-btns"><button type="button" data-car="-1" aria-label="Previous">←</button><button type="button" data-car="1" aria-label="Next">→</button></div></div>
 <div class="carousel"><div class="track" id="spaces">{spaces}</div></div>
</div></section>

{marquee(r)}

<section><div class="wrap">
 <div class="split">
  <a class="path a reveal" href="dealer-partners/"><img src="{U(IMG["partners"], 1000)}" alt="" loading="lazy"><div class="eyebrow">For dealers &amp; integrators</div><h3>Win more projects with a distributor who designs with you.</h3>
   <ul><li>Pre-sales system design and BOQ support</li><li>Complementary multi-brand portfolio</li><li>Demos, training and project support</li><li>Responsive after-sales service</li></ul><span class="btn">Partner with UBM →</span></a>
  <a class="path b reveal" href="contact/#enquiry"><img src="{U(IMG["boardroom-meeting-room-av-solutions"], 1000)}" alt="" loading="lazy"><div class="eyebrow">For organisations</div><h3>One accountable partner from first drawing to final handover.</h3>
   <ul><li>Vendor-neutral consultation</li><li>Design, supply and installation</li><li>Maintenance and service plans</li><li>Training for your team</li></ul><span class="btn">Start your project →</span></a>
 </div>
</div></section>

<section class="alt"><div class="wrap">
 <div class="sec-head"><div><div class="eyebrow">From our blog</div><h2>Guides for Indian schools, offices and venues</h2><p class="lead">Practical, vendor-neutral advice for buyers, consultants and integrators.</p></div><a class="btn btn-ghost" href="blog/">Read the blog</a></div>
 <div class="grid g3 m-swipe">{posts}</div>
</div></section>

<section><div class="wrap">{faq_block(GENERAL_FAQS[:5], "Questions buyers ask us")}</div></section>

{lead_section(r, "your AV project")}'''
    page("", "Pro AV Distributor in Mumbai & India Since 1997 | UBM",
         "Mumbai-based value-added pro AV distributor since 1997: Epson, Bose, ATEN, Liberty AV, BenQ, ViewSonic & TOA. Smart classrooms, boardrooms, video walls & more.",
         body, schemas=(faq_schema(GENERAL_FAQS[:5]), {"@context": "https://schema.org", "@type": "WebSite", "name": "UBM, Universal Business Machines", "url": BASE + "/"}), depth=0, priority="1.0")


def flow_svg():
    return '''<div class="flow" aria-hidden="true">
 <div class="flow-title"><span>Signal path · Boardroom 04</span><i>Live</i></div>
 <svg viewBox="0 0 420 300">
  <path class="wire" d="M100 50 C160 50 160 150 190 150"/><path class="wire" d="M100 150 H190"/><path class="wire" d="M100 250 C160 250 160 150 190 150"/>
  <path class="wire" d="M290 150 C330 150 330 60 330 60"/><path class="wire" d="M290 150 H320"/><path class="wire" d="M290 150 C330 150 330 240 330 240"/>
  <path class="pulse" d="M100 50 C160 50 160 150 190 150 H290 C330 150 330 60 330 60"/>
  <path class="pulse d2" d="M100 150 H190 H290 H320"/>
  <path class="pulse d3" d="M100 250 C160 250 160 150 190 150 H290 C330 150 330 240 330 240"/>
  <g class="node"><rect x="8" y="30" width="92" height="40" rx="8"/><text x="20" y="49">Laptop</text><text class="sub" x="20" y="62">Wireless BYOD</text></g>
  <g class="node"><rect x="8" y="130" width="92" height="40" rx="8"/><text x="20" y="149">VC Camera</text><text class="sub" x="20" y="162">Auto-framing</text></g>
  <g class="node"><rect x="8" y="230" width="92" height="40" rx="8"/><text x="20" y="249">Ceiling mics</text><text class="sub" x="20" y="262">Beamforming</text></g>
  <g class="node hub"><rect x="190" y="124" width="100" height="52" rx="10"/><text x="205" y="147">UBM-designed</text><text x="205" y="162" style="font-weight:600;font-size:10px">Matrix · DSP</text></g>
  <g class="node"><rect x="320" y="38" width="94" height="40" rx="8"/><text x="331" y="57">4K Display</text><text class="sub" x="331" y="70">86" interactive</text></g>
  <g class="node"><rect x="320" y="130" width="94" height="40" rx="8"/><text x="331" y="149">Projector</text><text class="sub" x="331" y="162">Laser · 6,000 lm</text></g>
  <g class="node"><rect x="320" y="222" width="94" height="40" rx="8"/><text x="331" y="241">Loudspeakers</text><text class="sub" x="331" y="254">Even coverage</text></g>
 </svg>
</div>'''


def planner():
    return '''<section id="planner"><div class="wrap">
 <div class="sec-head"><div><div class="eyebrow">Interactive planner</div><h2>What does your space need?</h2><p class="lead">Pick a space and size to see the system a UBM designer would typically start with. Then send it to us for a tailored proposal.</p></div></div>
 <div class="planner reveal">
  <div class="planner-controls">
   <p class="pl-label">1 · Type of space</p>
   <div class="seg" data-group="space">
    <button type="button" class="on" data-v="classroom">Classroom</button><button type="button" data-v="boardroom">Boardroom</button><button type="button" data-v="auditorium">Auditorium</button><button type="button" data-v="lobby">Lobby / Retail</button><button type="button" data-v="campus">Campus / Building</button></div>
   <p class="pl-label">2 · Size</p>
   <div class="seg" data-group="size"><button type="button" data-v="s">Small</button><button type="button" class="on" data-v="m">Medium</button><button type="button" data-v="l">Large</button></div>
   <p class="pl-hint" id="pl-hint"></p>
  </div>
  <div class="planner-out" aria-live="polite">
   <div class="pl-head"><span class="mono">RECOMMENDED STARTING SYSTEM</span><h3 id="pl-title">Medium classroom</h3></div>
   <ul id="pl-list"></ul>
   <div class="pl-brands" id="pl-brands"></div>
   <a class="btn btn-gold" id="pl-cta" href="contact/#enquiry">Get a proposal for this space →</a>
  </div>
 </div>
</div></section>'''



def related_brands(r, slugs):
    return "".join(logo_tile(r, BR[s]) for s in slugs if s in BR)


def build_solutions():
    r = rel(1)
    cards = "".join(sol_card(r, s) for s in SOLUTIONS)
    body = page_hero(r, [("Solutions", "solutions/")], "AV solutions for every kind of space", "From a single huddle room to an entire campus, designed, supplied, installed and supported by UBM.", "Solutions") + f'<section><div class="wrap"><div class="grid g3">{cards}</div></div></section>' + hub_extra(*HUBS["solutions"]) + cta_band(r)
    page("solutions/", "Pro AV Solutions for Every Space | UBM Mumbai", "Explore UBM's professional AV solutions: smart classrooms, boardroom AV, video walls, auditorium sound, AV over IP and public address systems.", body, "solutions", schemas=(faq_schema(HUBS["solutions"][1]), crumbs_schema([("Home", ""), ("Solutions", "solutions/")])), priority="0.9")
    for s in SOLUTIONS:
        r = rel(2)
        path = f'solutions/{s["slug"]}/'
        inc = "".join(f"<li>{e(x)}</li>" for x in s["includes"])
        sections = "".join(f"<h2>{e(h)}</h2><p>{e(p)}</p>" for h, p in s["body"])
        inds = "".join(f'<li><a href="{r}industries/{i}/">{e(IND[i]["name"])} <span>→</span></a></li>' for i in s["industries"])
        others = "".join(f'<li><a href="{r}solutions/{o["slug"]}/">{e(o["name"])} <span>→</span></a></li>' for o in SOLUTIONS if o["slug"] != s["slug"])
        body = page_hero(r, [("Solutions", "solutions/"), (s["name"], path)], s["h1"], s["intro"], s["name"]) + f'''
<section><div class="wrap content">
 <article class="prose">
  <img class="feature-img" src="{U(IMG[s["slug"]], 1400)}" alt="{e(s["name"])} by UBM" loading="lazy">
  <p class="story-lede">{e(s["answer"])} UBM has served customers from Mumbai since 1997.</p>
  {convert_strip(r, s["name"].lower())}
  <h2>What's included</h2><ul>{inc}</ul>
  {sections}
  <h2>Brands we use</h2><div class="logo-row" style="margin:10px 0 30px">{related_brands(r, s["brands"])}</div>
  <h2>Our process</h2>
  <table class="spec-table"><tbody>{"".join(f"<tr><th>{n}</th><td>{e(d)}</td></tr>" for _, n, d in SERVICES)}</tbody></table>
 </article>
 <aside class="aside">
  <div class="aside-card dark"><h3>Get a proposal</h3><p>Share your room details, we respond within one working day.</p><a class="btn btn-gold" href="{r}contact/?solution={s["slug"]}#enquiry">Request a quote</a><a class="btn btn-ghost" href="https://wa.me/{SITE["whatsapp"]}?text=Hi%20UBM%2C%20I%27m%20interested%20in%20{e(s["name"]).replace(" ", "%20")}" target="_blank" rel="noopener">WhatsApp us</a></div>
  <div class="aside-card"><h3>Industries</h3><ul>{inds}</ul></div>
  <div class="aside-card"><h3>Other solutions</h3><ul>{others}</ul></div>
 </aside>
</div></section>
<section><div class="wrap">{faq_block(s["faqs"])}</div></section>
{lead_section(r, s["name"].lower(), s["name"])}'''
        svc = {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["kw"], "description": s["answer"],
               "provider": {"@id": BASE + "/#org"}, "areaServed": {"@type": "Country", "name": "India"}, "url": BASE + "/" + path}
        page(path, s["title"], s["desc"], body, "solutions", schemas=(svc, faq_schema(s["faqs"]), crumbs_schema([("Home", ""), ("Solutions", "solutions/"), (s["name"], path)])), priority="0.9")


def build_industries():
    for i in INDUSTRIES:
        r = rel(2)
        path = f'industries/{i["slug"]}/'
        st = STORIES[i["slug"]]
        sols = "".join(sol_card(r, SOL[s]) for s in i["solutions"])
        stats = "".join(f'''<div class="fact"><strong>{e(v)}</strong><p>{e(l)}</p><a href="{e(u)}" target="_blank" rel="noopener nofollow">Source: {e(src)}</a></div>''' if u else f'''<div class="fact"><strong>{e(v)}</strong><p>{e(l)}</p><span>Source: {e(src)}</span></div>''' for v, l, src, u in st["stats"])
        pains = "".join(f'<div class="pain"><h3>{e(h)}</h3><p>{e(t)}</p></div>' for h, t in st["pains"])
        fixes = "".join(f'<div class="fix"><span class="fix-n">{n + 1}</span><div><h3>{e(h)}</h3><p>{e(t)}</p></div></div>' for n, (h, t) in enumerate(st["fixes"]))
        steps = "".join(f"<li>{e(x)}</li>" for x in st["project"])
        faqs = st["faqs"] + i["faqs"]
        topic = "AV for " + i["name"].lower()
        body = page_hero(r, [("Industries", "industries/"), (i["name"], path)], i["h1"], i["intro"], i["name"]) + f'''
<section class="story"><div class="wrap story-grid">
 <div class="story-text"><p class="story-lede">{e(st["story"])}</p>{convert_strip(r, topic)}</div>
 <div class="facts">{stats}</div>
</div></section>
<section class="alt"><div class="wrap">
 <div class="sec-head"><div><p class="kicker">What goes wrong</p><h2>The problems we hear from {e(i["name"].lower())} teams</h2><p class="lead">Real questions and complaints from buyers on Reddit, Quora and in our own site visits.</p></div></div>
 <div class="pains">{pains}</div>
</div></section>
<section><div class="wrap">
 <div class="sec-head"><div><p class="kicker">How UBM fixes it</p><h2>What changes when UBM designs your space</h2></div></div>
 <div class="fixes">{fixes}</div>
 <div class="journey"><h3>How a UBM project runs</h3><ol>{steps}</ol></div>
</div></section>
<section class="alt"><div class="wrap"><div class="sec-head"><div><p class="kicker">Solutions</p><h2>Solutions for {e(i["name"].lower())}</h2></div></div><div class="grid g2 m-swipe">{sols}</div></div></section>
<section><div class="wrap">{faq_block(faqs)}</div></section>{lead_section(r, topic)}'''
        page(path, i["title"], i["desc"], body, "", schemas=(faq_schema(faqs), crumbs_schema([("Home", ""), ("Industries", "industries/"), (i["name"], path)])), priority="0.8")
    # hub
    r = rel(1)
    cards = "".join(ind_card(r, i) for i in INDUSTRIES)
    page("industries/", "Industries We Serve | AV for Education & Business | UBM", "UBM delivers professional AV for education, corporate, hospitality, places of worship, stadiums, home theatre and retail.",
         page_hero(r, [("Industries", "industries/")], "AV expertise across industries", "Every sector has different rooms, users and priorities. We design for yours.", "Industries") + f'<section><div class="wrap"><div class="grid g3">{cards}</div></div></section>' + hub_extra(*HUBS["industries"]) + cta_band(r), schemas=(faq_schema(HUBS["industries"][1]), crumbs_schema([("Home", ""), ("Industries", "industries/")])), priority="0.8")


def build_brands():
    r = rel(1)
    cards = "".join(brand_card(r, b) for b in BRANDS)
    page("brands/", "Pro AV Brands We Distribute in India | UBM",
         "UBM distributes leading pro AV brands in India, Epson, Bose Professional, ATEN, Liberty AV Solutions, ViewSonic, BenQ and TOA.",
         page_hero(r, [("Brands", "brands/")], "Global brands, local expertise", "A complementary portfolio across display, projection, audio, signal management and connectivity.", "Brands") + f'<section><div class="wrap"><div class="grid g3">{cards}</div></div></section>' + hub_extra(*HUBS["brands"]) + cta_band(r), "", schemas=(faq_schema(HUBS["brands"][1]), crumbs_schema([("Home", ""), ("Brands", "brands/")])), priority="0.8")
    for b in BRANDS:
        r = rel(1)
        path = f'{b["slug"]}/'  # keeps legacy URLs like /epson/ and /bose/ intact
        lines = "".join(f'<div class="card reveal"><h3>{e(n)}</h3><p>{e(d)}</p><a class="link-arrow" href="{r}contact/#enquiry">Enquire</a></div>' for n, d in b["lines"])
        faqs = [(f"Does UBM supply {b['name']} products?", f"Yes. UBM supplies {b['name']} products to dealers, system integrators and end customers from Mumbai, with support across India."),
                (f"Can UBM help choose the right {b['name']} model?", f"Yes. UBM's team helps select the right {b['name']} products for your room, application and budget, and supports installation and after-sales service."),
                (f"How do I get a {b['name']} quote?", f"Send your requirement through the enquiry form, WhatsApp {SITE['mobile_display']} or email {SITE['email']}.")]
        ans = f"UBM (Universal Business Machines), a Mumbai-based value-added pro AV distributor since 1997, supplies {b['name']} products, " + ", ".join(n for n, _ in b["lines"]).lower() + f", to dealers, system integrators and organisations across India, with design, installation and after-sales support."
        body = page_hero(r, [("Brands", "brands/"), (b["name"], path)], f'{b["name"]}, supplied and supported by UBM', b["intro"], "Brand partner") + f'''
<section style="padding-bottom:0"><div class="wrap"><p class="story-lede" style="max-width:70ch">{e(ans)}</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-head"><div><div style="margin-bottom:18px">{logo_tile(r, b).replace("<a ", "<span ").replace("</a>", "</span>")}</div><h2>{e(b["name"])} product range</h2><p class="lead">Ask our team for specifications, availability and project pricing.</p></div></div><div class="grid g3">{lines}</div></div></section>
<section><div class="wrap">{faq_block(faqs)}</div></section>{lead_section(r, b["name"] + " products")}'''
        page(path, b["title"], b["desc"], body, "", schemas=(faq_schema(faqs), crumbs_schema([("Home", ""), ("Brands", "brands/"), (b["name"], path)])), priority="0.8")


def build_blog():
    r = rel(1)
    cards = "".join(post_card(r, p) for p in POSTS)
    page("blog/", "AV Blog: Guides for Schools, Offices & Venues in India | UBM",
         "Practical guides on smart classrooms, interactive displays, boardroom AV, AV over IP and auditorium sound from UBM's 25+ years in pro AV.",
         page_hero(r, [("Blog", "blog/")], "The UBM blog: practical AV guides for India", "Vendor-neutral advice from more than 25 years of designing and supplying AV systems.", "Blog", actions=False) + f'<section class="blog-hub"><div class="wrap">{blog_filters()}<div class="grid g3 bloglist" id="bloglist">{cards}</div></div></section>' + hub_extra(*HUBS["blog"]) + cta_band(r), "blog", schemas=(faq_schema(HUBS["blog"][1]), crumbs_schema([("Home", ""), ("Blog", "blog/")])), priority="0.8")
    for p in POSTS:
        r = rel(2)
        path = f'blog/{p["slug"]}/'
        toc = "".join(f'<li><a href="#{slugify(h)}">{e(h)}</a></li>' for h in re.findall(r"^## (.+)$", p["body"], re.M))
        rel_posts = "".join(f'<li><a href="{r}blog/{q["slug"]}/">{e(q["title"])}</a></li>' for q in sorted((q for q in POSTS if q["slug"] != p["slug"]), key=lambda q: q["cat"] != p["cat"])[:5])
        body = page_hero(r, [("Blog", "blog/"), (p["title"], path)], p["title"], p["desc"], f'{p["cat"]} · {p["read"]} min read', actions=False) + f'''
<section><div class="wrap content">
 <article class="prose">
  <p class="post-byline mono">By the UBM Solutions Team · Updated {p["date"]}</p>
  <img class="feature-img" src="{U(IMG.get(p["slug"], IMG["blog"]), 1400)}" alt="" loading="lazy">
  <p class="story-lede">{e(p["summary"])} This guide is from UBM (Universal Business Machines), a Mumbai-based pro AV distributor since 1997.</p>
  {md(p["body"], r)}
  <div class="author-box"><img src="{r}assets/img/favicon.svg" alt="" width="56" height="56"><div><b>Written by the UBM Solutions Team</b><p>Pro AV system designers and product specialists at Universal Business Machines, Mumbai, advising Indian schools, offices and venues since 1997. Reviewed for technical accuracy before publishing. Published {p["date"]}, last reviewed {TODAY}. <a href="{r}editorial-policy/">How we write and review guides</a>.</p></div></div>
  {faq_block(p["faqs"], "FAQs")}
 </article>
 <aside class="aside">
  <div class="aside-card"><h3>In this guide</h3><ul class="toc">{toc}</ul></div>
  <div class="aside-card dark"><h3>Need expert advice?</h3><p>Talk to a UBM AV specialist about your project.</p><a class="btn btn-gold" href="{r}contact/#enquiry">Get a free consultation</a></div>
  <div class="aside-card"><h3>More guides</h3><ul>{rel_posts}</ul></div>
 </aside>
</div></section>{lead_section(r, 'your project')}'''
        art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["desc"],
               "datePublished": p["date"], "dateModified": TODAY, "author": {"@type": "Organization", "name": "UBM Solutions Team", "url": BASE + "/editorial-policy/"}, "reviewedBy": {"@id": BASE + "/#org"}, "isAccessibleForFree": True, "inLanguage": "en-IN",
               "publisher": {"@id": BASE + "/#org"}, "mainEntityOfPage": BASE + "/" + path, "keywords": p["kw"], "articleSection": p["cat"]}
        page(path, p["title"] + (" | UBM" if len(p["title"]) <= 59 else ""), p["desc"], body, "blog", schemas=(art, faq_schema(p["faqs"]), crumbs_schema([("Home", ""), ("Blog", "blog/"), (p["title"], path)])), priority="0.7", og_type="article")


def build_static_pages():
    r = rel(1)
    # About
    svc = "".join(f'<div class="card reveal"><div class="icon">{ICONS[k]}</div><h3>{n}</h3><p>{e(d)}</p></div>' for k, n, d in SERVICES)
    facts = [f"Legal name: Universal Business Machines (UBM)", f"Founded: {SITE['founded']}, Mumbai, India", "Business: value-added distributor of professional audio-visual (pro AV) technology",
             "Brands: " + ", ".join(x["name"] for x in BRANDS), "Services: design, consultation, installation, maintenance, service and training",
             "Solutions: " + ", ".join(s["name"] for s in SOLUTIONS), "Industries: " + ", ".join(i["name"] for i in INDUSTRIES),
             f"Address: {SITE['street']}, {SITE['city']} {SITE['postcode']}", f"Phone: {SITE['phone_display']} / {SITE['mobile_display']}", f"Email: {SITE['email']}, {SITE['email2']}"]
    kf = "".join(f"<li>{e(x)}</li>" for x in facts)
    about = page_hero(r, [("About us", "about-us/")], "A quarter-century of pro AV, built on people", "Founded in 1997, UBM is a dedicated group of pro AV professionals, system designers and technology managers.", "About UBM") + f'''
<section><div class="wrap why">
 <div class="prose reveal"><h2>Our story</h2>
  <p>Founded in 1997, we at UBM are a dedicated group of pro AV professionals, system designers and technology managers working together to accelerate the adoption of the right AV solutions, with one goal: to serve your AV distribution needs.</p>
  <p>Through interoperability and standardisation, the products we distribute enable great AV experiences. UBM can design and implement professional AV solutions that are cost-effective, agile and scalable, meeting the needs of today and tomorrow.</p>
  <p>Our greatest strength is our knowledgeable, helpful team. Through confident, experienced people we help our dealer partners navigate unexpected developments and realise important opportunities. Key members of our team have been with us since our humble beginnings, and we build on that as we grow.</p></div>
 <div class="reveal"><div class="timeline">
  <div class="tl"><b>1997</b><p>UBM founded in Mumbai as a specialist AV distributor.</p></div>
  <div class="tl"><b>Growth</b><p>Portfolio expands across projection, displays, professional audio and signal management.</p></div>
  <div class="tl"><b>Value-added</b><p>Design, consultation, installation, maintenance, service and training added to support partners end-to-end.</p></div>
  <div class="tl"><b>Today</b><p>Serving dealers, integrators and organisations across India with {len(BRANDS)} global brands.</p></div>
 </div></div>
</div></section>
<section><div class="wrap"><div class="sec-head"><div><p class="kicker">Key facts</p><h2>Key facts about UBM</h2></div></div><ul class="ticks keyfacts">{kf}</ul></div></section>
<section class="alt"><div class="wrap"><div class="sec-head"><div><div class="eyebrow">What we do</div><h2>End-to-end AV services</h2></div></div><div class="grid g3">{svc}</div></div></section>
<div class="logos"><div class="wrap"><p>Brands we distribute</p><div class="logo-row">{"".join(logo_tile(r, b) for b in BRANDS)}</div></div></div>
''' + hub_extra("UBM (Universal Business Machines) is a Mumbai-based value-added distributor of professional audio-visual technology founded in 1997, supplying Epson, Bose Professional, ATEN, Liberty AV Solutions, ViewSonic, BenQ and TOA with design, installation, service and training.", ABOUT_FAQ) + cta_band(r)
    page("about-us/", "About UBM | Value-Added Pro AV Distributor in Mumbai Since 1997", "Founded in 1997 in Mumbai, UBM is a team of pro AV professionals and system designers serving dealers and organisations across India.", about, "about", schemas=(faq_schema(ABOUT_FAQ), crumbs_schema([("Home", ""), ("About us", "about-us/")])), priority="0.8")

    page("editorial-policy/", "Editorial Policy: How UBM Writes AV Guides | UBM", "How the UBM Solutions Team researches, writes, fact-checks and updates its AV buying guides for Indian schools, offices and venues.",
         page_hero(r, [("Editorial policy", "editorial-policy/")], "How we write and review our guides", "Practical, vendor-neutral and checked by people who design AV systems for a living.", actions=False) + f'''<section><div class="wrap prose" style="max-width:820px">
<h2>Who writes our content</h2><p class="story-lede">Every guide on this site is written by the UBM Solutions Team: pro AV system designers and product specialists at Universal Business Machines, Mumbai, who have advised Indian schools, offices, hotels and venues since 1997.</p>
<h2>How we research</h2><ul><li>We start from real questions buyers ask us, and on Reddit and Quora.</li><li>Statistics come from named, linked sources such as the Ministry of Education (UDISE+), CAIT and published market research.</li><li>We do not publish made-up prices, client names or numbers.</li></ul>
<h2>How we review</h2><ul><li>Each guide is checked for technical accuracy by a UBM specialist before publishing.</li><li>Guides are reviewed regularly and the "last reviewed" date is shown on every article.</li><li>We correct errors as soon as we find them. Spot one? Email <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>.</li></ul>
<h2>Vendor neutrality</h2><p>UBM distributes several brands. Our guides compare technologies on their merits and recommend what suits the room, not a single product line.</p></div></section>''', "", priority="0.4")
    page("privacy-policy/", "Privacy Policy | UBM - Universal Business Machines", "How Universal Business Machines (UBM) collects, uses and protects the information you share through this website's enquiry forms and WhatsApp.",
         page_hero(r, [("Privacy policy", "privacy-policy/")], "Privacy policy", "How we handle the information you share with us.", actions=False) + f'''<section><div class="wrap prose" style="max-width:820px">
<p class="story-lede">Universal Business Machines (UBM) uses the details you submit through this website only to respond to your enquiry and provide the products and services you ask about.</p>
<h2>What we collect</h2><ul><li>Details you enter in our enquiry forms: name, organisation, phone, email, city and project details.</li><li>Messages you send us on WhatsApp, phone or email.</li><li>Anonymous website usage statistics, if analytics is enabled.</li></ul>
<h2>How we use it</h2><ul><li>To reply to your enquiry and prepare proposals.</li><li>To provide installation, service and support.</li><li>We never sell your details or share them with third parties for marketing.</li></ul>
<h2>Your choices</h2><p>To update or delete your information, email <a href="mailto:{SITE["email"]}">{SITE["email"]}</a> or call {SITE["phone_display"]}.</p></div></section>''', "", priority="0.3")

    # Dealer partners
    perks = [("design", "Pre-sales design", "System design, drawings and BOQs to help you win tenders."),
             ("handshake", "Project support", "Project pricing support, specifications for consultants and demos for your customers."),
             ("train", "Training", "Regular product and system training for your sales and technical teams."),
             ("shield", "After-sales service", "Warranty coordination, troubleshooting and replacements from Mumbai."),
             ("network", "Complete portfolio", "Display, projection, audio, signal management and connectivity from one partner."),
             ("consult", "A team that picks up", "Experienced people who know AV, many with us for decades.")]
    pk = "".join(f'<div class="card reveal"><div class="icon">{ICONS[k]}</div><h3>{n}</h3><p>{e(d)}</p></div>' for k, n, d in perks)
    pfaq = [("Who can become a UBM dealer partner?", "AV dealers, system integrators, IT resellers and consultants who supply or specify professional AV in India."),
            ("What support do UBM partners get?", "Pre-sales design, project support, demos, training, and after-sales service across UBM's brand portfolio."),
            ("How do I apply?", "Fill in the form on this page with 'Dealer / Integrator' selected. Our partner team will get in touch.")]
    partners = page_hero(r, [("Dealer partners", "dealer-partners/")], "Grow your AV business with a distributor that designs with you", "UBM's value-added distribution gives dealers and integrators the products, design help and support to win and deliver more projects.", "Dealer & integrator programme") + f'''
<section><div class="wrap"><div class="sec-head"><div><div class="eyebrow">Partner benefits</div><h2>More than a price list</h2></div></div><div class="grid g3">{pk}</div></div></section>
<section class="alt"><div class="wrap form-wrap"><div class="reveal"><div class="eyebrow">Apply</div><h2>Become a UBM partner</h2><p class="lead">Tell us about your business and the projects you work on.</p>{faq_block(pfaq, "Partner FAQs")}</div>{enquiry_form(r).replace('value="Dealer / Integrator"', 'value="Dealer / Integrator" checked').replace('value="End customer" checked', 'value="End customer"')}</div></section>'''
    page("dealer-partners/", "Become an AV Dealer Partner | UBM Distribution", "Join UBM's dealer and integrator programme, multi-brand pro AV portfolio, pre-sales design, project support, training and after-sales service since 1997.", partners, "partners", schemas=(faq_schema(pfaq), crumbs_schema([("Home", ""), ("Dealer partners", "dealer-partners/")])), priority="0.9")

    # Contact
    contact = page_hero(r, [("Contact", "contact/")], "Let's talk about your space", "Share your requirement and a UBM specialist will respond within one working day.", "Contact UBM", actions=False) + f'''
<section><div class="wrap form-wrap">
 <div class="reveal"><h2>Reach us directly</h2><p class="lead">Prefer to talk? Call, WhatsApp or visit us in Bandra (East), Mumbai.</p>
  <ul class="contact-list">
   <li><div class="icon">{ICONS["phone"]}</div><div><b>Office phone</b><a href="tel:{SITE["phone_tel"]}">{SITE["phone_display"]}</a></div></li>
   <li><div class="icon">{ICONS["consult"]}</div><div><b>Mobile / WhatsApp</b><a href="tel:{SITE["mobile_tel"]}">{SITE["mobile_display"]}</a> · <a href="https://wa.me/{SITE["whatsapp"]}" target="_blank" rel="noopener">Chat on WhatsApp</a></div></li>
   <li><div class="icon">{ICONS["mail"]}</div><div><b>Email</b><a href="mailto:{SITE["email"]}">{SITE["email"]}</a><br><a href="mailto:{SITE["email2"]}">{SITE["email2"]}</a></div></li>
   <li><div class="icon">{ICONS["pin"]}</div><div><b>Office</b>{e(SITE["street"])}, {SITE["city"]} {SITE["postcode"]}</div></li>
  </ul>
  <iframe class="map" style="margin-top:26px" src="{SITE["map_embed"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="UBM office location on Google Maps"></iframe>
 </div>
 {enquiry_form(r)}
</div></section>''' + hub_extra("UBM (Universal Business Machines) is a value-added pro AV distributor in Bandra (East), Mumbai, serving India since 1997. Reach the team on 022 2647 5639 or +91 98202 93108, or at connect@ubm.co.in and balraj@ubm.co.in.", CONTACT_FAQ)
    page("contact/", "Contact UBM | Pro AV Distributor, Bandra East, Mumbai", "Contact UBM, Bandra (East), Mumbai. Call 022 2647 5639 or +91 98202 93108, or email connect@ubm.co.in / balraj@ubm.co.in.", contact, "contact", schemas=(faq_schema(CONTACT_FAQ), crumbs_schema([("Home", ""), ("Contact", "contact/")])), priority="0.9")

    # Careers
    careers = page_hero(r, [("Careers", "careers/")], "Build your career in pro AV", "Join a team where experience is valued and many colleagues have grown with us for decades.", "Careers", actions=False) + f'''
<section><div class="wrap"><div class="grid g2">
 <div class="card"><span class="tag">Mumbai</span><h3>Senior Accountant</h3><p>Own accounts, reconciliations and compliance for a growing AV distribution business.</p><a class="link-arrow" href="mailto:{SITE["email"]}?subject=Application%3A%20Senior%20Accountant%20(Mumbai)">Apply by email</a></div>
 <div class="card"><span class="tag">Pune</span><h3>Sales Executive</h3><p>Grow dealer and enterprise relationships across Pune for our pro AV portfolio.</p><a class="link-arrow" href="mailto:{SITE["email"]}?subject=Application%3A%20Sales%20Executive%20(Pune)">Apply by email</a></div>
</div><p class="muted" style="margin-top:24px">Don't see your role? Send your CV to <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>.</p></div></section>'''
    page("careers/", "Careers at UBM | Pro AV Jobs in Mumbai & Pune", "Current openings at UBM, Universal Business Machines, Mumbai pro AV distributor: Senior Accountant (Mumbai) and Sales Executive (Pune).", careers, "", priority="0.5")

    # FAQ
    faqp = page_hero(r, [("FAQ", "faq/")], "Frequently asked questions", "Quick answers about UBM, our brands, services and how to work with us.", "FAQ", actions=False) + f'<section><div class="wrap">{faq_block(GENERAL_FAQS, "About UBM")}</div></section>' + f'<section class="alt"><div class="wrap">{faq_block([f for s in SOLUTIONS for f in s["faqs"][:2]], "About our solutions")}</div></section>' + cta_band(r)
    allf = GENERAL_FAQS + [f for s in SOLUTIONS for f in s["faqs"][:2]]
    page("faq/", "FAQ | Pro AV, Smart Classrooms, Boardrooms & Video Walls | UBM", "Answers to common questions about UBM, pro AV distribution, smart classrooms, boardroom AV, video walls, auditorium sound, AV over IP and PA systems.", faqp, "", schemas=(faq_schema(allf),), priority="0.7")

    # 404
    nf = f'<section class="page-hero on-dark"><div class="wrap"><div class="eyebrow">404</div><h1>This page has moved</h1><p class="lead">Our website has been redesigned. Try one of these:</p><div class="hero-actions"><a class="btn btn-gold" href="/">Home</a><a class="btn btn-ghost" href="/solutions/">Solutions</a><a class="btn btn-ghost" href="/contact/">Contact</a></div></div></section>'
    page("404.html", "Page not found | UBM", "The page you are looking for has moved.", nf, depth=0)


def build_meta_files():
    urls = "".join(f"<url><loc>{BASE}/{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>" for p, pr in pages)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User",
            "Google-Extended", "Googlebot", "Bingbot", "Applebot", "Applebot-Extended", "CCBot", "meta-externalagent", "Amazonbot", "DuckAssistBot", "YouBot"]
    robots = "# UBM - Universal Business Machines. Search engines and AI assistants are welcome.\n\n" + "".join(f"User-agent: {x}\nAllow: /\n\n" for x in bots) + "User-agent: *\nAllow: /\n\n" + f"Sitemap: {BASE}/sitemap.xml\n# AI summary: {BASE}/llms.txt\n"
    (OUT / "robots.txt").write_text(robots)
    # llms.txt, a plain summary for AI assistants and answer engines (GEO)
    lines = [f"# Universal Business Machines (UBM)", "",
             f"> Mumbai-based value-added distributor of professional audio-visual (pro AV) technology, founded in {SITE['founded']}. Supplies Epson, Bose Professional, ATEN, Liberty AV Solutions, ViewSonic, BenQ and TOA, with design, consultation, installation, maintenance, service and training for dealers, integrators and organisations across India.", "",
             f"- Address: {SITE['street']}, {SITE['city']} {SITE['postcode']}, India",
             f"- Phone: {SITE['phone_display']} · Mobile/WhatsApp: {SITE['mobile_display']} · Email: {SITE['email']}, {SITE['email2']}", "", "## Solutions"]
    lines += [f"- [{s['name']}]({BASE}/solutions/{s['slug']}/): {s['answer']}" for s in SOLUTIONS]
    lines += ["", "## Industries"] + [f"- [{i['name']}]({BASE}/industries/{i['slug']}/): {i['answer']}" for i in INDUSTRIES]
    lines += ["", "## Brands"] + [f"- [{b['name']}]({BASE}/{b['slug']}/): {b['intro']}" for b in BRANDS]
    lines += ["", "## Guides"] + [f"- [{p['title']}]({BASE}/blog/{p['slug']}/): {p['summary']}" for p in POSTS]
    lines += ["", "## Company pages", f"- [About UBM]({BASE}/about-us/)", f"- [Dealer & integrator programme]({BASE}/dealer-partners/)", f"- [Contact]({BASE}/contact/)", f"- [FAQ]({BASE}/faq/)", f"- [Careers]({BASE}/careers/)"]
    lines += ["", "## Key facts"] + [f"- {q} {a}" for q, a in GENERAL_FAQS]
    (OUT / "llms.txt").write_text("\n".join(lines) + "\n")
    full = ["# Universal Business Machines (UBM): full reference for AI assistants", ""] + lines[2:4] + ["", "## About", GENERAL_FAQS[0][1], ""]
    for s in SOLUTIONS:
        full += [f"## {s['name']}", f"URL: {BASE}/solutions/{s['slug']}/", s["answer"], "Includes: " + "; ".join(s["includes"]), ""] + [f"Q: {q}\nA: {a}" for q, a in s["faqs"]] + [""]
    for i in INDUSTRIES:
        st = STORIES[i["slug"]]
        full += [f"## {i['name']}", f"URL: {BASE}/industries/{i['slug']}/", st["story"], ""] + [f"- {v}: {l} (source: {src})" for v, l, src, _ in st["stats"]] + [""]
    for p in POSTS:
        full += [f"## {p['title']}", f"URL: {BASE}/blog/{p['slug']}/", p["summary"], ""]
    (OUT / "llms-full.txt").write_text("\n".join(full) + "\n")
    (OUT / ".nojekyll").write_text("")
    import csv
    with open(ROOT / "seo/titles-and-descriptions.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["url", "title", "title_chars", "meta_description", "description_chars"])
        for t_path, t_title, t_desc in META_LOG:
            w.writerow([BASE + "/" + t_path, t_title, len(t_title), t_desc, len(t_desc)])


def main():
    for p in OUT.iterdir() if OUT.exists() else []:
        if p.name != "assets":
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    build_home(); build_solutions(); build_industries(); build_brands(); build_blog(); build_static_pages(); build_meta_files()
    print(f"Built {len(pages)} pages into {OUT} ({'production' if PROD else 'staging/noindex'})")


if __name__ == "__main__":
    main()
