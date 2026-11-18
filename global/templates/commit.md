<!--
TEMPLATE, not a command. Copy it to <project>/.claude/commands/commit.md and adapt it there;
drop this comment in the copy (the frontmatter must open the file).
Project-specific steps go in "Phase 7: Project-specific steps".
-->
---
name: commit
description: Create a commit with only the files of the current task and push it to the branch. Ignores parallel changes from other agents/the user without asking. Use whenever the user asks for a "commit".
---

# Commit

Create an isolated commit of the current task and push it to the branch.

**Philosophy:** you work in a repo where several agents edit in parallel in different windows, and the user also edits files directly. Your commit must contain **only the files that YOUR current task has touched**, not the changes of other agents or of the user. Do not ask about other people's files: ignore them silently.

## Hard rules (non-negotiable)

- **NEVER** `git push` to `master` / `main`. Feature branches only.
- **NEVER** `git add -A`, `git add .`, or global patterns. Always explicit paths.
- **NEVER** `--force` / `--force-with-lease`, `git merge`, `git rebase`, `git reset --hard`, `git commit --amend` without explicit consent for that specific operation.
- **NEVER** `--no-verify`, `--no-gpg-sign` or any bypass of hooks/signing unless the user explicitly asks for it.
- **NEVER** ask "what do I do with the files I did not touch?" — the canonical answer is: ignore them.

## Phase 1: Identify the files of the current task

The rule is: only the files that **this task** has modified get committed. To know which ones:

1. **If there is an active progress doc in `docs/progress/` or `docs/rework/`** → its "Files" section (or the paths mentioned in the phases) is the source of truth.
2. **If it is a Quick Fix without a progress doc** → use the session memory: the files the agent has read/edited in this conversation.
3. **If there is real doubt about whether a modified file is "mine"** → ask the user specifically, naming the concrete file. Do NOT ask generically.

> **The task's test files count as task files.** If this task added or modified tests (in the project's test directory), they are staged and committed together with the code they cover — they are part of the same change.

**Shared files where several agents usually write** (they vary per project — e.g. i18n indexes, product document, READMEs, module docs):

If this task has added content to one of those shared files, **the whole file is committed** even if it also contains changes from another agent — those parallel changes are additive and managing them is not your problem. The other agent will make its own commit on its branch.

## Phase 2: Check the branch

```bash
git branch --show-current
```

- If the output is `master` or `main` → **STOP**. Report to the user and ask before doing anything. Never commit directly to master/main.
- If it is a feature branch → continue.

## Phase 3: Edge case — no files of your own

If after Phase 1 there is no file of "yours" to commit but `git status` shows changes:

1. **STOP. Do not commit anything.**
2. Report to the user: "I have no files of my own to commit. There are N untouched changes that look like they belong to another agent or to you: [short list]. What should I do?"
3. Wait for explicit instructions.

## Phase 4: Selective staging

```bash
git status
```

Review what is modified. Then stage **only** the task's files, one by one or grouped with explicit paths:

```bash
git add backend/app/api/endpoints/foo.py backend/app/services/foo_service.py
git add frontend/src/features/bar/Baz.tsx frontend/src/i18n/locales/es/common.json
```

**NEVER:**

- `git add -A`
- `git add .`
- `git add backend/` (whole folder without specifying)

## Phase 5: Check what is staged

```bash
git diff --cached --stat
```

- Confirm that **exactly** the expected files appear.
- If a file that does not belong to this task slipped in → `git restore --staged <file>`.
- If a file of this task is missing → go back to Phase 4 and add it.

Optionally `git diff --cached` to review the content if the commit is large or ambiguous.

## Phase 6: Commit message

1. Check the project's style:

   ```bash
   git log --oneline -20
   ```

2. Write the message in **English**, conventional commits (`feat(scope): ...`, `fix(scope): ...`, `chore(scope): ...`, `docs(scope): ...`, etc.).
3. Concise title (≤72 chars ideally). If more context is needed, add a body.
4. If the commit is large, complex or the scope is unclear, show the draft to the user before running it. For routine commits, go straight ahead.

## Phase 7: Project-specific steps

<!-- PROJECT-SPECIFIC: steps that only apply to this project and run before the commit (e.g. files protected by a hook, a token a hook requires, extra checks). Empty in the template. -->

_None._

## Phase 8: Commit

Command: one `-m` per paragraph (a one-line subject, then an extra `-m` for the body and another for the trailer if needed). No heredocs:

```bash
git commit -m "feat(scope): short description" -m "Optional body explaining the why."
```

**If the pre-commit hook fails:** investigate the error, fix it, re-stage and create a **NEW** commit. **NEVER** `--amend` or `--no-verify`.

## Phase 9: Push to the branch

```bash
git push
```

- If the branch has no upstream yet: `git push -u origin <branch-name>`.
- **NEVER** `--force`, `--force-with-lease`, or `--no-verify`.
- If the push fails because of divergence with the remote (another agent pushed to the same branch — rare but possible), **STOP** and report to the user. Do not attempt `pull --rebase` or `merge` without consent.

## Phase 10: Report

Short summary to the user in one or two lines:

```text
Commit <short-sha> on <branch>: "<title>" — N files pushed.
```

If uncommitted changes remain (from other agents), mention it briefly as an informational note:

```text
M files left unstaged (parallel changes from other agents/the user).
```

## Flow summary

```text
Identify my files → Check branch → [if I have no files, ask]
  → Selective staging → Check staged → Write message → Project-specific steps → Commit → Push → Report
```
