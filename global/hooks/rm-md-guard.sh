#!/usr/bin/env bash
# PreToolUse hook for Bash: force a permission prompt for every `rm` that is not
# a plain deletion of progress documents. Staying silent lets the existing
# "Bash" allow rule approve the call, so silence must be reserved for provably
# safe cases.
#
# The safe case is judged by TARGET, not by syntax: every operand of `rm` (or
# `git rm`) must be a `.md` file living under docs/progress/ or docs/rework/.
# Quoting, `-f`/`-v`, absolute paths and Windows backslashes are all accepted,
# because the model picks a different spelling every time and none of them
# changes what gets deleted.
#
# A second safe case: a path that THIS SAME command creates (a `>`/`>>`
# redirection target or a `tee` operand) and then removes. That is a temporary
# scratch file (a debug test, a probe script), not existing work: the
# redirection has already overwritten whatever was there, and redirections are
# not gated by this hook anyway, so letting the matching `rm` through takes
# nothing away from the user.
#
# Compound commands are split on &&, || ; and newlines and inspected segment by
# segment. Heredoc bodies are data, not commands: they are dropped before
# splitting, unless they themselves mention `rm` (a `bash <<EOF` script), in
# which case we ask. Only the segments that mention `rm` are judged; the rest
# already run under the "Bash" allow rule (and its deny list), so this hook has
# no business second-guessing them.
#
# Contract:
#   - print an "ask" decision  -> Claude Code prompts the user
#   - print nothing, exit 0    -> falls through to the permission rules
# Any parsing doubt resolves to "ask" (fail-safe).

set -uo pipefail

ask() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"%s"}}\n' "$1"
  exit 0
}

pass() { exit 0; }

mentions_rm() {
  printf '%s' "$1" | grep -Eq '(^|[^[:alnum:]_.-])rm([^[:alnum:]_.-]|$)'
}

# A progress document: docs/progress/<name>.md or docs/rework/<name>.md,
# relative (optionally ./-prefixed) or absolute (POSIX, Git Bash /c/... or
# Windows C:/...), with no traversal and no glob characters.
is_progress_doc() {
  local path="$1"
  case "$path" in
    *..*|*'*'*|*'?'*|*'['*) return 1 ;;
  esac
  case "${path##*/}" in
    CLAUDE.md|README.md|.md) return 1 ;;
  esac
  printf '%s' "$path" | grep -Eq '^(\./|/[A-Za-z]/.*/|[A-Za-z]:/.*/|/.*/)?docs/(progress|rework)/[^/]+\.md$'
}

# Paths created by this very command: every `>`/`>>` redirection target and
# every `tee [-a|--append]` operand found in the heredoc-stripped text. Quotes
# are removed and backslashes normalised so the spelling matches what the rm
# operand will look like after the same treatment. `>&2`-style descriptor
# duplications and /dev/* targets are not files we create.
created=()
collect_created() {
  local text="$1" tok
  local operand='("[^"]*"|'"'"'[^'"'"']*'"'"'|[^[:space:];&|<>()]+)'
  while IFS= read -r tok; do
    [ -z "$tok" ] && continue
    tok=${tok//\\//}
    created+=("$tok")
  done < <(
    {
      printf '%s\n' "$text" \
        | grep -oE '>{1,2}[[:space:]]*'"$operand" \
        | sed -E 's/^>{1,2}[[:space:]]*//'
      printf '%s\n' "$text" \
        | grep -oE '(^|[^[:alnum:]_.-])tee([[:space:]]+(-a|--append))?[[:space:]]+'"$operand" \
        | sed -E 's/^.*tee([[:space:]]+(-a|--append))?[[:space:]]+//'
    } 2>/dev/null \
      | sed -E "s/^\"(.*)\"\$/\\1/; s/^'(.*)'\$/\\1/" \
      | grep -Ev '^(&|/dev/)'
  )
}

is_created_here() {
  local path="$1" c
  for c in ${created[@]+"${created[@]}"}; do
    [ "$c" = "$path" ] && return 0
  done
  return 1
}

is_safe_operand() {
  is_progress_doc "$1" || is_created_here "$1"
}

# Drops heredoc bodies from a multi-line command, leaving the command lines
# (including the `<<EOF` line itself). Sets $stripped. Asks if a body mentions
# `rm` (it may be a script fed to an interpreter) or is never terminated.
stripped=""
strip_heredocs() {
  local line term="" body="" trimmed
  stripped=""
  while IFS= read -r line || [ -n "$line" ]; do
    if [ -n "$term" ]; then
      trimmed="${line#"${line%%[!$'\t']*}"}"
      if [ "$trimmed" = "$term" ]; then
        mentions_rm "$body" && ask "rm inside a heredoc body"
        term="" body=""
      else
        body+="$line"$'\n'
      fi
      continue
    fi
    stripped+="$line"$'\n'
    if [[ "$line" =~ \<\<-?[[:space:]]*[\'\"]?([A-Za-z_][A-Za-z0-9_]*)[\'\"]? ]]; then
      term="${BASH_REMATCH[1]}"
    fi
  done <<< "$1"
  [ -n "$term" ] && ask "rm alongside an unterminated heredoc"
}

# Judges a single segment already known to mention `rm`.
check_rm_segment() {
  local segment="$1" token operands=0 git_mode=0

  # Nothing exotic is tolerated around an rm: no command substitution,
  # redirection, pipes or backgrounding. Quotes are fine (parsed below).
  case "$segment" in
    *'$('*|*'`'*|*'>'*|*'<'*|*'|'*|*'&'*|*'$'*)
      ask "rm with shell metacharacters" ;;
  esac

  # Backslashes only ever mean Windows path separators here; normalise them
  # before tokenising so that xargs does not read them as escapes.
  segment=${segment//\\//}

  local tokens=()
  if ! mapfile -t tokens < <(printf '%s\n' "$segment" | xargs -n1 printf '%s\n' 2>/dev/null); then
    ask "rm with unparseable quoting"
  fi
  [ "${#tokens[@]}" -eq 0 ] && ask "rm with unparseable quoting"

  if [ "${tokens[0]}" = "git" ]; then
    git_mode=1
    tokens=("${tokens[@]:1}")
  fi
  [ "${#tokens[@]}" -lt 2 ] && ask "rm without operands"
  [ "${tokens[0]}" != "rm" ] && ask "rm not in command position"

  local past_flags=0
  for token in "${tokens[@]:1}"; do
    if [ "$past_flags" -eq 0 ]; then
      case "$token" in
        --) past_flags=1; continue ;;
        -f|-v|-fv|-vf|--force|--verbose) continue ;;
        -q|--quiet) [ "$git_mode" -eq 1 ] && continue
                    ask "rm with disallowed flag: $token" ;;
        -*) ask "rm with disallowed flag: $token" ;;
      esac
    fi
    is_safe_operand "$token" || ask "rm of a target outside docs/progress or docs/rework and not created by this command: $token"
    operands=$((operands + 1))
  done

  [ "$operands" -eq 0 ] && ask "rm without operands"
}

input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null)
# Windows line endings would otherwise leave a stray \r on heredoc terminators.
cmd=${cmd//$'\r'/}

# Not a shell command we can read, or no `rm` anywhere: not our business.
[ -z "$cmd" ] && pass
mentions_rm "$cmd" || pass

# Heredoc bodies are data: drop them, then remember every path the remaining
# command lines create so that removing one of them counts as safe.
strip_heredocs "$cmd"
collect_created "$stripped"

# Split the compound command into segments on && || ; and newlines
sep=$'\x01'
split=${stripped//&&/$sep}
split=${split//||/$sep}
split=${split//;/$sep}
split=${split//$'\n'/$sep}

saved_ifs=$IFS
IFS=$sep read -r -d '' -a segments < <(printf '%s\0' "$split")
IFS=$saved_ifs

for segment in "${segments[@]}"; do
  # trim leading and trailing whitespace
  segment="${segment#"${segment%%[![:space:]]*}"}"
  segment="${segment%"${segment##*[![:space:]]}"}"
  [ -z "$segment" ] && continue
  mentions_rm "$segment" || continue
  check_rm_segment "$segment"
done

pass
