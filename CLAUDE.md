# CLAUDE.md

Rules for working ON this repository. This repo publishes a commented example of a Claude Code way of
working (a director session that orchestrates background worker agents); it is not an installable
package and it contains no language or framework skills.

## Layout

- `global/` — files a user copies to `~/.claude/` (director skill, agents, workflow commands,
  templates, hook, example settings).
- `optional/` — optional agents that override Claude Code's built-in ones only to choose model and
  effort.
- `project-example/` — files a user copies into a project repo and adapts (`CLAUDE.md` template,
  profiles, project hook, settings, deploy command).
- `docs/` — human-facing guides (when they exist).

## Git

- Work on the `work` branch. **Never commit or push to `main`**; merging into `main` is the
  maintainer's call.
- Explicit paths in `git add`; never `git add -A` or `git add .`. No `--amend`, `--force` or
  `--no-verify`.
- One git operation per command; commit messages in English.

## Language

- **Every file the model reads** (everything under `global/`, `optional/` and `project-example/`)
  is in **English**, in a single version. No translated copies of those files.
- **Human-facing docs are bilingual**: English plus Spanish, the Spanish one as `*.es.md` or under a
  Spanish name (e.g. `README.md` and `README.es.md`). Keep both versions in sync in the same commit.

## Content rules

- **No personal data**: no names, user names, emails, local paths (`C:\...`, `/home/...`), machine
  names, domains, or client/project names. Paths under `~/.claude/` are fine.
- No dates or "rule of <date>" tags inside the published files; the history of the rules lives in a
  separate rules log.
- Project-specific details in `project-example/` are always `<placeholders>`, never real values.
- `docs/informe-stream.md` is the maintainer's private working report: it is gitignored, never read
  it, never commit it, never un-ignore it.
