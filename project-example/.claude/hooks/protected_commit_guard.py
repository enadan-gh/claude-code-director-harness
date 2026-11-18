#!/usr/bin/env python3
"""Claude Code PreToolUse guard: human review before committing protected files.

This script runs before every Bash tool call. When the command is a ``git commit``
that touches a protected path (see PROTECTED_PREFIXES), the behaviour is:

  * If the command carries the approval token (see TOKEN; Claude sets it as an
    env-var prefix, e.g. ``PROTECTED_OK=1 git commit ...``), the hook returns
    ``permissionDecision: "allow"``. The token is Claude's explicit assertion that
    it has already reviewed the protected files per the project's CLAUDE.md, so no
    human prompt is needed.
  * Otherwise it returns ``permissionDecision: "ask"`` so Claude Code pauses. This
    is the fallback when a protected change is about to be committed without the
    token: the human reviews the files and approves only if they are correct.

Typical protected paths: user-facing translations, legal texts, generated
contracts, anything whose mistakes a compiler or a test suite will not catch.

Scope — only what actually enters the commit:
  * The gate looks at the files that *this* commit will contain, NOT the whole
    working tree. That is the staged set (``git diff --cached``) plus any explicit
    paths in a ``git add ...`` that precedes the commit in the same command (the
    ``git add X && git commit`` one-liner, where files are not staged yet when this
    PreToolUse hook runs).
  * This matters in a repo where several agents and the user edit in parallel: a
    protected file left dirty in the working tree by someone else must NOT block an
    unrelated commit that does not stage it. Only a commit that genuinely puts a
    protected file in is gated.
  * Sole exception: a wildcard add (``git add .`` / ``-A`` / ``--all`` / ``-u``)
    whose exact file set cannot be known from the command alone — there we fall
    back to the full working tree, conservatively, so protection is never lost.

Design notes:
  * No checker of any kind is run here. The "validation" is Claude's own review,
    asserted via the token; the ask is only the safety fallback.
  * For non-commit commands, or commits that touch no protected path, it stays
    completely silent (exit 0, no stdout) so the normal permission flow is
    untouched.
  * It fails OPEN: on any internal error it exits 0 without a decision. If you need
    a hard guarantee, add a git pre-commit hook that checks the same token in the
    environment as a backstop (keep the protected paths of both in sync).

Registration (project ``.claude/settings.json``)::

    "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command",
      "command": "python \\"${CLAUDE_PROJECT_DIR}/.claude/hooks/protected_commit_guard.py\\""}]}]}
"""

from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys

# --- Configuration ------------------------------------------------------------

# Repo-root-relative path prefixes to protect. Any file under one of these that
# enters a commit turns it into a "protected commit" that needs approval.
# Examples only: replace them with your own.
PROTECTED_PREFIXES = (
    "src/locales/",
    "docs/legal/",
)

# Approval token. When Claude prefixes the commit with ``PROTECTED_OK=1 git commit
# ...`` it asserts it already reviewed the protected files, so the hook allows it
# without prompting the human. Mention it in your CLAUDE.md or /commit command.
TOKEN = "PROTECTED_OK=1"

# --- Implementation -----------------------------------------------------------

# Flags on ``git add`` that stage an unknown set of files (cannot be resolved from
# the command text alone) -> conservative fallback to the full working tree.
_WILDCARD_ADD_TOKENS = {".", "-A", "--all", "-u", "--update", "-a"}

# Captures the argument list of every ``git add`` up to the next shell separator.
_GIT_ADD_RE = re.compile(r"git\s+add\b([^&|;\n]*)")


def _emit(decision: str, reason: str) -> None:
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": decision,
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )
    sys.stdout.write("\n")
    sys.exit(0)


def _repo_toplevel(cwd: str | None) -> str | None:
    """Repo root, so git paths are root-relative and match PROTECTED_PREFIXES
    regardless of the cwd the commit runs from."""
    try:
        return subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd or None,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip() or None
    except Exception:
        return cwd or None


def _run_git_paths(args: list[str], cwd: str | None) -> list[str]:
    out = subprocess.run(
        ["git", *args],
        cwd=cwd or None,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    paths: list[str] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        paths.append(line.strip())
    return paths


def _staged_paths(cwd: str | None) -> list[str]:
    """Paths already staged for commit (what ``git commit`` will write)."""
    return _run_git_paths(["diff", "--cached", "--name-only"], cwd)


def _git_status_paths(cwd: str | None) -> list[str]:
    """Every path with pending changes (staged, unstaged or untracked).

    Used only as the conservative fallback for a wildcard ``git add``.
    """
    out = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=cwd or None,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    paths: list[str] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        # Porcelain v1: "XY <path>" (3-char prefix). Renames: "<old> -> <new>".
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        if len(path) >= 2 and path[0] == '"' and path[-1] == '"':
            path = path[1:-1]
        paths.append(path)
    return paths


def _added_from_command(command: str) -> tuple[list[str], bool]:
    """Explicit paths staged by a ``git add`` in this command, plus a wildcard flag.

    Covers the ``git add X Y && git commit`` one-liner, where X/Y are not staged yet
    when this PreToolUse hook runs. Returns ([paths], wildcard) where wildcard is
    True if any ``git add`` uses ``.``/``-A``/``--all``/``-u`` (unknown file set).
    """
    paths: list[str] = []
    wildcard = False
    for match in _GIT_ADD_RE.finditer(command):
        args_str = match.group(1)
        try:
            tokens = shlex.split(args_str)
        except ValueError:
            tokens = args_str.split()
        for tok in tokens:
            if tok in _WILDCARD_ADD_TOKENS:
                wildcard = True
            elif tok.startswith("-"):
                continue  # other flags (-p, -v, ...) stage nothing by themselves
            else:
                paths.append(tok)
    return paths, wildcard


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # cannot parse input -> stay out of the way

    if data.get("tool_name") != "Bash":
        sys.exit(0)

    command = (data.get("tool_input") or {}).get("command", "") or ""
    if "git commit" not in command:
        sys.exit(0)  # not a commit -> no decision, normal flow

    if TOKEN in command:
        # Claude already reviewed the protected files and declared it with the token.
        _emit(
            "allow",
            f"Claude reviewed the protected files and declares it with {TOKEN}; "
            "no human review required.",
        )

    top = _repo_toplevel(data.get("cwd"))

    added, wildcard = _added_from_command(command)

    try:
        if wildcard:
            # Unknown staged set (git add . / -A): be conservative, look at the
            # whole working tree so protection is never lost.
            candidate = _git_status_paths(top)
        else:
            # Exactly what this commit will contain: already-staged files plus the
            # explicit paths added in this same command. NOT the whole working tree,
            # so a protected file left dirty by someone else never blocks this commit.
            candidate = _staged_paths(top) + added
    except Exception:
        sys.exit(0)  # fail open

    hits = [p for p in candidate if any(p.startswith(pref) for pref in PROTECTED_PREFIXES)]
    if not hits:
        sys.exit(0)  # no protected files entering the commit -> normal flow

    # Deduplicate while keeping order, for a clean message.
    seen: set[str] = set()
    unique_hits = [h for h in hits if not (h in seen or seen.add(h))]
    listing = "\n".join(f"  - {h}" for h in unique_hits)
    reason = (
        "This commit touches protected files:\n"
        f"{listing}\n\n"
        "Review them before approving. If they are correct, Claude should re-commit "
        f"with '{TOKEN} git commit ...' so this is not asked again."
    )
    _emit("ask", reason)


if __name__ == "__main__":
    main()
