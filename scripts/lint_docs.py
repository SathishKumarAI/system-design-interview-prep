#!/usr/bin/env python3
"""Lint a docs tree: frontmatter completeness, section contract, and near-duplicate topics.

The duplicate check is the interesting one. Doc sets don't acquire duplicates through
carelessness — they acquire them through distance. Someone writes caching.md in week one and
cache-strategies.md in week six, having forgotten. Normalising filenames and comparing catches
that class before it becomes two half-finished pages nobody wants to merge.

    python lint_docs.py <docs-root> [--require title type status] [--contract] [--json]

Exit code 0 when clean, 1 when there are findings.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher

DEFAULT_EXCLUDES = {".git", "node_modules", "vendor", ".obsidian", "__pycache__", ".venv"}
DEFAULT_REQUIRED = ["title", "type", "status", "updated"]

CONTRACT_SECTIONS = [
    "Core concept", "Mechanics & internals", "Numbers that matter", "Failure modes",
    "Trade-offs vs alternatives", "Real-world examples", "Follow-up questions",
    "See also", "Sources",
]

# Word pairs that mean the same topic. Normalised away before comparing filenames so
# "caching" and "cache-strategies" collide the way a human would expect them to.
SYNONYMS = {
    "caching": "cache", "caches": "cache", "strategies": "", "strategy": "",
    "patterns": "", "pattern": "", "guide": "", "overview": "", "intro": "",
    "basics": "", "fundamentals": "", "explained": "", "deep": "", "dive": "",
    "notes": "", "and": "", "the": "", "vs": "", "versus": "vs",
}


def iter_markdown(root: str, excludes: set[str]):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in excludes]
        for name in filenames:
            if name.lower().endswith((".md", ".markdown")):
                yield os.path.join(dirpath, name)


def normalise(stem: str) -> str:
    words = [w for w in re.split(r"[-_\s]+", stem.lower()) if w]
    out = []
    for w in words:
        w = SYNONYMS.get(w, w)
        if not w:
            continue
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]                       # crude singularisation, good enough for filenames
        out.append(w)
    return "-".join(sorted(out))


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fields = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--require", nargs="*", default=DEFAULT_REQUIRED,
                    help=f"required frontmatter fields (default: {' '.join(DEFAULT_REQUIRED)})")
    ap.add_argument("--contract", action="store_true",
                    help="also check the staff section contract on type: topic/case files")
    ap.add_argument("--threshold", type=float, default=0.85,
                    help="similarity above which two filenames are flagged (default 0.85)")
    ap.add_argument("--exclude", nargs="*", default=[])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        print(f"not a directory: {args.root}", file=sys.stderr)
        return 2

    excludes = DEFAULT_EXCLUDES | set(args.exclude)
    files = list(iter_markdown(args.root, excludes))

    missing_fm, missing_fields, missing_sections = [], [], []
    norm_map = defaultdict(list)

    for path in files:
        rel = os.path.relpath(path, args.root)
        stem = os.path.splitext(os.path.basename(path))[0]
        if stem.lower() not in {"readme", "index", "manifest"}:
            norm_map[normalise(stem)].append(rel)

        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue

        fm = parse_frontmatter(text)
        if fm is None:
            missing_fm.append(rel)
            continue
        absent = [f for f in args.require if f not in fm]
        if absent:
            missing_fields.append({"file": rel, "missing": absent})

        if args.contract and fm.get("type") in {"topic", "case"}:
            headings = set(re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE))
            absent_sections = [s for s in CONTRACT_SECTIONS if s not in headings]
            if absent_sections:
                missing_sections.append({"file": rel, "missing": absent_sections})

    exact_dupes = {k: v for k, v in norm_map.items() if len(v) > 1}

    near_dupes = []
    keys = sorted(norm_map)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if a and b and SequenceMatcher(None, a, b).ratio() >= args.threshold:
                near_dupes.append({"a": norm_map[a], "b": norm_map[b],
                                   "similarity": round(SequenceMatcher(None, a, b).ratio(), 2)})

    findings = {
        "files_scanned": len(files),
        "missing_frontmatter": missing_fm,
        "missing_fields": missing_fields,
        "missing_contract_sections": missing_sections,
        "duplicate_topics": exact_dupes,
        "near_duplicate_topics": near_dupes,
    }

    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        print(f"scanned {len(files)} markdown files\n")
        if missing_fm:
            print(f"no frontmatter ({len(missing_fm)}):")
            for f in missing_fm[:20]:
                print(f"  {f}")
        if missing_fields:
            print(f"\nincomplete frontmatter ({len(missing_fields)}):")
            for f in missing_fields[:20]:
                print(f"  {f['file']}  missing: {', '.join(f['missing'])}")
        if missing_sections:
            print(f"\nsection contract gaps ({len(missing_sections)}):")
            for f in missing_sections[:20]:
                print(f"  {f['file']}  missing: {', '.join(f['missing'])}")
        if exact_dupes:
            print(f"\nDUPLICATE topics — same normalised name ({len(exact_dupes)}):")
            for k, v in exact_dupes.items():
                print(f"  [{k}] {' | '.join(v)}")
        if near_dupes:
            print(f"\nnear-duplicate topics — review and merge or alias ({len(near_dupes)}):")
            for d in near_dupes[:20]:
                print(f"  {d['similarity']}  {d['a']} ~ {d['b']}")
        if not any([missing_fm, missing_fields, missing_sections, exact_dupes, near_dupes]):
            print("clean: frontmatter complete, no near-duplicate FILENAMES")
        # Always say what was not checked. An eval run found this script printing
        # "no duplicate topics" over a vault where rate-limiting.md and throttling.md
        # covered the same subject — true for filenames, dangerously misleading as a
        # summary. A clean report that overstates its scope is worse than no report.
        print("\nnot checked: semantic duplicates — two pages covering the same subject under\n"
              "unrelated names (rate-limiting.md / throttling.md) are invisible to filename\n"
              "comparison. Only reading the content, or a manifest with an aliases column,\n"
              "catches those.")

    has_findings = any([missing_fm, missing_fields, missing_sections, exact_dupes, near_dupes])
    return 1 if has_findings else 0


if __name__ == "__main__":
    sys.exit(main())
