# CLAUDE.md

<!--
TEMPLATE. Copy it to the root of your project and replace every <placeholder>.
The structure (priorities, work levels, router, profiles, git rules, docs locations) is the
methodology; the placeholders are your stack. Drop this comment in the copy.
-->

`<Project name>` is `<one-line description>`. Stack: `<backend stack>`; `<frontend stack>`; `<other relevant tooling>`.

---

## ABSOLUTE PRIORITY — These rules override everything

### 1. Never modify env files or LLM model settings without explicit permission

Reading `<env file paths, e.g. backend/.env>` is allowed and expected — read them whenever you need a config value to do your job. What is forbidden is **changing** them: NEVER use `Edit` or `Write` on them. If there's a config issue, ONLY inform the user.

`<If production secrets live outside the repo (in your hosting provider's dashboard), say so here: never treat a development key as the production one, nor the reverse, and never write a production secret anywhere in the repo.>`

NEVER change `temperature`, reasoning settings, max output tokens, model name, or any other LLM parameter in any file that instantiates an LLM client (`<paths where LLM clients are configured>`). Tell the user; wait for explicit approval.

### 2. Planning and multi-step tracking go through `/new-feature` or `/rework` progress docs

When a change adds or alters behaviour or contracts that the project docs describe — so those docs will have to be updated — the planning and tracking mechanism is:

1. Invoke the right planning skill to create a progress document:
   - `/new-feature` — new functionality → doc in `docs/progress/`.
   - `/rework` — changes to code that already exists and works (refactors, direction changes, POCs, tech-debt cleanup) → doc in `docs/rework/`.
2. Update that markdown file as you advance — checking off steps, recording decisions, noting blockers.
3. On a new chat / context compaction, re-read the progress file (per Workflow section).
4. When the work is implemented, verified and committed, close the task with `/update-docs` — it updates the project docs (PRD, module and technical docs) to match the code, then deletes the progress file.

A purely internal change with no counterpart in the project docs does not need a progress doc, however many files it spans. This is the ONLY planning workflow allowed. In-progress work must live in the repo so the user can see it across sessions and it survives context compaction.

### 3. Technical quality is non-negotiable — do it right, never patch around it

Every change MUST be done the right way technically: follow the project's standards, established patterns, and the best practices expected of a professional codebase. We do NOT ship band-aids. If doing it right means a refactor, do the refactor — don't bolt a workaround onto a broken design. Never leave gaps, half-measures, dead code, or "TODO: fix later" shortcuts behind a feature that looks done.

Apply the **Boy Scout rule**: leave the code cleaner than you found it. If, while working on something, you come across an anti-pattern, a bug, dead code, a violated convention, or any other mess in the area you're touching, fix it — even if it wasn't part of the original request. You don't have to go hunting for problems across the whole repo, but anything dirty you stumble upon in your path, you pick up.

**Exception — bounded agents.** Agents launched by the director workflow (`~/.claude/skills/profile-director/SKILL.md`) work inside a scope set by a brief:

- The `quick-fixer` does NOT apply the Boy Scout rule at all: it records what it finds, with `file:line`, in its report, and the director brings it to the user to decide together.
- The `worker` applies it only inside the files it already touches for its task; anything outside them goes in its report as a finding, with `file:line`.

The only limits on this are the other rules in this file: respect the approval workflow for non-trivial changes (diagnose and propose before a large refactor), and never breach the ABSOLUTE PRIORITY rules above (env files, LLM settings, planning workflow). When doing it right would require a big refactor outside the current scope, surface it and propose it rather than silently leaving the mess — but never choose the quick patch over the correct solution just to save effort.

### 4. Never assume verifiable state — check it, then speak

NEVER state, assume, guess, imagine, or invent the real state of anything you have the means to verify. If a claim touches the code, the database, migrations, configuration, dependencies, file contents, the git state, or any other fact a tool call could confirm, you MUST verify it first — read the file, run the query (via `<your sanctioned read-only DB query path>`), inspect the actual state — BEFORE you assert it. Answering from memory, assumption, or what "should" be true about something checkable is forbidden: either verify it and report the fact, or say plainly that you have not checked.

This is not optional and there is no "probably". When you genuinely cannot verify (no access, the check would be destructive, the tool isn't available), say so explicitly and stop — do NOT fill the gap with a plausible-sounding guess presented as fact. A wrong answer dressed as certain is worse than an honest "I haven't checked this yet."

---

## Workflow

The level of a change is NOT about how many files it touches — fixing a typo across five files is still trivial. It's about whether the change is mechanical or needs planning, and — separately — whether it touches the project's documentation.

### Trivial (no approval needed)

A mechanical change with no judgement involved (a typo, a rename, a comment, a lint fix), no matter how many files it spans. Make it and report.

### Quick Fix (lightweight approval)

A self-contained change that needs some thought but no real planning (a bug fix, a CSS tweak, minor config): diagnose + propose, wait for OK, implement. No progress doc.

### Non-trivial (full workflow)

A change that needs planning. Diagnose and propose a plan, wait for explicit approval, then implement. Never assume the user wants implementation just because they asked for analysis.

Create a progress doc (`/new-feature` or `/rework`) ONLY when the change touches the project's documentation — i.e. it adds or alters behaviour or contracts the project docs describe and will have to update; keep it updated as you go, and close it with `/update-docs` once the work is done (it updates the project docs to match the code and deletes the progress file). A purely internal refactor with no counterpart in the project docs does NOT need a progress doc, even if it needs planning.

**On context compaction or new chat:** read the progress file in `docs/progress/` or `docs/rework/` FIRST — single source of truth for in-flight work.

If a change that looked mechanical turns out to need planning, STOP and switch to the full workflow.

### Implementation profiles and delegation

The project defines work profiles (`profile-backend`, `profile-frontend`, `profile-planner`, `profile-auditor` and `profile-tester`) that scope the **currently active** edit surface. **They are repo-local skills, in `.claude/skills/profile-*/SKILL.md`** — a profile is just an MD that defines a role and a scope; activating one means reading its `SKILL.md` and adopting it. A profile scopes *what you may edit right now*, not *what the whole chat is forever allowed to be*: **exactly one profile is active at a time, but you can switch profile within the same session** (see "Switching profiles in-session" below). Separate sessions per profile are an option, never an obligation.

For **non-trivial cross-stack work**:

1. **Plan** (`/new-feature` or `/rework`): the progress doc splits the phases per profile in a `## Delegation` section, with the order between profiles (backend first when the frontend consumes its contract) and the contract each one exposes to the other.
2. **Implement** under the matching profile — pick up the doc with `/do-feature` and run the plan to completion. When the user asked for the whole task, `/do-feature` runs **every phase of every profile** until done (only a *manual* testing phase is excluded): on reaching another profile's phases the default is to **switch profile in-session and keep going** (read its `SKILL.md`, adopt its scope, note the switch in the doc), **never** to stop and ask the user "shall I continue / do you want to validate first?". The per-profile boundary fixes what you may *edit at any given moment* and *not* whether the task runs to the end; it is not a checkpoint that hands control back. You only stop at the boundary if the user explicitly scoped the work to one profile, a needed contract is missing (a real technical blocker), or you hit the manual testing phase — see `/do-feature` rule 8. Separate sessions per profile remain an option, never an obligation.
3. **Test — a separate, MANUAL final phase** (example policy; replace it with yours). Tests are **not** written during implementation (iterating a feature would mean rewriting them a dozen times for no value). The plan ends with a single dedicated testing phase, assigned to `profile-tester` and flagged **manual**: the user launches it only once they have validated the feature — the use case and the usability/UX. The implementation phases close on compile + typecheck + lint + existing suite green, never on writing new tests. **Only exception:** `/fix-bug`, whose red→green regression test ships inline with the fix.

   **Activating a profile ≠ running the task.** Activating `profile-*` only sets the scope and the reading list; it does NOT start implementation. If — in the same request or later — the user asks to **continue / finish / resume / complete / keep going with** a task that already has a progress doc in `docs/progress/` or `docs/rework/`, you MUST **invoke `/do-feature`** before touching code — it is the only sanctioned execution mode (run-to-completion, no deferring scope, hard per-profile boundary). Never implement a task with a progress doc by hand: even if you just activated a profile in the same message, the `/do-feature` trigger still applies.

#### Switching profiles in-session (profile handoff)

**Never throw away loaded context just to honour a profile boundary.** When you finish one profile's job and the next step needs another profile — the classic chain is audit → plan → implement — do NOT send the user to a fresh chat to pay, again, for rebuilding the context you already have in this one. Switch profile in place:

1. **Close the outgoing profile.** Announce the switch, and if its work leaves an artifact that would otherwise be lost, persist it first in its folder — an `auditor` writes its report to `docs/audit/`, a `planner` its progress doc to `docs/progress/` or `docs/rework/`. (That artifact is also what would let a separate session start cheap, if there ever is one.)
2. **Activate the incoming profile:** read its `profile-*/SKILL.md` (its "Required reading on activation"). From that point its edit scope and rules govern and the previous profile no longer applies — including a read-only auditor becoming an editing developer. Still exactly one profile active at a time.
3. **Keep the accumulated reading context.** The code and docs you already read stay valid; do NOT re-investigate what you already know — that is the entire point of switching in place.
4. **The workflow still applies.** Switching profile does not skip planning: non-trivial implementation that touches the project docs still goes through `/new-feature` or `/rework`, and a task that already has a progress doc still runs via `/do-feature`. The switch removes the *new-chat* tax, not the planning rules.

A fresh session per profile is still fine when the context is small or unrelated; **prefer the in-session switch whenever rebuilding the context would be expensive** — anything after a real audit, a deep investigation, or a long plan.

Activating a profile is optional for trivial or single-stack work; recommended to keep the scope bounded on large cross-stack features.

### Director workflow (optional)

For a multi-task work stream, activate `profile-director` (global skill): the session talks and decides with the user and delegates every task to background `worker` / `quick-fixer` agents, reviewing each delivery against the real diff. The rules in this file apply to the director and to its agents.

---

## When working on… (Task Router)

Read the matching agent-context file **before touching code** in that area. Then invoke the listed skill for generic theory.

**Rule of the router:** before improvising commands or searching the codebase blindly, scan this table. If the user's request involves DB inspection, running scripts, dependency changes, or any of the listed areas, **open the linked doc first** — improvise only if the doc has no answer.

| Task | Read | Skill |
| --- | --- | --- |
| `<frontend area, e.g. data fetching / cache>` | `docs/agent-context/<frontend-area>.md` | `<skill from your skills index>` |
| `<frontend area, e.g. forms>` | `docs/agent-context/<frontend-forms>.md` | `<skill>` |
| `<backend area, e.g. API endpoint / service>` | `docs/agent-context/<backend-area>.md` | `<skill>` |
| `<backend area, e.g. database / migration / model>` | `docs/agent-context/<backend-db>.md` | `<skill>` |
| **Any read access to the database** — inspecting tables, counting rows, debugging persisted state, validating a migration's result. If the task involves reading from the DB in ANY form, this is the only sanctioned path. | `<doc that describes your read-only query path>` | — |
| Writing / running tests (a **final, manual** phase via `profile-tester`), or a `/fix-bug` regression test | `docs/agent-context/testing.md` | `<skill>` |
| Dependencies / build / migrations / format / running scripts | `docs/technical/DEVELOPMENT.md` | — |

Index of all context files: `docs/agent-context/README.md`.

---

## Communication

- Responses to the user: **`<the user's language>`**.
- Code, identifiers, comments, documentation files: **English**.
- Git commits, branches, PR titles: **English**.

---

## Analysis vs Modification

If the user asks to analyze, review, or look at something, report only — do not modify. Only generate a `docs/audit/<TOPIC>_YYYY-MM-DD.md` report file when explicitly asked.

---

## Documentation location

All generated `.md` files MUST go inside `docs/`:

- Reports / audits → `docs/audit/`
- Technical docs → `docs/technical/`
- Per-task context for agents → `docs/agent-context/`
- Pending features → `docs/pending/`
- Temporary progress (new features) → `docs/progress/`
- Temporary progress (reworks) → `docs/rework/`
- Per-module documentation → `docs/modules/`

**Exception:** only `CLAUDE.md` and `README.md` may exist at root.

<If the repo holds gitignored credentials (e.g. `docs/secret/`), say here: never read, write, or commit it.>

---

## Database: local is disposable, production needs consent

Database rules have **nothing to do with git rules** — keep them separate.

- **Local DB — change it freely, never ask permission.** Applying migrations (`<local migrate command>`), recreating, emptying, or rewriting the local DB is normal development. Do it as part of your work without asking, **including destructive migrations**. The local DB is disposable: it restores with `<local restore command>`.
- **Production DB — explicit consent, always.** Any migration or write against production (`<production targets / env file>`) needs an explicit, separate instruction for that concrete action. See `docs/technical/DEPLOYMENT.md`.
- **Ad-hoc inline queries** (the read-only inspection path) stay read-only by default even on local — that guards against corrupting in-progress data with manual one-off `UPDATE`/`DELETE`. It is **not** about the migration workflow; running migrations locally is always fine.

---

## Git, deploy, and consent

This is about **git only** — database operations follow the section above, not these rules.

Never run git write operations (`commit`, `push`, `merge`) without an explicit user request. (Under the director workflow, launching a worker carries that request for the worker's own commits.)

**Single-developer convention:** when the user asks for a "commit", commit AND push to the current branch in one step. The user wants the remote always up to date with local work and there are no sync conflicts to worry about.

**Exceptions that still need explicit, separate instruction:**

- Pushing to `main` — only when the user says so.
- `<deploy branches>` — never touch (production, irreversible). Deploys go through `/deploy`. See `docs/technical/DEPLOYMENT.md`.
- `git merge` from another branch.
- Force-push of any kind.

**Files protected by a hook.** `.claude/hooks/protected_commit_guard.py` asks the user before any commit that touches `<protected paths, e.g. localization files>`. Review those files before committing them; once reviewed, commit with the hook's approval token as an env-var prefix (`<TOKEN> git commit ...`, e.g. `PROTECTED_OK=1 git commit ...`) so the hook lets it through. Agents launched by the director leave these files modified and unstaged; the director commits them.

Deploy workflow: `docs/technical/DEPLOYMENT.md` and `/deploy`.

---

## Logs

- DO NOT touch `<log file paths>`.
- DO remove temporary debug prints in code.

---

## Technical Reference

| Doc | Use it for |
| --- | --- |
| `docs/README.md` | General index |
| `docs/PRD.md` | Product requirements, module map |
| `docs/technical/DEVELOPMENT.md` | Commands, deps, migrations, code patterns |
| `docs/technical/ARCHITECTURE.md` | System architecture, layers, data flow |
| `docs/technical/API.md` | API reference (endpoints, auth, formats) |
| `docs/technical/DEPLOYMENT.md` | Deploy, branches, env vars |
| `docs/modules/` | Per-module deep docs |
| `docs/audit/` | Code audits and analyses |
| `docs/pending/` | Pending features & follow-ups |
