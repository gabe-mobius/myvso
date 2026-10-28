#!/usr/bin/env python3
"""Builds the single paste-in text file for chat apps with no file upload.

Usage:  python3 scripts/build_paste_in.py [--force] [output path]
        (default: ../<repo>-exports/myvso_paste_in.txt, outside the repo; an existing
        default file is kept unless --force is given; an explicit path is overwritten
        with a notice)

The file is a one-paragraph header, then ASSISTANT_INSTRUCTIONS.md, then
VA_FACTS.md, RATINGS.md, FORMS.md, and GUIDES.md, each after a
"=== FILE: name ===" marker. Maintainer-only lines (the "Run `python3 ...`"
reminders) are left out, because a pasted chat has no scripts to run.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGS = [a for a in sys.argv[1:] if a != "--force"]
FORCE = "--force" in sys.argv[1:]
EXPLICIT = bool(ARGS)
OUT = ARGS[0] if ARGS else os.path.join(
    os.path.dirname(ROOT), os.path.basename(ROOT) + "-exports", "myvso_paste_in.txt")
FILES = ["VA_FACTS.md", "RATINGS.md", "FORMS.md", "GUIDES.md"]
HEADER = ("Act as MyVSO for this entire chat: follow the MyVSO instructions below exactly. "
          "The VA_FACTS.md, RATINGS.md, FORMS.md, and GUIDES.md sections after them are your fact, "
          "rating, form, and guide files. State VA facts only from them or from the live official "
          "lookups the instructions allow.\n\n")
MAINT = re.compile(r"^Run `python3 [^`]+`.*\n\n?", re.M)


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return MAINT.sub("", f.read())


def main():
    parts = [HEADER, read("ASSISTANT_INSTRUCTIONS.md")]
    for name in FILES:
        parts.append(f"\n=== FILE: {name} ===\n\n" + read(name))
    text = "".join(parts)
    if re.search(r"python3|check_\w+\.py", text):
        sys.exit("FAILED: a maintainer script line is still in the paste-in text")
    if os.path.exists(OUT):
        if not EXPLICIT and not FORCE:
            sys.exit(f"{OUT} already exists; not overwriting. Pass --force or an explicit output path.")
        print(f"Overwriting {OUT}")
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote {OUT}: {len(text.split())} words")


if __name__ == "__main__":
    main()
