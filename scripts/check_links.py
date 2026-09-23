#!/usr/bin/env python3
"""Verify every relative Markdown link and image in a docs tree resolves to a real file.

Why this exists: relative links break silently. Nothing renders an error — the link is just
dead, and nobody notices for months. The two failure modes that dominate in real vaults are
(a) a file moved or renamed, and (b) unescaped spaces and parentheses in the target, which
break on GitHub while still looking fine in some editors.

    python check_links.py <docs-root> [--json] [--exclude vendor node_modules]

Exit code 0 if every link resolves, 1 otherwise, so it can gate a commit or CI step.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _md import in_code, mask_code                    # noqa: E402

# Matches [text](target) and ![alt](target). Target stops at the first ')' — which is exactly
# why unescaped parentheses in filenames are a bug worth reporting rather than parsing around.
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")

DEFAULT_EXCLUDES = {".git", "node_modules", "vendor", ".obsidian", "__pycache__", ".venv"}
SKIP_PREFIXES = ("http://", "https://", "#", "mailto:", "tel:", "data:", "//")


def iter_markdown(root: str, excludes: set[str]):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in excludes]
        for name in filenames:
            if name.lower().endswith((".md", ".markdown")):
                yield os.path.join(dirpath, name)


def check(root: str, excludes: set[str]):
    broken, checked, suspicious = [], 0, []

    for path in iter_markdown(root, excludes):
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError as exc:                      # unreadable file is itself a finding
            broken.append({"file": path, "target": "<unreadable>", "reason": str(exc)})
            continue

        base = os.path.dirname(path)
        # `path/to/file.md` inside a fenced usage example is documentation, not a link, and
        # it is never going to resolve. Reporting it forever is worse than not reporting it:
        # a gate that is permanently red teaches everyone to read past the number, and the
        # next real break goes with it.
        mask = mask_code(text)
        for match in LINK_RE.finditer(text):
            if in_code(mask, match.start()):
                continue
            target = match.group(1).strip()
            if target.startswith(SKIP_PREFIXES) or not target:
                continue

            # Strip a title: [x](./a.md "Title")
            if " " in target and target.rstrip().endswith(('"', "'")):
                target = target.split(" ", 1)[0]

            fragment_stripped = target.split("#", 1)[0]
            if not fragment_stripped:               # pure in-page anchor
                continue

            checked += 1
            resolved = os.path.normpath(
                os.path.join(base, urllib.parse.unquote(fragment_stripped))
            )
            if not os.path.exists(resolved):
                line = text[: match.start()].count("\n") + 1
                entry = {
                    "file": os.path.relpath(path, root),
                    "line": line,
                    "target": target,
                    "resolved": resolved,
                }
                # An unbalanced '(' in the captured target means the real filename contains
                # parentheses that were never escaped — report the fix, not just the symptom.
                if "(" in target or fragment_stripped.count("%28") != fragment_stripped.count("%29"):
                    entry["hint"] = "unescaped parenthesis in target — use %28 and %29"
                broken.append(entry)

            # Not broken, but will break on GitHub: raw spaces in the target.
            if " " in fragment_stripped:
                suspicious.append(
                    {"file": os.path.relpath(path, root), "target": target,
                     "hint": "raw space in link target — encode as %20"}
                )

    return checked, broken, suspicious


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", help="documentation root directory")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--exclude", nargs="*", default=[], help="extra directory names to skip")
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        print(f"not a directory: {args.root}", file=sys.stderr)
        return 2

    excludes = DEFAULT_EXCLUDES | set(args.exclude)
    checked, broken, suspicious = check(args.root, excludes)

    if args.json:
        print(json.dumps({"checked": checked, "broken": broken,
                          "suspicious": suspicious}, indent=2))
        return 1 if broken else 0

    print(f"checked {checked} relative links; broken: {len(broken)}")
    for b in broken:
        loc = f"{b['file']}:{b.get('line', '?')}"
        hint = f"  [{b['hint']}]" if "hint" in b else ""
        print(f"  BROKEN {loc} -> {b['target']}{hint}")
    if suspicious:
        print(f"\n{len(suspicious)} link(s) resolve locally but will break on GitHub:")
        for s in suspicious[:20]:
            print(f"  {s['file']} -> {s['target']}  [{s['hint']}]")
    if not broken:
        print("all relative links resolve")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
