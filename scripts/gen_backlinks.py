#!/usr/bin/env python3
"""Regenerate the "Referenced by" section in every Markdown file from actual inbound links.

Hand-maintained backlinks go stale within two edits and then actively mislead — a reader trusts
them, follows a link to a page that no longer references this one, and loses confidence in the
whole set. Generating them makes them true by construction.

    python gen_backlinks.py <docs-root> [--dry-run] [--heading "Referenced by"]

Placement: the section is inserted before "## Sources" when that heading exists (so the file
keeps the See also / Referenced by / Sources order), otherwise appended at the end.
Files with no inbound links get the section removed rather than left with a stale list.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.parse
from collections import defaultdict

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
DEFAULT_EXCLUDES = {".git", "node_modules", "vendor", ".obsidian", "__pycache__", ".venv"}
SKIP_PREFIXES = ("http://", "https://", "#", "mailto:", "tel:", "data:", "//")


def canon(path: str) -> str:
    """Canonical key for path comparison.

    os.walk yields paths in whatever separator style the root was given, while link targets
    get resolved through normpath. On Windows a forward-slash root therefore produces keys
    that never compare equal to resolved targets, and the script silently reports
    "0 changed" while exiting 0 — a failure indistinguishable from success. Comparing
    canonical forms on both sides removes the whole class of bug.
    """
    return os.path.normcase(os.path.abspath(path))


def iter_markdown(root: str, excludes: set[str]):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in excludes]
        for name in filenames:
            if name.lower().endswith((".md", ".markdown")):
                yield os.path.normpath(os.path.join(dirpath, name))


def title_of(path: str) -> str:
    """Prefer the frontmatter title, then the first H1, then the filename."""
    try:
        text = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return os.path.basename(path)
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            m = re.search(r"^title:\s*(.+)$", text[3:end], re.MULTILINE)
            if m:
                return m.group(1).strip().strip("\"'")
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return os.path.splitext(os.path.basename(path))[0]


def encode(rel: str) -> str:
    """Percent-encode the characters that break Markdown links, and nothing else."""
    return rel.replace("\\", "/").replace("%", "%25").replace(" ", "%20") \
              .replace("(", "%28").replace(")", "%29")


def build_index(root: str, excludes: set[str]):
    """target absolute path -> set of absolute paths that link to it."""
    inbound = defaultdict(set)
    files = list(iter_markdown(root, excludes))
    for path in files:
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        base = os.path.dirname(path)
        # Ignore links that live inside an existing Referenced by block, or a
        # regenerated section would keep citing itself into a fixed point.
        text = re.sub(r"\n##\s+Referenced by\b.*?(?=\n##\s|\Z)", "\n", text, flags=re.DOTALL)
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if target.startswith(SKIP_PREFIXES) or not target:
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = os.path.normpath(os.path.join(base, urllib.parse.unquote(target)))
            if os.path.isfile(resolved) and canon(resolved) != canon(path):
                inbound[canon(resolved)].add(path)
    return files, inbound


def render_section(target: str, sources: set[str], heading: str) -> str:
    if not sources:
        return ""
    base = os.path.dirname(target)
    rows = []
    for src in sorted(sources, key=lambda p: title_of(p).lower()):
        rel = encode(os.path.relpath(src, base))
        rows.append(f"- [{title_of(src)}]({rel})")
    return f"## {heading}\n\n" + "\n".join(rows) + "\n"


def apply_section(text: str, section: str, heading: str) -> str:
    pattern = re.compile(rf"\n##\s+{re.escape(heading)}\b.*?(?=\n##\s|\Z)", re.DOTALL)
    if pattern.search(text):
        return pattern.sub("\n" + section.rstrip() + "\n" if section else "\n", text).rstrip() + "\n"
    if not section:
        return text
    sources_re = re.compile(r"\n##\s+Sources\b")
    m = sources_re.search(text)
    if m:                                   # keep See also / Referenced by / Sources order
        return text[: m.start()] + "\n" + section + text[m.start():].rstrip() + "\n"
    return text.rstrip() + "\n\n" + section


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--dry-run", action="store_true", help="report changes without writing")
    ap.add_argument("--heading", default="Referenced by")
    ap.add_argument("--exclude", nargs="*", default=[])
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        print(f"not a directory: {args.root}", file=sys.stderr)
        return 2

    excludes = DEFAULT_EXCLUDES | set(args.exclude)
    files, inbound = build_index(args.root, excludes)

    changed = 0
    for path in files:
        try:
            original = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        section = render_section(path, inbound.get(canon(path), set()), args.heading)
        updated = apply_section(original, section, args.heading)
        if updated != original:
            changed += 1
            n = len(inbound.get(canon(path), set()))
            print(f"{'would update' if args.dry_run else 'updated'} "
                  f"{os.path.relpath(path, args.root)}  ({n} inbound)")
            if not args.dry_run:
                open(path, "w", encoding="utf-8", newline="\n").write(updated)

    total_links = sum(len(v) for v in inbound.values())
    print(f"\n{len(files)} files scanned, {total_links} inbound links mapped, {changed} changed")
    print("re-run check_links.py now — generated links are links too")
    return 0


if __name__ == "__main__":
    sys.exit(main())
