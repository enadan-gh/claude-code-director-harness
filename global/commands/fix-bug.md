---
name: fix-bug
description: Bug diagnosis and fixing with exhaustive end-to-end analysis. Validates hypotheses in the code before proposing solutions.
---

# Fix Bug

Systematic process to diagnose and fix bugs.

## Phase 1: Gather information

Carefully analyse ALL the information the user provides:

- Error logs
- Screenshots
- Steps to reproduce
- Expected vs actual behaviour
- Any other relevant context

If critical information is missing, ask before continuing.

## Phase 2: Exhaustive investigation

**FUNDAMENTAL RULE:** Do not stop at the first clue or evidence.

1. Identify the complete flow involved in the error
2. Review the code of that flow end to end
3. If you find clues, follow them to the end
4. Do not assume anything until you have reviewed the whole flow

**NOT allowed:**

- Concluding without having reviewed the complete flow
- Stopping at the first anomaly found
- Assuming the cause without verifying it

## Phase 3: Hypothesis validation

**CRITICAL RULE:** NEVER present to the user a hypothesis you have not checked in the code.

Before communicating any finding:

1. Formulate your hypothesis internally
2. Verify in the code that the hypothesis is correct
3. Look for evidence that confirms OR refutes your hypothesis
4. Only when you are certain, move on to the next phase

## Phase 4: Diagnosis to the user

Once the root cause is validated, present to the user:

1. **Root cause:** What is causing the bug (with references to the code)
2. **Why it happens:** Clear explanation of the problem
3. **Evidence:** Where in the code the diagnosis is confirmed

## Phase 5: Solution proposal

Propose the solution, explaining:

1. What changes are needed
2. In which files
3. Why this solution solves the problem
4. **Regression test (if the project has a test suite):** the solution includes a test that **fails with the bug present and passes after the fix** (red→green) — it is the guarantee that the bug does not come back. Find out the project's test framework and convention (`CLAUDE.md` / `docs/technical/DEVELOPMENT.md` or equivalent) and follow its pattern; place the test next to those of the area. If the project has no test infrastructure, skip it and say so.

## Phase 6: Implementation and verification

After the user's confirmation, implement the fix **and its regression test** (if applicable). Before considering it closed:

1. Check that the regression test **failed before** the fix and **passes after** it.
2. Run the suite of the touched area (if the project has one) and leave it green — a fix must not break other tests.
3. Verify typecheck / lint of the area, according to the project's commands.

## Flow summary

```text
Information → Exhaustive investigation → Validate hypothesis → Diagnosis → Proposal (+ regression test) → [Confirmation] → Implementation + verification (red→green, suite green)
```
