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

LIFECYCLE (on-demand, never always-on): the server auto-starts when a prompt
needs it and is shut down explicitly when the work session ends. Login
autostart is disabled (shortcut parked in D:\\database\\local-model\\).

Usage:
  python llm_local.py "Summarize the key renovation rules:" --file scraped.txt
  python llm_local.py "Rewrite this title 10 ways, keep the year:" --model qwen2.5:14b
  echo "text" | python llm_local.py "Classify relevan/junk per line:"
  python llm_local.py --check          # is the server up? which models?
  python llm_local.py --up             # start the server (detached)
  python llm_local.py --down           # unload models from VRAM + kill the server
"""
import argparse
import sys as _sys
if hasattr(_sys.stdout, 'reconfigure'):
    _sys.stdout.reconfigure(encoding='utf-8')
    _sys.stderr.reconfigure(encoding='utf-8')
import json
import os
import subprocess
import sys
import time

import requests

BASE = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:14b"
EMBED_MODEL = "nomic-embed-text"
OLLAMA_EXE = r"D:\Ollama\ollama.exe"

def server_up():
    try:
        requests.get(BASE + "/api/tags", timeout=2)
        return True
    except requests.RequestException:
        return False

def server_start(wait=45):
    """Start ollama serve detached; return once the API answers."""
    if server_up():
        return True
    exe = OLLAMA_EXE if os.path.exists(OLLAMA_EXE) else "ollama"
    subprocess.Popen([exe, "serve"], stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL,
                     creationflags=getattr(subprocess, "DETACHED_PROCESS", 0)
                     | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0))
    for _ in range(wait):
        time.sleep(1)
        if server_up():
            return True
    return False

def server_down():
    """Unload models from VRAM, then kill every ollama process."""
    if server_up():
        try:
            tags = requests.get(BASE + "/api/ps", timeout=5).json()
            for m in tags.get("models", []):
                requests.post(BASE + "/api/generate",
                              json={"model": m["name"], "keep_alive": 0},
                              timeout=30)
        except requests.RequestException:
            pass
    subprocess.run(["taskkill", "/F", "/IM", "ollama.exe", "/T"],
                   capture_output=True)
    subprocess.run(["taskkill", "/F", "/IM", "ollama app.exe", "/T"],
                   capture_output=True)
    print("ollama: models unloaded, server stopped (VRAM freed)")

def embed(texts, model=EMBED_MODEL):
    """Return embedding vectors for a list of texts (auto-starts server)."""
    if not server_up() and not server_start():
        raise RuntimeError("ollama server won't start")
    r = requests.post(BASE + "/api/embed",
                      json={"model": model, "input": texts}, timeout=120)
    r.raise_for_status()
    return r.json()["embeddings"]

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

def generate(model, prompt, content, temperature, max_tokens, keep_alive="10m"):
    if not server_up() and not server_start():
        print("OLLAMA ERROR: server won't start (check D:\\Ollama)", file=sys.stderr)
        sys.exit(1)
    full = prompt + ("\n\n---\n" + content if content else "")
    try:
        r = requests.post(BASE + "/api/generate", json={
            "model": model, "prompt": full, "stream": False,
            "keep_alive": keep_alive,
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
    ap.add_argument("--up", action="store_true", help="start the server (detached)")
    ap.add_argument("--down", action="store_true",
                    help="unload models from VRAM + stop the server")
    ap.add_argument("--keep-alive", default="10m",
                    help="how long the model stays in VRAM after this call (0 = unload now)")
    args = ap.parse_args()

    if args.check:
        sys.exit(check())
    if args.up:
        ok = server_start()
        print("ollama: server up" if ok else "ollama: FAILED to start")
        sys.exit(0 if ok else 1)
    if args.down:
        server_down()
        sys.exit(0)
    if not args.prompt:
        ap.error("prompt required (or --check / --up / --down)")
    content = ""
    if args.file:
        content = open(args.file, encoding="utf-8", errors="replace").read()
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    generate(args.model, args.prompt, content, args.temperature, args.max_tokens,
             args.keep_alive)

if __name__ == "__main__":
    main()
