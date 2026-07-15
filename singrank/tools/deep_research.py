#!/usr/bin/env python3
"""SingRank deep research — SERP top-10 teardown + fact harvesting.

Given the top-10 URLs for a target keyword (from Claude's WebSearch — keyless
engines are blocked on this network), this tool fetches every competitor page
and produces:
  1. Per-page teardown: word count, H2/H3 outline, tables, lists, stats
     sentences, FAQ questions, publish date, schema types.
  2. Coverage matrix: which subtopics (heading terms) each page covers.
  3. GAP report: subtopics covered by <=2 pages (information-gain candidates)
     and questions nobody answers well.
  4. Benchmark: median word count, table usage, freshness — what "good" looks
     like on this SERP.
  5. Fact bank: quotable stat sentences with their source URL (provenance
     candidates — each must still be verified via web_research.py verify).

Usage:
  python deep_research.py --keyword "hdb toilet renovation cost" \
      --urls https://a.com/x https://b.com/y ... [--out teardown.md] [--json t.json]
  python deep_research.py --keyword "..." --urls-file urls.txt

Zero-fabrication: this tool only reports what is literally on the fetched
pages. Anything it cannot fetch is marked UNREACHABLE, never guessed.
"""
import argparse
import sys as _sys
if hasattr(_sys.stdout, 'reconfigure'):
    _sys.stdout.reconfigure(encoding='utf-8')
    _sys.stderr.reconfigure(encoding='utf-8')
import json
import re
import sys
from collections import Counter

import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
TIMEOUT = 25

STOP = set("""the a an and or of to in for with on at from by is are was were be
been this that these those it its as your you we our us how what why when where
which can do does not no vs versus best top guide 2024 2025 2026 yang dan untuk
dengan dari pada atau adalah tidak bisa akan juga cara apa bagaimana di ke""".split())

def fetch_page(url):
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT,
                         allow_redirects=True)
    except requests.RequestException as e:
        return {"url": url, "status": f"UNREACHABLE ({type(e).__name__})"}
    if r.status_code != 200:
        return {"url": url, "status": r.status_code}
    soup = BeautifulSoup(r.text, "lxml")
    page = {"url": url, "status": 200}
    page["title"] = soup.title.get_text(strip=True) if soup.title else ""
    # schema types
    types = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
            items = data if isinstance(data, list) else [data]
            for it in items:
                if isinstance(it, dict):
                    for node in it.get("@graph", [it]):
                        t = node.get("@type")
                        types.extend(t if isinstance(t, list) else [t] if t else [])
        except (json.JSONDecodeError, TypeError):
            pass
    page["schema_types"] = sorted({t for t in types if t})
    # publish date
    date = ""
    for sel, attr in [("meta[property='article:published_time']", "content"),
                      ("meta[property='article:modified_time']", "content"),
                      ("time[datetime]", "datetime")]:
        el = soup.select_one(sel)
        if el and el.get(attr):
            date = el.get(attr)[:10]; break
    page["date"] = date
    # structural counts BEFORE stripping
    page["tables"] = len(soup.find_all("table"))
    page["lists"] = len(soup.find_all(["ul", "ol"]))
    # headings outline
    outline = [(h.name, re.sub(r"\s+", " ", h.get_text(" ", strip=True))[:120])
               for h in soup.find_all(["h2", "h3"])]
    page["outline"] = outline
    page["h2_count"] = sum(1 for n, _ in outline if n == "h2")
    page["h3_count"] = sum(1 for n, _ in outline if n == "h3")
    page["questions"] = [t for _, t in outline if t.endswith("?") or re.match(
        r"(?i)^(what|how|why|when|which|where|can|do|does|is|are|should|"
        r"apa|bagaimana|mengapa|kapan|berapa|apakah|haruskah)\b", t)]
    # main text
    for tag in soup(["script", "style", "nav", "footer", "header", "aside",
                     "form", "noscript"]):
        tag.decompose()
    main = soup.find("article") or soup.find("main") or soup.body or soup
    text = main.get_text(" ", strip=True)
    words = re.findall(r"\w+", text)
    page["words"] = len(words)
    page["numbers_per_100w"] = round(
        len(re.findall(r"\d[\d,.]*%?", text)) / max(1, len(words)) * 100, 1)
    # stat sentences: contain a number AND a unit/currency/% or source-ish cue
    stats = []
    for sent in re.split(r"(?<=[.!?])\s+", text):
        if len(sent) < 40 or len(sent) > 320:
            continue
        if re.search(r"\d", sent) and re.search(
                r"(?i)(\$|S\$|Rp|%|percent|per cent|according to|survey|study|"
                r"report|data|statistics|hdb|bca|lta|official|berdasarkan|"
                r"menurut|riset|laporan|sq ?ft|sqm|hours?|days?|weeks?|months?)", sent):
            stats.append(re.sub(r"\s+", " ", sent).strip())
        if len(stats) >= 12:
            break
    page["stat_sentences"] = stats
    return page

def heading_terms(outline):
    terms = set()
    for _, text in outline:
        for w in re.findall(r"[a-zA-ZÀ-ɏ]{4,}", text.lower()):
            if w not in STOP:
                terms.add(w)
        # bigrams for better topics
        toks = [w for w in re.findall(r"[a-zA-ZÀ-ɏ]{3,}", text.lower())
                if w not in STOP]
        for a, b in zip(toks, toks[1:]):
            terms.add(f"{a} {b}")
    return terms

def main():
    ap = argparse.ArgumentParser(description="SingRank SERP deep research")
    ap.add_argument("--keyword", required=True)
    ap.add_argument("--urls", nargs="*", default=[])
    ap.add_argument("--urls-file", help="file with one URL per line")
    ap.add_argument("--out", help="write markdown report to file")
    ap.add_argument("--json", dest="json_out", help="write JSON to file")
    args = ap.parse_args()

    urls = list(args.urls)
    if args.urls_file:
        urls += [l.strip() for l in open(args.urls_file, encoding="utf-8")
                 if l.strip() and not l.startswith("#")]
    if not urls:
        print("No URLs given. Get the top-10 with Claude's WebSearch first, "
              "then pass them via --urls.", file=sys.stderr)
        sys.exit(2)

    pages = [fetch_page(u) for u in urls]
    ok = [p for p in pages if p.get("status") == 200 and p.get("words", 0) > 150]

    # coverage matrix
    per_page_terms = {p["url"]: heading_terms(p["outline"]) for p in ok}
    counts = Counter()
    for terms in per_page_terms.values():
        counts.update(terms)
    n = max(1, len(ok))
    common = [(t, c) for t, c in counts.most_common(60) if c >= max(2, n // 2)]
    gaps = [(t, c) for t, c in counts.most_common(200)
            if c <= 2 and " " in t][:25]  # bigram topics few pages cover
    all_questions = []
    for p in ok:
        all_questions += [(q, p["url"]) for q in p["questions"]]

    med = lambda xs: sorted(xs)[len(xs)//2] if xs else 0
    bench = {
        "pages_fetched": len(ok),
        "median_words": med([p["words"] for p in ok]),
        "median_h2": med([p["h2_count"] for p in ok]),
        "median_tables": med([p["tables"] for p in ok]),
        "pages_with_tables": sum(1 for p in ok if p["tables"] > 0),
        "median_numbers_per_100w": med([p["numbers_per_100w"] for p in ok]),
        "freshest_date": max([p["date"] for p in ok if p["date"]], default=""),
        "schema_in_use": sorted({t for p in ok for t in p["schema_types"]}),
    }

    lines = [f"# SERP Deep Research — \"{args.keyword}\"",
             f"_Fetched {len(ok)}/{len(urls)} pages · singrank tools/deep_research.py_", "",
             "## Benchmark (what 'good' looks like on this SERP)",
             f"- Median words: **{bench['median_words']}** · median H2: {bench['median_h2']}"
             f" · numbers/100w: {bench['median_numbers_per_100w']}",
             f"- Tables: {bench['pages_with_tables']}/{len(ok)} pages use them"
             f" (median {bench['median_tables']}) — AI engines lift tables verbatim",
             f"- Freshest page: {bench['freshest_date'] or 'unknown'}",
             f"- Schema seen: {', '.join(bench['schema_in_use']) or '—'}", "",
             "## Coverage matrix (subtopics most pages cover — you MUST cover these)"]
    for t, c in common[:25]:
        lines.append(f"- {t} — {c}/{len(ok)} pages")
    lines += ["", "## ⭐ GAP candidates (≤2 pages cover — information-gain opportunities)"]
    for t, c in gaps:
        lines.append(f"- {t} — only {c} page(s)")
    lines += ["", "## Question bank (from competitor headings — answer these better)"]
    seen_q = set()
    for q, u in all_questions[:30]:
        if q.lower() not in seen_q:
            seen_q.add(q.lower())
            lines.append(f"- {q}  _({u})_")
    lines += ["", "## Fact bank (VERIFY EACH via web_research.py verify before using)"]
    for p in ok:
        for s in p["stat_sentences"][:4]:
            lines.append(f"- \"{s}\" — SOURCE: {p['url']}")
    lines += ["", "## Per-page teardown"]
    for p in pages:
        if p.get("status") != 200:
            lines.append(f"### {p['url']}\n- status: {p['status']}")
            continue
        lines.append(f"### {p['url']}")
        lines.append(f"- {p['words']}w · H2×{p['h2_count']} H3×{p['h3_count']} · "
                     f"tables {p['tables']} · num/100w {p['numbers_per_100w']} · "
                     f"date {p['date'] or '?'} · schema: {', '.join(p['schema_types']) or '—'}")
        for name, text in p["outline"][:20]:
            lines.append(f"  - {name.upper()}: {text}")
    report = "\n".join(lines)
    print(report)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(report)
    if args.json_out:
        open(args.json_out, "w", encoding="utf-8").write(json.dumps(
            {"keyword": args.keyword, "benchmark": bench,
             "coverage": common, "gaps": gaps,
             "questions": [q for q, _ in all_questions],
             "pages": pages}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
