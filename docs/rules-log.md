# Rules log

[Versión en español](registro-de-reglas.md) · [Back to the README](../README.md)

Most rules in this repository were born from a real failure: something went wrong, I understood why, and the rule is what stops it from happening again. Some did not come from a failure but follow from the way of working itself, and their entries say so. Inside the skills and agents the rules appear without dates, because the model only needs the rule. This log keeps the history: when each rule appeared, what happened, and why it is solved the way it is.

Each entry follows the same format: **What happened → The rule → Why it is solved this way**. When a rule has no incident behind it, the entry says so.

---

## 2026-09-23 — Launching a worker carries the commit authorization

**What happened.** There was no incident; this follows from the way the model works. By the time the director launches an agent, I have already talked through and decided with the director what we are going to do. The agents it launches work under its supervision, so they may modify files and commit. What they may never do is merge into `main`, publish, touch production or anything of that kind.

**The rule.** When the director launches a worker under the director profile, that counts as my authorization for the worker to commit and push its own work. Only push to `main`, merges, publishing, production and force operations stay reserved for my explicit consent.

**Why it is solved this way.** The worker has to finish without stops. Git keeps the history, and the director reviews after the commit, on the real diff; a bad commit is reverted with a new one. Asking before each commit would add a stop without adding control.

## 2026-10-01 — The report is the director's, and it commits it without asking

**What happened.** There was no incident. The report is not code: it is the director's own document, written by the director, so the director manages it. It is committed so that no information is lost: not with every sentence or every two minutes, but never a week without a commit either. And the director does not need to ask me each time; it is its report.

**The rule.** The report is the director's responsibility. It commits it when a part closes or when it makes sense, never so rarely that information could be lost. Typical moments are after a recorded decision, a launch, a closed review, or before a risk of compaction. It commits in its own batches, with an explicit path, without mixing in workers' files.

**Why it is solved this way.** The report is the director's working document, not a deliverable for me to approve. Keeping the remote copy up to date is part of managing it, and it adds no prompts.

## 2026-10-01 — All deletions at the end, with an inventory

**What happened.** A deletion in the middle of a task triggered a permission prompt from a hook, and the worker was left stopped, waiting for someone who was not watching.

**The rule.** During a task nothing is deleted. The agent keeps an inventory of everything it created that must disappear (what, where, how it is deleted) and runs all the deletions in one final step, right before its report. If something blocks there anyway, the report carries the pending inventory and the director resolves it.

**Why it is solved this way.** The prompt cannot always be avoided, but its timing can. At the end, a blocked deletion stops the agent with the work already done and committed; halfway through, it stops the whole task.

## 2026-10-16 — Tests use no external resources without approval

**What happened.** A test suite exhausted an external service's monthly quota.

**The rule.** Test suites touch only local, disposable resources and in-process fakes. Any test or fixture that would reach something outside the machine (an external API, a quota-limited or paid service, the production database), directly or as a side effect of the application starting up, is validated with me first, with its cost and quota stated. External switches are neutralised in the test setup before the application's configuration is loaded. The rule lives in the tester profile (`project-example/.claude/skills/profile-tester/SKILL.md`).

**Why it is solved this way.** The damage comes from side effects that nobody sees when reading a single test. Neutralising the switches before the configuration loads closes that door for every test at once, instead of relying on each test to remember it.

## 2026-11-01 — Zero avoidable permission prompts

**What happened.** Permission prompts kept popping up for me even with Bash allowed. The official documentation later confirmed why: compound commands are checked subcommand by subcommand, so a `cd` or a chain of git operations can prompt on its own.

**The rule.** No `cd` in commands (use `git -C <path>` or absolute paths). One git operation per call. Commit messages with `-m`, no heredocs. Nothing that a project hook will stop (protected files, deletions halfway through). And the `Monitor` tool is forbidden for agents: every use triggers a prompt and it adds nothing that a foreground command with a timeout, or a background command, does not already give.

**Why it is solved this way.** Every prompt from a background agent lands in my session and stops the agent until I answer. Writing commands in a shape that the allow rules already cover removes the prompt at the source, instead of approving it again and again.

## 2026-11-06 — The director does not commit while a worker is running

**What happened.** It happened more than once. The pre-commit framework stashes every unstaged change before a commit and restores it afterwards. With a worker's half-done files in the tree, every commit of the director took them out and put them back, and a failed restore would destroy them.

**The rule.** The director does not commit while any worker is running. Its edits to the report pile up on disk in the meantime. Right before every commit it runs `git status --short` and checks that the only modified files are its own; if anything else shows up, it waits. If the report must be committed while a worker is active, the worker is first asked to commit what it has. Nothing is committed during a manual testing phase with the development server running either.

**Why it is solved this way.** The stash is how the pre-commit framework works, and disabling it would mean skipping the hooks, which is forbidden. So the safe move is to commit only when the tree holds nobody else's work. The report on disk is already the memory; the commit is only its remote copy, and it can wait.

## 2026-11-09 — Every request to the user is self-contained

**What happened.** I do not follow the thread. Between two of my messages, the director had talked to workers and to other sessions, and messages like "still waiting for X" or "the document" meant nothing to me.

**The rule.** Every time the director needs something from me (a decision, a consent, something to read), the message carries the full context as if it were the first one of the day: which task it is about and how we got here, what exactly is being asked and why now, the options with a recommendation, the full path of anything I have to look at, and what happens once I answer. A bare "still waiting for X" and pronouns that point back to earlier messages are forbidden.

**Why it is solved this way.** The director knows everything that happened in between; I only read the end. Rebuilding the context costs the director a few lines and saves me reconstructing a conversation I did not see.

## 2026-11-10 — Quick fixes go to the quick-fixer, never to the director

**What happened.** No incident as such. When the director applied quick fixes itself, every fix dirtied its context and made it bigger for no reason. I moved quick fixes to a separate agent to keep the director's context as clean as possible.

**The rule.** The director does not apply quick fixes itself. It diagnoses, I approve, and a dedicated `quick-fixer` agent, on a cheaper model, applies the fix from a short brief, verifies it and commits it. The director reviews the diff afterwards, as with any worker.

**Why it is solved this way.** The director's context is what holds the thread of the whole stream; filling it with the details of each small fix makes it worse at its real job. The cheaper model comes second, and it is an optimization, not the reason: a quick fix has a bounded scope, so a cheaper model is enough.

## 2026-11-18 — Boy Scout only inside the worker's own files; none for the quick-fixer

**What happened.** The worker definition and a project's `CLAUDE.md` contradicted each other: one said to touch nothing outside the brief, the other said to fix any mess found along the way.

**The rule.** The worker leaves the code cleaner only inside the files it already touches for its task. The quick-fixer does no cleanup at all. Anything either of them sees wrong outside that goes into its report with `file:line`, and the director brings it to me as a decision.

**Why it is solved this way.** It resolves the contradiction while keeping each agent's diff on its task, which is what the director reviews. Problems found outside the task are not lost: they become decisions.

## 2026-11-18 — /commit and /update-docs become per-project commands

**What happened.** The global `/commit` and `/update-docs` commands had accumulated blocks that only applied to specific projects.

**The rule.** Both become templates in `global/templates/`. Each project keeps its own adapted copy in `.claude/commands/`, with its specific steps in the section the template reserves for them.

**Why it is solved this way.** Global commands are loaded in every project, so project-specific blocks were context noise and chains of decisions about projects unrelated to the current one. The cost is that template improvements are carried to each project by hand.

## 2026-11-18 — (optional preference) Ask in the chat, not with the multiple-choice question tool

**What happened.** No specific incident is recorded. This is a preference, not a fix.

**The rule.** Agents ask me their questions in the chat, once they have finished their work or stopped at a real blocker, instead of using the multiple-choice question tool.

**Why it is solved this way.** The tool blocks the session until I answer, the question arrives in the middle of the work, and if I am away the execution time is lost. Others may prefer the tool; see section 8 of the [guide](guide.md).
