# Skills Index — Claude Code Global Skills

Reference index of global skills available in Claude Code. These skills contain best practices, patterns, and known issues that MUST be consulted before writing code in the relevant area.

**How to use:** Invoke a skill with the `Skill` tool (e.g., `Skill: example-python-style`) to load its full content into context before implementing code in that domain.

> **List here the skills you have installed.** The entries below are fake examples that only show the format: replace them with your own language, framework and tooling skills, grouped by area, each with when to use it and what it prevents. The workflows section at the end is part of this harness and stays.

---

## Example area: Python

| Skill | When to use | Prevents |
|-------|-------------|----------|
| `example-python-style` | Writing any Python code. Types, structure, config patterns. | Undefined variables, missing code paths, scattered config |
| `example-sql-migrations` | Schema changes and database migrations. | Non-idempotent migrations, unsafe data changes |

## Example area: React / Frontend

| Skill | When to use | Prevents |
|-------|-------------|----------|
| `example-react-forms` | Building or modifying forms. | Uncontrolled inputs, stale default values, validation drift |

### Example decision tree

```
Building/modifying a form? ──────────────── example-react-forms
Changing the database schema? ───────────── example-sql-migrations
Any Python code (types, structure)? ─────── example-python-style
```

---

## Workflows (global, project-agnostic)

Skill:

- `new-feature` — Create progress document for new features

Commands (`~/.claude/commands/`):

- `/rework` — Create progress document for reworks, refactors, POCs, or changes over existing code
- `/do-feature` — Resume implementation from progress file (works for both `docs/progress/` and `docs/rework/`)
- `/fix-bug` — Bug diagnosis and fix workflow

Per-project commands (each project keeps its own copy in `<project>/.claude/commands/`, built from the templates in `~/.claude/templates/`):

- `/commit` — Commit only the current task's files and push to the branch
- `/update-docs` — Close completed tasks, update documentation (handles both progress and rework files)

> Other project-specific commands and skills (deploy pipelines, role/profile skills, etc.) live in the project's own `.claude/`, not in this global index.
