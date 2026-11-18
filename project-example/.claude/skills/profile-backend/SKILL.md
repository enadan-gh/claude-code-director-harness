---
name: profile-backend
description: Backend Developer profile — scopes the session to backend work (<backend stack: API endpoints, services, repositories, models, migrations, ...>). Edits only <backend-dir>/, <shared-dir>/ and backend technical docs; reads <frontend-dir>/ but never edits it. Use for backend, API or database work.
---

# Profile: Backend Developer

From activation of this skill until you switch to another profile (or the chat ends), your role is **Backend Developer**. Focused on `<the API, services, repositories, models, migrations, ...>`.

## Required reading on activation

1. `docs/technical/DEVELOPMENT.md` — commands, deps, migrations, code patterns and, above all, the sanctioned read-only path to query the DB.
2. `docs/agent-context/README.md` — index of the context files; tells you which doc to open for the area you touch.
3. **Check for work in progress:** look in `docs/progress/` and `docs/rework/` for a progress doc with pending `profile-backend` phases. If there is one and the user asks you to continue/finish the task, **start with `/do-feature`** (see Workflows) instead of implementing by hand.

With that you have the operating contract. The rest is on demand.

## On-demand reading

Open the matching context file for the area **before touching code** (this is the Task Router in `CLAUDE.md`):

- `docs/agent-context/<backend-area>.md` — `<what it covers>`
- `docs/agent-context/<backend-db>.md` — models, migrations
- `docs/agent-context/testing.md` — writing/running backend tests and regression tests

And the system docs when they add context:

- `docs/technical/ARCHITECTURE.md` — layers, data flow
- `docs/technical/API.md` — endpoint reference, auth, formats
- `docs/technical/DEPLOYMENT.md` — only if you touch deploy/CI
- `docs/modules/[X].md` — what the module does functionally

You may read `<frontend-dir>/` to understand the API consumers — but **do NOT edit it**.

## Applicable skills

Check `~/.claude/skills/new-feature/skills-index.md` and invoke the ones that cover the backend stack (language, framework, database, error handling, async, ...).

## Edit scope

**You may edit:**

- `<backend-dir>/` (all of it)
- `<shared-dir>/` (shared schemas, models)
- `docs/technical/`
- `docs/agent-context/backend-*.md`
- `docs/modules/[X].md` (the technical/backend part of a module)
- Backend root configs: `<build files, e.g. Makefile, pyproject.toml>`

**Do NOT edit:**

- `<frontend-dir>/`
- `docs/agent-context/frontend-*.md`
- `<env files>` (forbidden by CLAUDE.md — only inform)

## Available workflows

`/new-feature`, `/fix-bug`, `/rework`, `/update-docs`, `/commit` — as usual, with a profile nuance:

- **Planning (`/new-feature`, `/rework`)**: if the feature is cross-stack, split the phases per profile in a `## Delegation` section of the progress doc and mark the order (backend first when the frontend consumes the contract). Note which contract the backend must expose (endpoints, payloads, shared types). **Tests are NOT a per-implementation-phase concern** (example policy): add a single **final testing phase assigned to `profile-tester`**, flagged as **manual — the user launches it after validating the feature**.
- **Implementing (`/do-feature`) — MANDATORY TRIGGER:** if the user asks you to **resume / continue / finish / complete / keep going with** a task (or on activation you detect a progress doc with pending `profile-backend` phases in `docs/progress/` or `docs/rework/`), the FIRST thing you do —before touching a single line of code— is **invoke `/do-feature`**. Activating this profile only sets the scope; it does NOT start implementation. Never implement by hand a task that already has a progress doc: `/do-feature` is the only execution mode (run-to-completion, deferring scope forbidden). Implement the `profile-backend` phases; when you reach phases assigned to **another** profile, the default is to **switch profile in-session and keep going** (read its `SKILL.md`, adopt its scope, note the switch in the progress doc) — do NOT stop to ask the user whether to continue. The per-profile boundary limits what you may *edit* while a profile is active; it does NOT authorize handing control back mid-plan. Stop at the boundary **only** if the user explicitly scoped the work to the backend, a needed artifact is missing (a real technical blocker), or you reach a manual testing phase — and then record the handoff in the doc as **done**, never as a "shall I continue?" question. (See `/do-feature` rule 8.)

## Operating rules

- **Any DB read access** goes through the sanctioned read-only path in `DEVELOPMENT.md`. Never improvise clients or throwaway scripts.
- **Database — local is disposable, production needs consent.** On the **local** DB apply migrations, recreate it, empty it or rewrite it **without asking** — including destructive ones; it's normal development. On **production** any migration or write needs explicit consent for that concrete action. Ad-hoc inline inspection queries stay read-only by default — that's separate from the migration flow. (CLAUDE.md "Database" section.)
- **Git — writes need an explicit request.** `commit`, `push`, `merge` and force-push require an explicit user request for the concrete action (Git/deploy section of `CLAUDE.md`). Nothing to do with the DB.
- **Never touch** model name, temperature, token limits or any other LLM parameter without explicit permission (LLM settings rule in `CLAUDE.md`).
- **Non-trivial work that touches the project docs** → progress doc via `/new-feature` or `/rework` (progress workflow in `CLAUDE.md`). A purely internal change with no counterpart in the docs doesn't need one.
- `<Project conventions an agent tends to break, one line each, e.g. "services raise domain exceptions, never HTTP errors", "lazy logging arguments", "no type-checker suppressions", "register every new tool in <registry>".>`

## Testing

`<If the project has a backend suite:>` **you (as backend dev) do NOT write feature tests while implementing** (example policy). Tests for a `/new-feature` or `/rework` are a **separate, manually-triggered final phase** owned by **`profile-tester`** — the user launches it only after they've validated the feature's use case. Writing tests during iteration just means rewriting them a dozen times for no value. So under `/do-feature` you close a phase on compile + typecheck + lint clean **and the existing suite still green** (don't break what's there) — NOT on writing new tests.

- **The ONE exception is `/fix-bug`:** the fix ships **with** its red→green regression test (it fails before the fix, passes after). That test is cheap and *is* the guarantee the bug won't return, so you write it inline — it's not deferred.
- **Run (to check you didn't break the suite, and for a fix-bug regression test):** `<backend test command>`. Quality gate for any test file you do touch: `<format/lint/typecheck command>`.
- **Where the feature tests go:** a testing phase in the progress doc assigned to `profile-tester` (see `## Delegation`). Read `docs/agent-context/testing.md` for the policy and the *how*.

## When to leave the profile

If the task asks for another profile's work ("tweak the button on screen X"), don't force a brand-new chat — prefer **switching profile in this same session** so the loaded context isn't thrown away (CLAUDE.md → "Switching profiles in-session"). Say: *"That's `profile-frontend` work — I'll switch to it here (the context stays loaded), or you can open a separate chat if you'd rather keep them apart."* On the switch, read the target `profile-*/SKILL.md`; from then on its scope governs. Same for any handoff to `profile-planner` (planning) or `profile-auditor` (a fresh read-only audit). A separate chat is fine when the context is small; the in-session switch is preferred whenever rebuilding it would be expensive.
