# Guide

[Versión en español](guia.md) · [Back to the README](../README.md)

This guide explains how the pieces in this repository fit together and why they are the way they are. It describes my setup; wherever something is a preference rather than a requirement of the model, I say so and explain the alternative.

## 1. The roles

**The director** is the Claude Code session I talk to. I activate it with the `profile-director` skill (`global/skills/profile-director/SKILL.md`). Its contract is simple: I talk and decide; it does everything else through agents. It analyses the code before giving an opinion, presents options with a recommendation and their real cost, writes the briefs, launches the agents, reviews what they deliver and keeps the report. It never implements tasks itself, and it never turns me into a messenger: I am never asked to paste a brief into another window or to bring back an agent's summary.

The director and every agent it launches work inside the project: its repository, `~/.claude`, the session's scratchpad and temporary files. They do not go to another repository, another folder on the machine or another Claude Code session on their own initiative; they go there only when I ask for it and name the target, and that request is the authorization. Reach is not scope: permission rules, additional working directories in the settings or paths that appear in files do not widen the project. Inside it they work as usual; it is a boundary, not one more checkpoint.

**The worker** (`global/agents/worker.md`) executes one task from a brief, end to end, in the background. It reads the project's `CLAUDE.md`, activates the profile the brief names, runs the workflow the brief names (`/new-feature`, `/rework`, `/fix-bug`, then `/do-feature`), verifies, commits and pushes, closes out the documentation and finishes with a report of at most 20 lines. It does not make product decisions and it does not reopen closed ones. If it takes a decision on its own, it records it and reports it, and the director ratifies or corrects it.

**The quick-fixer** (`global/agents/quick-fixer.md`) applies one fix that the director has already diagnosed and I have already approved: a localized bug, a style tweak, a minor configuration change. Strict scope: if the fix turns out bigger than the brief says, needs a migration, crosses backend and frontend or deserves a regression test, it stops without touching anything and reports it. It does not write new tests. It runs on a cheaper model.

**Project profiles** are skills that live in each project (`project-example/.claude/skills/profile-*`): `profile-backend`, `profile-frontend`, `profile-planner`, `profile-auditor` and `profile-tester`. They are not agent types. A profile is a markdown file that defines a role, a reading list and an edit scope; the worker activates the one its brief names, and can switch profile in the same session when a task crosses from one area to another.

**Optional agents.** `optional/agents/Explore.md` overrides Claude Code's built-in Explore agent only to pick the model and effort; `optional/agents/web-fetch.md` is an additional lightweight agent that reads public web pages on a cheaper model, not an override. They are covered in section 8.

## 2. The report

The whole model rests on one living document per work stream: the director's report. The reports live in the project's `docs/director-streams/` (or the folder its `CLAUDE.md` names), one file per stream, with a short descriptive kebab-case name I will remember, such as `docs/director-streams/checkout-redesign.md`. The name is agreed when the director is activated: if my message says what the work is and it matches an existing stream, the director reads that report and picks it up; if it is new work, it proposes a name, tells me in one line so I can change it, and creates the report; if I only activate the profile, it shows me the streams that exist and asks whether to resume one or open a new one. Its structure:

- **Context and diagnosis**: what the stream is about and what the code looked like when it started.
- **Working model**: how this stream runs (sequential or not, who commits what).
- **Decisions table**: date, decision and reason, one row per decision.
- **Task queue**: numbered tasks, each with its status (`launched` → `delivered` → `in correction` → `approved and closed`), its brief pasted in full, the agent's identifier, the review verdict and the commit hashes.
- **Session log**: chronological, append-only.
- **Cumulative test script**: every closed task adds its numbered test cases, with concrete references, so that the final manual test is clicking, not searching.

The report is what survives. Context compactions lose detail and a new chat starts from nothing; the report is on disk and in git. When I open a new session, I tell the director what I am working on (or point it at a report, wherever it is) and it reads that report whole before saying anything.

Decisions are recorded in the same turn they are taken, and with my reason **in my own words** when I give one. The skill's example is "we don't sell toothpaste". A paraphrase loses the weight of the reason: three weeks later, a summary like "product scope" does not stop anyone from reopening the decision, while my own sentence does. Those decisions travel into the briefs marked as closed, and the agents do not reopen them.

The report is the director's responsibility. It commits it without asking me, in its own commits, with an explicit path, and never while a worker is running (section 4 explains why).

A director and its report serve one stream of work, a task or a block of related tasks, not the project for ever. When the block is done, I close the stream, and the next block starts with a new director session and a new report. A large report, even around 100k tokens, is fine when the work is that large: re-reading the report is still far cheaper than re-reading the conversation that produced it, and that is the point.

### Resuming after a break: the prompt cache

Claude Code keeps the conversation in the prompt cache for a limited time. According to the official [settings documentation](https://code.claude.com/docs/en/settings) (the `promptCacheTtl` setting), at the time of writing the default is 1 hour on a Claude subscription (within its usage limits) and 5 minutes with an API key, Bedrock, Vertex or Foundry. This may change.

Once the cache has expired, any new message in that conversation, even a trivial "give me a summary", sends and processes the whole conversation again. When the conversation was long, that is expensive in tokens.

With the report, I do not need to go back to the old conversation. I open a new session, activate the director and tell it which stream we are resuming; it finds the report in its folder. The only cost is reading the report, not re-sending a conversation that may be very long. So the report is not only what survives compactions and new chats: after a break, it also saves a lot of tokens.

## 3. A task's life

1. **Brief.** The director writes it and pastes it into the report before launching, so it survives compactions.
2. **Launch.** The director launches the agent with the `Agent` tool, in the background, with the brief as its prompt. It stays available to me while the agent works.
3. **Delivery.** When the agent finishes, a notification arrives with its final report. That report is the agent's only channel back, and I do not see it: the director records it and tells me at most one line ("T7 delivered, reviewing it") until the review is done.
4. **Review on the real diff.** The director reads the full diff of the task's commits, reads the critical files whole, repeats the key checks itself and goes through the agent's "decisions taken alone" one by one. It never approves on the summary.
5. **Corrections.** If something needs fixing, the director sends the corrections to the same agent with `SendMessage` (it keeps its context); the agent applies them, verifies and commits again, and the director reviews again. A rejected delivery is reverted with a new commit or redone, never by rewriting history.
6. **Close.** Only after an explicit verdict does the task become closed in the report.

The agent is not asked to wait for approval of its plan or for the review before committing. Git keeps the history and the director reviews afterwards, on the commit. That is what lets the agent run without stopping.

### How the director reports to me

What an agent reports is unverified when it arrives, so the director tells me about a delivery once, after the review: one message with the verified result, never a summary of the agent's report followed by a second message that corrects it. A task sent back for correction gets one line, and the review message comes when the task is closed, unless the correction needs a decision from me first. When a conclusion depends on several agents, it is written once, when the last one has delivered, and a request for a decision is held while a running agent can still change its options. A direct question from me is answered at once, whatever is running.

Ordinary replies have no template: they answer what I asked. Two pieces have a fixed shape: the delivery review (task, verdict, commits, review findings, the agent's own decisions ratified or corrected, loose ends) and the request for a decision or consent (task and context, what it needs from me, options with the recommended one first, where to look, what happens next). The full request is written once; while it stays open, later messages recall it in one line that stands on its own. Each message closes conversationally and, when something is pending from me, ends by saying so in plain words.

### What a good brief contains

The agent does not see the conversation, only the brief, the repository and its docs. A good brief:

- **Does not repeat the project's documentation.** It carries only what `CLAUDE.md` and the docs do not cover. Repeated generic instructions become noise and drift apart.
- **Starts with no questions.** It says which profile to activate, which workflow to run and on which document, and settles in advance everything an interactive workflow would ask ("the plan is already approved by the director").
- **Has a section of closed decisions** ("taken; do not reopen"). If the agent finds a reason to reopen one, it raises it in its report.
- **Has an explicit "out of scope"**, including what was parked on purpose and why, so nobody fixes it in passing.
- **Carries a staleness warning** when its material (an audit, an inventory) predates other changes: every item is re-verified against the current code before touching anything.
- **Has a close-out with no stops**: verify, commit, close out the docs, report. Phrases like "wait for approval" or "ask before X" are forbidden unless X is a real technical blocker.
- **Orders all deletions at the end, with an inventory.** During the task nothing is deleted; the agent lists what it created that must disappear (what, where, how) and deletes it in one final step. A deletion can trigger a permission prompt; at the end, that prompt stops the agent after the work is done instead of halfway through it.
- **Gives the concurrency context**: which other agents are active and which files that are not its own it may find modified.

## 4. Same working tree, no worktrees

The agents work in the same working tree as the director, without worktree isolation. I chose this because I work alone: the director reviews each delivery with `git show` and `git diff` on the same branch, and no merge is ever needed. Merges are expensive, and with one person deciding there is nobody to isolate from.

The cost is a set of commit rules, because several sessions share one tree:

- Each agent commits only its own paths, explicitly. Never `git add -A`.
- **The director does not commit while a worker is running.** The worker's half-done files are in the same tree, so a commit at the wrong moment can interfere with them. The director lets its edits to the report pile up on disk and commits only when no worker is running, after checking with `git status --short` that the only modified files are its own.
- Before each commit, an agent runs `git status --short` and checks that only its own files go into the commit. Other people's files stay modified and untouched.

If you work in a team, or you want several agents implementing at the same time, worktrees may suit you better. The director skill supports `isolation: "worktree"` when the user asks for it.

## 5. Several directors in parallel

Sometimes I run two work streams at once, each with its own director, in the same working tree. It works, with a few precautions.

**The coordination is deliberately not in the skill.** If the director skill said "other directors may exist", the model would check for them every time and fill its context with that. Instead, when I open a second director, I tell it in one sentence: "another director is handling X; it will contact you and you agree".

**I name one main coordinator.** Decisions about shared things (who commits when, who touches a shared file) are taken by one director, not by everyone talking to everyone.

**The known risk.** The rule "the director does not commit while a worker is running" protects that director's own workers, not another director's. A director that does not know about the other director's worker can commit in the middle of its task and interfere with its half-done files. The coordinator decides who commits and when, and every director runs `git status --short` before each commit and does not commit if it sees files that are not its own.

## 6. Per-project commands from templates

`/commit` and `/update-docs` are not global commands. Each project has its own copy in `.claude/commands/`, generated from the templates in `global/templates/` (kept in `~/.claude/templates/`), with the project's own steps filled in: files a hook protects, an approval token, extra documentation to keep in sync on closing.

Why: they used to be global, and over time they accumulated blocks that only applied to one project or another. Every session in every project loaded all of them. That is context noise, and worse, it gives the model chains of decisions about projects it is not working on ("if this is project A, do X").

The cost: when I improve a template, I have to carry the improvement to each project by hand.

The other workflows (`/fix-bug`, `/rework`, `/do-feature` and the `new-feature` skill) stay global because they contain nothing project-specific: they defer to each project's `CLAUDE.md` for commands, paths and policies.

## 7. Permissions

What follows is based on Claude Code's official documentation: [permissions](https://code.claude.com/docs/en/permissions), [permission modes](https://code.claude.com/docs/en/permission-modes) and [subagents](https://code.claude.com/docs/en/sub-agents). Check those pages for the current details; the behaviour may change between versions.

**Background agents run in your session.** Their permission prompts reach you, in the director's session, and an approval "for this session" covers them too. That is why every prompt an agent triggers matters: it interrupts me, and if I am not watching, the agent waits.

**Compound commands are checked per subcommand.** Bash permission rules are evaluated for each subcommand of a compound command, so `cd somewhere && git commit ...` can prompt even if Bash is allowed. Hence the rules every agent follows:

- never `cd` in a command (use `git -C <path>` or absolute paths);
- one git operation per call (`git add`, `git commit` and `git push` separately, never chained with `&&`);
- commit messages with `-m` (one for the subject, another for the trailer), no heredocs.

**Protected paths.** The `.claude` folder (and `.git`, `.vscode` and a few others) is a protected path: allow rules do not pre-approve writes there. In the default mode you approve them, and you can approve them for the session. The `auto` mode routes those writes to a classifier. `bypassPermissions` skips the checks, and I would only use it in an isolated environment (a container or a disposable machine).

The project example has a hook, `project-example/.claude/hooks/protected_commit_guard.py`, which asks before any commit that puts a protected file (translations, legal texts) into the commit, unless the command carries an approval token. Agents leave those files modified and unstaged, and the director commits them after reviewing them.

## 8. Optional preferences

These are choices I made for myself. Each one is an option; the reason is there so you can decide.

**(a) Questions in the chat instead of the multiple-choice question tool.** Claude Code has a tool to ask you questions with predefined options. I prefer the agent to ask me in plain chat. The tool blocks the session until I answer, the question arrives in the middle of the work, and if I am away the execution time is lost. I prefer the agent to finish its work (or stop at a real blocker) and then ask me in the chat. If you are usually in front of the screen, or you like answering with one click, the tool may suit you better.

**(b) Model and effort per agent.** The `worker` and `quick-fixer` frontmatter carry suggested `model` and `effort` values, marked as suggestions: remove them and the agent inherits the session's settings. The quick-fixer uses a cheaper model because a bounded, already diagnosed fix does not need the strongest one. `optional/agents/Explore.md` exists only to choose the model and effort of the built-in Explore agent: a user or project agent named `Explore` overrides the built-in one and keeps its own `model` field ([subagents documentation](https://code.claude.com/docs/en/sub-agents), "Built-in subagents"). `optional/agents/web-fetch.md` is not an override: it is an extra agent that reads public web pages on a cheaper model. If the defaults are fine for you, you need neither.

**(c) Testing policy.** In my projects, tests are not written during implementation: they are a final phase, triggered manually by me once I have validated the feature, and owned by `profile-tester`. The reason: while a feature is still being iterated, tests get rewritten again and again for no value. The only exception is `/fix-bug`, whose regression test ships with the fix. This is a policy of the project's `CLAUDE.md`, not of the global workflows: if a project has none, `/new-feature` and `/rework` plan the tests inside each phase. Many people prefer tests in every phase; both work with these files.

**(d) Boy Scout.** The project example's `CLAUDE.md` asks to leave the code cleaner than you found it. For bounded agents I limit that: the worker cleans up only inside the files it already touches for its task, and the quick-fixer does no cleanup at all. Anything they see outside goes into their report with `file:line`, and the director brings it to me as a decision. The reason: the worker definition (touch nothing outside the brief) and the project's `CLAUDE.md` (fix any mess you stumble upon) contradicted each other, and this settles it. The agent's diff stays on its task, which is what the director reviews, and what it finds outside reaches me as a decision instead of a change nobody asked for. If you want broader cleanup, give it its own task.

The guided route is three skills: `init-harness` sets the harness up, `harness-onboarding` runs a first task with you, and `harness-keeper` answers how things work and makes the later adjustments. These options are set with `harness-keeper` ("adjust the harness"), which offers each one when what you tell it touches it, or when you ask what can be tuned; the catalog it works from is [`global/skills/harness-keeper/optional-rules.md`](../global/skills/harness-keeper/optional-rules.md).

## 9. A known open point

There is a tension I have not resolved. `worker.md` says that only the worker's own files go into its commit. The `commit.md` template, on the other hand, says that if the task added content to a shared file (an index, a README, a module doc), the whole file is committed, even if it also holds another agent's changes.

How I live with it: each agent commits its own paths, and the case of two agents writing to the same shared file at the same time is rare, because the director runs implementation sequentially by default and only parallelises tasks with disjoint surfaces. When it does happen, the director catches it in the review. If your setup runs many agents in parallel, this is a point to decide for yourself.
