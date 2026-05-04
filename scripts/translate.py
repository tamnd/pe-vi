#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
pe-vi translation tool.

Translations live in scripts/data/{en,vi,zh_CN}/*.md files.
Each file covers a range of problems and uses the format:

    ## Problem N: Title
    Body text (may span multiple lines)

Usage:
  uv run scripts/translate.py status
  uv run scripts/translate.py apply [--start N] [--end N] [--dry-run] [-v]
  uv run scripts/translate.py extract [--start N] [--end N] [--lang en]
  uv run scripts/translate.py export [--start N] [--end N]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
POSTS = ROOT / "source" / "_posts"
DATA_DIR = Path(__file__).parent / "data"

# ---------------------------------------------------------------------------
# Markdown data loader
# ---------------------------------------------------------------------------

_HEADER_RE = re.compile(r"^## Problem (\d+):\s*(.+)$")


def load_lang(lang: str) -> dict[int, tuple[str, str]]:
    """Load all problem data for a language from scripts/data/<lang>/*.md.

    Returns {n: (title, body)}.
    """
    lang_dir = DATA_DIR / lang
    if not lang_dir.exists():
        return {}
    result: dict[int, tuple[str, str]] = {}
    for md_file in sorted(lang_dir.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        current_n: int | None = None
        current_title = ""
        body_lines: list[str] = []

        def flush():
            if current_n is not None:
                body = "\n".join(body_lines).strip()
                result[current_n] = (current_title, body)

        for line in text.splitlines():
            m = _HEADER_RE.match(line)
            if m:
                flush()
                current_n = int(m.group(1))
                current_title = m.group(2).strip()
                body_lines = []
            elif line.startswith("# "):
                # Top-level section header — skip
                pass
            else:
                if current_n is not None:
                    body_lines.append(line)
        flush()
    return result


def load_data() -> dict[int, dict[str, tuple[str, str]]]:
    """Load EN and VI data from markdown files."""
    en = load_lang("en")
    vi = load_lang("vi")
    all_n = set(en) | set(vi)
    result: dict[int, dict[str, tuple[str, str]]] = {}
    for n in all_n:
        entry: dict[str, tuple[str, str]] = {}
        if n in en:
            entry["en"] = en[n]
        if n in vi:
            entry["vi"] = vi[n]
        result[n] = entry
    return result


DATA = load_data()


# ---------------------------------------------------------------------------
# File parsing
# ---------------------------------------------------------------------------

def parse_post(path: Path) -> dict:
    """Return parsed sections of a problem post file."""
    text = path.read_text(encoding="utf-8")
    normalized = re.sub(r"\n\*\*\* *\n", "\n***\n", text)
    parts = normalized.split("\n***\n")
    return {
        "raw": text,
        "normalized": normalized,
        "parts": parts,
        "n_stars": len(parts) - 1,
    }


def extract_en_from_post(path: Path) -> tuple[str, str] | None:
    """Extract (en_title, en_body) from a problem file."""
    parsed = parse_post(path)
    parts = parsed["parts"]
    if len(parts) < 4:
        return None
    en_section = parts[2].strip()
    lines = en_section.split("\n")
    title = ""
    body_lines = []
    for line in lines:
        stripped = line.strip()
        m = re.match(r"^#{0,3}\s*\*\*(.+?)\*\*\s*$", stripped)
        if m and not title:
            title = m.group(1).strip()
        else:
            body_lines.append(line)
    body = "\n".join(body_lines).strip()
    return (title, body) if title else (en_section[:80], en_section)


def apply_translation(path: Path, n: int, vi_title: str, vi_body: str, dry_run: bool = False) -> bool:
    """Replace translation section with Vietnamese. Returns True if file changed."""
    parsed = parse_post(path)
    parts = parsed["parts"]
    if len(parts) < 3:
        print(f"  [SKIP] {path.name}: unexpected structure ({len(parts)} parts)")
        return False

    original_link = f"[Xem đề gốc (tiếng Anh)](https://projecteuler.net/problem={n})"
    vi_section = f"{original_link}\n\n## **{vi_title}**\n\n{vi_body}\n"
    new_text = "\n***\n".join(parts[:2]) + "\n***\n" + vi_section + "\n***\n"
    new_text = new_text.replace("﻿", "")  # strip BOM

    if parsed["normalized"].replace("﻿", "") == new_text:
        return False
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status(args: argparse.Namespace) -> None:
    total = len(list(POSTS.glob("[0-9]*.md")))
    vi_count = sum(1 for n in DATA if "vi" in DATA[n])
    en_count = sum(1 for n in DATA if "en" in DATA[n])
    print(f"Problems total (source files): {total}")
    print(f"VI translations in data/:      {vi_count}")
    print(f"EN data in data/:              {en_count}")
    print(f"Remaining to translate:        {total - vi_count}")
    if vi_count < total:
        missing = [n for n in range(1, total + 1) if n not in DATA or "vi" not in DATA[n]]
        print(f"Missing VI: {missing[:20]}{'...' if len(missing) > 20 else ''}")


def cmd_apply(args: argparse.Namespace) -> None:
    start, end = args.start, args.end
    changed = skipped = missing = 0
    for n in range(start, end + 1):
        path = POSTS / f"{n}.md"
        if not path.exists():
            continue
        if n not in DATA or "vi" not in DATA[n]:
            missing += 1
            if args.verbose:
                print(f"  [MISSING] {n}: no VI translation")
            continue
        vi_title, vi_body = DATA[n]["vi"]
        did_change = apply_translation(path, n, vi_title, vi_body, dry_run=args.dry_run)
        if did_change:
            changed += 1
            if args.verbose or args.dry_run:
                print(f"  {'[DRY]' if args.dry_run else '[OK]'} {n}: {vi_title}")
        else:
            skipped += 1
    label = "Would change" if args.dry_run else "Changed"
    print(f"{label}: {changed}  Already up-to-date: {skipped}  Missing VI: {missing}")


def cmd_extract(args: argparse.Namespace) -> None:
    """Print content from source files in markdown data format for a given lang."""
    start, end = args.start, args.end
    lang = args.lang
    lines = [f"# Project Euler Problems {start}–{end} ({lang.upper()})\n"]
    for n in range(start, end + 1):
        path = POSTS / f"{n}.md"
        if not path.exists():
            continue
        if lang == "en":
            result = extract_en_from_post(path)
            if result:
                title, body = result
                lines.append(f"\n## Problem {n}: {title}\n")
                if body:
                    lines.append(body + "\n")
        else:
            print(f"Extract for lang={lang} not supported via this command; edit data/{lang}/ directly.", file=sys.stderr)
            return
    print("".join(lines))


def cmd_export(args: argparse.Namespace) -> None:
    """Show bilingual EN+VI content."""
    start, end = args.start, args.end
    for n in range(start, end + 1):
        path = POSTS / f"{n}.md"
        if not path.exists():
            continue
        en = DATA.get(n, {}).get("en")
        if not en:
            result = extract_en_from_post(path)
            en = result if result else ("?", "?")
        vi = DATA.get(n, {}).get("vi")
        print(f"\n{'='*60}")
        print(f"Problem {n}")
        print(f"EN: {en[0]}")
        print(en[1])
        if vi:
            print(f"\nVI: {vi[0]}")
            print(vi[1])
        else:
            print("\nVI: [NOT TRANSLATED]")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show translation progress")

    p_apply = sub.add_parser("apply", help="Apply VI translations to source/_posts/")
    p_apply.add_argument("--start", type=int, default=1)
    p_apply.add_argument("--end", type=int, default=994)
    p_apply.add_argument("--dry-run", action="store_true")
    p_apply.add_argument("-v", "--verbose", action="store_true")

    p_extract = sub.add_parser("extract", help="Print content from source files in markdown format")
    p_extract.add_argument("--start", type=int, default=1)
    p_extract.add_argument("--end", type=int, default=994)
    p_extract.add_argument("--lang", default="en", choices=["en"])

    p_export = sub.add_parser("export", help="Show bilingual EN+VI content")
    p_export.add_argument("--start", type=int, default=1)
    p_export.add_argument("--end", type=int, default=994)

    args = parser.parse_args()
    {
        "status": cmd_status,
        "apply": cmd_apply,
        "extract": cmd_extract,
        "export": cmd_export,
    }[args.command](args)


if __name__ == "__main__":
    main()
