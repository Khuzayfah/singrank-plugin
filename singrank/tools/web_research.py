#!/usr/bin/env python3
"""SingRank web research tool — keyless search, fetch, and claim verification.

Three modes:
  search  — DuckDuckGo HTML search (no API key). Flags primary sources (gov/edu/official).
  fetch   — fetch a URL and extract title, meta, date, clean main text.
  verify  — fetch a URL and grade a claim against the page: EXACT / PARAPHRASE / NOT-FOUND.

Usage:
  python web_research.py search "hdb renovation permit rules 2026" --max 8
  python web_research.py search "biaya usaha laundry" --site go.id
  python web_research.py fetch https://www.hdb.gov.sg/... --max-chars 4000
  python web_research.py verify https://source.example "renovation permit costs $30 per application"

Zero-fabrication support: verify returns NOT-FOUND rather than guessing —
a NOT-FOUND claim must be marked [verify before publishing] or removed.
"""
import argparse
import sys as _sys
if hasattr(_sys.stdout, 'reconfigure'):
    _sys.stdout.reconfigure(encoding='utf-8')
    _sys.stderr.reconfigure(encoding='utf-8')
import html
import json
import re
import sys
import urllib.parse

import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
TIMEOUT = 20

PRIMARY_PATTERNS = [
    r"\.gov(\.[a-z]{2})?$", r"\.gov\.sg$", r"\.go\.id$", r"\.gov\.my$",
    r"\.edu(\.[a-z]{2})?$", r"\.edu\.sg$", r"\.ac\.id$", r"\.mil$",
    r"^(www\.)?(who|worldbank|imf|oecd|un)\.org$",
]
OFFICIAL_HOSTS = {"hdb.gov.sg", "lta.gov.sg", "mom.gov.sg", "muis.gov.sg",
                  "bca.gov.sg", "nea.gov.sg", "iras.gov.sg", "case.org.sg",
                  "bps.go.id", "kemenperin.go.id", "kemenkes.go.id",
                  "bpom.go.id", "kemendag.go.id", "imi.gov.my", "mm2h.gov.my"}

def is_primary(url):
    host = urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")
    if host in OFFICIAL_HOSTS:
        return True
    return any(re.search(p, host) for p in PRIMARY_PATTERNS)

def _decode_ddg(href):
    m = re.search(r"[?&]uddg=([^&]+)", href)
    url = urllib.parse.unquote(m.group(1)) if m else href
    return "https:" + url if url.startswith("//") else url

def bing_search(query, max_results=10, site=None):
    """Bing HTML search, no API key. (Primary engine — DDG is blocked on ID networks.)"""
    q = f"site:{site} {query}" if site else query
    r = requests.get("https://www.bing.com/search?q=" + urllib.parse.quote(q)
                     + f"&count={max_results}",
                     headers={"User-Agent": UA, "Accept-Language": "en-SG,en;q=0.9,id;q=0.8"},
                     timeout=TIMEOUT)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    results = []
    for li in soup.select("li.b_algo"):
        a = li.select_one("h2 a")
        if not a or not a.get("href", "").startswith("http"):
            continue
        cap = li.select_one(".b_caption p") or li.select_one("p")
        url = a["href"]
        results.append({
            "title": a.get_text(" ", strip=True), "url": url,
            "snippet": cap.get_text(" ", strip=True) if cap else "",
            "primary_source": is_primary(url),
        })
        if len(results) >= max_results:
            break
    return results

def ddg_search(query, max_results=10, site=None):
    """DuckDuckGo search, no API key. Tries html endpoint (GET), falls back to lite."""
    q = f"site:{site} {query}" if site else query
    last_err = None
    for endpoint, parser in [
        ("https://html.duckduckgo.com/html/?q=", "html"),
        ("https://lite.duckduckgo.com/lite/?q=", "lite"),
    ]:
        try:
            r = requests.get(endpoint + urllib.parse.quote(q),
                             headers={"User-Agent": UA}, timeout=TIMEOUT)
            r.raise_for_status()
        except requests.RequestException as e:
            last_err = e
            continue
        soup = BeautifulSoup(r.text, "lxml")
        results = []
        if parser == "html":
            for res in soup.select(".result"):
                a = res.select_one(".result__a")
                if not a or not a.get("href"):
                    continue
                url = _decode_ddg(a["href"])
                snippet_el = res.select_one(".result__snippet")
                results.append({
                    "title": a.get_text(" ", strip=True), "url": url,
                    "snippet": snippet_el.get_text(" ", strip=True) if snippet_el else "",
                    "primary_source": is_primary(url),
                })
                if len(results) >= max_results:
                    break
        else:  # lite: results are <a class="result-link"> followed by snippet cells
            links = soup.select("a.result-link") or [
                a for a in soup.find_all("a", href=True) if "uddg=" in a["href"]]
            for a in links:
                url = _decode_ddg(a["href"])
                td = a.find_parent("td")
                snippet = ""
                if td:
                    row = td.find_parent("tr")
                    nxt = row.find_next_sibling("tr") if row else None
                    if nxt:
                        snippet = nxt.get_text(" ", strip=True)[:300]
                results.append({
                    "title": a.get_text(" ", strip=True), "url": url,
                    "snippet": snippet, "primary_source": is_primary(url),
                })
                if len(results) >= max_results:
                    break
        if results:
            return results
    if last_err:
        raise last_err
    return []

def extract_page(url, max_chars=6000):
    r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT,
                     allow_redirects=True)
    out = {"url": url, "final_url": r.url, "status": r.status_code}
    if r.status_code != 200:
        return out
    soup = BeautifulSoup(r.text, "lxml")
    out["title"] = (soup.title.get_text(strip=True) if soup.title else "")
    md = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    out["meta_description"] = (md.get("content") or "").strip() if md else ""
    # publish date heuristics
    date = ""
    for sel, attr in [("meta[property='article:published_time']", "content"),
                      ("meta[name='date']", "content"), ("time[datetime]", "datetime")]:
        el = soup.select_one(sel)
        if el and el.get(attr):
            date = el.get(attr); break
    out["published"] = date
    for tag in soup(["script", "style", "nav", "footer", "header", "aside",
                     "form", "noscript", "iframe"]):
        tag.decompose()
    main = soup.find("article") or soup.find("main") or soup.body or soup
    text = re.sub(r"\n{3,}", "\n\n", main.get_text("\n", strip=True))
    out["word_count"] = len(re.findall(r"\w+", text))
    out["text"] = html.unescape(text[:max_chars])
    return out

SECONDARY_CUES = re.compile(
    r"(?i)\b(according to|as reported by|source[d]? from|cited by|via |data from|"
    r"a study by|research by|survey by|berdasarkan|menurut|dilansir|dikutip dari|"
    r"sumber:)\s+([A-Z][\w&.\- ]{2,40})")
ORIGINAL_MARKERS = re.compile(
    r"(?i)\b(we surveyed|our (study|survey|data|research|analysis)|methodology|"
    r"sample size|respondents|we analy[sz]ed|kami meneliti|survei kami|"
    r"metodologi|official statistics|press release)\b")

def source_check(url):
    """Grade a source: PRIMARY / OFFICIAL / ORIGINAL-RESEARCH / SECONDARY / AGGREGATOR.
    The test: is this page the ORIGIN of its claims, or is it retelling someone else's?"""
    page = extract_page(url, max_chars=100_000)
    out = {"url": url, "status": page.get("status"), "grade": "UNKNOWN",
           "signals": [], "retold_sources": [], "advice": ""}
    if page.get("status") != 200 or not page.get("text"):
        out["grade"] = "UNREACHABLE"
        return out
    text = page["text"]
    host = urllib.parse.urlparse(page.get("final_url") or url).netloc.lower()
    if is_primary(url):
        out["signals"].append(f"authority domain ({host})")
    retold = list({m.group(2).strip() for m in SECONDARY_CUES.finditer(text)})[:8]
    out["retold_sources"] = retold
    original = bool(ORIGINAL_MARKERS.search(text))
    if original:
        out["signals"].append("original-research markers (methodology/survey/own data)")
    if page.get("published"):
        out["signals"].append(f"dated ({page['published']})")
    else:
        out["signals"].append("NO publish date found")
    # grade
    if is_primary(url):
        out["grade"] = "PRIMARY"
        out["advice"] = "Cite directly."
    elif original and len(retold) <= 2:
        out["grade"] = "ORIGINAL-RESEARCH"
        out["advice"] = "Citable as the origin — name the publisher + year."
    elif len(retold) >= 3:
        out["grade"] = "AGGREGATOR"
        out["advice"] = ("This page RETELLS others. Do NOT cite it — trace the chain: "
                         "fetch/verify the origins it names: " + ", ".join(retold))
    elif retold:
        out["grade"] = "SECONDARY"
        out["advice"] = ("Retells " + ", ".join(retold) +
                         " — cite the ORIGIN instead; use this page only as corroboration.")
    else:
        out["grade"] = "UNCLEAR"
        out["advice"] = ("No authority domain, no original-research markers, no named "
                         "sources. Treat as opinion; find a stronger source or [VERIFY].")
    return out

def verify_claim(url, claim):
    page = extract_page(url, max_chars=200_000)
    result = {"url": url, "claim": claim, "status": page.get("status"),
              "confidence": "NOT-FOUND", "evidence": ""}
    if page.get("status") != 200 or not page.get("text"):
        result["confidence"] = "SOURCE-UNREACHABLE"
        return result
    text = page["text"]
    norm = lambda s: re.sub(r"\s+", " ", s.lower())
    tnorm = norm(text)
    # EXACT: the claim (or a long span of it) appears verbatim
    cnorm = norm(claim)
    if cnorm in tnorm or (len(cnorm) > 60 and cnorm[:60] in tnorm):
        result["confidence"] = "EXACT"
    else:
        # PARAPHRASE heuristic: all numbers present + majority of keywords
        numbers = re.findall(r"\d[\d,.–-]*%?", claim)
        nums_ok = all(n.rstrip(".,") in text for n in numbers) if numbers else True
        words = [w for w in re.findall(r"[a-zA-ZÀ-ɏ]{4,}", claim.lower())
                 if w not in {"yang", "untuk", "dengan", "dari", "this", "that",
                              "with", "from", "have", "will", "according"}]
        hits = sum(1 for w in set(words) if w in tnorm)
        ratio = hits / max(1, len(set(words)))
        if numbers and nums_ok and ratio >= 0.5:
            result["confidence"] = "PARAPHRASE"
        elif not numbers and ratio >= 0.75:
            result["confidence"] = "PARAPHRASE"
    if result["confidence"] != "NOT-FOUND":
        # pull the sentence around the first matching number/keyword as evidence
        probe = None
        nums = re.findall(r"\d[\d,.–-]*%?", claim)
        if nums:
            probe = nums[0].rstrip(".,")
        if probe and probe in text:
            i = text.index(probe)
            result["evidence"] = re.sub(r"\s+", " ", text[max(0, i-160):i+160]).strip()
    return result

def main():
    ap = argparse.ArgumentParser(description="SingRank web research")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("query")
    s.add_argument("--max", type=int, default=10); s.add_argument("--site")
    s.add_argument("--primary-only", action="store_true")
    f = sub.add_parser("fetch"); f.add_argument("url")
    f.add_argument("--max-chars", type=int, default=6000)
    v = sub.add_parser("verify"); v.add_argument("url"); v.add_argument("claim")
    sc = sub.add_parser("source-check"); sc.add_argument("url")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    if args.cmd == "search":
        try:
            res = bing_search(args.query, args.max, args.site)
        except requests.RequestException:
            res = []
        if not res:
            try:
                res = ddg_search(args.query, args.max, args.site)
            except requests.RequestException:
                res = []
        if not res:
            print("SEARCH-UNAVAILABLE: keyless engines (Bing/DDG) are blocked or "
                  "challenged on this network. Use Claude's WebSearch tool for the "
                  "search step, then this tool's fetch/verify on each result URL.",
                  file=sys.stderr)
            sys.exit(2)
        if args.primary_only:
            res = [r for r in res if r["primary_source"]]
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            for i, r in enumerate(res, 1):
                tag = " [PRIMARY]" if r["primary_source"] else ""
                print(f"{i}. {r['title']}{tag}\n   {r['url']}\n   {r['snippet']}\n")
            if not res:
                print("No results.")
    elif args.cmd == "fetch":
        page = extract_page(args.url, args.max_chars)
        if args.json:
            print(json.dumps(page, indent=2, ensure_ascii=False))
        else:
            print(f"# {page.get('title','')}\nURL: {page.get('final_url')}"
                  f"\nStatus: {page.get('status')} · {page.get('word_count',0)}w"
                  f" · published: {page.get('published') or '?'}\n")
            print(page.get("text", ""))
    elif args.cmd == "verify":
        res = verify_claim(args.url, args.claim)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res["confidence"] in ("EXACT", "PARAPHRASE") else 1)
    elif args.cmd == "source-check":
        res = source_check(args.url)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res["grade"] in ("PRIMARY", "ORIGINAL-RESEARCH") else 1)

if __name__ == "__main__":
    main()
