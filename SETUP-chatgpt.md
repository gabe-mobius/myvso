# Set up MyVSO in ChatGPT

## What you need

- A ChatGPT account.
- `ASSISTANT_INSTRUCTIONS.md`, `VA_FACTS.md`, `RATINGS.md`, `FORMS.md`, and `GUIDES.md` from this repo, or the single paste-in text file if you were given one.

## Set it up

1. In ChatGPT, create a new Project.
2. Paste the full text of `ASSISTANT_INSTRUCTIONS.md` into the instructions box.
3. Upload `VA_FACTS.md`, `RATINGS.md`, `FORMS.md`, and `GUIDES.md` as project files.
4. Start a chat in that project and say "Start."

No Project? Start a new chat, paste `ASSISTANT_INSTRUCTIONS.md`, then `VA_FACTS.md`, then `RATINGS.md`, then `FORMS.md`, then `GUIDES.md`, then say "Start."

OpenAI says new custom GPTs cannot be created on personal ChatGPT plans (https://help.openai.com/en/articles/8554407-gpts, checked 2026-10-23), so these steps do not use one.

## Answering questions

Short-answer questions (yes/no, your branch, which situation fits) come as a numbered list. Reply with just the number. Every list ends with "Not sure" and "Skip", and both are fine answers. Your story, your symptoms, and how the condition affects you are never multiple choice: you say those in your own words. For longer answers you can use your device's voice dictation, if it has it.

## Saving your place

At the end of each session you get a claim summary. Save it. Next time, paste it as your first message (after the instructions) and the assistant picks up where you left off without re-asking. It also prints on one page for a VSO.

## Staying current

- You download the files once, at setup. After that, your assistant keeps its own copy current by rechecking each fact against the official source linked in that row. It never pulls from this repository again.
- If your assistant can browse the web, it checks VA's rule book (eCFR) for changes at the start of a chat, once a month, or every week if you pick that during setup. Your choice is saved in your claim summary. Before it quotes a rule that changed, it rereads it and tells you, with the link and the date. If it can't reach the page, it says so instead of guessing.
- ChatGPT does not run on a schedule for you (Tier B or C), so it cannot remind you or recheck by itself. When you come back, ask **"What changed?"** and it will recheck the facts that matter to your claim summary against the official sources and tell you what changed, with links.

## Honest limits

- The assistant can still make mistakes. Check anything important on VA.gov.
- It cannot see your VA account or records, and it does not file for you.
- Do not give it your VA.gov password, SSN, or other login details.

## Good to know

- Your chats are stored by OpenAI under their terms. Leave out details you do not want stored.
- MyVSO is not a VSO and not the VA.
