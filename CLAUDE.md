# CLAUDE.md

Rules for working ON this repository. It publishes a commented example of a Claude Code way of working: a director session that orchestrates background worker agents. It is meant to be **adapted**, not installed as-is. It holds methodology only, with no language or framework skills: each reader brings the skills they use.

---

## Layout

- `global/` — files a user copies to `~/.claude/` (director skill, agents, workflow commands, templates, hook, example settings).
- `optional/` — optional agents. `Explore` overrides Claude Code's built-in Explore agent only to choose model and effort; `web-fetch` is an additional lightweight agent (not an override) that reads public web pages on a cheaper model.
- `project-example/` — files a user copies into a project repo and adapts (`CLAUDE.md` template, profiles, project hook, settings, deploy command).
- `docs/` — human-facing guides.

## Source of truth

The model-read files are published from the maintainer's daily copies in `~/.claude`. Improvements are made and tested there first, then carried here with the rules below applied. Real use decides what is good; this repo is the showcase.

## Git

- Work on the `work` branch. **Never commit or push to `main`**; merging into `main` is the maintainer's call. This keeps the convention and means `main` only receives reviewed work.
- Explicit paths in `git add`; **never `git add -A` or `git add .`**, so nobody else's files (or the private report) get swept in.
- **No `--amend`, `--force` or `--no-verify`**: the history is the review record.
- One git operation per command: compound commands trigger a permission prompt per subcommand.
- Commit messages in English.

## Language

- **Every file the model reads** (everything under `global/`, `optional/` and `project-example/`) is in **English**, in a single version. No translated copies. One language for the model, another for people; English costs fewer tokens, and two versions of the same instructions drift apart.
- **Human-facing docs are bilingual**: English plus Spanish, the Spanish one as `*.es.md` or under a Spanish name (`README.md` / `README.es.md`, `docs/guide.md` / `docs/guia.md`, `docs/rules-log.md` / `docs/registro-de-reglas.md`). Update both in the same commit: there is little serious material on this in Spanish, and a pair updated separately drifts.

## Content rules

- **No personal data in tracked files**: no names, user names, emails, local paths (`C:\...`, `/home/...`), machine names, domains, or client/project names. Paths under `~/.claude/` are fine. The repo is public and the author is already identified by the repo itself. The single exception is the copyright holder's name in `LICENSE`: the maintainer chose to sign the license with his name.
- **No dates or `rule of <date>` tags inside the published files.** Inside the skills a rule stands on its own; its history (date, incident, reason) lives in `docs/rules-log.md` and `docs/registro-de-reglas.md`.
- Project-specific details in `project-example/` are always `<placeholders>`, never real values: it is a template each reader fills with their own stack.
- **Check claims about Claude Code's behaviour** (built-in agents, permissions, settings, cache) against the official documentation before they go into a file. A draft once described an optional agent as overriding a built-in one, and the docs said otherwise.

## The stream report

`docs/informe-stream.md` is the maintainer's working report and the director's memory: the director reads it whenever it directs work on this repo. What is forbidden is **publishing** it: it is gitignored, so **never commit it and never un-ignore it**, because it holds local paths and project names. Workers that write published files do not read it, so nothing from it leaks into them; the director passes them what they need in the brief.
