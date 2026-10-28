#!/usr/bin/env python3
"""Checks ASSISTANT_INSTRUCTIONS.md for required tool behavior.

Usage:  python3 check_instructions.py [path/to/ASSISTANT_INSTRUCTIONS.md]

Fails (non-zero exit) and lists problems if:
  * the tagline "MyVSO is not a VSO and not the VA." is missing;
  * any required part heading (PART A through PART O) is missing;
  * the phrase "at least as likely as not" appears outside PART E's ban list
    (rule E2b), PART F (the doctor sheet), and the F4 rule;
  * the instructions, GUIDES.md, README.md, or a SETUP file mention a premium,
    upgrade, subscription, or price, or a fee/charge outside the sourced red flags;
  * 'Tier A', 'Tier B', 'Tier C', 'claim folder', the disclaimer, the find-a-VSO
    link, or the H0 timing rule is missing; the word 'knee' appears; or the
    OGC accreditation link is used instead of the single find-a-VSO link;
  * the 'which forms do I need' step (PART L) or its key rules are missing;
  * the 100% answer, the claim summary / resume / 'what to do today' rules,
    the choices rules (B7), the records guide (PART M), or the letter reader
    (PART N) is missing;
  * the TOP RULE (simple guided tour: about 60 words per message, one idea,
    everyday words, sources behind "Where does that come from?") is missing;
  * any sample assistant message (a quoted span) is over 60 words or contains
    a CFR/U.S.C. citation or a link;
  * the STUCK RULE (offer to work through a screenshot or error together, one
    step at a time; no credentials; no invented screen steps; other routes only
    after that fails) is missing;
  * the opening value statement, the statement offer (E5 step 5), the session
    recap (I3), or the "check what you were told" part (PART O) is missing;
  * the "what MyVSO can and can't do" answer (A10; GUIDES.md CC1-CC3) is missing;
  * GUIDES.md (question order, Part L questions, Part O display) is missing,
    incomplete, or uses banned wording; its quoted spans get the same checks;
  * a line in the instructions or GUIDES.md mentions suicide without X2 or 988,
    or a test profile step about suicide lacks 988 and "Are you safe right now?";
  * PART H states a percentage or adds ratings ("10 + 10") outside a quote, or a
    test profile expects a rating percentage outside a quote;
  * a FORMS.md row ID is not FM-prefixed, or a reference uses an old F5+ form ID
    (Part F rules are F1-F4; forms are FM1-FM21);
  * known-bad wording returns: a "what is this claim about" theory option in
    GL3, "caused by" in GUIDES.md, the story asked twice (QO3), QO4 without the
    forms step, "more back pay", "last four digits are enough", "take anything
    from anyone else", or a "50 percent" gloss on the doctor sheet;
  * a SETUP file does not load all five .md files, or the paste-in builder
    calls them the "only" source;
  * an 'added after ...' marker returns, E1's own-words or meaning safeguard is missing,
    or any quoted question (straight or curly) or "ask" sentence anywhere in the
    instructions or GUIDES.md names a criteria term, percentage, threshold, or
    suggested value (named devices and treatments in yes/no facts are allowed);
  * GL1-GL4 lack Not sure / Skip, or GUIDES.md re-asks a question;
  * the file is longer than 4,200 words (keeps it pasteable).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "ASSISTANT_INSTRUCTIONS.md")
TAGLINE = "MyVSO is not a VSO and not the VA."
PARTS = [f"PART {c}." for c in "ABCDEFGHIJKLMNO"]
GUIDES = os.path.join(os.path.dirname(os.path.abspath(PATH)), "GUIDES.md")
OPENING = ("I'll walk you through your VA claim, one easy step at a time. You'll end with your story written down, "
           "the forms you need, and what to do today. It's free. MyVSO is not a VSO and not the VA.")
SAMPLE_MAX_WORDS = 60
CFR_RE = re.compile(r"\bC\.?\s?F\.?\s?R\b|\u00a7|\bU\.?S\.?C\b", re.I)


def main():
    text = open(PATH, encoding="utf-8").read()
    problems = []
    if TAGLINE not in text:
        problems.append("tagline missing")
    for p in PARTS:
        if p not in text:
            problems.append(f"missing section heading '{p}'")
    # Find where each part starts, to locate phrase occurrences.
    starts = sorted((text.find(f"--- {p}"), p) for p in PARTS if text.find(f"--- {p}") >= 0)

    def part_at(i):
        cur = None
        for s, p in starts:
            if s <= i:
                cur = p
        return cur
    for m in re.finditer(r"at least as likely as not", text, re.I):
        part = part_at(m.start())
        if part not in ("PART E.", "PART F."):
            problems.append(f"'at least as likely as not' appears in {part or 'preamble'} (allowed only in PART E ban list and PART F)")
    # Fee language: MyVSO is free. Hard terms are banned outright (unless "Never mention");
    # soft terms (fee, charge, cost, price, paid) only in the sourced red-flag/free wording.
    _dir = os.path.dirname(os.path.abspath(PATH))
    hard = re.compile(r"\b(premium|upgrade|subscription|paid plan|paid version|pro plan|per month|monthly fee)\b|\$\d", re.I)
    soft = re.compile(r"\b(fees?|charg(e|es|ed|ing)|costs?|pric(e|es|ing)|paid|pay for)\b", re.I)
    allow = re.compile(r"Never mention an upgrade or paid service|fees before VA's initial decision \(VSO8\)|"
                       r"^Fee before the initial decision|charge you anything|^\W*\d\) Cost \(VSO3|"
                       r"only accredited attorneys and claims agents may charge, and not for work before", re.I)
    for fname in ["ASSISTANT_INSTRUCTIONS.md", "GUIDES.md", "README.md"] + sorted(
            f for f in os.listdir(_dir) if f.startswith("SETUP") and f.endswith(".md")):
        fp = PATH if fname == "ASSISTANT_INSTRUCTIONS.md" else os.path.join(_dir, fname)
        if not os.path.exists(fp):
            continue
        for s in re.split(r"(?<=[.!?])\s+|\n+", open(fp, encoding="utf-8").read()):
            s = s.strip()
            if hard.search(s) and "Never mention" not in s:
                problems.append(f"{fname}: fee/upgrade language: '{s[:80]}'")
            elif soft.search(s) and not allow.search(s):
                problems.append(f"{fname}: fee/charge wording outside the sourced red flags: '{s[:80]}'")
    if re.search(r"\bknee\b", text, re.I):
        problems.append("condition-specific wording ('knee') found; keep instructions generic")
    if "va.gov/ogc/apps/accreditation" in text:
        problems.append("use the single find-a-VSO link (find-rep), not the OGC search")
    for need in ["Tier A", "Tier B", "Tier C", "claim folder", "Disclaimer:",
                 "https://www.va.gov/get-help-from-accredited-representative/find-rep/", "H0.",
                 "PART K.", "FORMS.md", "Never recommend a specific",
                 "PART L. WHICH FORMS DO I NEED", "Never show the full form list",
                 "decision table", "intent to file first",
                 "Does this get me to 100%? No. Nobody can promise a rating, and anyone who does is selling something.",
                 "claim summary", "Picking up from your summary", "What to do today", "at most 3",
                 "B7. Choices", '"Not sure" and "Skip"', "Never offer choices for the story", "voice dictation",
                 "PART M. HELP PULLING RECORDS", "PART N. LETTER AND MAIL READER",
                 "Never pick an option", "never calculated by you",
                 "TOP RULE. A SIMPLE GUIDED TOUR", "about 60 words at most", "one idea per message",
                 "Everyday words. No form numbers, regulation citations, links, or legal terms unless the veteran asks.",
                 '"Where does that come from?"', "source URL and date checked",
                 "Before anything else, there's one quick step that can protect your start date for back pay.",
                 "STUCK RULE. IN THE FOXHOLE WITH THEM", "never hand the work back",
                 "Send me a screenshot of what you're seeing, or paste the error message, and we'll work through it together. Just cover any password, code, email, or username before you send it.",
                 "one step at a time", "Never invent screen steps", "never log in for them",
                 "only after working through it together has failed",
                 "The normal amount of pain is zero.", "Anything you might have missed before?",
                 "SAFETY RULE. HEAVY MOMENTS", "Are you safe right now?", "call 988 and press 1, or text 838255",
                 "Doing well and struggling can both be true.", "Never push to finish a section.",
                 OPENING, "Want to write your statement for this now?", "Here's what you got done today",
                 "PART O. CHECK WHAT YOU WERE TOLD", "Matches VA's rule", "Doesn't match VA's rule",
                 "I can't check this one", "Never say who to trust", "VSO8-VSO12", "GUIDES.md",
                 "RATINGS.md", "look it up live on eCFR", "say you don't have that rule", "Never paraphrase from memory",
                 "A10.", "See the full list", "Why not?", "TTY 800-799-4889",
                 "Any mention of suicide, including someone lost to it: X2 first",
                 "Never name a criteria term or level just shown",
                 "never swap the veteran's words for the rule's words", "Shape is your job; go all in",
                 "The rater does the matching", "Follow-up questions use plain topics only",
                 "Never a rating-schedule term or threshold",
                 "(C2, C3, L2, I3)", "is not a prediction; never apply it to them", "GUIDES.md KC1-KC3"]:
        if need not in text:
            problems.append(f"missing required text '{need}'")
    if re.search(r"anything true", text, re.I):
        problems.append("'anything true' found; it implies the veteran lied (use 'Anything you might have missed before?')")
    # GUIDES.md: reference detail moved out of the main file; must exist with its sections.
    if not os.path.exists(GUIDES):
        problems.append("GUIDES.md missing (question order, Part L questions, Part O display)")
        gtext = ""
    else:
        gtext = open(GUIDES, encoding="utf-8").read()
        for need in ["QO1.", "QO2.", "QO3.", "QO4.", "GL1.", "GL2.", "GL3.", "GL4.",
                     "GO1.", "GO2.", "GO3.", "GO4.", "GO5.", "GO6.", "the instructions win",
                     "CC1.", "CC2.", "CC3.", "I can't: promise or aim for a rating",
                     "Matches VA's rule", "Doesn't match VA's rule", "I can't check this one"]:
            if need not in gtext:
                problems.append(f"GUIDES.md: missing required text '{need}'")
        for bad in [r"anything true", r"\bknee\b", r"at least as likely as not"]:
            if re.search(bad, gtext, re.I):
                problems.append(f"GUIDES.md: banned wording '{bad}'")
    # Sample assistant wording: every quoted span ("..." or “...”) on a line
    # is treated as sample wording. Flag spans over about 60 words, or with a
    # CFR citation or a link (rule T1-T2: sources live behind "Where does that come from?").
    for name, body in [("", text), ("GUIDES.md ", gtext)]:
        for n, ln in enumerate(body.splitlines(), 1):
            for m in re.finditer(r'["\u201c]([^"\u201c\u201d]+)["\u201d]', ln):
                q = m.group(1)
                if len(q.split()) > SAMPLE_MAX_WORDS:
                    problems.append(f"{name}line {n}: sample message is {len(q.split())} words (max about {SAMPLE_MAX_WORDS}): '{q[:50]}...'")
                if CFR_RE.search(q):
                    problems.append(f"{name}line {n}: sample message contains a CFR citation: '{q[:50]}...'")
                if re.search(r"https?://|www\.", q):
                    problems.append(f"{name}line {n}: sample message contains a link: '{q[:50]}...'")
    # E1/B2: never swap the veteran's words for the rule's words, in questions or the statement.
    if re.search(r"\badded after\b|\bmark(s|ed)? (the |any )?additions\b", text + gtext, re.I):
        problems.append("banned 'added after ...' marker (E1 replaces it)")
    # Question guard (B2, B3, E5 step 1): every quoted question ("..." or curly quotes) anywhere in
    # the instructions or GUIDES.md, and every prose sentence that tells you to ask something, must not
    # name a criteria term, a percentage, a threshold, or a suggested value. Named devices and
    # treatments in yes/no fact questions are allowed.
    crit = re.compile(r"flexion|extension|instability|unstable|ankylos|\bdegrees?\b|impairment|prostrating|"
                      r"range of motion|incapacitating|subluxation|dislocation of|recurrent|"
                      r"occupational|characteristic|productive of|totally|\b(?!100\s*%)\d+\s*(%|percent)", re.I)
    thresh = re.compile(r"\b(more|less|fewer|greater|longer|shorter|worse|better) than\b|\bat least\b(?! as likely)|"
                        r"\bno more than\b|\bat most\b|\bup to \d|\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s*"
                        r"(minutes?|hours?|days?|weeks?|months?|years?|times|feet|yards|inches|pounds)\b|"
                        r"\b(once|twice)\s+(a|an|per|each)\s+(day|week|month|year)\b|\bout of (5|10)\b|\d+\s*/\s*10\b", re.I)
    value = re.compile(r"\bwould you say\b|\b(mild|moderate|severe|marked|total|serious|slight|extreme)\b|\bscale\b", re.I)
    def bad_term(s):
        for rx in (crit, thresh, value):
            m = rx.search(s)
            if m:
                return m.group(0)
        return None
    for name, body in [("", text), ("GUIDES.md ", gtext)]:
        for n, ln in enumerate(body.splitlines(), 1):
            if ln.lstrip().startswith("Forbidden:"):
                continue  # B3's examples of what never to ask
            for q in re.findall(r'"([^"\n]*\?)"|\u201c([^\u201d\n]*\?)\u201d', ln):
                q = q[0] or q[1]
                if "check for updates" in q:
                    continue  # J4 freshness choice, not a symptom question
                hit = bad_term(q)
                if hit:
                    problems.append(f"{name}line {n}: a question uses a rating term, threshold, or value ('{hit}'): '{q[:60]}'")
            for s in re.split(r"(?<=[.!?])\s+", ln):
                if re.search(r"\bask(s|ed|ing)?\b|\bquestions?\b", s, re.I) and not re.search(
                        r"\b(never|no|not|don't|avoid)\b", s, re.I):
                    hit = bad_term(re.sub(r'"[^"]*"|\u201c[^\u201d]*\u201d', "", s))
                    if hit:
                        problems.append(f"{name}line {n}: an ask instruction uses a rating term, threshold, or value ('{hit}'): '{s[:60]}'")
    # Guards for the recheck of a4cf24b.
    m = re.search(r"^   3\) Only after they've answered:.*$", text[text.find("E5."):], re.M)
    if not m:
        problems.append("E5 step 3 not found")
    else:
        s3 = m.group(0)
        if re.search(r"\d+\s*(%|percent)", s3, re.I):
            problems.append("E5 step 3 shows a percentage; show only RATINGS.md's plain words")
        for need in ["Never show levels or percentages", "What VA looks at", "Where does that come from?", "eCFR link"]:
            if need not in s3:
                problems.append(f"E5 step 3 missing '{need}'")
    m = re.search(r"^   3\) \"The last piece is the full claim form\.\"(.*)$", text, re.M)
    if not m or "If one was filed" not in m.group(1):
        problems.append("F1 step 3 must say the intent-to-file line only if one was filed")
    cc3 = re.search(r"^   3\) Filing, signing, representing.*$", gtext, re.M)
    cc3q = re.findall(r'"([^"]*)"', cc3.group(0)) if cc3 else []
    if not cc3q or cc3q[0] != "You decide, you sign, and you file.":
        problems.append("GUIDES.md CC3 reason 3 must be only 'You decide, you sign, and you file.' with no legal reason")
    for gl in ("GL1.", "GL2.", "GL3.", "GL4."):
        ln = next((l for l in gtext.splitlines() if l.startswith(gl)), "")
        if "Not sure / Skip" not in ln:
            problems.append(f"GUIDES.md {gl} needs Not sure / Skip choices")
    if re.search(r"\bask (it )?again\b", gtext, re.I):
        problems.append("GUIDES.md re-asks a question; 'Not sure' and 'Skip' are final (B4)")
    for need in ["if no sentence changes meaning", "Moving a sentence is fine; changing its words is not",
                 '"Ask about" item', "not statement words",
                 "never what an answer means for the rating", "no sentence changes meaning; no added"]:
        if need not in text:
            problems.append(f"missing required text '{need}' (device/treatment yes/no facts, E1 meaning safeguard)")
    for need in ["FM3", "FM4", "FM13", "FM14"]:
        if not re.search(r"^GL\d.*\b" + need + r"\b", gtext, re.M):
            problems.append(f"GUIDES.md Part L questions never reach {need}")
    qo2 = next((l for l in gtext.splitlines() if l.startswith("QO2.")), "")
    if "[condition]" in qo2 and not (-1 < qo2.find("What conditions") < qo2.find("[condition]")):
        problems.append("GUIDES.md QO2 uses [condition] before asking for the conditions")
    if "guarantees results" in gtext:
        problems.append("GUIDES.md: 'guarantees results' is broader than VSO10")
    if "get ready for a VA exam" in gtext:
        problems.append("GUIDES.md: 'get ready for a VA exam' is broader than LT2-LT5/EX1-EX3")
    if not re.search(r"stay on getting help \(CL2\) until they say they are safe", text):
        problems.append("X2 must say claim work resumes only once they say they are safe")
    # Guards for review findings on e45565f, so these exact problems can't come back.
    root = os.path.dirname(os.path.abspath(PATH))
    unquote = lambda s: re.sub(r'["\u201c][^"\u201c\u201d]*["\u201d]', '""', s)
    for name, body in [("", text), ("GUIDES.md ", gtext)]:
        for n, ln in enumerate(body.splitlines(), 1):
            if re.search(r"suicid", ln, re.I) and not re.search(r"X2|988", ln):
                problems.append(f"{name}line {n}: mentions suicide without X2 or the crisis line (988)")
    hs, he = text.find("--- PART H."), text.find("--- PART I.")
    for ln in text[hs:he].splitlines():
        u = unquote(ln)
        if re.search(r"\d+\s*(%|percent)", u, re.I) or re.search(r"\d+\s*\+\s*\d+", u):
            problems.append(f"PART H states a percentage or adds ratings outside a quote: '{ln[:60]}...'")
    for bad, why in [(r"more back pay", "sounds like a promise"), (r"last four digits are enough", "unsourced"),
                     (r"anything from anyone else", "unsourced"), (r"50 percent or greater", "unsourced gloss")]:
        if re.search(bad, text, re.I):
            problems.append(f"banned wording '{bad}' ({why})")
    for bad in [r"What is this claim about", r"caused by", r"QO3\. \"Tell me about your"]:
        if re.search(bad, gtext, re.I):
            problems.append(f"GUIDES.md: banned wording '{bad}'")
    m = re.search(r"^QO4\..*$", gtext, re.M)
    if not m or "Part L" not in m.group(0):
        problems.append("GUIDES.md: QO4 must include the forms step (Part L)")
    old_id = re.compile(r"\bF([5-9]|[1-9]\d)\b")
    for fname in ["ASSISTANT_INSTRUCTIONS.md", "GUIDES.md", "VA_FACTS.md", "README.md", "FORMS.md"]:
        fp = os.path.join(root, fname)
        if not os.path.exists(fp):
            continue
        body = open(fp, encoding="utf-8").read()
        for mm in old_id.finditer(body):
            problems.append(f"{fname}: old form ID '{mm.group(0)}' (forms are FM1-FM21; F1-F4 are Part F rules)")
        if fname == "FORMS.md" and re.search(r"\bF\d+\b", body):
            problems.append("FORMS.md: row IDs must be FM-prefixed")
    for fname in sorted(os.listdir(root)):
        if fname.startswith("SETUP-") and fname.endswith(".md"):
            body = open(os.path.join(root, fname), encoding="utf-8").read()
            for need in ["ASSISTANT_INSTRUCTIONS.md", "VA_FACTS.md", "RATINGS.md", "FORMS.md", "GUIDES.md"]:
                if need not in body:
                    problems.append(f"{fname}: does not load {need}")
    bp = os.path.join(root, "scripts", "build_paste_in.py")
    if not os.path.exists(bp):
        problems.append("scripts/build_paste_in.py missing")
    elif re.search(r"your only fact", open(bp, encoding="utf-8").read()):
        problems.append("build_paste_in.py header calls the files the 'only' source (blocks allowed live lookups)")
    pdir = os.path.join(root, "test_profiles")
    for fname in sorted(os.listdir(pdir)) if os.path.isdir(pdir) else []:
        if not fname.endswith(".json"):
            continue
        d = json.load(open(os.path.join(pdir, fname), encoding="utf-8"))
        items = [d.get("what_it_tests", "")] + list(d.get("expected_steps", []))
        for s in items:
            u = unquote(s)
            step = s is not items[0]
            if re.search(r"suicid|crosses my mind", s, re.I):
                if step and not ("988" in s and "Are you safe right now?" in s):
                    problems.append(f"test_profiles/{fname}: a step about suicide lacks 988 and \"Are you safe right now?\": '{s[:60]}...'")
                if not step and not re.search(r"X2|988|crisis line", s, re.I):
                    problems.append(f"test_profiles/{fname}: what_it_tests mentions suicide without X2 or the crisis line")
            if re.search(r"danger to self", s, re.I) and "988" not in s:
                problems.append(f"test_profiles/{fname}: 'danger to self' without 988: '{s[:60]}...'")
            if re.search(r"\b(?!100%\s+answer)\d+\s*(%|percent)", u, re.I) or re.search(r"\d+\s*\+\s*\d+", u):
                problems.append(f"test_profiles/{fname}: expects a rating number outside a quote: '{s[:60]}...'")
    words = len(text.split())
    if words > 4200:
        problems.append(f"{words} words (limit 4200)")
    print(f"ASSISTANT_INSTRUCTIONS.md: {words} words")
    if problems:
        print(f"FAILED: {len(problems)} problem(s):")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print("PASSED: tagline, all parts A-O, opening, GUIDES.md, claim summary, choices rules, 100% answer, guided-tour rule, stuck rule, sample messages short and citation-free, nexus phrase only where allowed, no fee language, length OK.")


if __name__ == "__main__":
    main()
