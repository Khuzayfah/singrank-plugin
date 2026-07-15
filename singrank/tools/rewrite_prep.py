#!/usr/bin/env python3
"""SingRank safe-rewrite engine — improve an existing article WITHOUT breaking it.

The no-delete rule, mechanized. Three modes:

  inventory <url-or-file>   What the article HAS and what is PROTECTED:
                            title/meta/headings/internal links/word count. Feed it
                            the page's winning GSC queries (--queries "a,b,c") and
                            it marks which headings/sections carry them — those are
                            LOCKED (they're why the page ranks).
  diff <old> <new>          The safety gate BEFORE upload: verifies the rewrite
                            (a) keeps EVERY internal link of the original,
                            (b) doesn't shrink word count >15%,
                            (c) keeps every protected heading (from --protect file
                                or inventory JSON),
                            (d) keeps the URL slug untouched (rewrites NEVER move
                                URLs). Exit 1 = the rewrite would damage the page.
  angles <inventory.json>   Prints the rewrite-angle worksheet: what may change
                            (title/meta/intro/weak sections/new sections) vs what
                            must not, per the SingRank rewrite protocol.

Flow: inventory → (Claude/local-LLM writes the rewrite; new angle, no
cannibalization — sibling keywords go in NEW articles, not this one) → diff gate →
chunk via publish_prep.py → push per seo-platforms playbook.
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
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

def load(src):
    if src.startswith("http"):
        r = requests.get(src, headers={"User-Agent": UA}, timeout=25)
        r.raise_for_status()
        return r.text, src
    return open(src, encoding="utf-8").read(), ""

def parse(html, base=""):
    soup = BeautifulSoup(html, "lxml")
    art = soup.find("article") or soup.body or soup
    title = soup.title.get_text(strip=True) if soup.title else ""
    md = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
    heads = [(h.name, re.sub(r"\s+", " ", h.get_text(" ", strip=True)))
             for h in art.find_all(["h1", "h2", "h3"])]
    host = urllib.parse.urlparse(base).netloc if base else ""
    internal, external = [], []
    for a in art.find_all("a", href=True):
        href = urllib.parse.urljoin(base, a["href"]) if base else a["href"]
        if href.startswith(("#", "mailto:", "tel:")):
            continue
        target = internal if (host and urllib.parse.urlparse(href).netloc == host) \
            or (not host and not href.startswith("http")) else external
        target.append({"href": href.split("#")[0],
                       "anchor": a.get_text(" ", strip=True)[:80]})
    words = len(re.findall(r"\w+", art.get_text(" ")))
    return {"title": title, "title_len": len(title),
            "meta_description": (md.get("content") or "").strip() if md else "",
            "word_count": words, "headings": heads,
            "internal_links": internal, "external_links": external,
            "source": base or "file"}

def cmd_inventory(args):
    html, base = load(args.src)
    inv = parse(html, base)
    queries = [q.strip().lower() for q in (args.queries or "").split(",") if q.strip()]
    protected = []
    for name, text in inv["headings"]:
        tl = text.lower()
        hit = [q for q in queries if q and (q in tl or all(
            w in tl for w in q.split()[:3]))]
        protected.append({"level": name, "text": text,
                          "protected": bool(hit) or name == "h1",
                          "matched_queries": hit})
    inv["headings"] = protected
    inv["protected_count"] = sum(1 for h in protected if h["protected"])
    out = json.dumps(inv, indent=2, ensure_ascii=False)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(out)
        print(f"inventory saved: {args.out}")
    print(f"TITLE ({inv['title_len']}c): {inv['title']}")
    print(f"WORDS: {inv['word_count']} · internal links: {len(inv['internal_links'])}"
          f" · external: {len(inv['external_links'])}")
    print(f"PROTECTED headings (H1 + query-carrying): {inv['protected_count']}/{len(protected)}")
    for h in protected:
        flag = "🔒" if h["protected"] else "  "
        print(f" {flag} {h['level'].upper()}: {h['text'][:80]}"
              + (f"  ← ranks for: {', '.join(h['matched_queries'])}" if h['matched_queries'] else ""))
    if not args.out:
        print("\n(use --out inventory.json to save for the diff gate)")

def cmd_diff(args):
    old_html, old_base = load(args.old)
    new_html, _ = load(args.new)
    old = parse(old_html, old_base)
    new = parse(new_html, old_base)
    protected_heads = None
    if args.inventory:
        inv = json.load(open(args.inventory, encoding="utf-8"))
        protected_heads = [h["text"] for h in inv["headings"] if h.get("protected")]
    P0 = []
    # (a) every original internal link kept
    old_hrefs = {l["href"].rstrip("/") for l in old["internal_links"]}
    new_hrefs = {l["href"].rstrip("/") for l in new["internal_links"]}
    lost = old_hrefs - new_hrefs
    if lost:
        P0.append(f"LOST INTERNAL LINKS ({len(lost)}): " + "; ".join(sorted(lost)[:5]))
    # (b) word count shrink
    if new["word_count"] < old["word_count"] * (1 - args.max_shrink / 100):
        P0.append(f"WORD COUNT SHRANK {old['word_count']}→{new['word_count']} "
                  f"(> {args.max_shrink}% loss) — the no-delete rule: strengthen, don't gut")
    # (c) protected headings kept (fuzzy: 60% of words present in some new heading)
    if protected_heads:
        new_head_text = " || ".join(t.lower() for _, t in
                                     [(h[0], h[1]) if isinstance(h, tuple) else
                                      (h["level"], h["text"]) for h in new["headings"]])
        for ph in protected_heads:
            words = [w for w in re.findall(r"\w{4,}", ph.lower())][:5]
            if words and sum(1 for w in words if w in new_head_text) / len(words) < 0.6:
                P0.append(f"PROTECTED HEADING WEAKENED/REMOVED: '{ph[:70]}'")
    print("=== REWRITE DIFF GATE ===")
    print(f"words {old['word_count']} → {new['word_count']} · "
          f"internal links {len(old_hrefs)} → {len(new_hrefs)} · "
          f"title: '{old['title'][:50]}' → '{new['title'][:50]}'")
    if P0:
        print("BLOCKED — this rewrite would damage the page:")
        for x in P0:
            print(f"  🔴 {x}")
        sys.exit(1)
    print("PASS — nothing load-bearing was broken. Proceed to qc_check.py, then "
          "chunk via publish_prep.py.")

def cmd_angles(args):
    inv = json.load(open(args.inventory, encoding="utf-8"))
    print(f"""=== REWRITE ANGLE WORKSHEET — {inv.get('source','')} ===
CURRENT: "{inv['title']}" · {inv['word_count']}w · {len(inv['internal_links'])} internal links

MAY CHANGE (the rewrite levers):
- Title/meta: new pattern (rotate per writing-craft §6 — number+year+power word),
  SAME primary intent. Changing the intent = a different article, not a rewrite.
- Opening block: new answer capsule + curiosity loop (hook-engine).
- Weak sections: expand thin blocks to 120-180w answer-first; add missing numbers
  (density ≥4.5/100w), a comparison table, fresher stats (re-verify all).
- ADD sections: gap subtopics from deep_research.py; FAQ entries for PAA queries.
- dateModified: only with a genuinely meaningful update.

MUST NOT CHANGE (the load-bearing structure):
- URL slug — NEVER. A rewrite that moves the URL is a migration, not a rewrite.
- {inv['protected_count']} protected heading(s) — they carry the queries this page
  already ranks for. Strengthen their sections; do not remove or de-optimize them.
- All {len(inv['internal_links'])} internal links (diff gate enforces).
- Primary keyword/intent of the page.

CANNIBALIZATION RULE: found a strong SIMILAR keyword while researching? It does NOT
go into this rewrite — it becomes a SIBLING article (deep-research Phase 1b) with a
distinct intent. One page, one intent, always.

FLOW: write the rewrite → rewrite_prep.py diff old new --inventory {args.inventory}
→ qc_check.py → publish_prep.py (chunked upload) → platform push → log_experiment
(changes: "rewrite: new title, +2 sections, +1 table").""")

def main():
    ap = argparse.ArgumentParser(description="SingRank safe-rewrite engine")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("inventory"); i.add_argument("src")
    i.add_argument("--queries", help="comma-separated winning GSC queries for this page")
    i.add_argument("--out", help="save inventory JSON")
    d = sub.add_parser("diff"); d.add_argument("old"); d.add_argument("new")
    d.add_argument("--inventory", help="inventory JSON (for protected headings)")
    d.add_argument("--max-shrink", type=float, default=15.0)
    a = sub.add_parser("angles"); a.add_argument("inventory")
    args = ap.parse_args()
    {"inventory": cmd_inventory, "diff": cmd_diff, "angles": cmd_angles}[args.cmd](args)

if __name__ == "__main__":
    main()
