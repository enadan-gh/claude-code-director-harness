---
name: rework
description: Changes of direction, refactors, proofs of concept and reworks over code that already exists and works. For when it is neither a new functionality (/new-feature) nor a bug (/fix-bug). Creates a progress doc in docs/rework/. Triggered by phrases like "rework", "refactor", "change of direction", "experiment", "POC", "let's redo X".
---

# Rework

Systematic process for reworks: refactors, changes of direction, proofs of concept and experiments over code that already exists and works.

## When to use this skill

Use `/rework` when:

- The code to be touched ALREADY EXISTS in the repo
- It is NOT broken (if it were, use `/fix-bug`)
- It is NOT a new functionality from scratch (if it were, use `/new-feature`)

It fits one of these cases:

- **Refactor** — change of structure/shape of the code with no visible functional change
- **Change of direction** — the current solution is not convincing, we are going to redo it another way
- **POC / experiment** — we are going to try X; if we do not like it, we throw it away
- **Improvement / polish** — it works, but we want to improve it

## Phase 1: Gather the context of the change

Carefully analyse ALL the information the user provides:

- **What exists today** (which part of the code is to be touched)
- **Why it is to be changed** (motivation: does it not scale?, does it look ugly?, do we want to try something else?, is there technical debt?)
- **Type of rework**: refactor / change of direction / POC / experiment / improvement
- **Reversibility**: final or experimental (if we do not like it, we throw it away)?

If critical information is missing, ask before continuing.

## Phase 2: Investigation of the existing code

**BEFORE planning**, investigate the current code thoroughly:

1. Identify ALL the files involved (concrete file paths)
2. Understand how it works now — **do not assume, read the code**
3. Identify dependencies: which other modules/components consume what you are going to touch
4. Review the project's patterns and conventions (`CLAUDE.md`, `docs/technical/`)
5. **Check the global skills index** (`~/.claude/skills/new-feature/skills-index.md`) to identify which skills apply to this task (language, framework, forms, async, etc.). Include the relevant skills in the plan so they are invoked during the implementation.

**NOT allowed:**

- Planning without having read the code that is going to be touched
- Assuming how something works based on names
- Ignoring dependencies / consumers of the code that is going to change

## Phase 3: Create the progress file

**MANDATORY:** before implementing ANYTHING, create a file in `docs/rework/[rework-name].md`

> **The `docs/rework/` folder must exist in the project.** If it does not exist, create it before writing the file (rare case — it should already be there).

The file MUST contain:

```markdown
# Rework: [Rework Name]
**Last updated**: YYYY-MM-DD HH:MM
**Overall status**: IN PROGRESS
**Type**: refactor | change of direction | POC | experiment | improvement
**Reversibility**: final | experimental (if we do not like it, we throw it away)

## Description
[What is to be changed and why]

## Current state
[What exists TODAY, with concrete file paths:
- `backend/app/services/foo.py` — does X
- `frontend/src/features/.../Bar.tsx` — does Y
- ...]

## Proposed changes
[What will be left after the rework]

## Out of scope
[What is NOT touched even if it is close. Anti-scope-creep belt:
- The behaviour of X is NOT changed
- Module Y is NOT touched even if it is in the same package
- ...]

## Applicable skills
[Skills from the index to invoke during the implementation]

## Phase 1: [Description]
- **Files**: `path/file1.py`, `path/file2.tsx`
- **Status**: [ ] PENDING

## Phase 2: [Description]
- **Files**: `path/file.tsx`
- **Status**: [ ] PENDING

[... more phases as needed ...]
```

**If the project defines implementation roles/profiles** (its `CLAUDE.md` will say so): tag each phase with the profile that implements it and add at the end a `## Delegation` section that splits the phases by profile, sets the order between profiles (which goes first according to the dependencies — e.g. backend before frontend if the latter consumes its contract) and notes the contract one profile must expose to another. If the project does not define profiles, skip this.

**If the project has a test suite**, plan the testing following the testing policy in the project's `CLAUDE.md`. If it has none, plan it in the progress doc: which value/risk areas to cover (new branches, contracts, regressions; in a rework, above all **tests that guarantee the behaviour does not change**), and whether the tests go **inside each phase** or in a dedicated **testing phase**. If there are profiles, in `## Delegation` the tests go to the profile that owns the code (backend→backend, frontend→frontend). Find out the project's framework and convention (`CLAUDE.md` / technical docs). If there is no test infrastructure, skip it.

**Present the plan to the user and wait for confirmation before continuing.** Exception: if the task was launched by a director brief that states the plan is already approved, do not wait.

## Phase 4: Implementation

**CRITICAL RULE:** After completing EACH phase, update the progress file BEFORE continuing.

Flow for each phase:

1. Mark the phase as `[!] IN PROGRESS` in the file
2. Implement all the work of that phase
3. Verify that it works (no compilation/analysis errors)
4. **Respect the "Out of scope"**: if you discover you need to touch something that was excluded, STOP and check with the user before continuing
5. Mark it as `[x] COMPLETED` and update the date
6. Only then move on to the next phase

**FORBIDDEN:**

- Completing a phase and moving on to the next without updating the document
- Completing several phases and then updating the document all at once
- Crossing the "Out of scope" limit without explicit consultation

## Phase 5: Verification

When the whole implementation is complete, validate that the code compiles / passes typecheck / has no static analysis errors. **The concrete commands depend on the project** — find them out, do not assume them:

1. Check `CLAUDE.md` and the project documentation (typically `docs/technical/DEVELOPMENT.md` or equivalent): the format / typecheck / lint / build commands for the stack are there.
2. If there are no clear docs, infer it from the project: `Makefile`, `package.json` (`scripts`), `pyproject.toml` / `.pre-commit-config.yaml`.
3. Run only what is relevant for the touched areas. **If the project has a test suite, run it for those areas** —including the tests written in the phases— and leave it green.
4. Fix any error (compilation, typecheck, lint or **red tests**) before considering the task complete.

## Flow summary

```text
Context → Investigate existing code → Create file in docs/rework/
  → [Confirmation] → Implement (phase by phase, respecting out of scope) → Verify
```

**Note:** To close the task (update documentation and delete the progress file), use the `/update-docs` command.

## Important reminder

If the context gets compacted or a new chat starts:

- **READ** first the corresponding progress file in `docs/rework/`
- The file is the ONLY source of truth about what is done and what is left
- If it is an **experimental** rework, remember that the result may be thrown away — do not treat it as a canonical decision
