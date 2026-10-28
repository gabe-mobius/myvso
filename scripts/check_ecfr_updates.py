#!/usr/bin/env python3
"""Maintainer check: has 38 CFR Part 3, 4, or 14 changed since our rows were checked?

Usage:  python3 scripts/check_ecfr_updates.py

Uses the eCFR versioner API (no key needed), verified 2026-10-24:
  https://www.ecfr.gov/api/versioner/v1/versions/title-38.json?part=3
  https://www.ecfr.gov/api/versioner/v1/versions/title-38.json?part=4
  https://www.ecfr.gov/api/versioner/v1/versions/title-38.json?part=14
  -> meta.latest_amendment_date (newest amendment in the part), and
     content_versions[] with identifier (e.g. "4.71a"), amendment_date, name.

For every table row in RATINGS.md and VA_FACTS.md that links to an eCFR
Part 3, 4, or 14 page (Part 14: LAW2, LAW3, LAW6), it compares that section's newest amendment_date with
the row's "Date checked". It prints the oldest and newest date checked, the
latest amendment date for each part, and any rows whose section was amended
after their date checked.

Exit codes: 0 nothing changed; 1 at least one section changed after its
check date; 2 could not reach or read the API (never treated as "no change").
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ["RATINGS.md", "VA_FACTS.md"]
PARTS = ["3", "4", "14"]
API = "https://www.ecfr.gov/api/versioner/v1/versions/title-38.json?part={}"
URL_RE = re.compile(r"https://www\.ecfr\.gov/current/title-38/[^\s|)\"]*?part-(\d+)(?:/subpart-[^/\s|]+)?(?:/section-([\w.]+))?(?=[\s|)\"]|$)")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fetch(part):
    req = urllib.request.Request(API.format(part), headers={"Accept": "application/json", "User-Agent": "myvso-ecfr-check"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def rows(path):
    """Yield (row_id, date_checked, [(part, section_or_None), ...]) for table rows."""
    header = None
    for ln in open(path, encoding="utf-8"):
        ln = ln.strip()
        if not ln.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if set(ln) <= set("|-: "):
            continue
        if "Date checked" not in header or len(cells) != len(header):
            continue
        date = cells[header.index("Date checked")]
        refs = [(m.group(1), m.group(2)) for m in URL_RE.finditer(ln)]
        if refs and DATE_RE.match(date):
            yield cells[0], date, refs


def main():
    latest_part, latest_sec, names = {}, {}, {}
    for p in PARTS:
        try:
            d = fetch(p)
        except Exception as e:  # network, HTTP, or JSON error
            print(f"ERROR: could not read {API.format(p)}: {e}")
            sys.exit(2)
        latest_part[p] = d["meta"]["latest_amendment_date"]
        for v in d["content_versions"]:
            sid, ad = v["identifier"], v["amendment_date"]
            if ad > latest_sec.get(sid, ""):
                latest_sec[sid], names[sid] = ad, v["name"]
        print(f"38 CFR Part {p}: latest amendment {latest_part[p]} ({API.format(p)})")

    all_dates, changed = [], []
    for f in FILES:
        for rid, date, refs in rows(os.path.join(ROOT, f)):
            all_dates.append(date)
            for part, sec in refs:
                if part not in PARTS:
                    continue
                amended = latest_sec.get(sec) if sec else latest_part[part]
                if amended is None:
                    changed.append(f"{f} {rid}: section {sec} not found in eCFR Part {part} (check link)")
                elif amended > date:
                    what = f"§ {sec}" if sec else f"Part {part}"
                    changed.append(f"{f} {rid}: {what} amended {amended}, after date checked {date}")
    if all_dates:
        print(f"eCFR-linked rows: {len(all_dates)}; date checked oldest {min(all_dates)}, newest {max(all_dates)}")
    if changed:
        print(f"CHANGED: {len(changed)} row(s) need a re-check against eCFR:")
        for c in sorted(set(changed)):
            print("  - " + c)
        sys.exit(1)
    print("No eCFR changes after any row's date checked.")


if __name__ == "__main__":
    main()
