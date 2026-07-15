#!/usr/bin/env python3
"""SingRank local LLM runner — heavy lifting with ZERO Claude tokens.

Runs prompts against the local Ollama server (D:\\Ollama, RTX 5080). Use for
bulk/mechanical language work where Claude tokens are wasteful:
- summarizing scraped pages before they enter context
- first-pass rewrites/drafts that Claude then refines
- bulk classification (relevan/junk), extraction, translation drafts
- title/meta variant generation (Claude picks the winner)

Claude stays the editor-in-chief: local output is a DRAFT INPUT, never published
as-is — it still goes through the full QC gate.

Usage:
  python llm_local.py "Summarize the key renovation rules:" --file scraped.txt
  python llm_local.py "Rewrite this title 10 ways, keep the year:" --model qwen2.5:14b
  echo "text" | python llm_local.py "Classify relevan/junk per line:"
  python llm_local.py --check          # is the server up? which models?
"""
import argparse
import sys as _sys
if hasattr(_sys.stdout, 'reconfigure'):
    _sys.stdout.reconfigure(encoding='utf-8')
    _sys.stderr.reconfigure(encoding='utf-8')
import json
import sys

import requests

BASE = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:14b"

def check():
    try:
        r = requests.get(BASE + "/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        print(json.dumps({"server": "up", "models": models,
                          "default": DEFAULT_MODEL,
                          "default_available": any(
                              m.startswith(DEFAULT_MODEL.split(":")[0]) for m in models)},
                         indent=2))
        return 0
    except requests.RequestException as e:
        print(json.dumps({"server": "down", "error": str(e),
                          "fix": "start Ollama (D:\\Ollama\\ollama serve) or open the Ollama app"}))
        return 1

def generate(model, prompt, content, temperature, max_tokens):
    full = prompt + ("\n\n---\n" + content if content else "")
    try:
        r = requests.post(BASE + "/api/generate", json={
            "model": model, "prompt": full, "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }, timeout=600)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"OLLAMA ERROR: {e}", file=sys.stderr)
        if "404" in str(e):
            print(f"Model '{model}' not installed. Run: ollama pull {model}",
                  file=sys.stderr)
        sys.exit(1)
    print(r.json().get("response", "").strip())

def main():
    ap = argparse.ArgumentParser(description="SingRank local LLM (Ollama)")
    ap.add_argument("prompt", nargs="?", default="")
    ap.add_argument("--file", help="file whose content is appended to the prompt")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--temperature", type=float, default=0.4)
    ap.add_argument("--max-tokens", type=int, default=2048)
    ap.add_argument("--check", action="store_true", help="server + model status")
    args = ap.parse_args()

    if args.check:
        sys.exit(check())
    if not args.prompt:
        ap.error("prompt required (or --check)")
    content = ""
    if args.file:
        content = open(args.file, encoding="utf-8", errors="replace").read()
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    generate(args.model, args.prompt, content, args.temperature, args.max_tokens)

if __name__ == "__main__":
    main()
