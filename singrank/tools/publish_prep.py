#!/usr/bin/env python3
"""SingRank publish prep — beat the Shopify/Wix MCP push limitations.

Two problems this solves:
1. SHOPIFY: article bodies >~30KB fail/truncate through the Admin API, and MCP
   tool-call payloads have their own size ceiling. → `shopify` mode splits an
   article HTML into ordered chunks at BLOCK boundaries (never mid-tag), each
   under --max-kb, with a manifest describing the exact push sequence
   (create-with-chunk-1 as draft → append chunks → verify → publish).
2. WIX: Draft Posts API takes RICOS JSON, not HTML — and a 2,500-word article
   as one RICOS payload can exceed the MCP call size. → `ricos` mode converts
   article HTML to RICOS nodes (headings, paragraphs, bold/italic/links,
   lists, blockquotes, tables) and emits them in ordered batches small enough
   to send as create-draft + N append-update calls before one UPDATE_PUBLISH.

Usage:
  python publish_prep.py shopify article.html --max-kb 25 --out-dir chunks/
  python publish_prep.py ricos article.html --batch-nodes 40 --out-dir ricos/
Both modes print a MANIFEST (push order + verification steps) and write files.
"""
import argparse
import sys as _sys
if hasattr(_sys.stdout, 'reconfigure'):
    _sys.stdout.reconfigure(encoding='utf-8')
    _sys.stderr.reconfigure(encoding='utf-8')
import json
import os
import re

from bs4 import BeautifulSoup, NavigableString, Tag

BLOCK_TAGS = ["h1", "h2", "h3", "h4", "p", "ul", "ol", "table", "blockquote",
              "div", "details", "figure", "pre"]

# ---------------- SHOPIFY: block-boundary chunking ----------------

def shopify_chunks(html, max_kb):
    soup = BeautifulSoup(html, "lxml")
    root = soup.find("article") or soup.body or soup
    blocks = [str(el) for el in root.children
              if isinstance(el, Tag) or (isinstance(el, NavigableString) and el.strip())]
    limit = max_kb * 1024
    chunks, cur, cur_len = [], [], 0
    for b in blocks:
        blen = len(b.encode("utf-8"))
        if blen > limit:
            # a single oversized block (huge table?) — split its children once
            inner = BeautifulSoup(b, "lxml")
            tag = inner.find()
            subs = [str(c) for c in tag.children] if tag else [b]
            for s in subs:
                if cur_len + len(s.encode("utf-8")) > limit and cur:
                    chunks.append("".join(cur)); cur, cur_len = [], 0
                cur.append(s); cur_len += len(s.encode("utf-8"))
            continue
        if cur_len + blen > limit and cur:
            chunks.append("".join(cur)); cur, cur_len = [], 0
        cur.append(b); cur_len += blen
    if cur:
        chunks.append("".join(cur))
    return chunks

# ---------------- WIX: HTML -> RICOS ----------------

_id = 0
def nid():
    global _id
    _id += 1
    return f"n{_id}"

def text_nodes(el):
    """Flatten inline content of an element into RICOS TEXT nodes with decorations."""
    out = []
    def walk(node, deco):
        if isinstance(node, NavigableString):
            t = str(node)
            if t.strip("\n"):
                out.append({"type": "TEXT", "id": "",
                            "textData": {"text": t, "decorations": list(deco)}})
            return
        if not isinstance(node, Tag):
            return
        d = list(deco)
        if node.name in ("strong", "b"):
            d.append({"type": "BOLD", "fontWeightValue": 700})
        elif node.name in ("em", "i"):
            d.append({"type": "ITALIC", "italicData": True})
        elif node.name == "a" and node.get("href"):
            d.append({"type": "LINK", "linkData": {
                "link": {"url": node["href"], "target": "BLANK"}}})
        for c in node.children:
            walk(c, d)
    for c in el.children:
        walk(c, [])
    return out

def paragraph(el_or_nodes):
    nodes = el_or_nodes if isinstance(el_or_nodes, list) else text_nodes(el_or_nodes)
    return {"type": "PARAGRAPH", "id": nid(), "nodes": nodes, "paragraphData": {}}

def convert_block(el):
    name = el.name
    if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        return [{"type": "HEADING", "id": nid(), "nodes": text_nodes(el),
                 "headingData": {"level": int(name[1])}}]
    if name == "p":
        return [paragraph(el)]
    if name == "blockquote":
        return [{"type": "BLOCKQUOTE", "id": nid(),
                 "nodes": [paragraph(el)], "blockquoteData": {}}]
    if name in ("ul", "ol"):
        t = "BULLETED_LIST" if name == "ul" else "ORDERED_LIST"
        items = []
        for li in el.find_all("li", recursive=False):
            items.append({"type": "LIST_ITEM", "id": nid(),
                          "nodes": [paragraph(li)]})
        data_key = "bulletedListData" if name == "ul" else "orderedListData"
        return [{"type": t, "id": nid(), "nodes": items, data_key: {"indentation": 0}}]
    if name == "table":
        rows = el.find_all("tr")
        if not rows:
            return []
        ncols = max(len(r.find_all(["td", "th"])) for r in rows)
        row_nodes = []
        for r in rows:
            cells = []
            for c in r.find_all(["td", "th"]):
                cells.append({"type": "TABLE_CELL", "id": nid(),
                              "nodes": [paragraph(c)], "tableCellData": {}})
            while len(cells) < ncols:
                cells.append({"type": "TABLE_CELL", "id": nid(),
                              "nodes": [paragraph([])], "tableCellData": {}})
            row_nodes.append({"type": "TABLE_ROW", "id": nid(), "nodes": cells,
                              "tableRowData": {}})
        return [{"type": "TABLE", "id": nid(), "nodes": row_nodes,
                 "tableData": {"dimensions": {
                     "colsWidthRatio": [1] * ncols,
                     "colsMinWidth": [120] * ncols}}}]
    if name in ("details",):  # FAQ accordion → heading (summary) + paragraphs
        out = []
        summ = el.find("summary")
        if summ:
            out.append({"type": "HEADING", "id": nid(), "nodes": text_nodes(summ),
                        "headingData": {"level": 3}})
        for p in el.find_all("p", recursive=False):
            out.append(paragraph(p))
        return out
    if name in ("div", "section", "figure"):
        out = []
        for c in el.children:
            if isinstance(c, Tag):
                out.extend(convert_block(c))
            elif isinstance(c, NavigableString) and c.strip():
                out.append(paragraph([{"type": "TEXT", "id": "",
                                       "textData": {"text": str(c).strip(),
                                                    "decorations": []}}]))
        return out
    if name == "script":
        return []  # schema goes via seoData.tags, never body
    # fallback: any other element → paragraph of its text
    txt = el.get_text(" ", strip=True)
    if txt:
        return [paragraph([{"type": "TEXT", "id": "",
                            "textData": {"text": txt, "decorations": []}}])]
    return []

def html_to_ricos(html):
    soup = BeautifulSoup(html, "lxml")
    root = soup.find("article") or soup.body or soup
    nodes = []
    for el in root.children:
        if isinstance(el, Tag):
            nodes.extend(convert_block(el))
        elif isinstance(el, NavigableString) and el.strip():
            nodes.append(paragraph([{"type": "TEXT", "id": "",
                                     "textData": {"text": str(el).strip(),
                                                  "decorations": []}}]))
    return nodes

def main():
    ap = argparse.ArgumentParser(description="SingRank publish prep")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("shopify"); s.add_argument("file")
    s.add_argument("--max-kb", type=int, default=25)
    s.add_argument("--out-dir", default="publish_chunks")
    w = sub.add_parser("ricos"); w.add_argument("file")
    w.add_argument("--batch-nodes", type=int, default=40)
    w.add_argument("--out-dir", default="publish_ricos")
    args = ap.parse_args()

    html = open(args.file, encoding="utf-8").read()
    os.makedirs(args.out_dir, exist_ok=True)

    if args.cmd == "shopify":
        chunks = shopify_chunks(html, args.max_kb)
        paths = []
        for i, c in enumerate(chunks, 1):
            p = os.path.join(args.out_dir, f"chunk-{i:02d}.html")
            open(p, "w", encoding="utf-8").write(c)
            paths.append((p, round(len(c.encode('utf-8'))/1024, 1)))
        print(f"=== SHOPIFY PUSH MANIFEST ({len(chunks)} chunks, max {args.max_kb}KB) ===")
        for p, kb in paths:
            print(f"  {p}  ({kb} KB)")
        print("""PUSH SEQUENCE:
1. Create the article as DRAFT with chunk-01 as body (articleCreate published:false,
   or X_RCS create_article for RCS).
2. Append remaining chunks IN ORDER via X_RCS append_to_article (RCS) — for other
   stores: graphql articleUpdate with read-current-body + append pattern is UNSAFE
   past ~30KB; use the THEME-SNIPPET route instead (body = intro chunk only; full
   content in snippets/article-<handle>.liquid pushed via themeFilesUpsert, >20KB
   files via gist->URL).
3. VERIFY: fetch the article back; word count must match the source file.
4. Publish only after approval. Then log_experiment.""")
    else:
        nodes = html_to_ricos(html)
        batches = [nodes[i:i+args.batch_nodes]
                   for i in range(0, len(nodes), args.batch_nodes)]
        for i, b in enumerate(batches, 1):
            p = os.path.join(args.out_dir, f"batch-{i:02d}.json")
            open(p, "w", encoding="utf-8").write(
                json.dumps(b, ensure_ascii=False, indent=1))
        print(f"=== WIX RICOS MANIFEST ({len(nodes)} nodes → {len(batches)} batches) ===")
        for i, b in enumerate(batches, 1):
            size = len(json.dumps(b).encode('utf-8'))
            print(f"  batch-{i:02d}.json  ({len(b)} nodes, {round(size/1024,1)} KB)")
        print("""PUSH SEQUENCE (CallWixSiteAPI — ExecuteWixAPI is read-only!):
1. CREATE draft post with batch-01 as richContent.nodes (Draft Posts v3).
2. For each next batch: GET the draft, APPEND batch nodes to richContent.nodes,
   UPDATE the draft (action UPDATE — still a draft; strip memberId from the GET
   response before re-sending; use fieldMask draftPost.richContent).
3. Set seoData (title/meta/schema Article+Breadcrumb+Speakable) in ONE more update.
4. VERIFY: GET the draft; node count must equal the manifest total.
5. UPDATE_PUBLISH once, only after approval. relatedPostIds max 3. Then log_experiment.
NOTE: test on ONE throwaway draft first — RICOS table/list node shapes should be
confirmed against a draft Wix accepts before pushing a full article.""")

if __name__ == "__main__":
    main()
