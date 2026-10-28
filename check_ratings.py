#!/usr/bin/env python3
"""Checks the sourcing rules in RATINGS.md.

Usage:  python3 check_ratings.py [path/to/RATINGS.md]

Exits non-zero and lists the offending rows if any table row:
  * has a different number of cells than its table header;
  * has an empty cell;
  * has no Source URL, a URL that is not https, or a URL whose host is not
    ecfr.gov or va.gov (or a subdomain of either);
  * has a missing or invalid "Date checked" (real YYYY-MM-DD, not in the future);
  * in the Criteria table: has no rating level ("NN%") unless it quotes the
    regulation's own method (hearing loss tables, "Evaluate ..." rows);
  * in the Criteria table: has a "What VA looks at" cell with a number, a
    percent, a degree sign, or a rating-schedule term (it is what the
    assistant shows the veteran, so it must never show levels), a level word,
    a direction word, or a threshold;
  * in the Criteria table: has an "Ask about" cell whose items (split on ";")
    carry a number, percent, level word, or threshold (devices, treatments,
    and medical events only, asked as yes/no facts in E5 step 1), unless it
    is "None (open questions only)".
Also fails if a Criteria row's Source URL is not an eCFR 38 CFR Part 4 page.
"""
import datetime
import os
import re
import sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "RATINGS.md")
ALLOWED = ["ecfr.gov", "va.gov"]
PART4 = "https://www.ecfr.gov/current/title-38/chapter-I/part-4/section-4."


# Words that would turn a plain-words or Ask-about cell into a level ladder,
# a threshold, or a hint about what raises a rating (E5 steps 1 and 3).
NUMWORDS = (r"one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
            r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|half|quarter|single|double")
LEVEL_RE = re.compile(r"\d|%|°|percent|degrees?\b|\b(" + NUMWORDS + r")\b|flexion|extension|ankylosis|prostrating|"
                      r"incapacitating|occupational|impairment|instability|subluxation|economic|inadaptability|"
                      r"\b(mild|moderate|moderately|severe|severely|marked|complete|total|gross|near-continuous)\b", re.I)
DIRECTION_RE = re.compile(r"\b(raises|raising|lowers|lowering|higher|lower|more|less|most|least|counts?|matters?|"
                          r"worse|better|rate[sd]?|rating|level|levels|under|over|above|below|exceeds?|"
                          r"once|twice|frequent|weekly|monthly|per)\b", re.I)
THRESH_RE = re.compile(r"\b(at least|or more|or less|times|weeks?|months?|years?|days?|hours?|minutes?|inches|cm)\b", re.I)


def host_ok(url):
    u = urlparse(url)
    h = (u.hostname or "").lower().rstrip(".")
    return u.scheme == "https" and any(h == d or h.endswith("." + d) for d in ALLOWED)


def date_ok(s):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return False
    try:
        return datetime.date.fromisoformat(s) <= datetime.date.today()
    except ValueError:
        return False


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main():
    problems, section, header, rows = [], None, None, 0
    for n, line in enumerate(open(PATH, encoding="utf-8"), 1):
        if line.startswith("## "):
            section, header = line[3:].strip(), None
            continue
        if not line.lstrip().startswith("|"):
            header = None
            continue
        c = cells(line)
        if header is None:
            header = c
            continue
        if all(re.fullmatch(r":?-+:?", x) for x in c):
            continue
        rows += 1
        where = f"line {n} ({section})"
        if len(c) != len(header):
            problems.append(f"{where}: {len(c)} cells, header has {len(header)}")
            continue
        r = dict(zip(header, c))
        for k, v in r.items():
            if not v:
                problems.append(f"{where}: empty '{k}'")
        url = r.get("Source URL", "")
        if not url:
            problems.append(f"{where}: no Source URL column/value")
        elif not host_ok(url):
            problems.append(f"{where}: source not https ecfr.gov/va.gov: {url}")
        if not date_ok(r.get("Date checked", "")):
            problems.append(f"{where}: missing or invalid Date checked")
        if section == "Criteria":
            if not url.startswith(PART4):
                problems.append(f"{where}: criteria source must be an eCFR 38 CFR Part 4 section page")
            lv = r.get("Rating levels (38 CFR Part 4 text)", "")
            if not re.search(r"\d+%", lv) and not re.search(r"Table VII|\bEvaluate\b", lv):
                problems.append(f"{where}: no rating levels")
            plain = r.get("What VA looks at (plain words, E5 step 3)")
            ask = r.get("Ask about (yes/no facts, E5 step 1)")
            if plain is None:
                problems.append(f"{where}: no 'What VA looks at (plain words, E5 step 3)' column")
            elif LEVEL_RE.search(plain) or DIRECTION_RE.search(plain):
                problems.append(f"{where}: plain-words cell shows a level, number, threshold, direction, or criteria term")
            if ask is None:
                problems.append(f"{where}: no 'Ask about (yes/no facts, E5 step 1)' column")
            elif ask != "None (open questions only)":
                for item in ask.split(";"):
                    if not item.strip() or LEVEL_RE.search(item) or DIRECTION_RE.search(item) or THRESH_RE.search(item):
                        problems.append(f"{where}: Ask about item '{item.strip()}' has a number, threshold, or criteria term")
            if not r.get("DC"):
                problems.append(f"{where}: no diagnostic code")
    if rows == 0:
        problems.append("no table rows found")
    print(f"{os.path.basename(PATH)}: {rows} rows")
    if problems:
        print("FAILED:")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print("PASSED: every row has an official ecfr.gov/va.gov https source and a valid date checked.")


if __name__ == "__main__":
    main()
