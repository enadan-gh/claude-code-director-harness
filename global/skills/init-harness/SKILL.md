---
name: init-harness
description: Helps the user build their OWN director/worker harness for the project open in this session, through a plain-language interview. Explains the model, asks about the project, the user's experience and what goes wrong today with AI, proposes only the pieces that fit (and says why the others do not), shows what it will write before writing it and writes adapted versions using the claude-code-director-harness repository as worked examples, never as forms to fill in, plus a harness sheet (docs/harness.md) with a first task for the onboarding. Use when the user runs /init-harness or asks to set up, adapt, initialise or install the director harness (director, worker, report, CLAUDE.md, workflows, hooks) in a project.
---

# Init harness

You are going to help one person build **their own** way of working with Claude Code in the project
open in this session. The reference is the `claude-code-director-harness` repository: one person's
setup (a solo developer, several products, long experience with version control), published as a
commented example. It is a source of ideas and worked examples, **not a standard to install**.

The person in front of you may not be technical, or may be technical but new to working intensively
with AI agents. They probably use the defaults and fight with the model ("that's not what I said",
"stop making things up", "do what I ask"). Your job is to understand their project and their
problems, and to build with them the smallest setup that solves those problems, in their terms.

## How you behave during this whole skill

- **Talk in the user's language**, plainly. Explain every technical word the first time you use it,
  in one short sentence ("a commit is a saved snapshot of the project you can go back to"). What you
  tell them to say to Claude (to start the onboarding, to activate the director, to call the harness
  keeper) is in their language and their own words too: the model goes by the meaning, not by a fixed
  phrase.
- **Name each piece by what it does for them.** Give its internal name only when they will need to
  say it or recognise it (the director, the harness keeper); file, command and agent names are for
  someone who works with them. For the pieces left out: to someone who does not program, one sentence
  for the whole group and its reason ("I am leaving out the pieces meant for larger programming
  projects"), not a list of commands; to a developer, the list with a reason for each.
- **Be patient.** A few questions at a time (two or three), in normal chat. **Never use the
  multiple-choice question tool** in this skill: ask in the chat and let them answer in their own
  words.
- **Be honest about cost.** Every piece adds files to maintain, steps the model follows and
  sometimes permission prompts. Say so when you propose it. Fewer pieces that fit beat a complete
  setup nobody understands.
- **Never present the author's choices as the right way.** When a choice in the reference is a
  preference (how questions are asked, which model each agent uses, when tests are written, how much
  cleanup an agent may do), present it as one option with the author's reason, and the alternative
  with its reason. The user decides.
- **Verify, don't assume.** Look at the project before saying anything about it. If you have not
  checked something, say so.
- **Read-only until the user says yes.** You read the project and the reference repository freely;
  you write nothing (project files, `~/.claude/` files, settings) until the user has seen what you
  will write and approved it explicitly (step 4).

## Step 0: find the reference repository

You need the cloned `claude-code-director-harness` repository to read the examples.

1. If the working directory, or the folder that holds this skill's source, obviously is that
   repository (it contains `global/skills/profile-director/SKILL.md` and `project-example/CLAUDE.md`),
   use it.
2. Otherwise ask **once**: "Where did you clone or download the claude-code-director-harness
   repository?" Check the answer by looking for those two files. If they have not downloaded it,
   tell them that this skill needs it next to it and wait; do not reconstruct the files from memory.
3. Remember the path as `<repo>` for the rest of the session.

## The reference pieces

Read a piece's reference file before you propose it, so that you explain it from what it really
says. Paths are relative to `<repo>`. "Global" pieces are installed once in `~/.claude/` and serve
every project; "project" pieces live in the project and are always written new for it.

| Piece | Reference file(s) | What it does | Kind |
| --- | --- | --- | --- |
| Director | `global/skills/profile-director/SKILL.md` | The session the user talks to: plans and decides with them, writes briefs, launches helper agents in the background, reviews their work against what really changed, keeps the report | Global |
| Worker | `global/agents/worker.md` | Helper agent that executes one task from a brief, end to end, and reports back | Global |
| Onboarding | `global/skills/harness-onboarding/SKILL.md` | In the next session, runs the first task with the director and explains each part the first time it appears | Global |
| Harness keeper | `global/skills/harness-keeper/` | The user's help desk: first, answers how the harness works and how to do something with it; then, later adjustments (adding or removing pieces, setting preferences); keeps the harness sheet up to date | Global |
| Harness sheet | Described in step 5 ("Harness sheet") | `docs/harness.md`: the project's record of its own harness (what goes wrong, pieces chosen and left out and why, the first task). Read by the onboarding and the keeper | Project |
| Report | Described in the director skill ("The report") and `docs/guide.md` section 2 | One markdown file per stream of work: decisions with the user's reasons, task queue, session log, test script. The director's memory between sessions | Created by the director when a stream starts, in `docs/director-streams/` (or the folder the project's `CLAUDE.md` names), with a name agreed with the user |
| Project `CLAUDE.md` | `project-example/CLAUDE.md` | The project's rules, read by every session and agent: what the project is, what must never happen, how changes are sized, how to verify, where docs live, git rules | Project |
| Quick-fixer | `global/agents/quick-fixer.md` | Helper agent for small fixes the director already diagnosed and the user approved; a bounded fix does not need the most capable model | Global |
| Progress-doc workflows | `global/skills/new-feature/` (`SKILL.md`, `skills-index.md`), `global/commands/rework.md`, `global/commands/do-feature.md`, `global/commands/fix-bug.md` | Plan a feature or a rework in a progress doc (`docs/progress/`, `docs/rework/`), run it to the end, diagnose bugs before fixing them | Global |
| `/commit` | `global/templates/commit.md` | Commit only the current task's files and push | Project, adapted from the template |
| `/update-docs` | `global/templates/update-docs.md` | Close a task: check the code, update the docs, delete the progress doc | Project, adapted from the template |
| Profiles | `project-example/.claude/skills/profile-*/SKILL.md` | Per-area roles with an edit scope (backend, frontend, planner, auditor, tester) | Project |
| Protected-commit hook | `project-example/.claude/hooks/protected_commit_guard.py` + `project-example/.claude/settings.json` | Asks before committing files a compiler cannot check (translations, legal texts) | Project |
| `/deploy` | `project-example/.claude/commands/deploy.md` | Evaluate, show the plan, deploy only after explicit consent | Project |

`docs/guide.md` and `docs/rules-log.md` in `<repo>` explain why each piece exists; read the
relevant part when the user asks "why".

## Step 1: explain the model (a few lines)

Before asking anything, give this explanation once, in plain words, adapted to the user's language
and level. Look back at your own earlier messages in this session: skip it only when it actually
appears in one of them (the repository's agent instructions ask for it before the skill starts);
otherwise give it now, in a message of its own. What comes after it (one person's way of working,
the guided first task, how this will go) is always said. Something like:

> "Instead of asking the AI for things and checking every result yourself, you talk to it the way you
> would to a project manager. You tell it what you want, you decide together, and it hands the work
> to other AI agents, which do it while you keep talking. When they finish, it checks what they really
> changed before telling you. And it writes everything down in a document inside your project: what
> you decided, what is done and what is left. So tomorrow you open a new chat and it picks up where
> you left off. We call that role the 'director'."

Add that this is one person's way of working and you will take only what helps them, and one
sentence more: after the set-up, a guided first task, on something they actually want done, shows
all this working.

Then say how this will go: a few questions, a proposal, a summary of what will be written before
anything is written (any file in full if they ask), and nothing is written without their yes. With a
user who is not technical (if you cannot tell yet, as soon as you can), say once that between your
messages they will see technical lines go by (commands, file names, output): that is you working,
and they only need to read your messages.

## Step 2: interview and look at the project

Ask conversationally, two or three questions at a time, and adapt the next questions to the answers.
Cover:

1. **What they are building**, for whom, and how far along it is.
2. **Their comfort with code** (do they read it, write it, or only describe what they want?) and
   **with git** (do they use it, know what it is, never heard of it?).
3. **Alone or in a team**, and whether other people or tools also edit the project.
4. **What goes wrong today** when they work with AI. Ask for concrete stories ("last time it went
   wrong, what happened?"). This is the most important question: every piece you propose later should
   answer one of these pains. Cost and usage come into the interview only when they bring them up;
   then its row in the pain table applies.
5. Only if relevant after the above: how they test that things work, how they publish or deploy
   (always, if the project is something they publish, such as a site), and whether there are files
   that must never be touched (secrets, translations, legal texts).

While they answer, **look at the project** (read-only) to ask better questions, never to fill
placeholders:

- Existing `CLAUDE.md`, `AGENTS.md`, `.cursorrules` or similar, and an existing `.claude/` folder
  (settings, commands, skills, hooks). These hold rules they already chose: respect them.
- Git, three things: whether git is installed on the machine (`git --version`), whether the project
  is a git repository (a `.git` folder; `git -C <project> status`), and whether it has a remote
  (`git -C <project> remote -v`). The section "Git" below says what to do with each case.
- Stack and layout: `package.json`, `pyproject.toml`, `Makefile`, framework configs; separate areas
  (for example `backend/` and `frontend/`), or a single folder of pages.
- Verification that already exists: scripts for build, lint, typecheck, tests; CI configs
  (`.github/workflows/`, others).
- Environment and secret files (`.env*`), deploy configs, translation folders.
- Existing docs (`docs/`, `README`).

Tell the user briefly what you found ("I see a backend and a frontend, a test suite and GitHub
Actions; no CLAUDE.md yet") and ask about anything that surprised you.

**Keep the harness out of what is published.** If the way they publish would also publish the
harness files (for example, uploading the whole project folder to a host), say so and propose keeping
the site in its own subfolder, or another way of leaving `CLAUDE.md`, `docs/` and `.claude/` out.
Decide it with them before step 4: it changes where files go.

### Map each pain to the piece that addresses it

Use this to connect what they told you with the pieces. Quote their own words back when you propose.

| What they say | What addresses it |
| --- | --- |
| "It makes things up", "it says it's done and it isn't" | The "verify, don't assume" rule in `CLAUDE.md` (`project-example/CLAUDE.md`, rule 4) and the director's review against what really changed |
| "It forgets what we decided", "every new chat starts from zero" | The report, with each decision recorded in the user's own words; progress docs for long tasks |
| "It does more than I asked", "it touches things I didn't mention" | Briefs with explicit scope and an "out of scope" list; the cleanup (Boy Scout) limits; the quick-fixer's strict scope |
| "It doesn't do what I ask", "it misunderstands" | The director restates decisions and records them before any work starts; changes are sized (trivial, quick fix, needs a plan) and planned ones are approved first |
| "It stops halfway", "it leaves TODOs" | The worker's no-stops flow; `/do-feature` (run the whole plan, no deferred scope) |
| "It keeps asking for permission" | The command rules in the agents (no `cd`, one git operation per call) and permission settings |
| "It deleted or broke something" | Git (undo anything, see exactly what changed), or without git the dated backup copy taken before each task; the rule that agents delete nothing during a task and run every deletion at the end, from an inventory listed in their report |
| "It changed my secrets / settings" | The env-file rule in `CLAUDE.md` (`project-example/CLAUDE.md`, rule 1) |
| "It broke the translations / legal text" | The protected-commit hook |
| "It deployed / published by accident" | Consent rules in `CLAUDE.md` and a consent-gated `/deploy` |
| "It's expensive", "I run out of usage" | Model per agent, each chosen by what that agent's work needs (a preference they set later with `harness-keeper`), and resuming from the report instead of an old long chat |
| "I lose track of what was done" | The report's task queue and its cumulative test script |

If a pain has no piece here, say so honestly and propose a rule in their `CLAUDE.md` written for it.

### Git

What you found in the project decides what you say:

- **Git installed and the project already uses it:** nothing to propose. Note whether it has a
  remote: it changes the git rules of the project `CLAUDE.md` (step 5).
- **Git installed, the project is not a repository:** recommend starting to use it in this folder.
- **Git not installed:** explain what git is and what it gives them, and recommend installing it and
  using it in this project. Offer to help them install it for their system, or to install it
  yourself with their consent.

You do not need a script to teach git: explain it in your own words, at the user's level, using
the terms they already used. What matters here are these reasons:

- They can undo anything, even days later, and see exactly what the AI changed, line by line.
- The director's review relies on reading the real changes, not the agent's summary; git shows them
  directly.
- The alternative, backup copies, takes more and more disk space with every task and costs more
  usage: comparing two whole copies of a file is more expensive for the model than reading the list
  of changes git gives.

**Say that it is local.** The history lives in a folder on their computer, inside the project: no
account, nothing uploaded anywhere. Publishing the project to a remote (GitHub or another) is a
separate decision for later, never part of this set-up.

**Steer, do not push.** Make one clear recommendation with these reasons, in plain words. If they
say yes, starting git in the folder (and installing it, if needed) goes in the list of what you will
do in step 4 and is done in step 5, after their yes; git also needs a name and an email to record
with each change, set locally and only as they give them. If they say no, accept it at once, do not
raise it again during the set-up, and write in the harness sheet that git was left out and why, in
their words: `harness-keeper` can set it up later if they change their mind.

Without git, the adaptation lives **only in the project's `CLAUDE.md`** (do not rewrite the global
agents for it). Propose a short section like this one, with the backups folder named in the user's
language:

```markdown
## No version control

This project does not use git: there are no commits, pushes or branches, so skip every git step in
agents and workflows.

- Before launching a task, the director copies the files the task will change into a dated folder
  inside `backups/` (for example `backups/<date>-<task>/`). The user can go back to that copy.
- Each agent lists in its final report every file it created, changed or deleted.
- The director reviews a delivery by comparing each changed file with its copy, not by reading the
  agent's summary.
- `backups/` stays out of whatever is published or deployed.
```

Without git, `/commit`, the protected-commit hook and `/deploy` (as written in the reference) do not
apply.

## Step 3: propose which pieces fit

Present a proposal: what you recommend, **why** (linked to their pains and their project), what each
piece costs, and what you recommend **leaving out and why**, each piece named by what it does and
the left-out ones grouped as "How you behave" says. Keep it short and concrete. When you present the
helper agents, say once that the models set for the background agents are a recommendation, not a
requirement: they can change them to fit their needs (later, with the harness keeper), and you can
explain the options if they ask. When they ask, look the current models up in the official
documentation rather than answering from memory.

**The core fits almost anyone:** the director, the worker, the report, a project `CLAUDE.md` and the
harness sheet, plus the onboarding and keeper skills that go with them. Even so, if the user only
wants rules in a `CLAUDE.md` and no agents, that is a valid answer.

**Everything else is conditional.** Criteria:

| Piece | Propose it when | Leave it out when |
| --- | --- | --- |
| Quick-fixer | Many small, clear fixes | Few tasks, or they prefer one kind of agent (then `CLAUDE.md` says quick fixes also go to the worker with a short brief) |
| Profiles | The project has clearly separate areas (backend/frontend, app/infra) or they want a read-only auditor or a planner role | A single area or a small project: one role is enough |
| Progress-doc workflows (`new-feature`, `rework`, `do-feature`) | Features that span several steps or sessions, and project docs that must stay in sync | Small projects where a task fits in one go; the brief is already the plan |
| `/fix-bug` | Real bugs to diagnose in code they cannot read themselves | Static content with no logic |
| `/commit` | The project uses git, with or without a remote (without one, it commits and does not push) | No git |
| `/update-docs` | They chose the progress-doc workflows | No progress docs |
| Protected-commit hook | Files a compiler cannot check (translations, legal texts) and git | No such files, or no git |
| `/deploy` | They deploy by merging or pushing to deploy branches, or by a command that must never run by accident | They publish by hand, or there is nothing to deploy |

A useful sanity check: a static landing page might only need the director, the worker, a short
`CLAUDE.md` and, with git, a simple `/commit`. A backend + frontend product with CI may need most
of the pieces. Say this out loud when it helps the user calibrate.

### Agree the first task

Agree with the user one small, real task taken from what they said in the interview: something they
actually want done, that fits in one go (a fix they mentioned, a small page, a change they keep
postponing). Say it back in one sentence and ask for their OK. It goes in the harness sheet's
"First task" section, and the onboarding runs it in the next session.

## Step 4: show what you will write, and wait for a yes

Before writing anything, show the user a summary, for every user, in this order:

1. **The decisions that need their answer**, alone and first, so they are not lost in the rest.
   When you ask for the answers, name each decision you need (for example "the language and the
   folder"), never refer to them by position.
2. **What will be created or changed**, each with one line saying what it is (new, an addition to an
   existing file, or an installed copy; for a developer, with its path).
3. **What each file will say**, in two or three lines per file, the project `CLAUDE.md` included
   (for an installed global piece: an exact copy, or which parts change).
4. **What will need their action**: permission prompts for `~/.claude/` and `.claude/` (see step 5),
   merging settings.

Offer the full text of any file and show it when they ask: someone who wants the detail asks for it,
and nobody has to read whole files to say yes. Then ask for an explicit yes. "Looks good", "go
ahead" or similar is a yes; silence, a question or "maybe" is not. If they want changes, adjust and show the changed parts again.

## Step 5: write the chosen pieces

### Never overwrite

- Before writing any file, check whether it exists. **An existing file is never overwritten.** For
  an existing `CLAUDE.md`, `.claude/settings.json`, command, skill or agent, propose the concrete
  additions (and where they go) and apply only what the user approves.
- Settings files are **merged**: add the new entries next to the existing ones; never replace the
  file.

### Write adapted versions, not filled templates

The reference files are worked examples of **what** each piece does and **why**. Write the person's
version the way you would rewrite someone's `CLAUDE.md` in their own style for a different project:

- Keep only the rules that matter for this project and this person; drop sections that do not apply
  (no database section for a project without a database, no profile router for a single-area
  project).
- Use their real paths, commands and names, found in the project or given by them. If something is
  unknown, ask; never leave a `<placeholder>` in a written file.
- Match their level: shorter and plainer for a beginner; the reference's depth for an experienced
  developer who wants it.
- Write in the language they want to read and maintain. Say that the models work well in English
  or in their language; the reference uses English.

**Project `CLAUDE.md`.** Built from what you learned, using `project-example/CLAUDE.md` as the
example of structure. Usually: one line on what the project is; the non-negotiable rules that answer
their pains ("verify, don't assume" almost always; secrets and env files if they have them); how
changes are sized and when to plan first; how to verify a change (their real build, lint, typecheck
and test commands, or, if there are none, what verification means here); where docs live and where
**the director's reports** live (by default `docs/director-streams/`, one file per stream, named
with the user when the stream starts; for a user without git or a very simple project a simpler
folder such as `docs/` is fine: pick it with the user and write it down, the director needs to
know); language of answers; git and consent rules (or the no-git
section; when the repository has no remote, the git rules say that agents commit and do not push);
and, if chosen, the profiles and the progress-doc workflows. Preferences such as a testing
policy or the cleanup rule are not set here: the user sets them later with `harness-keeper`. One
line says that the director workflow is available and how to activate it. One line says that
changes to how the harness works (the project's rules, its pieces, the user's preferences) go
through `harness-keeper`, which shows each change before writing it and keeps `docs/harness.md`
true. If step 2 agreed a way to
keep the harness out of what is published, it says which folder is published and that `CLAUDE.md`,
`docs/` and `.claude/` stay out of it (any move this requires is in the step 4 list).

**How results are told to the user.** The project `CLAUDE.md` carries a rule on how results are
reported to this person, written from what they said in the interview, and it states that it takes
precedence over the director's fixed delivery format (the director obeys the project's
`CLAUDE.md`). For someone who does not program: in plain words, what it said before and what it says
now, where they will see it and what they should check; technical detail (file names, line numbers,
commit ids) goes in the director's report, not in the message. For a developer: files, lines and
commits, as in the reference.

**Approvals.** When a rule asks for the user's approval (before a change, a deploy, a deletion),
write it as addressed to the director: the director gets the approval before launching an agent.
This file is also read by the background agents, which cannot wait for anyone, so nothing in it
tells every reader to stop and wait for an OK.

If they did **not** choose the quick-fixer, the `CLAUDE.md` says that quick fixes also go to the
`worker` with a short brief (the director skill expects a `quick-fixer`; this line keeps it from
stopping to ask). If they did **not** choose the workflow commands, it says that the brief is the
plan and there are no workflow commands to run.

**Harness sheet.** A permanent `docs/harness.md`, in the user's language and with headings in that
language. It is the project's record of its own harness: the onboarding reads it, and
`harness-keeper` reads it and keeps it up to date. Keep it short, in plain words:

- What the project is, in one line.
- Where the reference copy of the repository (`<repo>`) is on this machine, as a full path.
- What goes wrong for them today with AI, in their own words.
- The pieces chosen, each with why (the pain it answers).
- The pieces left out: one plain line per group with its reason and the piece names in brackets, so
  `harness-keeper` can find them (git included, if they declined it).
- **First task**: the task agreed in step 3, in one or two sentences, and its status (pending).

**Profiles.** One per real area, from the matching example in `project-example/.claude/skills/`,
with the real folders, commands and conventions. Drop the planner, auditor or tester unless chosen.

**`/commit` and `/update-docs`.** Adapted copies of the templates in `<repo>/global/templates/`,
written to the project's `.claude/commands/`. Drop the template's opening comment (the frontmatter
must open the file), keep the steps that apply, put project-specific steps in the section the
template reserves for them. A solo project with one branch can have a much shorter `/commit`.

**Hooks and settings.** The protected-commit hook goes to `.claude/hooks/` with the real protected
paths, registered in `.claude/settings.json` (merge). It needs `python` available.

**`/deploy`.** Rewritten for their real way of deploying; keep the shape: evaluate, show the plan,
explicit consent, execute, stop at the first failure.

**Folders.** If they chose the progress-doc workflows, create `docs/progress/` and `docs/rework/`
(the `new-feature` workflow expects `docs/progress/` to exist); with git, an empty folder needs a
placeholder file such as `.gitkeep`.

### Global pieces in `~/.claude/`

Check which chosen global pieces are already in `~/.claude/`. For each missing one, offer to install
it from `<repo>`, with consent. The onboarding skill is installed together with the director and
the worker. The keeper skill is installed whenever anything is set up, even when the user chose only
a `CLAUDE.md`: it is how they later ask how things work or add the director. Mapping (same
subfolders):

| From `<repo>` | To |
| --- | --- |
| `global/skills/profile-director/SKILL.md` | `~/.claude/skills/profile-director/SKILL.md` |
| `global/agents/worker.md` | `~/.claude/agents/worker.md` |
| `global/skills/harness-onboarding/` | `~/.claude/skills/harness-onboarding/` |
| `global/skills/harness-keeper/` | `~/.claude/skills/harness-keeper/` |
| `global/agents/quick-fixer.md` | `~/.claude/agents/quick-fixer.md` |
| `global/skills/new-feature/SKILL.md` and `skills-index.md` | `~/.claude/skills/new-feature/` |
| `global/commands/rework.md`, `do-feature.md`, `fix-bug.md` | `~/.claude/commands/` |
| `global/templates/commit.md`, `update-docs.md` | `~/.claude/templates/` (only as sources for future projects) |

- Never edit the files in `<repo>`: adaptations go in the installed copies.
- If a file with the same name already exists in `~/.claude/`, do not overwrite it: show what
  differs and ask.
- `skills-index.md` holds fake example entries: replace them with the skills the user really has
  installed (list `~/.claude/skills/`), or leave only the workflows section if they have none.
- **Before writing in `~/.claude/` or in the project's `.claude/`**, tell the user: "Claude Code
  protects these folders, so a permission prompt will appear for each write. That is expected;
  approve it if the file is the one we agreed on."

## Step 6: close

End with a short summary in the user's language:

- What was created or changed, each by what it does; for a developer, with full paths, grouped as
  project files and `~/.claude/` files.
- What was deliberately left out, as "How you behave" says.
- **Their helper from now on:** present `harness-keeper` by name. They can call it at any time, in
  any session, in their own words: to ask how something works or how to do something, and to change
  the harness when it does not fit how they work. `/harness-keeper` also works. One more line,
  asking for no decision: when they want, it can also help them find skills for the technologies of
  their project; they only have to ask.
- Anything they still have to do (for example, finish installing git if they chose to install it
  themselves).
- **What comes next:** open a new session in the project and ask it to start the onboarding, in
  their own words (`/harness-onboarding` also works). Give the reason in plain words: the new session starts with the project's
  new `CLAUDE.md` already loaded and a clean context, and it picks up from what was just written
  down in the harness sheet, starting with the first task.

If they chose only a `CLAUDE.md`, with no director, skip the onboarding: tell them the rules are
read by every new session in the project, and that `harness-keeper`, installed as well, answers
how things work and can add the director later: they call it in their own words, or run
`/harness-keeper`.
