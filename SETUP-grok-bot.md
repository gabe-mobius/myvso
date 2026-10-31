# MyVSO: Setup: Grok Bot (Tier A)

## What you need

- Grok Bot. It runs agents with their own cloud computer, so it can save files, run the checks, and keep a schedule (Tier A).
- The MyVSO files from this repository: `ASSISTANT_INSTRUCTIONS.md`, `VA_FACTS.md`, `RATINGS.md`, `FORMS.md`, and `GUIDES.md`.

## Set it up

Easiest way: import the ready-made [MyVSO Grok Bot template](https://x.ai/bot/WgrtZt_85lbuzoFBQWM_f). It loads the files and runs the setup questions for you. To set it up by hand instead:

1. Create a new bot and attach the five MyVSO files above, or give it this repository's address.
2. Start a conversation. Before it says hello, your bot downloads the files once from the public MyVSO repository onto its own computer: `ASSISTANT_INSTRUCTIONS.md`, `VA_FACTS.md`, `RATINGS.md`, `FORMS.md`, `GUIDES.md`, the check scripts, the README, and VERSION. It uses all five .md files; without RATINGS.md, FORMS.md, or GUIDES.md it cannot show VA's rating rules, the forms, or the advice checks. It runs the source checks before using them, and it never overwrites a facts file or claim summary it already has.
3. Answer the questions one at a time: your intent to file, the records you have, and what happened in your own words.
4. You get your claim summary right away: your conditions in your own words, the facts gathered, which forms apply, the evidence you have and what's missing, and up to 3 next steps, each with its official source. Your bot updates it as you go and gives it again at the end of each session.
5. If you want, your bot can remind you before your intent-to-file year ends. It sets this up only if you say yes.

Prefer to do it by hand? Start a conversation, attach `ASSISTANT_INSTRUCTIONS.md`, `VA_FACTS.md`, `RATINGS.md`, `FORMS.md`, and `GUIDES.md`, and say "Follow these instructions and use only the sourced rows for VA facts. Start."

## Answering questions

Grok Bot can ask a question as a card you answer by tapping: when a question allows several answers, you select the ones you want and press Submit (Grok Bot changelog, v0.25.0, https://x.ai/changelog/bot, checked 2026-10-23). MyVSO uses these cards only for short-answer questions (yes/no, your branch, which situation fits). If you see a numbered list instead, reply with just the number. Every set of choices ends with "Not sure" and "Skip", and both are fine answers.

Your story, your symptoms, and how the condition affects you are never multiple choice: you say those in your own words. For longer answers, the same changelog says you can press or hold ⌘D (Ctrl+D on Windows and Linux) to dictate into the message field.

## Staying current

- Your bot downloads the files once, at setup. After that, it keeps its own copy current by rechecking each fact against the official source linked in that row, monthly if you agree to that routine. It never pulls from this repository again.
- If your assistant can browse the web, it checks VA's rule book (eCFR) for changes at the start of a chat, once a month, or every week if you pick that during setup. Your choice is saved in your claim summary. Before it quotes a rule that changed, it rereads it and tells you, with the link and the date. If it can't reach the page, it says so instead of guessing.
- When a source has changed, it updates its copy and tells you what changed for your claim summary, as old versus new, with the link. If nothing changed, it sends nothing. You can also ask **"What changed?"** any time.

## Honest limits

- The assistant can still make mistakes. Check anything important on VA.gov.
- It cannot see your VA account or records, and it does not file for you.
- Do not give it your VA.gov password, SSN, or other login details.

## Good to know

- Conversations are stored under the service's terms. Leave out details you do not want stored.
- MyVSO is not a VSO and not the VA.
