#!/usr/bin/env python3
"""Self-check for the fence masking the doc scripts rely on.

    python scripts/test_doc_scripts.py

No framework, no fixtures. Every assertion here is a bug that has actually happened in
this repo, named after the damage it did. Exits 0 when all pass.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _md import blank_span, in_code, mask_code, mask_fences   # noqa: E402
from gen_backlinks import apply_section                       # noqa: E402


def test_mask_preserves_length_and_lines():
    """Offsets found in the mask must index the original string unchanged."""
    text = "a\n```\nsecret\n```\nb\n"
    mask = mask_fences(text)
    assert len(mask) == len(text), (len(mask), len(text))
    assert mask.count("\n") == text.count("\n")
    assert mask.startswith("a\n")
    assert mask.endswith("\nb\n")


def test_fenced_heading_is_masked():
    """The CLAUDE.md damage: a contract example containing the heading it documents."""
    text = "# Doc\n\n```\n## Referenced by\n\n- [x](y.md)\n```\n\nreal body\n"
    mask = mask_fences(text)
    assert "## Referenced by" not in mask
    assert "real body" in mask


def test_unfenced_heading_survives():
    text = "# Doc\n\n## Referenced by\n\n- [x](y.md)\n"
    assert "## Referenced by" in mask_fences(text)


def test_info_string_and_tilde_fences():
    for opener, closer in (("```mermaid", "```"), ("~~~", "~~~"), ("````", "````")):
        text = f"before\n{opener}\n## Sources\n{closer}\nafter\n"
        mask = mask_fences(text)
        assert "## Sources" not in mask, opener
        assert "before" in mask and "after" in mask, opener


def test_apply_section_does_not_write_into_a_fence():
    """The actual regression: gen_backlinks.py injected a backlink list into an example."""
    text = (
        "# Contract\n\n"
        "Files end like this:\n\n"
        "```\n"
        "## Referenced by\n"
        "\n"
        "- generated, do not hand-maintain\n"
        "```\n\n"
        "## Sources\n\n"
        "- something\n"
    )
    out = apply_section(text, "## Referenced by\n\n- [Other](other.md)\n", "Referenced by")

    # The fenced example is byte-for-byte intact...
    fence = "```\n## Referenced by\n\n- generated, do not hand-maintain\n```"
    assert fence in out, out

    # ...and the real section landed before ## Sources, exactly once outside the fence.
    assert out.count("- [Other](other.md)") == 1
    assert out.index("- [Other](other.md)") < out.index("## Sources")


def test_apply_section_replaces_a_real_section():
    text = "# T\n\n## Referenced by\n\n- [Stale](stale.md)\n\n## Sources\n\n- s\n"
    out = apply_section(text, "## Referenced by\n\n- [Fresh](fresh.md)\n", "Referenced by")
    assert "stale.md" not in out
    assert "fresh.md" in out
    assert out.index("## Referenced by") < out.index("## Sources")


def test_inline_code_span_is_masked():
    """The last permanently-broken link: a link written inside backticks, in prose."""
    text = "The script rewrites them to `[...](path/to/file.md)` links.\n"
    mask = mask_code(text)
    assert "path/to/file.md" not in mask
    assert "The script rewrites them to" in mask
    assert len(mask) == len(text)


def test_inline_code_outside_backticks_survives():
    text = "Real: [Other](other.md) and code: `x`\n"
    mask = mask_code(text)
    assert "[Other](other.md)" in mask
    assert "`x`" not in mask


def test_unmatched_backtick_does_not_swallow_the_line():
    text = "a ` b [Real](real.md)\n"
    assert "[Real](real.md)" in mask_code(text)


def test_double_backtick_span():
    text = "use ``a ` b`` here [Real](real.md)\n"
    mask = mask_code(text)
    assert "[Real](real.md)" in mask
    assert "a ` b" not in mask


def test_same_line_triple_backticks_are_not_a_fence():
    """The regression this fix caused once: an unterminated 'fence' ate the rest of the file.

    basic/prep/CAP theorem.md line 8 is ```text``` on one line. Reading it as an opener
    masked everything after it, including the real '## Referenced by' — so gen_backlinks
    appended a second copy on every run and never converged.
    """
    text = "intro\n```Networks aren't reliable.```\n\n## Referenced by\n\n- [x](y.md)\n"
    mask = mask_code(text)
    assert "## Referenced by" in mask
    assert "Networks" not in mask                      # still masked, as inline code
    assert len(mask) == len(text)


def test_backlinks_converge_on_that_file_shape():
    text = "intro\n```Networks aren't reliable.```\n\n## Referenced by\n\n- [Old](old.md)\n"
    once = apply_section(text, "## Referenced by\n\n- [New](new.md)\n", "Referenced by")
    twice = apply_section(once, "## Referenced by\n\n- [New](new.md)\n", "Referenced by")
    assert once == twice, "second pass must be a no-op"
    assert once.count("## Referenced by") == 1
    assert "old.md" not in once


def test_blank_span_and_in_code():
    mask = mask_fences("abc\n")
    assert not in_code(mask, 0)
    assert in_code(blank_span(mask, 0, 3), 0)
    assert not in_code(mask, 999)                      # out of range is not "in code"


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
