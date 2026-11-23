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

**The rule.** The director does not commit while any worker is running. Its edits to the report pile up on disk in the meantime. Right before every commit it runs `git status --short` and checks that the only modified files are its own; if anything else shows up, it waits.

**Why it is solved this way.** Another agent's half-done files are in the same tree, so a commit at the wrong moment can interfere with them. The safe move is to commit only when the tree holds nobody else's work. The report on disk is already the memory; the commit is only its remote copy, and it can wait.

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

## 2026-11-23 — This project only

**What happened.** I asked a session in one project to "review the streams", and it started listing the other sessions on the machine and reading reports and git history from other projects. It modified nothing.

**The rule.** The director and every agent it launches work inside the project: its repository, `~/.claude`, the session's scratchpad and temporary files, and the director's own agents. They do not go outside it on their own initiative: no other repositories or folders on the machine, and no other Claude Code sessions (listing them, reading what they do, messaging them). They go outside only when I ask for it and name the target; that request is the authorization. That a tool, a permission, an additional working directory or a path in a file can reach something does not put it in scope. "The directors", "the streams", "the reports" are this project's, and searches start from the project, never from a parent folder or a drive. A worker goes outside only if its brief names that exact path or session; if it thinks something outside is needed, it says so in its report.

**Why it is solved this way.** The boundary comes from my request, not from what the machine lets the model reach: each person configures their machine for their own reasons, and that says nothing about what I want looked at. It is a boundary, not a checkpoint: inside the project, work goes on as usual and nothing new is asked.

## 2026-11-23 — One message per delivery, after the review

**What happened.** No specific incident is recorded.

**The rule.** When a delivery arrives (worker, `quick-fixer` or exploration agent), the director writes at most one line ("T7 delivered, reviewing it") and does the review; it writes to me once, with the result already verified. A task sent back for correction is announced in one line, and the review message is written when it closes, unless the correction needs a decision from me first. If a conclusion depends on several agents, the synthesis is written when the last one delivers. Requests are held while a running agent can change their options or the recommendation, saying in one line what is held and which agent it waits for. A direct question from me is answered at once.

**Why it is solved this way.** What an agent reports is unverified when its notification arrives. Telling me then and again after checking it makes me read the same thing twice, the first time in its least reliable version, and a review that corrects the agent's summary contradicts what the director had already said.

## 2026-11-23 — Reply format

**What happened.** The first version of this rule, written that same day, closed every message with a fixed three-line block (what is running, what comes next, what is pending from me) inside a code block. In use, the lines did not wrap and forced horizontal scrolling, and the block was written even when it had nothing to say ("Running: nothing"). I removed it the same day.

**The rule.** A conversational reply has no template: it answers what was asked. Two pieces have a fixed shape, in my language and with no empty sections: the delivery review (task, verdict, commits, review findings, the worker's own decisions ratified or corrected, loose ends) and the request for a decision or consent (task and context, what it needs from me, options with the recommended one first, where to look, what happens next). The message closes conversationally and, when something is pending from me, ends by saying so in plain words; a request still unanswered is recalled at the end in one line that stands on its own.

**Why it is solved this way.** What matters is that at the end of the message I see what is pending from me, and saying it in plain words already achieves that. The fix was to undo the change, not to add rules about the failure.

## 2026-11-23 — The director's reports, in a fixed folder and with an agreed name

**What happened.** The director skill only said to create the report in the project's documents path, with no folder or name. One project ended up with a generic `informe-stream.md` that said nothing about its work, and it was only found because that project's `CLAUDE.md` named it.

**The rule.** The director's reports live in the project's `docs/director-streams/` (or the folder its `CLAUDE.md` names), one file per stream, with a short descriptive kebab-case name I will remember (`docs/director-streams/checkout-redesign.md`). The name is agreed on activation: if my message says what the work is and it matches an existing stream, the director reads that report whole and resumes it; if it is new work, it proposes a descriptive name, tells me in one line so I can change it, and creates the report; if I only activate the profile, it shows me the existing streams and asks in the chat whether I resume one or open another, what the work is and what to call it. A report I point to somewhere else is still read whole and used as it is.

**Why it is solved this way.** With a fixed folder the director finds the streams on its own when it activates, and a name agreed at the start is one I remember when I come back.
