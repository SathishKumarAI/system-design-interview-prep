#!/usr/bin/env python3
"""Shared Markdown scanning helper for the doc scripts in this folder.

Owns one thing: telling the other scripts which byte offsets of a file are inside a
fenced code block, so a heading or a link that only appears in an *example* is never
treated as real.

Does not own: link parsing, backlink rendering, or the section contract.
"""
from __future__ import annotations

import re

_FENCE_OPEN = re.compile(r"(`{3,}|~{3,})")
_BACKTICK_RUN = re.compile(r"`+")

NUL = "\x00"


def mask_code(text: str) -> str:
    """Blank every fenced block **and** every inline code span, preserving length.

    This is what the doc scripts should call. Both kinds of code are illustrations: a
    link written as `[...](path/to/file.md)` in a sentence explaining link syntax is no
    more a real link than the same line inside a fence, and reporting it as broken has
    exactly the same cost — a permanently red gate that everyone learns to read past.
    """
    return _mask_inline_code(mask_fences(text))


def mask_fences(text: str) -> str:
    """Return a copy of `text` with every fenced code block blanked to NUL.

    The result is the **same length** as the input and keeps every newline, so an
    offset found in the mask indexes the original string unchanged. That is the whole
    point: match on the mask, slice the original.

    Why this exists: `gen_backlinks.py` matches `## Referenced by` and `## Sources`
    textually. A fenced example containing either heading used to have a generated
    backlink list injected into it — this repo's own CLAUDE.md and CONVENTIONS.md were
    damaged that way, and both state their contract as a table now to dodge it.
    `check_links.py` had the mirror-image bug: `path/to/file.md` inside a fenced usage
    example was reported as a broken link forever, which trained everyone to read
    "4 broken, as expected" and wave the fifth one through.

    Fence handling is deliberately CommonMark-lite: an opening fence is three or more
    backticks or tildes at the start of a line (leading whitespace allowed), and the
    block ends at the next line whose first non-space characters are the same fence
    character repeated at least as many times. Info strings (```mermaid) are ignored.
    Indented-by-four-spaces code blocks are NOT masked — this vault does not use them,
    and treating every indented line as code would mask real content inside lists.
    """
    out: list[str] = []
    fence: str | None = None

    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()

        if fence is None:
            match = _FENCE_OPEN.match(stripped)
            # CommonMark: a backtick fence's info string may not contain a backtick. So
            # ```like this``` on one line is an inline code span, not an opener — and
            # treating it as one masks the entire rest of the file. That is not
            # hypothetical: basic/prep/CAP theorem.md line 8 is exactly this shape, and
            # it hid the real "## Referenced by" 19 lines below it.
            if match and not (match.group(1)[0] == "`" and "`" in stripped[match.end():]):
                fence = match.group(1)
                out.append(_blank(line))
            else:
                out.append(line)
            continue

        out.append(_blank(line))
        closing = _FENCE_OPEN.match(stripped)
        if closing and closing.group(1)[0] == fence[0] and len(closing.group(1)) >= len(fence):
            fence = None

    return "".join(out)


def _mask_inline_code(text: str) -> str:
    """Blank inline code spans, line by line, preserving length.

    CommonMark-lite: a run of N backticks opens a span that the next run of exactly N
    backticks closes. Spans are scoped to one line — a span that genuinely wraps is rare
    in prose and not worth the ambiguity of guessing where it ends. An unmatched opener
    is left alone rather than swallowing the rest of the line.
    """
    out: list[str] = []
    for line in text.splitlines(keepends=True):
        if "`" not in line:
            out.append(line)
            continue

        chars = list(line)
        runs = [(m.start(), m.end()) for m in _BACKTICK_RUN.finditer(line)]
        i = 0
        while i < len(runs):
            start, start_end = runs[i]
            width = start_end - start
            closer = next(
                (j for j in range(i + 1, len(runs)) if runs[j][1] - runs[j][0] == width),
                None,
            )
            if closer is None:
                break
            for k in range(start, runs[closer][1]):
                if chars[k] != "\n":
                    chars[k] = NUL
            i = closer + 1
        out.append("".join(chars))
    return "".join(out)


def _blank(line: str) -> str:
    """Same length, same trailing newline, nothing a heading or link regex can match."""
    if line.endswith("\r\n"):
        return NUL * (len(line) - 2) + "\r\n"
    if line.endswith("\n"):
        return NUL * (len(line) - 1) + "\n"
    return NUL * len(line)


def blank_span(mask: str, start: int, end: int) -> str:
    """Blank `mask[start:end]` in place, preserving length."""
    return mask[:start] + NUL * (end - start) + mask[end:]


def in_code(mask: str, offset: int) -> bool:
    """Is this offset inside a fenced block?"""
    return 0 <= offset < len(mask) and mask[offset] == NUL
