---
name: walkthrough
description: Walk the user through a codebase block by block in a local web page with plain explanations, a verdict per block, and a comment box you answer. Use when the user asks for a code walkthrough or to review or understand their code line by line.
---

# Code walkthrough

A local page shows the code block by block, your explanation beside each block, and a comment box. The user's
comments land in a file; you answer them in the page. Scripts are in `${CLAUDE_PLUGIN_ROOT}/scripts`.

## 1. Write the notes

Read the code first. Then write `<code folder>/.walkthrough/notes.json`:

```json
{"repos": [{"name": "myapp", "summary": "One line on what it is.",
  "files": [{"path": "myapp/main.py", "about": "What the file is for, one or two sentences.",
    "blocks": [{"id": "main-1", "start": 1, "end": 12, "title": "Imports and settings",
                "verdict": "keep", "what": "What these lines do.", "why": "Your judgement: why it is needed, or what to change."}]}]}]}
```

- `path` is relative to the code folder. Files go in the order the app uses them, starting at the entry point.
- Blocks cover every line, split at natural boundaries (a function, a group of constants). Block ids are unique.
- `verdict` is one of `keep`, `simplify`, `remove`, `fix`. Be honest: flag dead code, duplication and bugs.
- Plain short English. Explain to someone reading this code for the first time.
- For a large codebase, write the first files, start the page, and add the rest while the user reads.

If the user asks for a walkthrough of only part of the code, cover only that part.

## 2. Start the page

Run in the background: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/serve.py" "<code folder>" [port]` (port 8090 by
default; pick another if it is taken). Tell the user the URL.

Suggest adding `.walkthrough/` to `.gitignore`.

## 3. Answer comments

Start the Monitor tool on `python3 -u "${CLAUDE_PLUGIN_ROOT}/scripts/watch.py" "<code folder>"`, with the
longest timeout, and re-arm it whenever it expires. Each line it prints is a comment: `{"block": id, "text": ...}`.

Answer each by appending one line to `<code folder>/.walkthrough/comments.jsonl`:

```json
{"at": "HH:MM", "who": "Claude", "block": "<the block id>", "text": "your answer"}
```

- Answer the question asked, plainly; the page refreshes by itself.
- Change the code only when the user asks for it in a comment or the chat. Then say in the answer what changed,
  and fix the `start`/`end` line numbers in notes.json for every block the edit moved.
