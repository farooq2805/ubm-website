# UBM (ubm.co.in) — Website revamp, SEO / AEO / GEO and B2B lead-generation plan

Prepared October 2026. Data: live crawl of ubm.co.in and live Google India searches (12 money keywords, 20 Oct 2026). Search volumes are not included because the keyword-volume tool had no credits; priorities are based on intent, live results and competitor presence.

---

## 1. What we found on the current site

| Area | Finding | Impact |
|---|---|---|
| **Google Analytics / Tag Manager** | **None installed.** No GA4 (`G-…`), Universal Analytics, GTM, Meta Pixel or Clarity code anywhere in the HTML. | Zero visibility of traffic or leads today. |
| **Google Search Console** | **No verification meta tag in the HTML.** It *could* still be verified via DNS or an HTML file — ask the client to check search.google.com/search-console with their Google account. | Unknown indexing health. |
| Title / meta | Every page's title is just **"UBM"**; **no meta descriptions**. | Google has nothing to rank pages for. |
| Rankings | ubm.co.in appears in the **top 10 for none** of the 12 core keywords tested (AV distributor India, Epson projector distributor Mumbai, video wall solutions Mumbai, etc.). | No organic lead flow. |
| robots.txt / sitemap.xml | **Neither exists** — both URLs return the homepage. | Weak crawling. |
| Soft 404s | Any random URL returns the homepage with status 200. | Duplicate-content signals. |
| Schema | No structured data (Organization, LocalBusiness, FAQ). | Not eligible for rich results; weak AI-answer signals. |
| Content | Very thin; "Learn more" buttons only open pop-overs; some text is machine-spun ("financial institution" for "content bank", "video partitions" for "video walls"). | Hurts trust and E-E-A-T. |
| Contact | Two different phone numbers/emails across pages (022 2647 5639 / connect@ vs +91 98202 93108 / balraj@). Social icons link to `/1`, `/2`, `/3`, `/4` (broken). Copyright 2022. | Inconsistent entity data hurts local SEO and AI answers. |
| Lead capture | One generic form; no WhatsApp pre-fill, no segmentation (dealer vs end customer), no tracking. | Leads not qualified or measured. |

## 2. Competitive landscape (live Google India results)

| Keyword | Who ranks (top results) | AI Overview? |
|---|---|---|
| AV distributor in India | actis.co.in, avnirvanaindia.com, radiant.in, alphatec.co.in, miantic.com + directories | No |
| pro AV distributor Mumbai | proaudiovideo.in, netlabindia.com, allwaveav.com, radiant.in | No |
| boardroom AV solutions Mumbai | vcnow.in, allwaveav.com, turbonet.co.in, sispl.co.in, pratyam.co.in | No |
| Epson projector distributor Mumbai | epsonshop.co.in, epson.co.in, Justdial, IndiaMART | No |
| Bose professional distributor India | boseprofessional.com, audiomaxx.in, avstore.in, sunlitesystems.com | No |
| Aten KVM distributor India | aten.com, **rptechindia.com**, itgindia.com | **Yes** — cites rptechindia, aten, team5tech |
| interactive flat panel distributor India | IndiaMART, TradeIndia, raisesolutions.in, adrtechindia.com | **Yes** — cites IndiaMART, gladwingroup, TradeIndia |
| smart classroom solutions India | mafatlaltechnology, navneettoptech, adrtechindia | **Yes** — cites adrtechindia, advancetechindia, smarttech |
| auditorium sound system installation Mumbai | audioshop.in, asaudio.in, Justdial, IndiaMART | **Yes** — cites avenuesound, audioshop, Justdial |
| AV over IP solutions India | bzbgear, imagsystems + global sites | **Yes** — cites avaccess.in, avinity.in |

**Takeaways**
1. **IndiaMART, Justdial and TradeIndia take 2–4 spots on most commercial searches and are cited in AI Overviews.** A complete, consistent UBM listing on each is the fastest visibility win (GEO).
2. Competitor sites win with **dedicated pages per solution and per brand** and FAQ-rich content. UBM had neither; the new site has 6 solution pages, 7 industry pages, 7 brand pages and 6 guides.
3. AI Overviews already appear for education, AV-over-IP, KVM and auditorium searches. Pages with a clear direct answer, FAQ schema and consistent business details are the ones that get cited, so every new page is built that way.

## 3. Keyword strategy (priority)

Full map with target pages: `seo/keywords.csv` (39 keywords). The core:

**P1: high intent, money pages**
- Distribution: *AV distributor in India · pro AV distributor Mumbai · value added AV distributor India* → Home, Dealer Partners
- Brands: *Epson projector distributor Mumbai · Bose Professional distributor India · ATEN KVM distributor India* → /epson/, /bose/, /aten/ (same URLs as today, so existing equity is kept)
- Solutions: *smart classroom solutions India/Mumbai · boardroom AV solutions Mumbai · video wall solutions Mumbai · auditorium sound system installation Mumbai · AV over IP solutions India · interactive flat panel distributor India*

**P2: supporting and informational (blog, AEO)**
- *smart class setup cost in India · smart classroom equipment list · interactive flat panel vs projector · what is AV over IP · auditorium sound system design · PA system for office India · best pro AV distributor India*

**P3: industries**
- *hotel AV solutions · church sound system · home theatre installation Mumbai*

## 4. B2B lead-generation engine (no ads, no video)

1. **Two audience paths on every key page:** "Dealers & integrators" (the distributor's core business) and "Organisations" (end customers), each with its own CTA.
2. **Interactive Space Planner** on the homepage: the visitor picks a space type and size, sees a recommended system, then clicks "Get a proposal" with the plan already filled into the form. Engaging, and it pre-qualifies the lead.
3. **Qualified enquiry form:** role, organisation, solution, city, number of rooms and timeline. It sends to WhatsApp today; set `form_endpoint` in `src/content.py` to send to a CRM, Google Sheet (via Apps Script) or Formspree.
4. **Sticky WhatsApp and mobile call/quote bar** on every page.
5. **GA4 `generate_lead` event** fires on every form submission, so leads are measurable as soon as the GA4 ID is added.
6. **Dealer programme page** to recruit integrators, which is UBM's biggest growth lever as a distributor.
7. **LinkedIn (organic):** turn each blog guide into 3–4 LinkedIn posts or carousels (use the `content-repurposing` skill). LinkedIn is where institutional and corporate buyers are.
8. **Directory listings (GEO):** Google Business Profile, IndiaMART, Justdial, TradeIndia and LinkedIn Company Page, all with identical name, address, phone, founding year and brand list.
9. **Brand-partner backlinks:** ask Epson, BenQ, ViewSonic, ATEN, Liberty AV and TOA to list UBM on their "where to buy / distributor" pages. These are the highest-authority links available.

## 5. SEO / AEO / GEO built into the new site

- Unique, keyword-led title and meta description on every page; one H1; clean URLs; canonical tags; Open Graph tags.
- **Schema:** Organization + LocalBusiness (founding date 1997, address, geo, phone), Service, FAQPage, BreadcrumbList, BlogPosting.
- **Answer-first blocks** ("In short" / "Quick answer") at the top of every solution, industry and blog page, the format AI Overviews and LLMs quote.
- **`/llms.txt`:** a plain-language summary of UBM for ChatGPT, Perplexity, Claude and Gemini crawlers.
- sitemap.xml, robots.txt, real 404 page, fast static HTML, mobile-first layout.
- **Monitoring:** `seo/audit.py` (technical, AEO and GEO score per page), `seo/rank_tracker.py` (Google India positions and AI Overview citations each week), a GitHub Action that runs both every Monday, and four Claude agents in `.claude/agents/` (seo-auditor, aeo-geo-optimizer, rank-tracker, content-writer).

## 6. Switching to the new site without losing rankings

The current site ranks for very little, so the risk is low. Do it properly anyway:

1. **Keep the domain** `www.ubm.co.in`. Never launch on a new domain.
2. **Keep brand URLs identical:** /epson/, /bose/, /aten/, /liberty-av-solutions/, /viewsonic/, /benq/ already match.
3. **301-redirect every old URL** to its new equivalent. The full map and nginx rules are in `seo/redirects.md`.
4. **The staging preview is `noindex`**, so Google won't index a duplicate before launch. At launch, build with `UBM_ENV=production`, which removes noindex and sets canonical URLs to www.ubm.co.in.
5. **Before switching DNS:** add the GA4 ID and Search Console verification in `src/content.py`, and copy the brand-logo images from `/asset/img/` to the new host.
6. **On launch day:** verify the domain in Search Console, submit `sitemap.xml`, use URL Inspection on the homepage and top pages, and check the old URLs return 301s.
7. **First 4 weeks:** watch Search Console coverage and 404 reports weekly (the seo-auditor agent does this).

## 7. Confirm with the client before production

- Is UBM an **authorised** distributor for each brand? The site currently says "brands we distribute" and avoids "authorised" until confirmed.
- What is the "sehn" logo on the current site? It's unlabelled, so it was left out.
- Real numbers to add for trust: projects delivered, dealer-partner count, cities covered, notable clients or case studies (with permission), certifications. **None were invented.**
- Which phone and email should leads go to: connect@ubm.co.in / 022 2647 5639, or balraj@ubm.co.in / +91 98202 93108?
- Social profile URLs (LinkedIn especially).
- Real project photos. The site uses designed visuals for now; real installation photos will lift trust and conversion.
