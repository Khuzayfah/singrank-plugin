#!/usr/bin/env python3
"""SingRank smart scrape — GPU-powered deep scraping (fetch wide, understand locally).

The honest architecture: fetching is network-bound (threads, not GPU); the GPU
powers the UNDERSTANDING layer that makes scraping smart:
  1. FETCH   — parallel download of seed URLs (+ optional depth-1 crawl of
               same-domain links).
  2. FILTER  — embedding relevance (nomic-embed-text on the RTX 5080): every
               page/candidate link is scored against the research topic;
               irrelevant pages are dropped BEFORE they cost anything.
  3. EXTRACT — the local LLM (qwen2.5:14b) reads each surviving page and emits
               structured JSON: citable facts (with the exact sentence), numbers,
               entities, dates, and a relevance verdict. Zero Claude tokens spent
               on raw HTML.
  4. PACK    — one distilled research pack (facts.jsonl + PACK.md) — only
               high-quality, source-attributed material reaches the writer.

Every extracted fact carries its source URL and the VERBATIM sentence — before an
article uses one, it still goes through web_research.py verify (zero-fabrication).
The ollama server auto-starts for the run; end your session with
`python llm_local.py --down` to free the GPU.

Usage:
  python smart_scrape.py --topic "hdb renovation permit rules 2026" \
      --urls https://a.com/x https://b.com/y [--depth 1] [--max-pages 20] \
      [--min-relevance 0.45] [--out-dir scrape_pack]
"""
import argparse
import sys as _sys
if hasattr(_sys.stdout, 'reconfigure'):
    _sys.stdout.reconfigure(encoding='utf-8')
    _sys.stderr.reconfigure(encoding='utf-8')
import json
import math
import os
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

import llm_local  # sibling module: server_start/embed/BASE

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
TIMEOUT = 25

EXTRACT_PROMPT = """You are a research extraction engine. From the page text below, extract ONLY
material that is factual and citable. Respond with STRICT JSON, nothing else:
{"relevant": true/false,
 "relevance_reason": "one line",
 "facts": [{"claim": "the fact, restated precisely",
            "verbatim": "the exact sentence from the text",
            "numbers": ["every figure in it"],
            "entities": ["named orgs/places/rules"],
            "date_context": "year/date if stated, else \"\""}],
 "page_summary": "3 sentences max"}
Rules: max 8 facts, only facts with a number/date/named entity; skip opinions,
marketing fluff, and anything not about: {topic}"""

def fetch_one(url):
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT,
                         allow_redirects=True)
        if r.status_code != 200:
            return {"url": url, "status": r.status_code}
        soup = BeautifulSoup(r.text, "lxml")
        title = soup.title.get_text(strip=True) if soup.title else ""
        links = []
        host = urllib.parse.urlparse(r.url).netloc
        for a in soup.find_all("a", href=True):
            href = urllib.parse.urljoin(r.url, a["href"]).split("#")[0]
            if (urllib.parse.urlparse(href).netloc == host
                    and href.startswith("http") and not re.search(
                        r"\.(jpg|png|pdf|zip|mp4)$|/(cart|account|login|tag|search)", href)):
                links.append((href, a.get_text(" ", strip=True)[:80]))
        for t in soup(["script", "style", "nav", "footer", "header", "aside",
                       "form", "noscript"]):
            t.decompose()
        main = soup.find("article") or soup.find("main") or soup.body or soup
        text = re.sub(r"\s+", " ", main.get_text(" ", strip=True))
        return {"url": r.url, "status": 200, "title": title,
                "text": text[:18000], "words": len(text.split()),
                "links": links[:60]}
    except requests.RequestException as e:
        return {"url": url, "status": f"ERR {type(e).__name__}"}

def cos(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(y*y for y in b))
    return dot / (na*nb) if na and nb else 0.0

def llm_extract(topic, page):
    prompt = EXTRACT_PROMPT.replace("{topic}", topic)
    try:
        r = requests.post(llm_local.BASE + "/api/generate", json={
            "model": llm_local.DEFAULT_MODEL,
            "prompt": prompt + "\n\nPAGE TITLE: " + page["title"]
                      + "\nPAGE TEXT:\n" + page["text"][:12000],
            "stream": False, "format": "json", "keep_alive": "10m",
            "options": {"temperature": 0.1, "num_predict": 1500},
        }, timeout=300)
        r.raise_for_status()
        return json.loads(r.json().get("response", "{}"))
    except (requests.RequestException, json.JSONDecodeError) as e:
        return {"relevant": False, "relevance_reason": f"extract error: {e}",
                "facts": [], "page_summary": ""}

def main():
    ap = argparse.ArgumentParser(description="SingRank GPU-powered smart scrape")
    ap.add_argument("--topic", required=True)
    ap.add_argument("--urls", nargs="+", required=True)
    ap.add_argument("--depth", type=int, default=0, choices=[0, 1],
                    help="1 = also crawl relevant same-domain links from seeds")
    ap.add_argument("--max-pages", type=int, default=20)
    ap.add_argument("--min-relevance", type=float, default=0.45,
                    help="embedding cosine floor vs topic (0-1)")
    ap.add_argument("--out-dir", default="scrape_pack")
    ap.add_argument("--threads", type=int, default=8)
    args = ap.parse_args()

    if not llm_local.server_up() and not llm_local.server_start():
        print("ollama server won't start — GPU layer unavailable", file=_sys.stderr)
        _sys.exit(1)
    os.makedirs(args.out_dir, exist_ok=True)
    topic_vec = llm_local.embed([args.topic])[0]

    # ---- FETCH seeds in parallel
    print(f"[fetch] {len(args.urls)} seed URLs, {args.threads} threads…")
    pages = []
    with ThreadPoolExecutor(args.threads) as ex:
        for f in as_completed([ex.submit(fetch_one, u) for u in args.urls]):
            pages.append(f.result())
    ok = [p for p in pages if p.get("status") == 200 and p.get("words", 0) > 120]

    # ---- DEPTH-1: harvest candidate links, embedding-filter, fetch the best
    if args.depth == 1 and len(ok) < args.max_pages:
        cands, seen = {}, {p["url"] for p in ok}
        for p in ok:
            for href, anchor in p.get("links", []):
                if href not in seen and anchor:
                    cands.setdefault(href, anchor)
        if cands:
            keys = list(cands.keys())[:150]
            vecs = llm_local.embed([cands[k] for k in keys])
            scored = sorted(((cos(topic_vec, v), k) for v, k in zip(vecs, keys)),
                            reverse=True)
            budget = args.max_pages - len(ok)
            follow = [k for s, k in scored[:budget] if s >= args.min_relevance]
            print(f"[crawl] depth-1: {len(cands)} candidates → following {len(follow)} "
                  f"(embedding-relevant)")
            with ThreadPoolExecutor(args.threads) as ex:
                for f in as_completed([ex.submit(fetch_one, u) for u in follow]):
                    r = f.result()
                    if r.get("status") == 200 and r.get("words", 0) > 120:
                        ok.append(r)

    # ---- FILTER pages by embedding relevance (title + first text)
    reps = [p["title"] + ". " + p["text"][:600] for p in ok]
    if reps:
        vecs = llm_local.embed(reps)
        for p, v in zip(ok, vecs):
            p["relevance"] = round(cos(topic_vec, v), 3)
        before = len(ok)
        ok = [p for p in ok if p["relevance"] >= args.min_relevance]
        print(f"[filter] {before} pages → {len(ok)} above relevance "
              f"{args.min_relevance} (GPU embeddings)")

    # ---- EXTRACT with the local LLM (GPU)
    all_facts, lines = [], []
    fx = open(os.path.join(args.out_dir, "facts.jsonl"), "w", encoding="utf-8")
    for i, p in enumerate(sorted(ok, key=lambda x: -x.get("relevance", 0)), 1):
        print(f"[extract {i}/{len(ok)}] {p['url'][:80]} (rel {p.get('relevance')})")
        res = llm_extract(args.topic, p)
        if not res.get("relevant"):
            continue
        lines.append(f"\n## {p['title'] or p['url']}\n{p['url']} · relevance "
                     f"{p.get('relevance')} · {res.get('page_summary','')}")
        for fact in res.get("facts", []):
            fact["source_url"] = p["url"]
            all_facts.append(fact)
            fx.write(json.dumps(fact, ensure_ascii=False) + "\n")
            lines.append(f"- {fact.get('claim','')}  \n"
                         f"  ↳ verbatim: \"{fact.get('verbatim','')[:180]}\"")
    fx.close()

    pack = (f"# SMART SCRAPE PACK — \"{args.topic}\"\n"
            f"_{len(ok)} relevant pages · {len(all_facts)} citable facts · "
            f"GPU: embeddings + {llm_local.DEFAULT_MODEL}_\n"
            "\n**Every fact must still pass `web_research.py verify <source_url> "
            "\"<claim>\"` before it enters an article (zero-fabrication).**\n"
            + "\n".join(lines))
    open(os.path.join(args.out_dir, "PACK.md"), "w", encoding="utf-8").write(pack)
    print(f"\n=== DONE: {len(all_facts)} facts from {len(ok)} pages → "
          f"{args.out_dir}\\PACK.md + facts.jsonl ===")
    print("Free the GPU when the session ends: python llm_local.py --down")

if __name__ == "__main__":
    main()
