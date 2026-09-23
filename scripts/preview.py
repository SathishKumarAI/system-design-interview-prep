#!/usr/bin/env python3
"""Render this vault in a browser, so diagrams can be seen rather than asserted.

    python scripts/preview.py [--port 8765] [--root .]

Why this exists: the Definition of Done in CLAUDE.md requires "at least two diagram types
per case file, reusing the components.md vocabulary". Nothing checked that the Mermaid
actually *parses* — a syntax error renders as an error box on GitHub and as nothing at all
in some viewers, and `grep -c '```mermaid'` counts a broken block just as happily as a
working one. This serves the vault with the same renderer GitHub uses, and reports every
diagram that fails to parse.

Stdlib only on the server side. Markdown and Mermaid are rendered in the browser from
cdnjs, so the first run needs network; after that the browser cache covers it.

Serves:
    /                 the viewer shell
    /api/files        JSON list of every Markdown file, with its diagram counts
    /raw/<path>       the file's raw text

Read-only. It never writes to the vault.
"""
from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

EXCLUDE_DIRS = {".git", ".obsidian", "vendor", "node_modules", "__pycache__", ".venv", "assets"}
MERMAID_RE = re.compile(r"^```mermaid\s*$(.*?)^```\s*$", re.MULTILINE | re.DOTALL)
KIND_RE = re.compile(r"^\s*(flowchart|graph|sequenceDiagram|stateDiagram-v2|stateDiagram|erDiagram|gantt|classDiagram|journey|pie)\b")

ROOT = "."


def md_files(root: str) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            if name.lower().endswith((".md", ".markdown")):
                rel = os.path.relpath(os.path.join(dirpath, name), root)
                out.append(rel.replace(os.sep, "/"))
    return sorted(out)


def diagram_kinds(path: str) -> list[str]:
    """Which Mermaid diagram types a file declares. Empty list means no diagrams."""
    try:
        text = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return []
    kinds = []
    for block in MERMAID_RE.findall(text):
        first = next((ln for ln in block.splitlines() if ln.strip()), "")
        m = KIND_RE.match(first)
        kinds.append(m.group(1) if m else "UNKNOWN")
    return kinds


def safe_join(root: str, rel: str) -> str | None:
    """Resolve a request path inside root, or None if it escapes."""
    rel = posixpath.normpath("/" + rel).lstrip("/")
    full = os.path.normpath(os.path.join(root, rel.replace("/", os.sep)))
    if os.path.commonpath([os.path.abspath(full), os.path.abspath(root)]) != os.path.abspath(root):
        return None
    return full


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):            # one line per request, not three
        sys.stderr.write(f"  {self.command} {self.path}\n")

    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]

        if path in ("/", "/index.html"):
            return self._send(200, SHELL.encode("utf-8"), "text/html; charset=utf-8")

        if path == "/api/files":
            payload = []
            for rel in md_files(ROOT):
                kinds = diagram_kinds(os.path.join(ROOT, rel.replace("/", os.sep)))
                payload.append({"path": rel, "diagrams": kinds})
            body = json.dumps(payload).encode("utf-8")
            return self._send(200, body, "application/json; charset=utf-8")

        if path.startswith("/raw/"):
            full = safe_join(ROOT, path[len("/raw/"):])
            if not full or not os.path.isfile(full):
                return self._send(404, b"not found", "text/plain; charset=utf-8")
            body = open(full, "rb").read()
            return self._send(200, body, "text/plain; charset=utf-8")

        self._send(404, b"not found", "text/plain; charset=utf-8")


SHELL = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>system-design-prep — preview</title>
<style>
  /* Catppuccin Mocha */
  :root{
    --base:#1e1e2e; --mantle:#181825; --crust:#11111b; --surface0:#313244; --surface1:#45475a;
    --text:#cdd6f4; --subtext:#a6adc8; --overlay:#6c7086;
    --blue:#89b4fa; --green:#a6e3a1; --yellow:#f9e2af; --red:#f38ba8; --mauve:#cba6f7; --teal:#94e2d5;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--base);color:var(--text);
       font:14px/1.6 -apple-system,"Segoe UI",system-ui,sans-serif;display:flex;height:100vh}
  #side{width:340px;flex:none;background:var(--mantle);border-right:1px solid var(--surface0);
        display:flex;flex-direction:column}
  #side header{padding:12px 14px;border-bottom:1px solid var(--surface0)}
  #side h1{margin:0 0 8px;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--overlay)}
  #q{width:100%;padding:7px 9px;background:var(--crust);color:var(--text);
     border:1px solid var(--surface0);border-radius:6px;font:inherit}
  #check{width:100%;margin-top:7px;padding:6px 9px;background:var(--surface0);color:var(--text);
         border:1px solid var(--surface1);border-radius:6px;font:inherit;cursor:pointer}
  #check:hover{background:var(--surface1)}
  #stats{padding:8px 14px;font-size:12px;color:var(--subtext);border-bottom:1px solid var(--surface0)}
  #stats b{color:var(--text)}
  #list{overflow:auto;flex:1;padding:6px 0}
  .f{display:block;padding:5px 14px;color:var(--subtext);text-decoration:none;
     white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer;border-left:2px solid transparent}
  .f:hover{background:var(--surface0);color:var(--text)}
  .f.on{background:var(--surface0);color:var(--blue);border-left-color:var(--blue)}
  .f .dir{color:var(--overlay)}
  .tag{font-size:10px;padding:0 5px;border-radius:8px;margin-left:5px;
       background:var(--surface1);color:var(--subtext);vertical-align:1px}
  .tag.ok{background:#2a3b2a;color:var(--green)} .tag.no{background:#3b2a2f;color:var(--red)}
  #main{flex:1;overflow:auto;padding:26px 42px 90px}
  #doc{max-width:900px;margin:0 auto}
  #doc h1,#doc h2,#doc h3,#doc h4{line-height:1.25;margin:1.6em 0 .6em}
  #doc h1{font-size:28px;border-bottom:1px solid var(--surface0);padding-bottom:.3em}
  #doc h2{font-size:21px;color:var(--blue);border-bottom:1px solid var(--surface0);padding-bottom:.25em}
  #doc h3{font-size:17px;color:var(--mauve)}
  #doc a{color:var(--blue)}
  #doc code{background:var(--crust);padding:.15em .4em;border-radius:4px;font-size:.88em;color:var(--teal)}
  #doc pre{background:var(--crust);padding:12px 14px;border-radius:8px;overflow:auto;border:1px solid var(--surface0)}
  #doc pre code{background:none;padding:0;color:var(--text)}
  #doc table{border-collapse:collapse;width:100%;margin:1em 0;display:block;overflow-x:auto}
  #doc th,#doc td{border:1px solid var(--surface0);padding:7px 10px;text-align:left;vertical-align:top}
  #doc th{background:var(--surface0)}
  #doc tr:nth-child(even) td{background:rgba(255,255,255,.02)}
  #doc blockquote{border-left:3px solid var(--mauve);margin:1em 0;padding:.2em 1em;color:var(--subtext)}
  #doc hr{border:0;border-top:1px solid var(--surface0);margin:2em 0}
  .mermaid{background:#fff;border-radius:8px;padding:14px;margin:1.2em 0;text-align:center;overflow-x:auto}
  .mmerr{background:#3b2a2f;border:1px solid var(--red);color:var(--red);
         padding:10px 12px;border-radius:8px;margin:1.2em 0;white-space:pre-wrap;font-family:ui-monospace,monospace;font-size:12px}
  #fm{background:var(--mantle);border:1px solid var(--surface0);border-radius:8px;
      padding:10px 14px;margin-bottom:22px;font-size:12px;color:var(--subtext);font-family:ui-monospace,monospace;white-space:pre-wrap}
  #empty{color:var(--overlay);text-align:center;margin-top:24vh}
</style>
</head><body>
<div id="side">
  <header>
    <h1>system-design-prep</h1>
    <input id="q" placeholder="filter files…" autocomplete="off">
    <button id="check">Check every diagram parses</button>
  </header>
  <div id="stats"></div>
  <div id="list"></div>
</div>
<div id="main"><div id="doc"><div id="empty">Pick a file. Diagram counts are in the sidebar;<br>a red badge means the file declares no Mermaid.</div></div></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.1/mermaid.min.js"></script>
<script>
mermaid.initialize({startOnLoad:false, securityLevel:'loose', theme:'default'});

let FILES = [];
const $list = document.getElementById('list');
const $doc  = document.getElementById('doc');
const $q    = document.getElementById('q');

const NL = String.fromCharCode(10);
const MERMAID_BLOCK = /^```mermaid[ \t]*\n([\s\S]*?)^```[ \t]*$/gm;

// At least one file in this vault is CRLF (the Windows write_text trap in STATUS.md).
// The block regex anchors on \n, so normalise before matching or those diagrams
// silently do not exist as far as the viewer is concerned.
const normalise = s => s.split('\r\n').join(NL);
const firstLine = e => String((e && e.message) || e).split(NL)[0];
const escapeHtml = s => s.replace(/[<>&]/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;'}[c]));

function render(filter){
  const rows = FILES.filter(f => f.path.toLowerCase().includes(filter.toLowerCase()));
  $list.innerHTML = '';
  for (const f of rows){
    const a = document.createElement('a');
    a.className = 'f'; a.dataset.path = f.path;
    const cut = f.path.lastIndexOf('/');
    const dir = cut < 0 ? '' : f.path.slice(0, cut+1);
    const base = cut < 0 ? f.path : f.path.slice(cut+1);
    a.innerHTML = `<span class="dir">${dir}</span>${base}`;
    if (f.diagrams.length){
      const uniq = [...new Set(f.diagrams)].map(k => k.replace('stateDiagram-v2','state').replace('sequenceDiagram','seq'));
      a.innerHTML += `<span class="tag ok">${f.diagrams.length} · ${uniq.join(' ')}</span>`;
    }
    a.onclick = () => open(f.path);
    $list.appendChild(a);
  }
  document.getElementById('stats').innerHTML =
    `<b>${rows.length}</b> files · <b>${rows.reduce((n,f)=>n+f.diagrams.length,0)}</b> diagrams`;
}

async function open(path){
  for (const el of document.querySelectorAll('.f')) el.classList.toggle('on', el.dataset.path === path);
  location.hash = path;
  const raw = await (await fetch('/raw/' + path.split('/').map(encodeURIComponent).join('/'))).text();
  const text = normalise(raw);

  let body = text, fm = '';
  const m = text.match(/^---\n([\s\S]*?)\n---\n/);
  if (m){ fm = m[1]; body = text.slice(m[0].length); }

  // Pull the mermaid blocks out before marked touches them, so nothing escapes the source.
  const blocks = [];
  body = body.replace(/^```mermaid[ \t]*\n([\s\S]*?)^```[ \t]*$/gm, (_, src) => {
    blocks.push(src); return `\n@@MERMAID${blocks.length - 1}@@\n`;
  });

  let html = marked.parse(body, {gfm:true, breaks:false});
  html = html.replace(/<p>@@MERMAID(\d+)@@<\/p>|@@MERMAID(\d+)@@/g,
    (_, a, b) => `<div class="mermaid" data-i="${a ?? b}"></div>`);

  $doc.innerHTML = (fm ? `<div id="fm">${fm.replace(/[<>&]/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;'}[c]))}</div>` : '') + html;

  let bad = 0;
  for (const host of $doc.querySelectorAll('.mermaid')){
    const src = blocks[+host.dataset.i];
    try {
      const {svg} = await mermaid.render('m' + Math.random().toString(36).slice(2), src);
      host.innerHTML = svg;
    } catch (e) {
      bad++;
      host.className = 'mmerr';
      host.textContent = 'MERMAID PARSE ERROR\n\n' + (e && e.message ? e.message : e) + '\n\n' + src.trim().split('\n').slice(0,6).join('\n');
      console.error('[preview] mermaid failed in', path, e);
    }
  }
  console.log(`[preview] ${path}: ${blocks.length} diagram(s), ${bad} failed`);
  document.getElementById('main').scrollTop = 0;
}

$q.oninput = () => render($q.value);

// Whole-vault parse sweep. This is the check the Definition of Done was missing:
// grep counts a broken ```mermaid block exactly like a working one.
window.checkAll = async function(){
  const files = await (await fetch('/api/files')).json();
  const fails = []; let total = 0;
  for (const f of files.filter(x => x.diagrams.length)){
    const raw = await (await fetch('/raw/' + f.path.split('/').map(encodeURIComponent).join('/'))).text();
    const blocks = [...normalise(raw).matchAll(MERMAID_BLOCK)].map(m => m[1]);
    for (let i = 0; i < blocks.length; i++){
      total++;
      try { await mermaid.parse(blocks[i]); }
      catch (e) { fails.push(`${f.path} block ${i+1}: ${firstLine(e)}`); }
    }
  }
  const line = `${total} diagrams parsed, ${fails.length} failed`;
  console.log('[preview] ' + line);
  for (const f of fails) console.error('[preview] ' + f);
  $doc.innerHTML = `<h1>Diagram check</h1><p>${line}</p>` +
    (fails.length ? '<pre>' + fails.map(escapeHtml).join(NL) + '</pre>'
                  : '<p>Every Mermaid block in the vault parses.</p>');
  return {total, failed: fails.length, fails};
};
document.getElementById('check').onclick = window.checkAll;

fetch('/api/files').then(r => r.json()).then(f => {
  FILES = f; render('');
  const want = decodeURIComponent(location.hash.slice(1));
  if (want) open(want);
  console.log(`[preview] ready: ${FILES.length} files, ${FILES.reduce((n,x)=>n+x.diagrams.length,0)} diagrams`);
});
</script>
</body></html>
"""


def main() -> int:
    global ROOT
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="vault root (default: cwd)")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        print(f"not a directory: {args.root}", file=sys.stderr)
        return 2
    ROOT = args.root

    files = md_files(ROOT)
    total = sum(len(diagram_kinds(os.path.join(ROOT, f.replace("/", os.sep)))) for f in files)
    print(f"serving {len(files)} Markdown files, {total} Mermaid diagrams")
    print(f"  http://127.0.0.1:{args.port}/")
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
