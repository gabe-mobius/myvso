# MyVSO: Setup: Muse and Claude (Tier A/B)

You can run MyVSO with Muse (this app) or in a Claude Project. What you get depends on how you set it up. Where files and scheduling are available, you get the full behavior. Everywhere, you get the complete step-by-step guide and your claim summary.

## Option 1: In this app (Muse)

1. Say: **"Start MyVSO."**
2. Muse downloads the working files once from the public repository (`ASSISTANT_INSTRUCTIONS.md`, `VA_FACTS.md`, `RATINGS.md`, `FORMS.md`, `GUIDES.md`, and the check scripts) and runs the source checks on them. Those files become your own copy, kept on your side. After this first download, Muse does not go back to the repository.
3. Answer the questions one at a time: your intent to file, the records you have, and what happened in your own words.
4. You get your claim summary right away: your conditions in your own words, the facts gathered, which forms apply, the evidence you have and what's missing, and up to 3 next steps, each with its official source. It is updated as you go and given again at the end of each session.
5. For reminders (for example before your intent-to-file year ends), ask for scheduled check-ins when you set up. Otherwise check in any time and ask **"What's next?"**

## Option 2: A Claude Project (claude.ai)

1. Create a new Project and name it MyVSO.
2. Paste the full text of `ASSISTANT_INSTRUCTIONS.md` (from the repository) into the project's custom instructions.
3. Download `VA_FACTS.md`, `RATINGS.md`, `FORMS.md`, and `GUIDES.md` from the repository and add them to the project's knowledge.
4. Start a chat in the project and say: **"Start MyVSO."**
5. Where it can save files, it saves your claim summary in your folder (for example, my-claim-summary.txt) and reads it when you return. Otherwise, keep the summary it gives you and paste it back next time.

## Answering questions

- **Muse:** MyVSO does not rely on tappable buttons here. Short-answer questions (yes/no, your branch, which situation fits) come as a numbered list. Reply with just the number. Every list ends with "Not sure" and "Skip", and both are fine answers. Your story, your symptoms, and how the condition affects you are never multiple choice: you say those in your own words. For longer answers you can use your device's voice dictation, if it has it.
- **Claude Project:** Anthropic says "Claude may present interactive options you can click or tap — like multiple choice questions" and "You can still type a response if you prefer," and that availability may vary (https://support.claude.com/en/articles/13641943-visual-and-interactive-content, checked 2026-10-23). If you see choices, tap one; if you see a numbered list, reply with the number. Your story and symptoms are always in your own words.

## Staying current

- Your copy stays current because your assistant maintains it, not because it re-downloads anything. With Muse, on a monthly cycle, it rechecks each fact in your copy against its official government source. It updates the facts that changed and tells you about the changes that affect your claim summary. It never pulls from the repository again.
- If your assistant can browse the web, it checks VA's rule book (eCFR) for changes at the start of a chat, once a month, or every week if you pick that during setup. Your choice is saved in your claim summary. Before it quotes a rule that changed, it rereads it and tells you, with the link and the date. If it can't reach the page, it says so instead of guessing.
- On the Project path there is no schedule running for you. Ask **"What changed?"** when you check in, and it will recheck the facts that apply to you against the official sources right then.
- Claude cannot promise reminders on the Project path. If reminders matter to you, use the Grok Bot build (Tier A) or check-ins here in the app.

## Good to know

- Your claim summary holds personal details. Keep it in your own files and never post it publicly. Never share your VA.gov password or SSN with any assistant.
- MyVSO is not a VSO and not the VA. This is general information, not legal advice.
