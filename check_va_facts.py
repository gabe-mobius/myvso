#!/usr/bin/env python3
"""Checks the sourcing rules in VA_FACTS.md.

Usage:  python3 check_va_facts.py [path/to/VA_FACTS.md]
With no argument it checks VA_FACTS.md in the same folder as this script.

The script exits with a non-zero code and lists the offending rows if:
  * a table row does not have exactly 7 cells;
  * a row's Status is not exactly `sourced` or `UNVERIFIED`;
  * a row has a missing or duplicate ID in the "#" column;
  * a `sourced` row has an empty Source URL, a URL that is not http(s), or a
    URL whose host is not on an allowed official domain (see below);
  * a `sourced` row has an empty "Source quote or value" or an empty "Fact";
  * any row has a missing or invalid "Date checked" (it must be a real
    calendar date in YYYY-MM-DD form and not in the future).
It prints counts (sourced / UNVERIFIED / total) for each section.

Allowed domains for `sourced` rows (a host matches a domain if it is that
domain or any subdomain of it). Only official U.S. government sources:
  * va.gov            U.S. Department of Veterans Affairs (incl. benefits., knowva.ebenefits.)
  * ecfr.gov          Electronic Code of Federal Regulations
  * govinfo.gov       U.S. Government Publishing Office (U.S. Code, Federal Register)
  * congress.gov      Library of Congress, bills and statutes
  * supremecourt.gov  Supreme Court of the United States
  * uscourts.gov      Federal courts (incl. cafc.uscourts.gov, cavc)
  * army.mil, navy.mil, af.mil, dfas.mil, whs.mil   Military departments and DoD agencies
  * war.gov, defense.gov   Department of War (Defense), incl. comptroller.
  * archives.gov           National Archives (NPRC military records).
Never add blogs, news, law-firm, forum, or commercial claims-help sites, and
never add third-party mirrors of VA manuals.
"""
import datetime
import os
import re
import sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "VA_FACTS.md")

ALLOWED_DOMAINS = [
    "va.gov", "ecfr.gov", "govinfo.gov", "congress.gov", "supremecourt.gov",
    "uscourts.gov", "army.mil", "navy.mil", "af.mil", "dfas.mil", "whs.mil",
    "war.gov", "defense.gov", "archives.gov",
]
STATUSES = {"sourced", "UNVERIFIED"}
HEADER = ["#", "Topic", "Fact", "Source URL", "Source quote or value", "Date checked", "Status"]


def host_allowed(host):
    host = host.lower().rstrip(".")
    return any(host == d or host.endswith("." + d) for d in ALLOWED_DOMAINS)


def valid_date(s):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return False
    try:
        d = datetime.date.fromisoformat(s)
    except ValueError:
        return False
    return d <= datetime.date.today()


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main():
    problems, counts, order, seen = [], {}, [], set()
    section, in_table = None, False
    with open(PATH, encoding="utf-8") as f:
        lines = f.readlines()
    for n, line in enumerate(lines, 1):
        if line.startswith("## "):
            section, in_table = line[3:].strip(), False
            continue
        if not line.lstrip().startswith("|"):
            in_table = False
            continue
        cells = split_row(line)
        if cells == HEADER:
            in_table = True
            if section not in counts:
                counts[section] = {"sourced": 0, "UNVERIFIED": 0}
                order.append(section)
            continue
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        if not in_table:
            problems.append(f"line {n}: table row outside a recognized facts table")
            continue
        label = f"{section} row {cells[0] if cells else '?'} (line {n})"
        if len(cells) != 7:
            problems.append(f"{label}: expected 7 cells, found {len(cells)}")
            continue
        rid, topic, fact, url, quote, date, status = cells
        if not rid:
            problems.append(f"{label}: missing ID")
        elif rid in seen:
            problems.append(f"{label}: duplicate ID '{rid}'")
        seen.add(rid)
        if status not in STATUSES:
            problems.append(f"{label}: Status must be exactly `sourced` or `UNVERIFIED`, found '{status}'")
            continue
        counts[section][status] += 1
        if not valid_date(date):
            problems.append(f"{label}: Date checked '{date}' is not a valid YYYY-MM-DD date (or is in the future)")
        if status == "sourced":
            if not fact:
                problems.append(f"{label}: sourced row has no Fact")
            if not url:
                problems.append(f"{label}: sourced row has no Source URL")
            else:
                p = urlparse(url)
                if p.scheme not in ("http", "https") or not p.hostname or " " in url:
                    problems.append(f"{label}: Source URL '{url}' is not a single valid http(s) URL")
                elif not host_allowed(p.hostname):
                    problems.append(f"{label}: Source URL host '{p.hostname}' is not on an allowed official domain")
            if not quote:
                problems.append(f"{label}: sourced row has no Source quote or value")

    print("Counts per section:")
    for s in order:
        c = counts[s]
        print(f"  {s}: sourced={c['sourced']} UNVERIFIED={c['UNVERIFIED']} total={c['sourced'] + c['UNVERIFIED']}")
    if not order:
        problems.append("no facts tables found")
    if problems:
        print(f"\nFAILED: {len(problems)} problem(s):")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print("\nPASSED: every sourced row has an allowed official URL, a quote, and a valid date.")


if __name__ == "__main__":
    main()
