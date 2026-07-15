#!/usr/bin/env python3
"""SingRank prospect hunter — qualified B2B lead generation for the agency.

The strategy: don't spray. QUALIFY. Find businesses whose SEO is measurably weak,
prove it with a real audit, and reach them via their OWN published business
contact. A pitch with a concrete finding ("your site has 12 broken links and
ranks nowhere for your main service") converts; a cold blast does not.

SCOPE & ETHICS (baked in, not optional):
- PUBLIC BUSINESS contact only — the email/phone/form a company publishes on its
  own Contact/About/footer for exactly this purpose. Business data, not personal.
- Skips obvious personal addresses (gmail/hotmail/yahoo/outlook personal) unless
  it's clearly the business's listed contact.
- Respects robots.txt on the target's own domain; rate-limited; identifies itself.
- Does NOT bypass logins, anti-bot, or paywalls; does NOT scrape event attendee
  lists or personal directories. Singapore PDPA: business-contact, opt-out honoured
  downstream, no personal-data harvesting.

Two modes:
  qualify   Given candidate business URLs (from Claude's WebSearch of a niche +
            area — keyless search is blocked here), for each: run the SEO audit,
            pull the PUBLIC contact, and score the LEAD (weaker SEO + reachable =
            hotter prospect, because there's more for us to fix and a way in).
  pack      Merge qualified leads into leads.jsonl + LEADS.md (ranked, CRM-ready),
            each row carrying the specific audit hook to open the pitch with.

Usage:
  python prospect_hunter.py qualify --niche "dental clinic singapore" \
      --urls https://clinicA.sg https://clinicB.sg ... --out-dir leads_dental
  python prospect_hunter.py pack --in-dir leads_dental
Facts are audit-derived (real, from the live site) — no fabricated metrics.
"""
import argparse
import sys as _sys
if hasattr(_sys.stdout, 'reconfigure'):
    _sys.stdout.reconfigure(encoding='utf-8')
    _sys.stderr.reconfigure(encoding='utf-8')
import json
import os
import re
import time
import urllib.parse
import urllib.robotparser
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

import seo_audit  # sibling: check_robots, audit_page, fetch

UA = ("Mozilla/5.0 (compatible; SingRankProspect/1.0; +https://singrank.com) "
      "AppleWebKit/537.36")
TIMEOUT = 20
CONTACT_PATHS = ["/contact", "/contact-us", "/contactus", "/about", "/about-us",
                 "/get-in-touch", "/enquiry", "/reach-us"]
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
SG_PHONE_RE = re.compile(r"(?:\+?65[\s\-]?)?[689]\d{3}[\s\-]?\d{4}")
PERSONAL_HOSTS = {"gmail.com", "hotmail.com", "yahoo.com", "yahoo.com.sg",
                  "outlook.com", "icloud.com", "live.com", "qq.com"}
# tech/tracking/CDN noise — never a real business contact
NOISE_EMAIL = re.compile(
    r"(?i)(sentry|wixpress|\.wix\.|shopify|cloudflare|google|gstatic|"
    r"schema\.org|example\.|sentry-next|@2x|\.png|\.jpg|\.svg|w3\.org|"
    r"placeholder|domain\.com|yourdomain|email@|@email)")

def robots_ok(base, path="/"):
    try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(base + "/robots.txt")
        rp.read()
        return rp.can_fetch(UA, base + path)
    except Exception:
        return True  # no robots = allowed

def get(url):
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT,
                         allow_redirects=True)
        return r if r.status_code == 200 else None
    except requests.RequestException:
        return None

def find_contact(base, home_html):
    """Pull public business email/phone/contact-form from the site."""
    host = urllib.parse.urlparse(base).netloc.lower().removeprefix("www.")
    emails, phones, contact_page = set(), set(), ""
    def harvest(html):
        for m in EMAIL_RE.findall(html):
            e = m.lower()
            if NOISE_EMAIL.search(e):
                continue
            dom = e.split("@")[1]
            if dom in PERSONAL_HOSTS:
                continue
            # same-domain business email is the gold standard; else any non-noise biz email
            if dom == host or host.split(".")[0] in dom or True:
                emails.add(e)
        for m in SG_PHONE_RE.findall(html):
            digits = re.sub(r"\D", "", m)
            if len(digits) >= 8:
                phones.add(m.strip())
    # mailto links are the cleanest signal
    soup = BeautifulSoup(home_html, "lxml")
    for a in soup.find_all("a", href=True):
        if a["href"].lower().startswith("mailto:"):
            e = a["href"][7:].split("?")[0].strip().lower()
            if EMAIL_RE.fullmatch(e) and not NOISE_EMAIL.search(e) \
                    and e.split("@")[1] not in PERSONAL_HOSTS:
                emails.add(e)
        if any(p in a["href"].lower() for p in ["contact", "enquir", "about"]):
            contact_page = contact_page or urllib.parse.urljoin(base, a["href"])
    harvest(home_html)
    # visit one contact page if we still have no email
    if not emails:
        for p in ([contact_page] if contact_page else []) + \
                 [base + p for p in CONTACT_PATHS]:
            if not p:
                continue
            time.sleep(0.6)  # polite rate limit
            r = get(p)
            if r:
                harvest(r.text)
                contact_page = contact_page or p
                if emails:
                    break
    return {"emails": sorted(emails)[:3], "phones": sorted(phones)[:2],
            "contact_page": contact_page}

def score_lead(audit_score, contact, page):
    """Hotter lead = weaker SEO (more to fix) AND reachable AND a real business."""
    reachable = 2 if contact["emails"] else (1 if contact["phones"] or contact["contact_page"] else 0)
    if reachable == 0:
        return 0, "no public contact — skip"
    # SEO weakness = opportunity. 40-70 = sweet spot (fixable, clearly needs help).
    if audit_score is None:
        opp = 40
    elif audit_score < 40:
        opp = 70   # badly broken — huge upside but may be abandoned
    elif audit_score < 70:
        opp = 100  # clearly needs help + salvageable = best prospect
    elif audit_score < 85:
        opp = 55
    else:
        opp = 25   # already strong — low need
    lead = round(opp * (0.6 + 0.2 * reachable), 1)  # reachability weighting
    tier = "🔥 HOT" if lead >= 80 else "warm" if lead >= 50 else "cold"
    return lead, tier

def qualify_one(url):
    u = urllib.parse.urlparse(url if "://" in url else "https://" + url)
    base = f"{u.scheme}://{u.netloc}"
    if not robots_ok(base):
        return {"url": base, "skipped": "robots.txt disallows"}
    r = get(base)
    if not r:
        return {"url": base, "skipped": "unreachable"}
    # SEO audit (reuse seo_audit internals)
    robots = seo_audit.check_robots(base)
    page = seo_audit.audit_page(base, u.netloc)
    site = {"robots": robots, "llms_txt": False, "sitemap_found": bool(robots.get("sitemaps"))}
    ascore = seo_audit.score(site, [page])
    contact = find_contact(base, r.text)
    lead, tier = score_lead(ascore, contact, page)
    # the pitch hook = the single most citable audit weakness
    hooks = []
    if page.get("issues"): hooks += page["issues"][:2]
    if page.get("warnings"): hooks += page["warnings"][:2]
    if robots.get("ai_bots_blocked"): hooks.append(f"AI crawlers blocked: {', '.join(robots['ai_bots_blocked'][:3])}")
    title = ""
    soup = BeautifulSoup(r.text, "lxml")
    if soup.title: title = soup.title.get_text(strip=True)[:80]
    return {"url": base, "business": title, "seo_score": ascore,
            "lead_score": lead, "tier": tier,
            "emails": contact["emails"], "phones": contact["phones"],
            "contact_page": contact["contact_page"],
            "pitch_hooks": hooks[:4]}

def main():
    ap = argparse.ArgumentParser(description="SingRank qualified B2B prospect hunter")
    sub = ap.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("qualify")
    q.add_argument("--niche", required=True)
    q.add_argument("--urls", nargs="+", required=True)
    q.add_argument("--out-dir", default="leads")
    q.add_argument("--threads", type=int, default=5)
    p = sub.add_parser("pack"); p.add_argument("--in-dir", required=True)
    args = ap.parse_args()

    if args.cmd == "qualify":
        os.makedirs(args.out_dir, exist_ok=True)
        print(f"[qualify] {len(args.urls)} candidates for niche '{args.niche}'…")
        leads = []
        with ThreadPoolExecutor(args.threads) as ex:
            for f in as_completed([ex.submit(qualify_one, u) for u in args.urls]):
                r = f.result(); leads.append(r)
                tag = r.get("tier", r.get("skipped", "?"))
                print(f"  {tag:8} {r.get('url','')} "
                      f"(seo {r.get('seo_score','-')}, lead {r.get('lead_score','-')})")
        leads = [l for l in leads if not l.get("skipped")]
        leads.sort(key=lambda x: -x.get("lead_score", 0))
        meta = {"niche": args.niche, "count": len(leads)}
        open(os.path.join(args.out_dir, "leads.jsonl"), "w", encoding="utf-8").write(
            "\n".join(json.dumps(l, ensure_ascii=False) for l in leads))
        open(os.path.join(args.out_dir, "meta.json"), "w", encoding="utf-8").write(
            json.dumps(meta, ensure_ascii=False))
        _write_pack(args.out_dir, args.niche, leads)
    else:
        leads = [json.loads(l) for l in
                 open(os.path.join(args.in_dir, "leads.jsonl"), encoding="utf-8")
                 if l.strip()]
        meta = json.load(open(os.path.join(args.in_dir, "meta.json"), encoding="utf-8"))
        _write_pack(args.in_dir, meta["niche"], leads)

def _write_pack(out_dir, niche, leads):
    hot = [l for l in leads if l.get("lead_score", 0) >= 80]
    lines = [f"# PROSPECT LEADS — {niche}",
             f"_{len(leads)} qualified · {len(hot)} HOT · singrank prospect_hunter_",
             "",
             "> Public business contact only (PDPA-safe B2B). Open each pitch with the",
             "> audit hook — a real finding from their live site, not a cold intro.",
             "", "| Lead | Business | SEO | Contact | Pitch hook |",
             "|---|---|---|---|---|"]
    for l in leads:
        contact = l["emails"][0] if l["emails"] else (
            l["phones"][0] if l["phones"] else l.get("contact_page", "—"))
        hook = (l["pitch_hooks"][0] if l.get("pitch_hooks") else "—")[:60]
        lines.append(f"| {l.get('tier','')} {l.get('lead_score','')} | "
                     f"{(l.get('business') or l['url'])[:40]} | {l.get('seo_score','-')} | "
                     f"{contact} | {hook} |")
    lines.append("\n## Full lead detail\n")
    for l in leads:
        lines.append(f"### {l.get('tier','')} {l['url']} (lead {l.get('lead_score')})")
        lines.append(f"- Business: {l.get('business','')}")
        lines.append(f"- SEO score: {l.get('seo_score','-')}/100")
        lines.append(f"- Emails: {', '.join(l['emails']) or '—'} · "
                     f"Phones: {', '.join(l['phones']) or '—'} · "
                     f"Contact: {l.get('contact_page','—')}")
        lines.append(f"- Pitch hooks (real audit findings): " +
                     ("; ".join(l.get("pitch_hooks", [])) or "—"))
        lines.append("")
    open(os.path.join(out_dir, "LEADS.md"), "w", encoding="utf-8").write("\n".join(lines))
    print(f"\n=== {len(leads)} leads ({len(hot)} HOT) → {out_dir}\\LEADS.md + leads.jsonl ===")
    print("Next: for a HOT lead, run seo_audit.py --out for the full report to attach,")
    print("then a personalised pitch built on its pitch_hooks. Log outreach separately.")

if __name__ == "__main__":
    main()
