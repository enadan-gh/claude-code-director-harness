<!--
TEMPLATE, not a command. Copy it to <project>/.claude/commands/update-docs.md and adapt it there;
drop this comment in the copy (the frontmatter must open the file).
Project-specific steps go in "Step 4: Project-specific steps" of Phase 4.
-->
---
name: update-docs
description: Closing of completed tasks. Verifies the implementation, updates the documentation and deletes the progress file.
---

# Update Docs

Closing process for completed tasks. Updates all the project documentation.

## Phase 1: Identify the task to close

Look for active progress files in `docs/progress/` (features from `/new-feature`) and in `docs/rework/` (reworks from `/rework`):

1. List all the `.md` files in both folders
2. Identify the task to close:
   - If there is only one file (in either folder) → that is the one
   - If there are several but the conversation context makes it clear which one was just
     implemented (because we come from implementing it, we talked about it, or it
     matches the recent changes in git) → use that one without asking
   - Only ask if, after reviewing the context, it is still ambiguous which one to close
3. If there is none, tell the user and stop

Read the whole progress file to understand:

- What functionality was implemented
- Which files were affected (`Files`)
- The current state of each phase

## Phase 2: Verify the implementation

**CRITICAL RULE:** Do not trust that the document is up to date. Verify in the code.

For each phase marked as completed in the progress file (`[x] COMPLETED`):

1. Review the files mentioned
2. Confirm that the code exists and is implemented
3. If something is not implemented, tell the user and do NOT continue
4. **If the project has a test suite, run it as the final gate** (the task's areas, or the whole suite if it is fast): it must be green before closing. If something is red, do not close — report it to the user.

**If you find discrepancies:**

- List exactly what is missing
- Ask the user how they want to proceed
- Do NOT update the documentation until everything is really implemented

## Phase 3: Update the product document (if the project has one)

If the project keeps a product/requirements document (e.g. `docs/PRD.md` or equivalent), read it and update it. If it does not exist, skip this phase.

1. Add the new functionality in the corresponding section
2. Keep the document's existing format and style
3. Be concise but complete in the description

**Typical entry format (example for a PRD):**

```markdown
### [Feature Name]
- Short description of what it does
- Key implementation points
- Affected endpoints/screens (if applicable)
```

## Phase 4: Update the functional and technical documentation

The goal is for the project documentation to faithfully reflect what the code does NOW, not what it did before the change.

**Step 1: Find out where the project documentation lives.** Do not assume a fixed structure. Explore `docs/` to find the relevant folders. Common examples:

- `docs/product/modules/` — functional documentation per module (what each feature does, flows, business rules)
- `docs/implementation/` — technical documentation (architecture, decisions, integrations)
- `docs/technical/` — development guides, patterns, conventions
- Another structure of the project's own

**Step 2: Identify which documents need updating.** Look for documents that describe the functionality that was modified. If a document describes a flow that no longer exists or that changed, it MUST be updated. Also check whether the PRD (Phase 3) references module documents that should exist and do not — in that case, create them.

**Step 3: Update or create.**

- If the feature modified an existing flow: update the document to reflect the new flow
- If the feature is new and the project documents modules individually: create the corresponding document
- If it is a minor feature with no impact on existing documentation: this step can be skipped
- When in doubt, ask the user

**Step 4: Project-specific steps.**

<!-- PROJECT-SPECIFIC: extra documentation that only this project keeps in sync on closing (e.g. end-user help, in-app help, generated indexes). Empty in the template. -->

_None._

## Phase 5: Delete the progress file

**ONLY after completing the previous phases:**

1. Confirm with the user that everything is correct
2. Delete the file with **exactly** this command, from the repo root and with the relative path (no `cd`, no absolute paths, no quotes, no extra flags):
   - Features from `/new-feature` → `rm -f docs/progress/[task-name].md`
   - Reworks from `/rework` → `rm -f docs/rework/[task-name].md`

   This form is the one the global hook `rm-md-guard.sh` lets through without asking for permission; any other variant interrupts the automatic flow.
3. Tell the user that the closing is complete

## Flow summary

```text
Identify progress → Verify code → Update PRD.md → Update technical docs (if applicable) → [Confirmation] → Delete progress
```

## Reminder

This command is used AFTER:

- The implementation is complete
- The code has been verified (with the project's verification commands)
- The user has committed the changes
