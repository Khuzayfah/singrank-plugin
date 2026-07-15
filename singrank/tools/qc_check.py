#!/usr/bin/env python3
"""SingRank QC v1.2 — deterministic checks (Pipeline Stage 5 companion).

Runs the machine-checkable half of the SingRank QC gate on a finished article:
link liveness, GEO capsule structure, FAQ extractability, banned AI-filler
phrases, burstiness, schema deprecation lint (FAQPage/HowTo = P0), language
mix, word count. Factcheck-vs-brief and registry compliance remain manual
(Claude does those with web_research.py verify + the playbook roster).

Usage:
  python qc_check.py article.html --base-url https://client.com
  python qc_check.py article.html --base-url https://client.com --lang id --min-words 2500
Exit code: 0 = no P0 found, 1 = P0 present (blocking).
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

import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36 SingRankQC/1.2")
TIMEOUT = 15

BANNED_PHRASES = [
    "in today's digital landscape", "in the ever-evolving", "it's worth noting",
    "as we all know", "let's dive in", "without further ado",
    "in this article, we will", "welcome to our guide", "in conclusion",
    "to summarize", "in summary", "final thoughts", "wrapping up",
    "navigate the complexities", "testament to", "plays a crucial role",
    "when it comes to", "unlock the", "elevate your", "delve into",
    "tapestry", "in the realm of", "di era digital ini", "tanpa basa-basi",
    "seperti yang kita ketahui",
]
DEPRECATED_SCHEMA = {"FAQPage", "HowTo", "SpecialAnnouncement"}
ID_STOPWORDS = {"yang", "dan", "untuk", "dengan", "dari", "adalah", "tidak",
                "bisa", "akan", "juga", "pada", "atau", "kami", "anda"}
EN_STOPWORDS = {"the", "and", "for", "with", "from", "that", "this", "your",
                "are", "will", "can", "also", "our", "you"}

def check_links(soup, base_url, skip_live):
    p0, p1, rows = [], [], []
    host = urllib.parse.urlparse(base_url).netloc if base_url else ""
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        url = urllib.parse.urljoin(base_url or "", href)
        anchor = a.get_text(" ", strip=True)
        if re.fullmatch(r"(click here|read more|here|selengkapnya|baca selengkapnya|klik di sini)",
                        anchor.lower()):
            p1.append(f"weak anchor '{anchor}' → {url}")
        if url in seen:
            continue
        seen.add(url)
        if skip_live:
            rows.append((url, "skipped", anchor)); continue
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT,
                             allow_redirects=True, stream=True)
            status = r.status_code
            hops = len(r.history)
            r.close()
            rows.append((url, status, anchor))
            if status >= 400:
                p0.append(f"BROKEN LINK {status}: {url} (anchor '{anchor}')")
            elif hops >= 2:
                p1.append(f"redirect chain {hops} hops: {url}")
        except requests.RequestException as e:
            p0.append(f"LINK UNREACHABLE: {url} ({type(e).__name__})")
            rows.append((url, "error", anchor))
    return p0, p1, rows

def section_blocks(soup):
    """Yield (heading_text, level, words_in_section, first60_words_text)."""
    heads = soup.find_all(re.compile(r"^h[23]$"))
    for h in heads:
        words, first = [], []
        for sib in h.find_all_next():
            if sib.name and re.fullmatch(r"h[1-6]", sib.name):
                break
            if sib.name == "p":
                w = re.findall(r"\w+", sib.get_text(" "))
                if not first:
                    first = w[:60]
                words.extend(w)
        yield h.get_text(" ", strip=True), int(h.name[1]), len(words), " ".join(first)

def check_geo(soup):
    p0, p1 = [], []
    n_ok = n_total = 0
    for text, level, wc, first60 in section_blocks(soup):
        if wc == 0:
            continue
        n_total += 1
        if 120 <= wc <= 180:
            n_ok += 1
        # answer-first: first 60 words should carry a number or a definitive verb clause
        if not first60:
            p1.append(f"section '{text[:50]}' has no paragraph text directly under it")
    if n_total and n_ok / n_total < 0.5:
        p1.append(f"only {n_ok}/{n_total} H2/H3 sections are 120-180w self-contained blocks")
    # FAQ extractability: h3 questions
    faq_qs = [t for t, lvl, wc, _ in section_blocks(soup)
              if lvl == 3 and (t.endswith("?") or re.match(
                  r"(?i)^(what|how|why|when|where|can|do|does|is|are|apa|bagaimana|mengapa|kapan|berapa|apakah)\b", t))]
    details = soup.find_all("summary")
    if len(faq_qs) + len(details) < 5:
        p1.append(f"FAQ: only {len(faq_qs)+len(details)} question headings/summaries found (target ≥5)")
    return p0, p1

def check_schema(soup):
    p0, p1, types = [], [], []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
        except (json.JSONDecodeError, TypeError):
            p1.append("invalid JSON-LD block (parse error)")
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, dict):
                for node in item.get("@graph", [item]):
                    t = node.get("@type")
                    if isinstance(t, list): types.extend(t)
                    elif t: types.append(t)
    dep = DEPRECATED_SCHEMA.intersection(types)
    if dep:
        p0.append(f"DEPRECATED schema present: {', '.join(sorted(dep))} — strip it; "
                  "keep Q&A as on-page content (engine-standard §4 / QC v1.2 Check 6)")
    if types and "Article" not in types and "BlogPosting" not in types:
        p1.append(f"no Article/BlogPosting schema (found: {', '.join(sorted(set(types))) or 'none'})")
    return p0, p1, sorted(set(types))

def check_style(soup, lang):
    p0, p1 = [], []
    text = soup.get_text(" ")
    low = re.sub(r"\s+", " ", text.lower())
    hits = [ph for ph in BANNED_PHRASES if ph in low]
    if hits:
        p1.append("banned AI-filler phrases: " + "; ".join(f"'{h}'" for h in hits[:6]))
    # burstiness: flag paragraphs where 3+ consecutive sentences are all >=15 words
    flat = 0
    for para in soup.find_all("p"):
        sents = re.split(r"(?<=[.!?])\s+", para.get_text(" ", strip=True))
        lens = [len(s.split()) for s in sents if s.strip()]
        run = 0
        for L in lens:
            run = run + 1 if L >= 15 else 0
            if run >= 3:
                flat += 1
                break
    if flat > 3:
        p1.append(f"burstiness: {flat} paragraphs have 3+ consecutive long sentences — vary rhythm")
    # language mix
    words = re.findall(r"[a-z]+", low)
    idc = sum(1 for w in words if w in ID_STOPWORDS)
    enc = sum(1 for w in words if w in EN_STOPWORDS)
    if idc > 20 and enc > 20 and min(idc, enc) / max(idc, enc) > 0.35:
        p0.append(f"LANGUAGE MIX detected (id~{idc} vs en~{enc} stopword hits) — one language per article")
    elif lang == "id" and enc > idc:
        p1.append("expected Bahasa Indonesia but English dominates")
    elif lang == "en" and idc > enc:
        p1.append("expected English but Bahasa Indonesia dominates")
    return p0, p1

def main():
    ap = argparse.ArgumentParser(description="SingRank QC deterministic checks")
    ap.add_argument("file", help="article HTML file")
    ap.add_argument("--base-url", default="", help="client base URL for resolving relative links")
    ap.add_argument("--lang", choices=["en", "id"], help="expected language")
    ap.add_argument("--min-words", type=int, default=2500)
    ap.add_argument("--skip-links", action="store_true", help="skip live link checks")
    ap.add_argument("--json", dest="json_out", help="write JSON result to file")
    args = ap.parse_args()

    html_text = open(args.file, encoding="utf-8").read()
    soup = BeautifulSoup(html_text, "lxml")

    P0, P1 = [], []
    wc = len(re.findall(r"\w+", soup.get_text(" ")))
    if wc < args.min_words:
        P0.append(f"WORD COUNT {wc} < floor {args.min_words}")

    lp0, lp1, link_rows = check_links(soup, args.base_url, args.skip_links)
    gp0, gp1 = check_geo(soup)
    sp0, sp1, schema_types = check_schema(soup)
    tp0, tp1 = check_style(soup, args.lang)
    P0 += lp0 + gp0 + sp0 + tp0
    P1 += lp1 + gp1 + sp1 + tp1

    # deterministic score share (max 60 of the QC-v1.2 100; factcheck 30 +
    # compliance 10 stay manual): links 15, GEO 20, schema 10, style 15
    s = 60
    s -= min(15, 8 * len(lp0) + 2 * len(lp1))
    s -= min(20, 10 * len(gp0) + 4 * len(gp1))
    s -= min(10, 10 * len(sp0) + 3 * len(sp1))
    s -= min(15, 8 * len(tp0) + 3 * len(tp1))
    s = max(0, s)

    print("=== SINGRANK QC (deterministic) ===")
    print(f"FILE: {args.file}   WORDS: {wc}   SCHEMA: {', '.join(schema_types) or '—'}")
    print(f"DETERMINISTIC SCORE: {s}/60  (factcheck 30 + registry compliance 10 = manual)")
    print(f"LINKS CHECKED: {len(link_rows)}")
    print("P0 (blocking):" if P0 else "P0 (blocking): none")
    for x in P0: print(f"  🔴 {x}")
    print("P1 (major):" if P1 else "P1 (major): none")
    for x in P1: print(f"  🟡 {x}")
    print("MANUAL NEXT: factcheck every claim vs brief provenance "
          "(web_research.py verify), registry compliance, hook-gate, disclaimer.")
    print("=== END ===")
    if args.json_out:
        open(args.json_out, "w", encoding="utf-8").write(json.dumps(
            {"words": wc, "score60": s, "p0": P0, "p1": P1,
             "schema_types": schema_types,
             "links": [{"url": u, "status": st, "anchor": a} for u, st, a in link_rows]},
            indent=2, ensure_ascii=False))
    sys.exit(1 if P0 else 0)

if __name__ == "__main__":
    main()
