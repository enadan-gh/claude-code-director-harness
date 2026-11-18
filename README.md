# claude-code-director-harness

[Leer en español](README.es.md)

This is how I work with Claude Code. I build real products on my own, with Claude Code inside VS Code, and some friends asked me how I organise it. Instead of explaining it over and over, I put the files I actually use here, cleaned of anything personal and with comments on why each piece exists.

## What it is

A commented example of a way of working: one Claude Code session acts as a **director** that talks with me, decides with me and hands the work to **agents running in the background**, then reviews what they deliver. In one line: it is like talking to a project manager who has handed the work to their team.

The repository contains the files that make that possible: a skill for the director, two agent definitions (`worker` and `quick-fixer`), the workflow commands the agents follow, templates for per-project commands, a safety hook, example settings, and a full example of what a project repository carries (its `CLAUDE.md`, work profiles, a project hook and a deploy command).

It does not contain language or framework skills, and it is not a package you install.

## Who it is for

People who already use Claude Code on real work and want to see one concrete way of organising it: how to keep a long thread of decisions alive across compactions and new chats, how to delegate tasks to background agents without losing control, and how to keep permission prompts from interrupting you all day.

If you are starting with Claude Code, the official documentation is a better first stop. This comes after.

## Adapt, don't copy

This is what works for me, in my context: one person, several products, one working tree per project. It is not a recipe, and it is not meant to be installed and used as-is.

Several pieces are personal preferences (how the agent asks me questions, which model each agent uses, when tests are written, how much cleanup an agent may do). In the [guide](docs/guide.md) I present them as options and explain why I chose each one, so you can decide what fits how you or your team work. Take the ideas, read the files, and rewrite them for yourself.

## The working model

I open a Claude Code session in the project and activate the director profile. From then on I only talk and decide. The director reads the real code before giving an opinion, lays out options with their real cost and a recommendation, and records each decision I take, with my reason in my own words.

When something is decided, the director writes a **brief**: a self-contained task description with the closed decisions, what is out of scope, and how the task must end. It launches a `worker` agent in the background with that brief (or a `quick-fixer`, a cheaper agent, for small, already diagnosed fixes). The agent executes the whole task without stopping: plan, implementation, verification, commit and push, documentation close-out, and a short final report. Meanwhile the director stays available to me and prepares the next brief.

When the agent finishes, the director **reviews the delivery against the real diff**, never against the agent's summary. It reads the commits, repeats the key checks itself, and either approves or sends corrections to the same agent. Every round of this review has caught something the summary did not mention.

Everything lives in one **report**: a markdown file in the project with the context, the decisions table, the task queue, the session log and a cumulative test script. The report is the director's memory. It survives context compactions and new chats: if I open a new session tomorrow, I point the director at the report and it picks up the thread. That also saves tokens after a break: once the prompt cache has expired, any message in the old conversation re-sends all of it, while a new session only has to read the report (details in the [guide](docs/guide.md)).

## Repository map

| Folder | What it holds | Where it goes |
| --- | --- | --- |
| `global/` | Director skill (`skills/profile-director/`), agents (`agents/worker.md`, `agents/quick-fixer.md`), workflow commands (`commands/do-feature.md`, `commands/fix-bug.md`, `commands/rework.md`), the `new-feature` skill with its skills index, the `rm-md-guard.sh` hook and `settings.example.json` | `~/.claude/`, keeping the same subfolders. Merge `settings.example.json` into your own `~/.claude/settings.json` instead of overwriting it |
| `global/templates/` | `commit.md` and `update-docs.md`: templates, not commands | The source stays in `~/.claude/templates/`; an adapted copy goes to each project's `.claude/commands/` |
| `optional/` | `Explore`, which overrides the built-in Explore agent only to choose model and effort, and `web-fetch`, an extra lightweight agent that reads public web pages on a cheaper model | `~/.claude/agents/`, if you want them |
| `project-example/` | What a project repository carries: a `CLAUDE.md` template, five work profiles (`.claude/skills/profile-*`), a project hook that guards commits of protected files, project settings and a `/deploy` command | A project repository, replacing every `<placeholder>` |
| `docs/` | This documentation: the guide and the rules log, in English and Spanish | Nowhere; it is for reading |

## Getting started

1. **Read before copying.** Go through `global/skills/profile-director/SKILL.md` and `global/agents/worker.md` first; they hold the whole model.
2. **Copy and adapt the global part.** Copy the contents of `global/` into `~/.claude/`. Merge the hook registration and the deny rules from `settings.example.json` into your settings. The hook needs `jq` installed. Replace the fake entries in `skills/new-feature/skills-index.md` with your own skills.
3. **Prepare a project.** Copy `project-example/CLAUDE.md` and `project-example/.claude/` into your project and replace the placeholders. Create the project's `/commit` and `/update-docs` from `global/templates/`. Keep only the profiles that make sense for your stack.
4. **Open a session in the project** and activate the director: "activate the director profile" (or "director mode").
5. **Tell it what you want**, as you would tell a project manager. It will read the code, ask you what it needs to decide, and start launching agents.

An interactive setup command that asks about the optional preferences and generates the files for you is planned.

## Further reading

- [Guide](docs/guide.md): the roles, the report, a task's life, permissions, parallel directors and the optional preferences.
- [Rules log](docs/rules-log.md): each rule with the failure that produced it and why it is solved the way it is.
