#!/usr/bin/env python3
"""Checks the sourcing rules in FORMS.md.

Usage:  python3 check_forms.py [path/to/FORMS.md]

Exits non-zero and lists problems if:
  * a table row does not have exactly 9 cells;
  * Status is not exactly sourced or UNVERIFIED;
  * a row has a missing or duplicate ID;
  * a sourced row has an empty Source URL, a non-http(s) URL, or a host not
    on an allowed official domain;
  * a sourced row has an empty Purpose, Online, Title, or Edition/quote cell;
  * any row has a missing or invalid Date checked (YYYY-MM-DD, not future).
Also checks the decision table: it must exist, and every FM-row it names
must exist above and be `sourced`.
Prints counts (sourced / UNVERIFIED / total) for each section.

Allowed domains: va.gov, ecfr.gov, govinfo.gov, archives.gov, gsa.gov,
supremecourt.gov, uscourts.gov, army.mil, navy.mil, af.mil, dfas.mil,
whs.mil, war.gov, defense.gov.
"""
import datetime
import os
import re
import sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "FORMS.md")
ALLOWED = [
    "va.gov", "ecfr.gov", "govinfo.gov", "archives.gov", "gsa.gov",
    "supremecourt.gov", "uscourts.gov", "army.mil", "navy.mil", "af.mil",
    "dfas.mil", "whs.mil", "war.gov", "defense.gov",
]
STATUSES = {"sourced", "UNVERIFIED"}
N_CELLS = 9


def host_ok(host):
    host = host.lower().rstrip(".")
    return any(host == d or host.endswith("." + d) for d in ALLOWED)


def valid_date(s):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return False
    try:
        d = datetime.date.fromisoformat(s)
    except ValueError:
        return False
    return d <= datetime.date.today()


def cells(line):
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
        c = cells(line)
        if c and c[0] == "#":
            in_table = True
            continue
        if not in_table or (c and set(c[0]) <= {"-"}):
            continue
        if len(c) != N_CELLS:
            problems.append(f"line {n}: expected {N_CELLS} cells, got {len(c)}")
            continue
        rid, form, title, purpose, online, url, edition, checked, status = c
        if section not in counts:
            counts[section] = {"sourced": 0, "UNVERIFIED": 0, "total": 0}
            order.append(section)
        counts[section]["total"] += 1
        if not rid or rid in seen:
            problems.append(f"line {n}: missing or duplicate ID {rid!r}")
        seen.add(rid)
        if status not in STATUSES:
            problems.append(f"line {n} ({rid}): status {status!r} not in {STATUSES}")
        else:
            counts[section][status] += 1
        if not valid_date(checked):
            problems.append(f"line {n} ({rid}): bad date {checked!r}")
        if status == "sourced":
            if not form or not title or not purpose or not online or not edition:
                problems.append(f"line {n} ({rid}): sourced row missing form/title/purpose/online/edition")
            if not url.startswith("http://") and not url.startswith("https://"):
                problems.append(f"line {n} ({rid}): sourced URL must be http(s)")
            else:
                host = urlparse(url).hostname or ""
                if not host_ok(host):
                    problems.append(f"line {n} ({rid}): host {host!r} not allowed")
            if " " in url.strip() or "\n" in url:
                problems.append(f"line {n} ({rid}): URL cell must be a single bare URL")
    # Decision table: every FM-row it names must exist above and be sourced.
    status_by_id = {}
    sec = None
    for line in lines:
        if line.startswith("## "):
            sec = line[3:].strip()
        c = cells(line) if line.lstrip().startswith("|") else []
        if len(c) == N_CELLS and re.fullmatch(r"FM\d+", c[0]):
            status_by_id[c[0]] = c[8]
    text = "".join(lines)
    i = text.find("## Which forms do I need (decision table)")
    if i < 0:
        problems.append("decision table section '## Which forms do I need (decision table)' is missing")
    else:
        dt = text[i:]
        rows = [l for l in dt.splitlines() if re.match(r"\|\s*\d+\s*\|", l)]
        if len(rows) < 5:
            problems.append(f"decision table has only {len(rows)} rows")
        for l in rows:
            for ref in re.findall(r"\bFM\d+\b", l):
                if ref not in status_by_id:
                    problems.append(f"decision table names {ref}, which is not a FORMS.md row")
                elif status_by_id[ref] != "sourced":
                    problems.append(f"decision table names {ref}, which is not sourced")
        print(f"Decision table: {len(rows)} situations, all form references checked.")
    print("Counts per section:")
    for s in order:
        c = counts[s]
        print(f"  {s}: sourced={c['sourced']} UNVERIFIED={c['UNVERIFIED']} total={c['total']}")
    if problems:
        print(f"FAILED: {len(problems)} problem(s):")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print("PASSED: every sourced form row has an allowed official URL, an edition quote, and a valid date.")


if __name__ == "__main__":
    main()
