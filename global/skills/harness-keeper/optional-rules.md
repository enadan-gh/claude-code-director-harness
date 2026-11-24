# Optional rules catalog

Read by the `harness-keeper` skill when the user's story touches an entry or they ask what can be
tuned. Each entry is a **preference**, not a
requirement of the director/worker model. Present both sides to the user, with the author's reason
as one option among others, and apply only what they choose.

Every entry has the same parts: what it does · why someone would want it · why someone would not ·
the text ready to insert and where it goes. "Installed copies" means the files in `~/.claude/`,
never the files in the reference repository.

---

## (a) Questions in the chat instead of the multiple-choice question tool

**What it does.** Claude Code has a tool that asks the user a question with predefined options to
click. This rule makes sessions and agents ask in plain chat instead, once they have finished their
work or stopped at a real blocker.

**Why someone would want it (the author's reason).** The tool blocks the session until you answer,
the question arrives in the middle of the work, and if you are away the execution time is lost. The
author prefers the work to finish (or stop at a real blocker) and then read the questions in the
chat.

**Why someone would not.** If you are usually in front of the screen, or you like answering with one
click, the tool is quicker and clearer. Beginners often find the options easier than writing an
answer. Without this rule, Claude Code's default behaviour stays: nothing to insert.

**Text to insert.**

```markdown
## Questions

Ask me questions in plain chat, never with the multiple-choice question tool. Do not interrupt the
work to ask: finish what you can (or stop at a real blocker) and then ask everything you need in one
message, with the options and your recommendation written out.
```

**Where it goes.** In `~/.claude/CLAUDE.md` (the user's personal instructions, read in every project)
if it is a personal preference; in the project's `CLAUDE.md` if it should apply only to this project.
If either file exists, add the section; never replace the file.

---

## (b) Model per agent

**What it does.** Each agent definition can set the model (and effort) it runs on, in its
frontmatter. The reference sets `model: opus` and `effort: medium` for the worker, and
`model: sonnet` and `effort: high` for the quick-fixer, both marked as suggestions.

**Why someone would want it (the author's reason).** Each agent gets the model its work needs to be
done well. A bounded, already diagnosed fix does not need the most capable model, so the quick-fixer
runs on a less capable one; the worker, which plans and implements whole tasks, gets a more capable
one.

**The director's model.** The director is the session itself, not an agent file: the user chooses
its model with `/model` (and its effort with the slider there, or `/effort`) before activating the
profile. The recommendation, never imposed: the most capable model they have, with high effort. The
director understands the problem, decides with the user, writes the briefs and reviews against the
real diff, so a mistake there spreads through every worker; the workers receive the reasoning
already done in the brief, so a less capable model holds up there. A skill's `model` frontmatter
field only lasts for the turn that invokes it, so it cannot fix the director's model for the session.

**Why someone would not.** If you already pick the model per session and want every agent to follow
it, or your plan has no access to a given model, fixed values get in the way. Inheriting is the
simplest choice.

**Options and text.** Edit the frontmatter of the installed copies:

- **Keep the suggestions** (`~/.claude/agents/worker.md` with `model: opus`,
  `~/.claude/agents/quick-fixer.md` with `model: sonnet`): nothing to change.
- **Inherit the session's model**: in each installed agent, replace the `model:` line with
  `model: inherit`, or delete the `model:` and `effort:` lines.
- **Other aliases**: `opus`, `sonnet` or `haiku`, one per agent, as the user chooses. Keep the
  trailing `# suggestion` comment or drop it.

**Where it goes.** The frontmatter of `~/.claude/agents/worker.md` and
`~/.claude/agents/quick-fixer.md` (and of the optional agents in entry c, if installed).

---

## (c) The optional Explore and web-fetch agents

**What it does.** Two extra agent files, only to choose the model that fits two common jobs:

- `optional/agents/Explore.md` **overrides** Claude Code's built-in Explore agent (the read-only
  search agent) only to set its model and effort; a user agent named `Explore` replaces the built-in
  one.
- `optional/agents/web-fetch.md` is an **additional** agent (not an override) that reads public web
  pages and answers a question about them, on a model chosen for that job.

**Why someone would want it (the author's reason).** Broad code searches and reading web pages are
done well without the most capable model, so each runs on the model that fits the job.

**Why someone would not.** If the defaults are fine for you, you need neither. Overriding a built-in
agent also means your copy does not follow future changes to the built-in one.

**Text to insert.** No new text: copy the files from the reference repository, then apply entry (b)
to their `model:` and `effort:` lines if the user wants different values.

**Where it goes.** `~/.claude/agents/Explore.md` and `~/.claude/agents/web-fetch.md`. If a file with
that name exists, do not overwrite it.

---

## (d) Testing policy

**What it does.** Decides when tests are written. The global workflows (`new-feature`, `rework`,
`do-feature`) follow whatever the project's `CLAUDE.md` says; if it says nothing, they plan tests
inside each phase. `/fix-bug` always ships its regression test with the fix, if the project has a
test suite.

**Why someone would want a final manual phase (the author's reason).** While a feature is still
being iterated, tests get rewritten again and again for no value. The author validates the feature
first (use case and usability) and only then launches a dedicated testing phase, owned by a tester
profile.

**Why someone would want tests inside each phase.** Each phase is proven before the next starts, so a
mistake is caught where it happens. Many people prefer this, and it is the workflows' default.

**When neither applies.** A project with no test suite (a static site, for instance): skip this entry
and write nothing about tests beyond how a change is verified.

**Text to insert, option 1 (final manual phase).**

```markdown
## Testing

Tests are not written during implementation. A plan (`/new-feature` or `/rework`) ends with one
dedicated testing phase, assigned to `profile-tester` and marked **manual**: I launch it only after
I have validated the feature. Implementation phases close when the build, typecheck and lint are
clean and the existing test suite is still green. Only exception: `/fix-bug`, whose regression test
(fails before the fix, passes after) ships with the fix.
```

This option needs a tester profile (adapted from
`project-example/.claude/skills/profile-tester/SKILL.md`); propose it together.

**Text to insert, option 2 (tests inside each phase).**

```markdown
## Testing

Each implementation phase writes the tests for the code it adds or changes, and a phase is complete
only when its tests pass and the existing suite is still green. `/fix-bug` ships its regression test
(fails before the fix, passes after) with the fix.
```

**Where it goes.** The project's `CLAUDE.md`, with the real test commands next to it.

---

## (e) Cleanup rule (Boy Scout)

**What it does.** "Leave the code cleaner than you found it": decides whether, and where, an agent
may fix problems it sees that are not part of its task.

**Why someone would want the author's version.** The installed agents already carry it: the worker
cleans up only inside the files it already touches for its task, and the quick-fixer does no cleanup
at all. Anything they see outside goes into their report with `file:line`, and the director brings it
to the user as a decision. The author's reason: the agent's changes stay on its task, which is what
the director reviews, and problems found elsewhere reach the user as decisions instead of changes
nobody asked for. If you want broader cleanup, give it its own task.

**Why someone would want a different rule.** A beginner may prefer **no cleanup at all** (only what
was asked, nothing else), which makes every change easier to follow. An experienced developer may
want **broader cleanup** in the area of the task, accepting bigger changes to review.

**Text to insert, option 1 (the author's version).** Nothing to change in the installed agents. If
the project's `CLAUDE.md` has a general "leave it cleaner" rule, add next to it:

```markdown
**Exception for agents launched by the director.** The `worker` cleans up only inside the files it
already touches for its task; the `quick-fixer` does no cleanup at all. Anything either of them sees
outside goes in its report with `file:line`, and the director brings it to me as a decision.
```

**Text to insert, option 2 (no cleanup at all).** In the installed `~/.claude/agents/worker.md`,
replace the sentence that starts with "**Boy Scout only inside your own files**" (up to "with
`file:line`.") with:

```markdown
**No cleanup outside the task**: change only what the brief asks for, even inside the files you
touch; anything you see wrong (bugs, debt, broken conventions, dead code) goes in your report as a
finding, with `file:line`.
```

The quick-fixer already does no cleanup: nothing to change there.

**Text to insert, option 3 (broader cleanup).** In the installed `~/.claude/agents/worker.md`,
replace the same sentence with:

```markdown
**Boy Scout in the area of your task**: leave the code cleaner than you found it in the files and
modules your task touches (small, safe fixes only: dead code, naming, obvious bugs); list every such
fix in your report so the director can review it. Anything larger, or outside that area, goes in
your report as a finding, with `file:line`.
```

**Where it goes.** The installed `~/.claude/agents/worker.md` (options 2 and 3) and, for any option,
the project's `CLAUDE.md` if it has its own cleanup rule that would contradict the agents.
