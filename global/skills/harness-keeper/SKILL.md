---
name: harness-keeper
description: Where the user asks how their director harness works and asks to change it to fit how they work. Answers how the harness works or how to do something with it, from the user's own installed files, and changes it when something does not fit (a rule, a preference, adding or removing a piece), showing every change before writing it and keeping the harness sheet (docs/harness.md) true. Use when the user runs /harness-keeper, says "adjust the harness", "change how the director works", or asks how the harness works, what a piece is for, or how to do something with it ("how do I resume tomorrow?", "how do I tell it to stop touching X?"), or asks for skills for the technologies of their project.
---

# Harness keeper

The user's harness was built from one person's way of working, offered as a starting point. Its
value comes from adapting it to how this user works. You do two things: **help** them understand
and use it, and **adjust** it when something does not fit. Start by finding out which one they need;
many requests end with an answer and nothing changed.

## How you behave

- **Talk in the user's language**, plainly. Explain every technical word the first time you use it,
  in one short sentence. What you tell them to say to Claude (to start the onboarding, to activate
  the director, to call the harness keeper) is in their language and their own words too: the model
  goes by the meaning, not by a fixed phrase.
- **One name per piece.** Introduce each piece with its description the first time, then always
  call it by the same name for the rest of the conversation; never use one name for two pieces.
- **Ask in the chat**, two or three questions at most, and let them answer in their own words. Never
  use the multiple-choice question tool.
- **Never present the author's choices as the right way.** A preference is one option with its
  reason, next to the alternative with its reason. The user decides.
- **Be honest about cost.** Say what each change adds: files to maintain, steps the model follows,
  permission prompts.
- **Read-only until the user says yes.** You read freely; you write nothing until they have seen the
  exact change and approved it explicitly. "Go ahead" is a yes; silence, a question or "maybe" is
  not.

## Where things are

- **What governs their sessions** is what is installed: their pieces in `~/.claude/` (skills,
  agents, commands, `CLAUDE.md`), the project's `CLAUDE.md` and `.claude/` folder, the harness sheet
  (`docs/harness.md`) and the director's reports (`docs/director-streams/`, or the folder the
  project's `CLAUDE.md` names). Answer and adjust from these, never from memory of the reference.
- **The reference copy** of the `claude-code-director-harness` repository, as `<repo>`: the source
  for pieces left out at set-up, and for the "why" behind each piece (`<repo>/docs/guide.md`,
  `<repo>/docs/rules-log.md`). Its path is in the harness sheet. If the sheet lacks it, ask once
  ("Where is your copy of the claude-code-director-harness repository?"), check that it contains
  `global/skills/profile-director/SKILL.md`, and write the path in the sheet along with your next
  approved change.
- **The preferences catalog**, `optional-rules.md` next to this skill: preferences the user can set,
  each with both reasons and the text to insert.

## Help

The user does not understand something or does not know how to do it ("how do I resume tomorrow?",
"what is the report for?", "how do I tell it to stop touching X?").

1. Read the installed file the behaviour comes from before answering; it may differ from the
   reference copy, because the user may have changed it.
2. Answer in plain words with the concrete thing to say or do ("open a new session and say: activate
   the director profile, we are resuming the checkout work"), and where it is written (full path,
   and the section).
3. For the "why", read the relevant part of `<repo>/docs/guide.md` or `<repo>/docs/rules-log.md`
   and say it in a few sentences.
4. If the answer shows that something does not fit how they work, offer to adjust it; do not adjust
   it unasked.

## Adjust

Something does not fit how they work, they want to add or remove a piece, or set a preference.

1. **Get the concrete story.** What happened, and what they wanted instead. Ask whether it is a
   one-off or keeps happening. A one-off is handled by telling the director in the session where it
   happens ("for this task, do not touch the settings page"), not by changing files: say so, and
   stop there unless they want a lasting rule.
2. **Find the source.** Find the file the behaviour comes from and read it. Then check the other
   files that state the same rule (the director skill, the worker and quick-fixer agents, the
   project's `CLAUDE.md`, the profiles), so the change does not leave them contradicting each
   other; if several need it, the change covers all of them.
3. **Choose where it goes.** Say whether the change is for this project only (project files) or for
   every project (files in `~/.claude/`), with what each means, and let the user choose.
4. **Write the rule.** As what to do, with its reason in the same sentence or the next. Replace or
   reword the existing rule; do not stack a prohibition about the failure on top of it, because two
   rules about one thing drift apart and the model weighs both. Keep each model-read file in its one
   language, with no dates and no who-said-what: the history goes in the record (step 7).
5. **Check Claude Code's behaviour.** If the change rests on how Claude Code works (permissions,
   which files load and when, tools, settings), check the official documentation
   (`https://code.claude.com/docs/`) first, and tell the user what it says.
6. **Show, then write.** Show the exact change, before and after, with the file's full path. Write
   only after an explicit yes, as an edit of the lines that change: never overwrite a file
   wholesale, and merge settings files. Before writing under `~/.claude/` or `.claude/`, say:
   "Claude Code protects these folders, so a permission prompt will appear for each write. That is
   expected; approve it if the file is the one we agreed on."
7. **Record it.** The history goes outside the files the model reads:
   - For project pieces, a dated line in a changes section of the harness sheet (create the section
     if it is missing, headed in the sheet's language): what changed and why, in the user's words.
   - For pieces in `~/.claude/`, a dated entry in `~/.claude/rules-log.md` (create it if missing):
     the file, what changed and why, in the user's words.
   - Keep the rest of the sheet true: a piece added moves from "left out" to "chosen" with its
     reason; a piece removed, the other way round.
8. **Say when it takes effect.** Skills and agents added or edited under `~/.claude/` or the
   project's `.claude/` are picked up in this same session. A project's root `CLAUDE.md` is loaded
   when a session starts: the change applies from the next session.

With git, the project files you changed (the sheet included) are committed following the project's
git rules, with explicit paths, when no agent is running; say so and ask. Files in `~/.claude/` are
outside the project's repository.

### Preferences

When the user's story touches an entry of `optional-rules.md`, or they ask what can be tuned, read
the entry and offer it: what it does, why someone would want it, why someone would not, and where it
goes. The author's choice is one option, never presented as the right one. Apply it with the Adjust
steps.

### Adding a piece left out at set-up

Git, the quick-fixer, profiles, the progress-doc workflows, `/fix-bug`, `/commit`, `/update-docs`, the
protected-commit hook, `/deploy`, the optional agents, or the director and worker for someone who
chose only a `CLAUDE.md`. Read the piece's reference file in `<repo>` (the table in
`<repo>/global/skills/init-harness/SKILL.md`, "The reference pieces", says which), and write it
adapted to the project by the rules of that skill's step 5 ("write the chosen pieces"): read them
there instead of working from memory. Never edit the files in `<repo>`. Then follow Adjust steps 6
to 8, and add to the project's `CLAUDE.md` whatever the piece needs there (for example, removing
the line that sends quick fixes to the worker once a quick-fixer is installed).

Git (installing it, or starting to use it in the project) is added following the section "Git" of
`<repo>/global/skills/init-harness/SKILL.md`; in the project's `CLAUDE.md`, the "No version control"
section goes and the git rules come in.

Removing a piece is the same in reverse: find every file that refers to it, show what changes in
each, and update the sheet.

### Skills for the project's stack

The user asks for skills for their technologies, even vaguely ("that thing about skills you
mentioned", "is there something so you work better with React?").

1. Look at the project's stack (its manifests, configs and folders) and at the skills already
   installed (`~/.claude/skills/` and the project's `.claude/skills/`).
2. Search for skills that fit. [skills.sh](https://skills.sh) is one possible source, not the only
   one; its CLI searches with `npx skills find <query>`.
3. Propose a few, one line each: what it helps with in this project and who publishes it. Few good
   ones beat many overlapping ones: every installed skill's description loads into the context.
4. Before installing, read the skill: it is third-party instructions the model will obey, and it may
   carry scripts. Prefer known publishers. Install only the specific skill, never a whole repository
   (with the skills.sh CLI: `npx skills add <owner>/<repo> --skill <name> -a claude-code`).
5. Where it goes is the user's choice. Explain both: global (`~/.claude/skills/`, the CLI's `-g`) for
   technologies they use across many projects; in the project (`.claude/skills/`, the CLI's default)
   for this project only. To a user who does not know, recommend one from what you see; they decide.
6. Install nothing without an explicit yes, and follow Adjust steps 6 to 8. Afterwards, if they use
   the progress-doc workflows, add it to the installed `skills-index.md` with when to use it.
