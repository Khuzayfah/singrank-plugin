#!/usr/bin/env python3
"""SingRank originality guard — catch copy-paste, enforce synthesis.

The rule: facts are borrowed, WORDS are ours. We write from understanding and cite
the source — we never lift a source's sentences. This tool mechanizes that: it
compares every draft sentence against the source material (the verbatim sentences
captured by smart_scrape/deep_research, or any scraped text) and flags anything too
close to the original wording.

What it flags:
- LIFTED   : a run of >= N consecutive words identical to a source sentence
             (default N=8) — near-certain copy-paste, a P0.
- ECHO     : high word-shingle overlap (Jaccard) with a source sentence but not a
             verbatim run — a paraphrase that stayed too close; rewrite it.
- ORIGINAL : synthesized in our own words (the goal).

It does NOT check facts (that's web_research.py verify) — it checks WORDING. A
sentence can be 100% original in words and still need a citation for its fact.

Usage:
  python originality_check.py draft.html --sources facts.jsonl
  python originality_check.py draft.html --sources scrape_pack/PACK.md pack2/PACK.md
  python originality_check.py draft.html --sources src_dir/ --min-run 8 --echo 0.6
Exit 1 if any LIFTED passage is found (blocks publish).
"""
import argparse
import sys as _sys
if hasattr(_sys.stdout, 'reconfigure'):
    _sys.stdout.reconfigure(encoding='utf-8')
    _sys.stderr.reconfigure(encoding='utf-8')
import glob
import json
import os
import re
import sys

from bs4 import BeautifulSoup

WORD = re.compile(r"[a-zA-ZÀ-ɏ0-9]+")

def norm_words(text):
    return [w.lower() for w in WORD.findall(text)]

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if len(s.strip()) > 25]

def load_sources(paths):
    """Return a list of source sentences (their verbatim wording)."""
    src = []
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += glob.glob(os.path.join(p, "**", "*.*"), recursive=True)
        else:
            files += glob.glob(p)
    for f in files:
        try:
            raw = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if f.endswith(".jsonl"):
            for line in raw.splitlines():
                try:
                    obj = json.loads(line)
                    for key in ("verbatim", "claim", "page_summary"):
                        if obj.get(key):
                            src.extend(sentences(obj[key]))
                except json.JSONDecodeError:
                    pass
        elif f.endswith((".md", ".txt", ".html")):
            txt = raw
            if f.endswith(".html"):
                txt = BeautifulSoup(raw, "lxml").get_text(" ")
            src.extend(sentences(txt))
    # dedupe, keep only substantive
    seen, out = set(), []
    for s in src:
        k = " ".join(norm_words(s))
        if k and k not in seen and len(norm_words(s)) >= 5:
            seen.add(k); out.append(s)
    return out

def build_runs_index(src_sentences, run):
    """Map every N-word shingle in the sources to the source sentence."""
    idx = {}
    for s in src_sentences:
        w = norm_words(s)
        for i in range(len(w) - run + 1):
            idx.setdefault(" ".join(w[i:i+run]), s)
    return idx

def shingles(words, k=3):
    return {" ".join(words[i:i+k]) for i in range(len(words)-k+1)} or set(words)

def check_sentence(sent, run_index, src_shingle_sets, run, echo_thr):
    w = norm_words(sent)
    if len(w) < run:
        return ("ORIGINAL", None, 0.0)
    # LIFTED: any N-word run present verbatim in a source
    for i in range(len(w) - run + 1):
        key = " ".join(w[i:i+run])
        if key in run_index:
            return ("LIFTED", run_index[key], 1.0)
    # ECHO: high shingle overlap with any single source sentence
    dsh = shingles(w)
    best, best_src = 0.0, None
    for ssh, ssent in src_shingle_sets:
        if not ssh:
            continue
        inter = len(dsh & ssh)
        if inter:
            jac = inter / len(dsh | ssh)
            if jac > best:
                best, best_src = jac, ssent
    if best >= echo_thr:
        return ("ECHO", best_src, round(best, 2))
    return ("ORIGINAL", None, round(best, 2))

def main():
    ap = argparse.ArgumentParser(description="SingRank originality guard")
    ap.add_argument("draft", help="draft article (html/md/txt)")
    ap.add_argument("--sources", nargs="+", required=True,
                    help="facts.jsonl / PACK.md / scraped text files or dirs")
    ap.add_argument("--min-run", type=int, default=8,
                    help="consecutive-word run = LIFTED (default 8)")
    ap.add_argument("--echo", type=float, default=0.6,
                    help="shingle-Jaccard >= this = ECHO/too-close paraphrase")
    ap.add_argument("--json", dest="json_out", help="write JSON result")
    args = ap.parse_args()

    raw = open(args.draft, encoding="utf-8", errors="replace").read()
    draft_text = BeautifulSoup(raw, "lxml").get_text(" ") if args.draft.endswith((".html", ".htm")) else raw
    draft_sents = sentences(draft_text)
    src_sents = load_sources(args.sources)
    if not src_sents:
        print("No source sentences loaded — nothing to compare against.", file=sys.stderr)
        sys.exit(2)
    run_index = build_runs_index(src_sents, args.min_run)
    src_shingle_sets = [(shingles(norm_words(s)), s) for s in src_sents]

    lifted, echo, results = [], [], []
    for s in draft_sents:
        verdict, src, score = check_sentence(s, run_index, src_shingle_sets,
                                             args.min_run, args.echo)
        results.append({"sentence": s, "verdict": verdict, "score": score,
                        "matched_source": src})
        if verdict == "LIFTED":
            lifted.append((s, src))
        elif verdict == "ECHO":
            echo.append((s, src, score))

    n = len(draft_sents) or 1
    orig_pct = round(100 * (n - len(lifted) - len(echo)) / n, 1)
    print(f"=== ORIGINALITY GUARD ===")
    print(f"draft sentences: {n} · sources: {len(src_sents)} · "
          f"min-run {args.min_run} · echo {args.echo}")
    print(f"ORIGINALITY: {orig_pct}%  (LIFTED {len(lifted)} · ECHO {len(echo)})")
    if lifted:
        print("\n🔴 LIFTED (copy-paste — rewrite from understanding, P0):")
        for s, src in lifted[:15]:
            print(f"  DRAFT : {s[:140]}")
            print(f"  SOURCE: {(src or '')[:140]}\n")
    if echo:
        print("🟡 ECHO (paraphrase too close — reword in our voice):")
        for s, src, sc in echo[:15]:
            print(f"  [{sc}] {s[:130]}")
    if not lifted and not echo:
        print("\n✅ Clean — every sentence is original wording. (Facts still need "
              "citations — that's web_research.py verify, not this tool.)")
    if args.json_out:
        open(args.json_out, "w", encoding="utf-8").write(json.dumps(
            {"originality_pct": orig_pct, "lifted": len(lifted), "echo": len(echo),
             "results": results}, indent=2, ensure_ascii=False))
    sys.exit(1 if lifted else 0)

if __name__ == "__main__":
    main()
