---
name: deploy
description: Deploy the current state to production by merging into main and the deploy branch(es), then pushing. Evaluates first, shows the full plan and acts only after the user's explicit consent.
---

<!--
EXAMPLE. Adapt the branches, the migration check and the commands to your hosting.
The shape is what matters: evaluate -> show the plan -> explicit consent -> execute,
stopping at the first failure. Drop this comment in your copy.
-->

# Deploy

Deploy the current state to production by merging into `main` and the deploy branch(es), then pushing.

## Deploy branches

| Branch | Services |
| --- | --- |
| `<deploy-branch-backend>` | `<backend service>` |
| `<deploy-branch-frontend>` | `<frontend service>` |

## Phase 1: Full evaluation (before touching anything)

Before doing anything, gather ALL information needed to assess the deploy:

1. Run `git status` to check for uncommitted changes
2. Run `git log --oneline main..HEAD` to see commits ahead of main (if not on main)
3. Run `git log --oneline -1 main` and `git log --oneline -1 <deploy-branch>` for every deploy branch to see the current state of all branches
4. Run `git diff main..HEAD --name-only -- <migrations-dir>` to detect pending database migrations

**If there are uncommitted changes:** STOP and inform the user. Do NOT proceed.

## Phase 2: Show the plan and wait for consent

Present a COMPLETE summary to the user covering everything that will happen:

- Current branch and commits to merge
- Current state of deploy branches vs main
- **Pending migrations:** list them explicitly, or state "no pending migrations"
- If there ARE migrations: warn that they will need to be applied to production BEFORE pushing

**Wait for the user's explicit confirmation before proceeding.** Invoking this command is not that confirmation: the user confirms after seeing the plan.

## Phase 3: Merge to main

If NOT already on main:

1. Note the current branch name (to return later)
2. `git checkout main`
3. `git merge <source-branch>` (the branch we were on)

If already on main, skip this step.

**If merge conflict:** STOP and inform the user. Do NOT force anything.

## Phase 4: Merge to deploy branches

For every deploy branch: `git checkout <deploy-branch>` → `git merge main`

**If merge conflict on any branch:** STOP and inform the user.

## Phase 5: Apply pending migrations (if any)

If Phase 1 detected pending migrations, apply them BEFORE pushing:

1. Ask the user for explicit permission to run the migrations against production
2. Run `<migrate-production command>`
3. Verify with `<check-production-migration command>` that the migration was applied correctly
4. **If migration fails:** STOP and inform the user. Do NOT push.

If Phase 1 detected no migrations, skip this step entirely.

**Migrations MUST be applied before pushing** so the database schema is ready when the new backend starts.

## Phase 6: Push all branches

Push main and every deploy branch:

```bash
git push origin main <deploy-branch-backend> <deploy-branch-frontend>
```

## Phase 7: Return to original branch

Switch back to the branch the user was on before the deploy started.

## Summary

```text
Full evaluation (state + migrations) → Plan → [User confirms] → Merge to main → Merge to deploy branches
  → Apply migrations if needed [User confirms] → Push all → Return to original branch
```

**IMPORTANT:**

- NEVER force push
- NEVER skip merge conflicts
- ALWAYS confirm with the user before pushing
- If anything fails, STOP and report to the user
