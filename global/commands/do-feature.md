---
name: do-feature
description: Run, resume, continue, finish or keep going with the implementation of a task (feature, rework or fix) that already has a progress file in docs/progress/ or docs/rework/. Use it whenever the user asks to "finish/continue/resume/keep going with the task" and a progress doc exists — even if they have just activated a profile-* in the same message.
---

# Do Feature

Process to run or resume the implementation of a planned feature.

## Execution rules (READ BEFORE STARTING)

These rules are **absolute** and override any default instinct of the model. Once `/do-feature` is invoked, the contract is: **run the plan from start to finish without interrupting the user**.

1. **Run-to-completion.** Once started, run all the pending phases of the progress doc until done. Do not stop to ask for intermediate approval, do not ask "shall I go on with the next phase?", do not give intermediate summaries waiting for a green light. The user already approved the plan by running this command — the approval is total, not phase by phase.
2. **Deferring scope is forbidden.** It is strictly FORBIDDEN to:
   - Mark sub-tasks as "future TODO", "pending", "out of scope", "next iteration".
   - Decide unilaterally that something is "too complex" and leave it undone.
   - Create tickets, issues or follow-up notes instead of implementing.
   - Close a phase with notes like "X is left pending" — if something is left, the phase is NOT closed.
   If the plan says it gets done, it gets done. If you discover that the plan is wrong and needs to change, see rule 5.
3. **Interrupting the flow is forbidden.** No non-blocking questions are asked to the user. Detail decisions (names, styles, microcopy, internal structure of a helper, which library to use for something trivial) are taken with your own judgement based on:
   - The context of the plan.
   - The conventions of the codebase (read neighbouring files).
   - The project rules (CLAUDE.md and the project context docs it points to).
   The only valid reason to interrupt is a **real technical blocker** (rule 4).
4. **Only valid reason to stop and ask:** a technical blocker that prevents continuing and cannot be solved with the available information. Valid examples:
   - A credential / environment variable is missing.
   - The plan assumes an API/service that does not exist.
   - There is an internal contradiction in the plan that cannot be solved by reading the code.
   - The user has to run something manually (e.g. a project-specific build or deploy step defined in CLAUDE.md) and the flow requires it.
   **Invalid** examples for stopping: "it is complex", "I'd rather confirm", "there are several ways to do it", "this may have side effects", "do you prefer A or B?", "shall I go on with the next phase?", "shall I switch profile and continue?", "do we go on with X now or do you prefer to validate/review first?". Crossing the boundary between profiles (e.g. backend→frontend) is **NOT** a blocker: it is an automatic switch (see rule 8), never a question.
5. **If you discover new scope during the implementation:**
   - **Needed for the current phase to work** → implement it silently, note it in one line inside the phase in the progress doc.
   - **Optional / tangential / improvement** → note it in a `## Findings` section at the end of the progress doc and CONTINUE. Do not implement it in this `/do-feature`.
   - **Contradicts the plan** → stop (rule 4), report the concrete contradiction to the user, wait for a decision.
6. **Operational definition of "phase complete":** a phase is closed `[x]` ONLY if:
   - Everything described in its section is implemented.
   - The code compiles / passes typecheck.
   - **If the project has a test suite:** the tests of the touched area —including those the plan assigns to this phase— are written and pass green. If the project has no test infrastructure, this point does not apply.
   - There are no TODOs, stubs, `NotImplementedError`, `throw new Error("TODO")`, or "// implement later" comments left.
   - The obvious side effects are handled (e.g. if you add a new endpoint, it is registered in the router; if you add a new item to a project registry, it is registered there).
   If any of this fails, the phase stays `[!]` and work on it continues.
7. **Using `TodoWrite` is forbidden.** The progress doc (in `docs/progress/` or `docs/rework/`) is the ONLY tracking source. If the project's `CLAUDE.md` forbids `TodoWrite`, that rule applies here too.
8. **Execution scoped by role/profile (if applicable).** If the project defines profiles and the progress doc splits the phases by profile (a `## Delegation` section or a profile tag per phase), "run all the phases" means **run the WHOLE plan, of all the profiles, until done** (except a testing phase marked manual). The boundary between profiles is **NOT a stopping point nor a question to the user**.

   - **Default behaviour: automatic and silent switch.** When you reach phases of another profile, **switch profile in the same session** — read its `SKILL.md`, adopt its scope and rules, leave a line in the progress doc noting the switch — and **continue without asking**. You keep the context already loaded; you do not hand control back to the user.
   - **The profile limit is about EDITING, not about execution.** While a profile is active you do not edit outside its scope; but that limit **never** authorizes you to stop the plan halfway and ask "shall I go on with the other part?". The split by profiles bounds *what you touch at each moment*, not *whether the task gets finished*.
   - **You stop at the boundary ONLY if:** (a) the user explicitly scoped the work to one profile ("do only the backend"); (b) the incoming profile needs a contract/artifact that does not exist yet and you cannot create it from here (real technical blocker → rule 4); or (c) you reach a testing phase marked **manual**. In those cases note the handoff in the doc and report it as **done**, **never** as a question like "do we go on now or do you prefer to validate first?".

   If the project does not define profiles or the doc does not split by role, run all the phases (default behaviour).

## Testing policy

Follow the testing policy in the project's `CLAUDE.md` (some projects defer tests to a final, manually triggered phase). If it has none, tests are planned and written within the phases (the rules above).

## Phase 1: Locate the progress file

Look for the progress file in `docs/progress/` (features from `/new-feature`) or in `docs/rework/` (reworks from `/rework`):

1. If the user specifies the name, look for `[name].md` in both folders
2. If they do not specify it, list the files available in both folders:
   - If there is exactly one, take it.
   - If there are several, list them and stop.

**If there is no progress file:** tell the user to use `/new-feature` (new functionality) or `/rework` (change over existing code) first.

## Phase 2: Analyse the current state

Read the progress file and determine:

1. **Completed phases**: marked with `[x]`
2. **Phase in progress**: marked with `[!]` (if any)
3. **Pending phases**: marked with `[ ]`
4. **Split by profile** (if the doc has a `## Delegation` section): which phases belong to the profile active in this session. Only those go in (see rule 8); those of another profile are left for its session.

Announce briefly which phase you are resuming from (one line, do not wait for confirmation) and start.

## Phase 3: Implementation

Resume from the first non-completed phase and run until the end of the plan without interrupting.

**CRITICAL RULE:** After completing EACH phase, update the progress file BEFORE continuing.

Flow for each phase:

1. Mark the phase as `[!] IN PROGRESS` in the file
2. Implement all the work of that phase (all of it, see rule 6 above)
3. Verify that it works (no compilation / typecheck / analysis errors)
4. Mark it as `[x] COMPLETED` and update the date (`Last updated`)
5. Move on immediately to the next phase (without asking for permission)

**FORBIDDEN:**

- Completing a phase and moving on to the next without updating the document
- Completing several phases and then updating the document all at once
- Forgetting to update the document
- Closing a phase partially
- Stopping between phases to ask for confirmation

## Phase 4: Final verification

When all the phases of the plan are complete, validate that the code compiles / passes typecheck / has no static analysis errors.

**The concrete commands depend on the project** — this skill is generic. To know what to run:

1. Check `CLAUDE.md` and the project documentation (typically `docs/technical/DEVELOPMENT.md` or equivalent) — the format / typecheck / lint / build commands for the stack will be there (Python with `make type-check`, Node/Bun with `bun run build`, Flutter with `flutter analyze`, Go with `go vet`, etc.).
2. If there are no clear docs, infer from the project:
   - `Makefile` → look for `format`, `lint`, `type-check`, `test` targets.
   - `package.json` → look at `scripts` (`build`, `typecheck`, `lint`).
   - `pyproject.toml` / `pre-commit-config.yaml` → configured tools.
3. Run the relevant commands **only for the touched areas** (do not run the frontend build if you only changed the backend). **If the project has a test suite, run it for those areas** —including the tests written in the phases— and leave it green; if it has no tests, skip it.
4. Fix any error (compilation, typecheck, lint or **red tests**) in the same `/do-feature` before considering the task complete. **They are not reported as "pending"**.
5. Mark the progress doc as complete in its header (`Overall status`).

## Phase 5: Report

Only when **everything** is finished, report to the user in a few lines:

- What was implemented (summary of completed phases).
- If there is a `## Findings` section in the progress doc, mention it.
- Suggested next step: `/update-docs` to close the task.

## Flow summary

```text
Locate progress → Analyse state → Implement ALL the phases without interrupting
  → Verify → Report at the end
```

**Note:** To close the task (update documentation and delete the progress file), use the `/update-docs` command.
