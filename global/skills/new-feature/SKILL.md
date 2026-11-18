---
name: new-feature
description: Implementation of new functionalities with structured planning and a mandatory progress file.
---

# New Feature

Systematic process to implement new functionalities.

## Phase 1: Requirements analysis

Carefully analyse ALL the information the user provides:

- Description of the functionality
- Expected behaviour
- Use cases
- Any additional context

If critical information to start is missing, ask before continuing.

## Phase 2: Investigation of the existing code

**BEFORE planning**, investigate the current code:

1. Identify existing components that can be reused
2. Review the project's patterns and architecture
3. Look for similar code that can serve as a reference
4. Identify all the files that will be affected
5. **Check `${CLAUDE_SKILL_DIR}/skills-index.md`** to identify which global skills apply to this task (Python, React, forms, async, etc.). Include the relevant skills in the plan so they are invoked during the implementation

**NOT allowed:**

- Starting to plan without knowing the existing code
- Proposing solutions that duplicate existing functionality
- Ignoring the project's architectural patterns

## Phase 3: Create the progress file

**MANDATORY:** Before implementing ANYTHING, create a file in `docs/progress/[feature-name].md`

> **The `docs/progress/` folder already exists. Do NOT check whether it exists, do NOT try to create it. Write the file directly.**

The file MUST contain:

```markdown
# Progress: [Feature Name]
**Last updated**: YYYY-MM-DD HH:MM
**Overall status**: IN PROGRESS

## Description
[Short description of the functionality]

## Applicable skills
[Skills from the skills index to invoke during implementation, e.g. `example-python-style`, `example-react-forms`]

## Phase 1: [Description]
- **Files**: `path/file1.ext`, `path/file2.ext`
- **Status**: [ ] PENDING

## Phase 2: [Description]
- **Files**: `src/module/file.ext`
- **Status**: [ ] PENDING

[... more phases as needed ...]
```

**If the project defines implementation roles/profiles** (its `CLAUDE.md` will say so): tag each phase with the profile that implements it and add at the end a `## Delegation` section that splits the phases by profile, sets the order between profiles (which goes first according to the dependencies — e.g. backend before frontend if the latter consumes its contract) and notes the contract one profile must expose to another. If the project does not define profiles, skip this.

**If the project has a test suite**, plan the testing following the testing policy in the project's `CLAUDE.md`. If it has none, plan it in the progress file: which value/risk areas to cover (new branches, API/data contracts, validation), and whether the tests go **inside each phase** or in a dedicated **testing phase**. If there are profiles, in `## Delegation` the tests go to the profile that owns the code (backend→backend, frontend→frontend). Find out the project's framework and convention (`CLAUDE.md` / technical docs). If there is no test infrastructure, skip it.

**Present the plan to the user and wait for confirmation before continuing.** Exception: if the task was launched by a director brief that states the plan is already approved, do not wait.

## Phase 4: Implementation

**CRITICAL RULE:** After completing EACH phase, update the progress file BEFORE continuing.

Flow for each phase:

1. Mark the phase as `[!] IN PROGRESS` in the file
2. Implement all the work of that phase
3. Verify that it works (no compilation/analysis errors)
4. Mark it as `[x] COMPLETED` and update the date
5. Only then move on to the next phase

**FORBIDDEN:**

- Completing a phase and moving on to the next without updating the document
- Completing several phases and then updating the document all at once
- Forgetting to update the document

## Phase 5: Verification

When the whole implementation is complete, validate that the code compiles / passes typecheck / has no static analysis errors. **The concrete commands depend on the project** — find them out, do not assume them:

1. Check `CLAUDE.md` and the project documentation (typically `docs/technical/DEVELOPMENT.md` or equivalent): the format / typecheck / lint / build commands for the stack are there.
2. If there are no clear docs, infer it from the project: `Makefile` (targets `format`/`lint`/`type-check`), `package.json` (`scripts`), `pyproject.toml` / `.pre-commit-config.yaml`.
3. Run only what is relevant for the touched areas (do not run the frontend build if you only touched the backend). **If the project has a test suite, run it for those areas** —including the tests written in the phases— and leave it green.
4. Fix any error (compilation, typecheck, lint or **red tests**) before considering the task complete.

## Flow summary

```text
Requirements → Investigate code → Create progress file → [Confirmation] → Implement (phase by phase) → Verify
```

**Note:** To close the task (update documentation and delete the progress file), use the `/update-docs` command.

## Important reminder

If the context gets compacted or a new chat starts:

- **READ** first the corresponding progress file
- The file is the ONLY source of truth about what is done and what is left
