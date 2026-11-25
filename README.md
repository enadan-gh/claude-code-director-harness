# claude-code-director-harness

[Leer en español](README.es.md)

> **Constantly evolving.** This repository is a starting point that each person adapts to how they work. It does not accept contributions (issues and pull requests are closed), but you are free to copy it and adapt it to your needs; that is the whole idea.

## Set it up with your AI agent

Open Claude Code in your project and tell it: "Set up the director harness from https://github.com/enadan-gh/claude-code-director-harness in this project." You can also just give it the link in your own words and ask whether it fits you. You need Claude Code, because the harness is made of Claude Code skills and agents.

### Instructions for the agent

If a user gave you this repository's URL and asked you to set it up in their project, do this, in order. Whenever you need something from the user, ask in the chat, in plain words, and let them answer in their own words.

1. Do not install anything into the user's project yet. Your first message to the user is this explanation, in their language, in a message of its own, sent before any question or action that needs them: "Instead of asking the AI for things and checking every result yourself, you talk to it the way you would to a project manager. You tell it what you want, you decide together, and it hands the work to other AI agents, which do it while you keep talking. When they finish, it checks what they really changed before telling you. And it writes everything down in a document inside your project: what you decided, what is done and what is left. So tomorrow you open a new chat and it picks up where you left off. We call that role the 'director'." Give it whole: you may adapt it to their language, but do not drop or summarise any part of it. Then tell them you will now run an interview to build their own version.
2. Get a local copy of this repository OUTSIDE the user's project. You may read this repository however you need in order to follow these steps; what you agree with the user beforehand is where the local copy that stays on their machine goes (propose, for example, `~/claude-code-director-harness`). Then, if git is installed, run `git clone https://github.com/enadan-gh/claude-code-director-harness.git` into that folder; without git on the machine, download and extract <https://github.com/enadan-gh/claude-code-director-harness/archive/refs/heads/main.zip> there instead. Whether the user uses git is covered later by the init-harness skill.
3. Copy `global/skills/init-harness/` from that copy to `~/.claude/skills/init-harness/`. Tell the user that a permission prompt will appear because `~/.claude` is protected, and that this is expected, and go ahead: installing it is what they asked for, and the permission prompt is where they accept or decline. If that folder already exists, do not overwrite it: tell the user, and use the existing one only if it is identical to the copy, otherwise ask.
4. A skill copied during a session is picked up in that same session: run `/init-harness` now, using the local copy from step 2 as the reference repository (`<repo>`). If `/init-harness` is not available, read the copied `~/.claude/skills/init-harness/SKILL.md` and follow it step by step. Do not ask the user to restart.
5. Follow that skill's rules: plain language, a few questions at a time in chat, show what you will write before writing it, never overwrite.

This is the same route described in "Guided route" under "Getting started", driven by your agent.

This is how I work with Claude Code. I build real products on my own, with Claude Code inside VS Code, and some friends asked me how I organise it. Instead of explaining it over and over, I put the files I actually use here, cleaned of anything personal and with comments on why each piece exists.

## What it is

A commented example of a way of working: one Claude Code session acts as a **director** that talks with me, decides with me and hands the work to **agents running in the background**, then reviews what they deliver. In one line: it is like talking to a project manager who has handed the work to their team.

It is not an agent or a complete harness. Claude Code is the harness: the loop, the tools, the permissions. This is a layer of method on top of it: who decides, who executes, how the work is reviewed and where the thread is kept. The ideas could be adapted to other tools such as Codex, but the files are written for Claude Code and have only been tested there.

The repository contains the files that make that possible: a skill for the director, two agent definitions (`worker` and `quick-fixer`), the workflow commands the agents follow, templates for per-project commands, and a full example of what a project repository carries (its `CLAUDE.md`, work profiles, a project hook and a deploy command).

It does not contain language or framework skills, and it is not a package you install.

**Skills for your stack.** Each reader brings the skills for their own languages and frameworks. If you set it up with the guided route and want some, ask the harness keeper in your own words: it looks at your project's technologies, searches for skills ([skills.sh](https://skills.sh) is one place to find them, not the only one), proposes a few, checks each one before installing it and installs nothing without your yes.

## Who it is for

You need Claude Code. Beyond that, there are two ways in.

**If you do not program, or have not worked seriously with AI agents**, the guided route is your way in. You give Claude Code the link in your project. It explains the idea, asks what goes wrong for you today with AI and proposes only what fits. It does the technical part itself, copying and adapting the files, and shows you everything before writing it. It also works on small projects. What it solves is not about size: it is the AI touching what it should not, forgetting what was decided, or saying something is done without checking it.

**If you are technical**, use it to complete your own methodology, or take only some pieces: for example the report, the briefs, or the review against the real diff. The manual route is for that.

Either way, what you get is one concrete way of organising work with Claude Code: how to keep a long thread of decisions alive across compactions and new chats, how to delegate tasks to background agents without losing control, and how to keep permission prompts from interrupting you all day.

## Adapt, don't copy

This is what works for me, in my context: one person, several products, one working tree per project. It is not a recipe, and it is not meant to be installed and used as-is.

Several pieces are personal preferences (how the agent asks me questions, which model each agent uses, when tests are written, how much cleanup an agent may do). In the [guide](docs/guide.md) I present them as options and explain why I chose each one, so you can decide what fits how you or your team work. Take the ideas, read the files, and rewrite them for yourself.

## The working model

I open a Claude Code session in the project and activate the director profile. From then on I only talk and decide. The director reads the real code before giving an opinion, lays out options with their real cost and a recommendation, and records each decision I take, with my reason in my own words.

**Which model for the director.** My recommendation, not a requirement: activate the director with the most capable model you have, with high reasoning effort, chosen with `/model` before activating the profile. The director understands the problem, decides with you, writes the briefs and reviews against the real diff, so a mistake there spreads through every worker. The workers receive the reasoning already done in the brief, so a less capable model holds up there. The [guide](docs/guide.md) gives an example of current models.

When something is decided, the director writes a **brief**: a self-contained task description with the closed decisions, what is out of scope, and how the task must end. It launches a `worker` agent in the background with that brief (or a `quick-fixer` for small, already diagnosed fixes, which do not need the most capable model). The agent executes the whole task without stopping: plan, implementation, verification, commit and push, documentation close-out, and a short final report. Meanwhile the director stays available to me and prepares the next brief.

When the agent finishes, the director **reviews the delivery against the real diff**, never against the agent's summary. It reads the commits, repeats the key checks itself, and either approves or sends corrections to the same agent. Every round of this review has caught something the summary did not mention.

Everything lives in one **report**: a markdown file in the project with the context, the decisions table, the task queue, the session log and a cumulative test script. The report is the director's memory. It survives context compactions and new chats: if I open a new session tomorrow, I point the director at the report and it picks up the thread. That also saves tokens after a break: once the prompt cache has expired, any message in the old conversation re-sends all of it, while a new session only has to read the report (details in the [guide](docs/guide.md)).

## Repository map

| Folder | What it holds | Where it goes |
| --- | --- | --- |
| `global/` | Director skill (`skills/profile-director/`), the three guided-route skills (`skills/init-harness/`, `skills/harness-onboarding/`, `skills/harness-keeper/`), agents (`agents/worker.md`, `agents/quick-fixer.md`), workflow commands (`commands/do-feature.md`, `commands/fix-bug.md`, `commands/rework.md`) and the `new-feature` skill with its skills index | `~/.claude/`, keeping the same subfolders |
| `global/templates/` | `commit.md` and `update-docs.md`: templates, not commands | The source stays in `~/.claude/templates/`; an adapted copy goes to each project's `.claude/commands/` |
| `optional/` | `Explore`, which overrides the built-in Explore agent only to choose model and effort, and `web-fetch`, an extra agent that reads public web pages on a model chosen for that job | `~/.claude/agents/`, if you want them |
| `project-example/` | What a project repository carries: a `CLAUDE.md` template, five work profiles (`.claude/skills/profile-*`), a project hook that guards commits of protected files, project settings and a `/deploy` command | A project repository, replacing every `<placeholder>` |
| `docs/` | This documentation: the guide and the rules log, in English and Spanish | Nowhere; it is for reading |

## Getting started

There are two routes. The guided route needs no technical knowledge. The manual route is for technical people who want to choose and adapt the files themselves.

### Guided route (no technical knowledge needed)

Claude Code builds your own version with you and does the technical part itself.

1. **Give it the link.** Open Claude Code in your project and give it the link to this repository. Ask it to set it up, or just ask whether it fits you. The sentence under "Set it up with your AI agent" works too.
2. **Talk about what goes wrong.** It explains the idea and asks you a few questions, including what goes wrong for you today with AI. That is what decides whether it helps you. It proposes only the pieces that fit your project.
3. **Check before it writes.** It copies and adapts the files itself. It shows you what it will write before writing it, and it does not overwrite your files. Claude Code asks your permission when it copies into `~/.claude`; that is expected.
4. **Do a first small task together.** It agrees a small first task with you. Then open a new session in the project and say "start the onboarding" (`/harness-onboarding`). It does that task with you, the way every task will be done, and explains each part the first time it appears.
5. **Adjust it later.** To ask how something works, add or remove pieces or change a preference, say "adjust the harness" (`/harness-keeper`).

If you prefer to start it by hand: clone or download this repository, copy `global/skills/init-harness/` to `~/.claude/skills/`, open Claude Code in your project and run `/init-harness`. It will ask where you put the copy of this repository.

### Manual route (for technical people)

1. **Read before copying.** Go through `global/skills/profile-director/SKILL.md` and `global/agents/worker.md` first; they hold the whole model.
2. **Copy and adapt the global part.** Copy the contents of `global/` into `~/.claude/`. Replace the fake entries in `skills/new-feature/skills-index.md` with your own skills.
3. **Prepare a project.** Copy `project-example/CLAUDE.md` and `project-example/.claude/` into your project and replace the placeholders. Create the project's `/commit` and `/update-docs` from `global/templates/`. Keep only the profiles that make sense for your stack.
4. **Open a session in the project** and activate the director: "activate the director profile" (or "director mode").
5. **Tell it what you want**, as you would tell a project manager. It will read the code, ask you what it needs to decide, and start launching agents.

## Further reading

- [Guide](docs/guide.md): the roles, the report, a task's life, permissions, parallel directors and the optional preferences.
- [Rules log](docs/rules-log.md): each rule with the failure that produced it and why it is solved the way it is.

## License

MIT — see [LICENSE](LICENSE).
