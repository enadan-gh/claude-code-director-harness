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
  in one short sentence.
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

In two or three plain sentences, for example: "We are going to do a real task now: <the first task>.
It will be done exactly the way every task will be done from now on. The first time each part
appears, I will explain it in a sentence or two."

## Step 3: run the first task as the director

Invoke the `profile-director` skill and follow it from then on, with all its rules in force. The
work is the first task from the sheet: start it as new work, so the director proposes a name for the
stream and creates its report. Confirm the task with the user first; if they no longer want it,
agree another small, real one.

## Step 4: explain each thing the first time it happens

The first time each of these happens, add one or two plain sentences and show it. Only the first
time; after that the director works as usual.

| When | What to explain and show |
| --- | --- |
| The stream gets its name and its report | The report is the director's memory: decisions, tasks and what was done. Give its full path and invite them to open it |
| A decision is recorded | Their decision is written in the report in their own words, with their reason, so nobody reopens it later. Point to the line |
| The director asks for their OK before launching | Nothing starts until they say yes; this is where they stay in control |
| A helper agent is launched | It works in the background; they can keep talking to the director meanwhile, and ask anything |
| The director reviews the delivery | It checks what really changed (with git, the real changes; without git, by reading the files), not what the helper says it did |
| The director gives the result | One message, after the review, with the verified result; they do not get the same news twice |
| The report is updated at the end | Show the closed task in the report: that is what a new session will read tomorrow |

## Step 5: close

When the task is closed, tell the user in a short message:

- **How to resume tomorrow:** open a new session in the project, say "activate the director profile"
  and say what they are working on; the director finds the report and picks up where they left off.
- **What was left out at set-up**, from the sheet, in one line each, so they know it exists.
- **How to get help or change the harness:** when they do not know how to do something, or
  something does not fit how they work, they say "adjust the harness" (or `/harness-keeper`), and it
  explains it or helps them change it.

Then mark the first task as done in the sheet's first-task section (one line, in the sheet's
language). It is the director's own housekeeping, like the report: commit it with an explicit path,
with the report or on its own, when no agent is running, following the project's git rules (without
git, just save it).
