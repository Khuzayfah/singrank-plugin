#!/usr/bin/env python3
"""SingRank standalone technical SEO audit — no API keys needed.

Audits any URL/domain live: robots.txt (AI-crawler access), llms.txt, sitemap,
and per-page on-page checks (title, meta, canonical, H1, headings, viewport,
og:image, schema types incl. deprecated FAQPage/HowTo lint, img alt, thin
content, noindex, link counts). Outputs a markdown report + score.

Usage:
  python seo_audit.py https://example.com                 # homepage + 5 sitemap pages
  python seo_audit.py https://example.com/page --single   # just this page
  python seo_audit.py https://example.com --pages 10 --out report.md --json report.json
"""
import argparse
import sys as _sys
if hasattr(_sys.stdout, 'reconfigure'):
    _sys.stdout.reconfigure(encoding='utf-8')
    _sys.stderr.reconfigure(encoding='utf-8')
import json
import re
import sys
import urllib.parse
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36 SingRankAudit/1.0")
TIMEOUT = 20

AI_BOTS = ["GPTBot", "OAI-SearchBot", "ClaudeBot", "PerplexityBot",
           "Google-Extended", "Googlebot-Extended", "Applebot-Extended",
           "CCBot", "Amazonbot", "meta-externalagent", "Bytespider",
           "Diffbot", "cohere-ai", "anthropic-ai"]

DEPRECATED_SCHEMA = {"FAQPage", "HowTo", "SpecialAnnouncement"}

def fetch(url, method="GET"):
    try:
        r = requests.request(method, url, headers={"User-Agent": UA},
                             timeout=TIMEOUT, allow_redirects=True)
        return r
    except requests.RequestException as e:
        return e

def check_robots(base):
    out = {"exists": False, "ai_bots_blocked": [], "ai_bots_allowed": [],
           "sitemaps": [], "blocks_all": False}
    r = fetch(base + "/robots.txt")
    if isinstance(r, Exception) or r.status_code != 200:
        return out
    out["exists"] = True
    txt = r.text
    out["sitemaps"] = re.findall(r"(?im)^sitemap:\s*(\S+)", txt)
    # Parse per-agent groups
    groups, agent = {}, None
    for line in txt.splitlines():
        line = line.split("#")[0].strip()
        m = re.match(r"(?i)user-agent:\s*(.+)", line)
        if m:
            agent = m.group(1).strip()
            groups.setdefault(agent, [])
            continue
        m = re.match(r"(?i)disallow:\s*(.*)", line)
        if m and agent is not None:
            groups[agent].append(m.group(1).strip())
    star_blocked = "/" in groups.get("*", [])
    out["blocks_all"] = star_blocked
    lower = {k.lower(): v for k, v in groups.items()}
    for bot in AI_BOTS:
        rules = lower.get(bot.lower())
        if rules is not None:
            (out["ai_bots_blocked"] if "/" in rules else out["ai_bots_allowed"]).append(bot)
        elif star_blocked:
            out["ai_bots_blocked"].append(bot)
        else:
            out["ai_bots_allowed"].append(bot)
    return out

def sitemap_urls(base, robots, limit):
    candidates = robots.get("sitemaps") or [base + "/sitemap.xml"]
    urls, seen = [], set()
    for sm in candidates[:3]:
        r = fetch(sm)
        if isinstance(r, Exception) or r.status_code != 200:
            continue
        soup = BeautifulSoup(r.text, "xml")
        # sitemap index → follow first few child sitemaps
        children = [l.text.strip() for l in soup.select("sitemap > loc")][:3]
        for child in children:
            rc = fetch(child)
            if not isinstance(rc, Exception) and rc.status_code == 200:
                soup2 = BeautifulSoup(rc.text, "xml")
                for loc in soup2.select("url > loc"):
                    u = loc.text.strip()
                    if u not in seen:
                        seen.add(u); urls.append(u)
                    if len(urls) >= limit: return urls
        for loc in soup.select("url > loc"):
            u = loc.text.strip()
            if u not in seen:
                seen.add(u); urls.append(u)
            if len(urls) >= limit: return urls
    return urls

def audit_page(url, host):
    p = {"url": url, "issues": [], "warnings": []}
    r = fetch(url)
    if isinstance(r, Exception):
        p["issues"].append(f"FETCH FAILED: {r}")
        return p
    p["status"] = r.status_code
    p["final_url"] = r.url
    p["redirect_hops"] = len(r.history)
    if r.status_code != 200:
        p["issues"].append(f"HTTP {r.status_code}")
        return p
    if p["redirect_hops"] >= 2:
        p["warnings"].append(f"redirect chain {p['redirect_hops']} hops")
    soup = BeautifulSoup(r.text, "lxml")

    # noindex
    robots_meta = soup.find("meta", attrs={"name": re.compile("^robots$", re.I)})
    if robots_meta and "noindex" in (robots_meta.get("content") or "").lower():
        p["issues"].append("NOINDEX meta present (CRITICAL if page should rank)")

    # title
    title = (soup.title.string or "").strip() if soup.title and soup.title.string else ""
    p["title"] = title
    p["title_len"] = len(title)
    if not title: p["issues"].append("missing <title>")
    elif len(title) > 60: p["warnings"].append(f"title {len(title)}c (>60, truncates)")
    elif len(title) < 30: p["warnings"].append(f"title {len(title)}c (<30, wasted space)")

    # meta description
    md = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    desc = (md.get("content") or "").strip() if md else ""
    p["meta_desc_len"] = len(desc)
    if not desc: p["issues"].append("missing meta description")
    elif not (120 <= len(desc) <= 165): p["warnings"].append(f"meta desc {len(desc)}c (target 150-160)")

    # canonical
    can = soup.find("link", rel=lambda v: v and "canonical" in v)
    p["canonical"] = can.get("href", "").strip() if can else ""
    if not p["canonical"]:
        p["warnings"].append("no canonical tag")
    else:
        cu = urllib.parse.urlparse(p["canonical"])
        fu = urllib.parse.urlparse(r.url)
        if (cu.netloc, cu.path.rstrip("/")) != (fu.netloc, fu.path.rstrip("/")):
            p["warnings"].append(f"canonical points elsewhere: {p['canonical']}")

    # H1
    h1s = soup.find_all("h1")
    p["h1_count"] = len(h1s)
    if len(h1s) == 0: p["issues"].append("no H1")
    elif len(h1s) > 1: p["issues"].append(f"{len(h1s)} H1 tags (must be 1)")

    # heading order
    levels = [int(h.name[1]) for h in soup.find_all(re.compile("^h[1-6]$"))]
    for a, b in zip(levels, levels[1:]):
        if b - a > 1:
            p["warnings"].append(f"heading order skip h{a}→h{b}")
            break

    # viewport / og:image
    if not soup.find("meta", attrs={"name": "viewport"}):
        p["warnings"].append("no viewport meta (mobile)")
    if not soup.find("meta", attrs={"property": "og:image"}):
        p["warnings"].append("no og:image (social share)")

    # schema JSON-LD
    types = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
        except (json.JSONDecodeError, TypeError):
            p["warnings"].append("invalid JSON-LD block")
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, dict):
                for node in item.get("@graph", [item]):
                    t = node.get("@type")
                    if isinstance(t, list): types.extend(t)
                    elif t: types.append(t)
    p["schema_types"] = sorted(set(types))
    dep = DEPRECATED_SCHEMA.intersection(types)
    if dep:
        p["issues"].append(f"DEPRECATED schema for rich results: {', '.join(sorted(dep))} — strip; keep Q&A as on-page content")
    if not types:
        p["warnings"].append("no JSON-LD schema found")

    # images alt
    imgs = soup.find_all("img")
    noalt = [i for i in imgs if not (i.get("alt") or "").strip()]
    p["images"] = len(imgs); p["images_no_alt"] = len(noalt)
    if imgs and len(noalt) / len(imgs) > 0.3:
        p["warnings"].append(f"{len(noalt)}/{len(imgs)} images missing alt")

    # word count / thin
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    words = len(re.findall(r"\w+", soup.get_text(" ")))
    p["word_count"] = words
    if words < 300:
        p["warnings"].append(f"thin content ({words} words in raw HTML — check JS rendering)")

    # links
    internal = external = 0
    for a in soup.find_all("a", href=True):
        href = urllib.parse.urljoin(r.url, a["href"])
        if urllib.parse.urlparse(href).netloc == host: internal += 1
        elif href.startswith("http"): external += 1
    p["internal_links"] = internal; p["external_links"] = external
    if internal < 5: p["warnings"].append(f"only {internal} internal links (target ≥5)")
    return p

def score(site, pages):
    s = 100
    if not site["robots"]["exists"]: s -= 5
    if site["robots"]["blocks_all"]: s -= 30
    s -= min(15, 2 * len(site["robots"]["ai_bots_blocked"]))
    if not site["llms_txt"]: s -= 5
    if not site["sitemap_found"]: s -= 5
    for p in pages:
        s -= min(15, 5 * len(p.get("issues", [])))
        s -= min(6, 1 * len(p.get("warnings", [])))
    return max(0, s)

def main():
    ap = argparse.ArgumentParser(description="SingRank standalone SEO audit")
    ap.add_argument("url")
    ap.add_argument("--pages", type=int, default=5, help="max sitemap pages to audit")
    ap.add_argument("--single", action="store_true", help="audit only the given URL")
    ap.add_argument("--out", help="write markdown report to file")
    ap.add_argument("--json", dest="json_out", help="write JSON to file")
    args = ap.parse_args()

    u = urllib.parse.urlparse(args.url if "://" in args.url else "https://" + args.url)
    base = f"{u.scheme}://{u.netloc}"
    host = u.netloc

    robots = check_robots(base)
    llms = fetch(base + "/llms.txt")
    llms_ok = not isinstance(llms, Exception) and llms.status_code == 200 and len(llms.text) > 20

    targets = [args.url if "://" in args.url else base]
    sitemap_found = False
    if not args.single:
        sm = sitemap_urls(base, robots, args.pages)
        sitemap_found = bool(sm)
        for x in sm:
            if x not in targets and len(targets) < args.pages + 1:
                targets.append(x)
    site = {"base": base, "robots": robots, "llms_txt": llms_ok,
            "sitemap_found": sitemap_found or bool(robots["sitemaps"])}
    pages = [audit_page(t, host) for t in targets]
    total = score(site, pages)

    lines = [f"# SEO Audit — {host}",
             f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · singrank tools/seo_audit.py_",
             "", f"## Score: {total}/100", "", "## Site level",
             f"- robots.txt: {'OK' if robots['exists'] else 'MISSING'}"
             + (" — ⚠️ BLOCKS ALL CRAWLERS" if robots["blocks_all"] else ""),
             f"- AI crawlers blocked: {', '.join(robots['ai_bots_blocked']) or 'none'}",
             f"- llms.txt: {'present' if llms_ok else 'MISSING'}",
             f"- sitemap: {'found' if site['sitemap_found'] else 'NOT FOUND'}", ""]
    for p in pages:
        lines.append(f"## {p['url']}")
        if "status" in p:
            lines.append(f"- status {p['status']} · title {p.get('title_len','?')}c · "
                         f"meta {p.get('meta_desc_len','?')}c · H1×{p.get('h1_count','?')} · "
                         f"{p.get('word_count','?')}w · int links {p.get('internal_links','?')} · "
                         f"schema: {', '.join(p.get('schema_types') or ['—'])}")
        for i in p.get("issues", []): lines.append(f"- 🔴 {i}")
        for w in p.get("warnings", []): lines.append(f"- 🟡 {w}")
        lines.append("")
    report = "\n".join(lines)
    print(report)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(report)
    if args.json_out:
        open(args.json_out, "w", encoding="utf-8").write(
            json.dumps({"score": total, "site": site, "pages": pages}, indent=2))
    sys.exit(0 if total >= 70 else 1)

if __name__ == "__main__":
    main()
