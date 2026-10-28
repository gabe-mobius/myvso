**MyVSO walks you through your VA claim, one easy step at a time. You end with your story written down, the forms you need, and what to do today. It's free. MyVSO is not a VSO and not the VA.**

> **Does this get me to 100%?** No. Nobody can promise a rating, and anyone who does is selling something. This helps you show VA what your records actually support. It is free.

It is a free self-help guide for one VA disability claim. You decide, you sign, you file.

MyVSO is a set of instructions you load into an AI assistant (ChatGPT, Grok Bot, or similar). The assistant then walks a veteran through organizing one claim: what happened, what records exist, what is missing, and how to file. It keeps the veteran's own words. It does not coach, predict ratings, suggest answers, or write medical opinions.

What a session gives the veteran:

- **Less typing.** Questions with fixed answers (yes/no, branch, which form path) come as choices to tap where the platform shows them, or as a numbered list answered with one number. The story, symptoms, and how the condition affects them are always typed or dictated in the veteran's own words; there are never answer choices for those.
- **Your statement, written with you:** after each condition, it offers to write your statement from only your own words, and you check every line.
- **A claim summary** at the end of every session, after a short "what you got done today" recap: conditions in the veteran's words, facts gathered, which forms apply, evidence they have and still need, and up to 3 next steps (intent to file first if not filed). It fits on one printed page for a VSO, and it picks up where they left off next time (saved as a file where the platform allows, otherwise pasted in).
- **Help pulling records:** service treatment records, VA medical records, private records (21-4142/4142a), and the claim file (C-file), from official sources only.
- **A letter reader:** paste a VA email or a photo of a VA letter to get what it is, any deadline it states, and the options. It never picks an option, and points to free accredited help for appeals and complex cases.
- **Check what you were told:** paste or photograph advice from a VSO, company, lawyer, buddy, or social media, and it checks each claim against VA's own rules, with the source.

## What MyVSO can and can't do

**It can:** walk you through VA.gov one screen at a time, put your story in your own words, find which forms apply, explain VA's rules and your letters, check advice you were given, help you ask for your records, explain exam letters and rescheduling, and do the math on ratings VA already gave you.

**It can't:** promise or aim for a rating, suggest symptoms or how bad they are, write anything you didn't say, file or sign for you, hold power of attorney, use your VA.gov login, represent you, or charge you anything.

**Why not:** Nobody can promise a rating; VA warns about ads that guarantee large awards or instant results. What you send VA has to be true, because false statements can carry penalties, so MyVSO never suggests symptoms or adds anything you didn't say. You decide, you sign, and you file. VA says never to share your VA.gov login. MyVSO is free, and VSO help is free too. Each point is a sourced row in `VA_FACTS.md` (VSO3, VSO8, VSO10, VSO11, LAW8). This is general information, not legal advice.

## What is here

| File | What it is |
|---|---|
| `ASSISTANT_INSTRUCTIONS.md` | The instructions you give the assistant. |
| `GUIDES.md` | Reference detail the instructions point to: question order, the "which forms" questions, how to show "check what you were told", and the "what MyVSO can and can't do" answer. Load it with the other files. |
| `VA_FACTS.md` | The VA and DoD facts the tool relies on, each with an official source link, a quote, and the date checked. |
| `RATINGS.md` | Rating criteria for common conditions, quoted from 38 CFR Part 4 on eCFR, with link and date checked. Other conditions are looked up live. |
| `FORMS.md` | Forms a veteran may need across this scope, each with edition date, online option, official URL, and quote, plus the "which forms do I need" decision table. |
| `SETUP-chatgpt.md` | How to set it up in ChatGPT. |
| `SETUP-grok-bot.md` | How to set it up in Grok Bot. |
| `SETUP-MUSE.md` | How to set it up in Muse or a Claude Project. |
| `check_va_facts.py` | Checks every row of `VA_FACTS.md` for format, status, official source, quote, and date. |
| `check_ratings.py` | Checks every row of `RATINGS.md` for an ecfr.gov or va.gov source and a valid date checked. |
| `check_forms.py` | Checks every row of `FORMS.md` the same way. |
| `check_instructions.py` | Checks the instructions and `GUIDES.md` for the opening, tagline, all required parts, and banned wording. |
| `check_public.py` | Scans the repo for personal information and non-official sources. |
| `scripts/build_paste_in.py` | Builds the single paste-in text file (header, the instructions, then the four data files; maintainer script lines left out). Run `python3 scripts/build_paste_in.py [--force] [output path]`; it won't overwrite the default export without `--force`. |
| `scripts/check_ecfr_updates.py` | Maintainer check: lists rules changed on eCFR after their date checked. |
| `.github/workflows/ecfr-monthly.yml` | Runs that check monthly and opens an issue only if something changed. |
| `test_profiles/` | Made-up veterans for checking how the assistant behaves. None are real people. |
| `VERSION` | Date of the last fact check. |
| `LICENSE` | MIT license for the code and scripts. |
| `LICENSE-DOCS.txt` | CC BY 4.0 license for the written guides and documents. |

## How sourcing works

Every row in `VA_FACTS.md` is either `sourced` or `UNVERIFIED`.

- A `sourced` row has an official link (va.gov, ecfr.gov, govinfo.gov, supremecourt.gov, archives.gov, or a .mil site), a quote from that page, and the date it was checked.
- An `UNVERIFIED` row is something the tool needs but that has not been confirmed against an official page yet. The assistant is told never to state these as fact.
- Forum posts, social media, and unofficial copies of VA manuals are not used.

Run the checks:

```
python3 check_va_facts.py
python3 check_forms.py
python3 check_ratings.py
python3 check_instructions.py
MYVSO_BLOCKED_NAMES_FILE=/path/outside/repo/names.txt python3 check_public.py
python3 scripts/check_ecfr_updates.py
```

## Testing the assistant with test_profiles/

`test_profiles/` is for checking the assistant's behavior, not for the scripts. A normal install does not need it. Each file is a made-up veteran (`"made_up": true`) with a `profile` (how to act) and `what_it_tests` (the behavior to watch for).

1. Set up the assistant on your platform, following a SETUP file.
2. Open a new chat, say "Start," and play the veteran in `profile`, using their words.
3. Compare what the assistant does with `what_it_tests`. For example, it must refuse to exaggerate, must not suggest answers or ratings, and must keep the veteran's own words in the statement and the claim summary.
4. Run all of them after you change `ASSISTANT_INSTRUCTIONS.md`, and on each new platform.

## Updates

Every rule in `RATINGS.md` and `VA_FACTS.md` shows the date it was checked. VA's rules don't change often, but when they do, MyVSO catches it:

- **The veteran's assistant does it.** Once a veteran has a copy, their assistant keeps it current on its own. If it can browse the web, then at the start of a chat (once a month, or weekly if the veteran picks that at setup) it asks eCFR when 38 CFR Parts 3 and 4 were last changed. If nothing changed after the dates checked, it moves on. If something did, it rereads the rules that veteran needs before quoting them, uses the new wording, and says so, with the link and today's date. If it can't reach eCFR, it says so instead of guessing. Other facts are rechecked against the official page linked in their row. It never pulls from this repository, so pulling the maintainer's updates is optional.
- **The maintainer's check.** `scripts/check_ecfr_updates.py` asks the eCFR versioner API (`https://www.ecfr.gov/api/versioner/v1/versions/title-38.json?part=3` and `?part=4`) for the latest amendment dates and lists any row whose section changed after its date checked (exit code 1 if any, 2 if eCFR can't be reached). `.github/workflows/ecfr-monthly.yml` runs it on the 1st of each month and opens an issue only when something changed.

How often the assistant can act on its own depends on your platform (see "Platform tiers" in `ASSISTANT_INSTRUCTIONS.md`). `VERSION` shows the date of the last full check of these files.

## Important

This is general information. It is not legal, tax, or financial advice, and it is not a substitute for an accredited VSO, attorney, or claims agent. MyVSO does not file anything, does not see your VA account, and cannot tell you what VA will decide. Free help from accredited Veterans Service Organizations is available; find one at https://www.va.gov/get-help-from-accredited-representative/find-rep/. Always confirm deadlines and rules on VA.gov.
