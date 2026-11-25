---
name: harness-onboarding
description: Walks the user through their first real task with the director harness that init-harness just set up in this project. Reads the project's harness sheet (docs/harness.md) and CLAUDE.md, activates the director profile and runs the agreed first task with the director's normal flow, explaining each part in plain words the first time it appears. Use when the user runs /harness-onboarding or says "start the onboarding", "harness onboarding" or similar, usually in the first session after init-harness.
---

# Harness onboarding

The user has just set up their harness with `init-harness` and opened a new session in the project.
Your job is to do one small, real task with them, the way every task will be done from now on, and
to explain each part the first time it appears. They learn by watching it work, not by reading.

## How you behave

- **Talk in the user's language**, plainly. Explain every technical word the first time you use it,
  in one short sentence. What you tell them to say to Claude (to start the onboarding, to activate
  the director, to call the harness keeper) is in their language and their own words too: the model
  goes by the meaning, not by a fixed phrase.
- **One name per piece.** Introduce each piece with its description the first time, then always
  call it by the same name for the rest of the conversation; never use one name for two pieces.
- **Ask in the chat**, two or three questions at most, and let them answer in their own words. Never
  use the multiple-choice question tool.
- **Never present the author's choices as the right way.** If they ask why something works the way it
  does, give the reason and say that it can be changed (see the close).
- **Explanations are additions.** They never replace, skip or delay a step of the director, and they
  never break its rules (in particular "one message per delivery": an explanation goes inside a
  message the director would write anyway, never in a message of its own).

## Step 1: read what was set up

Read `docs/harness.md` (the harness sheet) and the project's `CLAUDE.md` whole. The sheet's headings
are in the user's language; find its sections by meaning: what the project is, what goes wrong
today, the pieces chosen and left out, and the first task.

If there is no sheet, say in one sentence that `init-harness` creates it when it sets up the
harness, and offer to agree a first task right now instead: something small and real they want
done, that fits in one go.

## Step 2: say what is about to happen

Two or three plain sentences, for example: "We are going to do a real task now: <the first task>,
the way every task will be done from now on, and I will explain each part as it happens." With a
user who is not technical, add once that between your messages they will see technical lines go by
(commands, file names, output): that is you working, and they only need to read your messages.

## Step 3: run the first task as the director

Invoke the `profile-director` skill and follow it from then on, with all its rules in force. The
work is the first task from the sheet: start it as new work, so the director proposes a name for the
stream and creates its report. Confirm the task with the user first; if they no longer want it,
agree another small, real one.

## Step 4: explain each thing the first time it happens

The first time each of these happens, add one or two plain sentences and show it. Each explanation
is given once, at that moment: not announced beforehand and not recapped at the end. After that the
director works as usual.

| When | What to explain and show |
| --- | --- |
| The stream gets its name and its report | The report is the director's memory: decisions, tasks and what was done. Give its full path and invite them to open it |
| A decision is recorded | Their decision is written in the report in their own words, with their reason, so nobody reopens it later. Point to the line |
| The director asks for their OK before launching | Nothing starts until they say yes; this is where they stay in control |
| A worker is launched | The agent that carries out the task from the director's brief; it works in the background; they can keep talking to the director meanwhile, and ask anything |
| The director reviews the delivery | It checks what really changed (with git, the real changes; without git, by reading the files), not what the worker says it did |
| The director gives the result | One message, after the review, with the verified result; they do not get the same news twice |
| The report is updated at the end | Show the closed task in the report: that is what a new session will read tomorrow |

## Step 5: close

When the task is closed, tell the user in a few lines, without repeating what was already explained:

- **How to resume tomorrow:** open a new session in the project, ask it to activate the director
  profile and say what they are working on; the director finds the report and picks up where they
  left off.
- **What was left out at set-up**, from the sheet, so they know it exists: to someone who does not
  program, one sentence for the whole group and its reason, not a list of commands; to a developer,
  the groups with their reasons.
- **How to get help or change the harness:** when they do not know how to do something, or something
  does not fit how they work, they call the harness keeper, in their own words (or
  `/harness-keeper`), and it explains it or helps them change it.

Then mark the first task as done in the sheet's first-task section (one line, in the sheet's
language). It is the director's own housekeeping, like the report: commit it with an explicit path,
with the report or on its own, when no agent is running, following the project's git rules (without
git, just save it).
