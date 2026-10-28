#!/usr/bin/env python3
"""Scans every text file in this repository for content that should not be public.

Usage:  python3 check_public.py [repo_folder]

Fails (non-zero exit) and lists file:line hits for:
  * personal names that must not appear. The list is read from the file named
    by the MYVSO_BLOCKED_NAMES_FILE environment variable (keep it outside the
    repo, one name per line). The scan fails if that variable is unset or the
    file can't be read or is empty.
  * forum and social sources (reddit, pebforum, facebook groups) and known
    third-party mirrors of VA manuals;
  * email addresses other than official .gov/.mil ones;
  * Social Security number patterns, and macOS home-folder paths (/Users/...).
Test profiles are synthetic and are scanned like everything else.
"""
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
SELF = os.path.abspath(__file__)
NAMES_FILE = os.environ.get("MYVSO_BLOCKED_NAMES_FILE", "")


def load_names():
    """Blocked names live outside the repo so the list itself is never published."""
    names = []
    if NAMES_FILE:
        try:
            names = [n.strip().lower() for n in open(NAMES_FILE, encoding="utf-8") if n.strip() and not n.startswith("#")]
        except OSError:
            names = []
    if not names:
        print("FAILED: the blocked-names list was not read (MYVSO_BLOCKED_NAMES_FILE unset, unreadable, or empty).")
        print("Set MYVSO_BLOCKED_NAMES_FILE to a file outside this repo with one name per line.")
        sys.exit(2)
    return names
BLOCKED_SOURCES = ["reddit", "pebforum", "facebook.com/groups", "navigatingva"]
PATTERNS = [
    ("SSN pattern", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("macOS home path", re.compile(r"/Users/[A-Za-z]")),
]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")


def main():
    names = load_names()
    hits = []
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != ".git"]
        for fn in files:
            path = os.path.join(dirpath, fn)
            try:
                lines = open(path, encoding="utf-8").read().splitlines()
            except (UnicodeDecodeError, OSError):
                continue
            rel = os.path.relpath(path, ROOT)
            for n, line in enumerate(lines, 1):
                low = line.lower()
                for w in names:
                    if re.search(r"\b" + w + r"\b", low):
                        hits.append(f"{rel}:{n}: name '{w}'")
                for s in ([] if os.path.abspath(path) == SELF else BLOCKED_SOURCES):
                    if s in low:
                        hits.append(f"{rel}:{n}: source '{s}'")
                for label, rx in PATTERNS:
                    if rx.search(line):
                        hits.append(f"{rel}:{n}: {label}")
                for m in EMAIL.finditer(line):
                    dom = m.group(1).lower()
                    if not (dom.endswith(".gov") or dom.endswith(".mil")):
                        hits.append(f"{rel}:{n}: non-government email '{m.group(0)}'")
    if hits:
        print(f"FAILED: {len(hits)} hit(s):")
        for h in hits:
            print("  - " + h)
        sys.exit(1)
    print("PASSED: no blocked names, forum sources, personal emails, SSN patterns, or home-folder paths.")


if __name__ == "__main__":
    main()
