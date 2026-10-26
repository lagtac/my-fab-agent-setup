---
name: my-git-squasher
description: Use when the user wants to squash, clean up, or consolidate consecutive minor commits (fix, chore, style, docs, formatting, cleanup) in git history. Also when invoked as /my-git-squasher.
---

# Git Squasher

Fold consecutive minor commits into one commit, and stop at commits that carry meaning of their own.

Boundaries matter: a `feat:` commit is usually the one a reviewer or a `git blame` reader wants to find, and squashing it into its neighbours destroys the record of why the change happened.

## Arguments

```
/my-git-squasher            # commits ahead of the default branch: main, else master, else HEAD~20
/my-git-squasher <ref>      # <ref>..HEAD
/my-git-squasher --dry-run  # print the plan, change nothing
```

## 1. Scope and safety

Base is the argument when given, else `main`, else `master`, else `HEAD~20`. Clamp it to the root commit (`git rev-list --max-parents=0 HEAD`) when the history is shorter than that, because every `git log <base>..HEAD` below fails outright on a base that does not exist. Resolve the base once and reuse it. The range is `<base>..HEAD`.

Inspect before touching anything:

```bash
git status --porcelain
git branch --show-current
git rev-parse --abbrev-ref '@{u}' 2>/dev/null   # upstream name, or nothing when there is none
git log --oneline '@{u}..HEAD'                  # only when an upstream exists
git log --merges --oneline <base>..HEAD
```

Stop and report, changing nothing, when:

- **The tree is dirty.** Ask the user to commit or stash. Never stash for them.
- **A commit in a squash group is missing from the upstream range**, so it is pushed. Squashing it needs a force-push. Continue only on an explicit yes in this conversation.
- **The branch is `main` or `master`.** Continue only on an explicit yes.
- **The range contains merge commits.** `git rebase -i` flattens them, and `git diff` cannot detect the loss because the files come out identical. Offer to squash only the linear commits after the last merge.

With no upstream, nothing is pushed and everything is safe to rewrite.

Once the checks pass, record the way back:

```bash
ORIG=$(git rev-parse HEAD)
git branch "backup/squash-$(date +%Y%m%d-%H%M%S)" "$ORIG"
```

## 2. Group

List the range oldest first, merges already excluded:

```bash
git log --no-merges --reverse --format="%h|%an|%s" <base>..HEAD
```

**Squashable**, case-insensitive: `fix:`, `chore:`, `style:`, `docs:`, each with or without a scope, and trivial unprefixed messages such as "cleanup", "fix typo", "update gitignore".

**Boundary**, keep: `feat:`, `refactor:`, `test:`, `breaking:`, `fixup!`, `squash!`, and anything the user marks keep.

Walk the log oldest first. Adjacent squashable commits form one group; a boundary ends it. Skip single-commit runs. Show a group that mixes authors, but leave it out of the plan unless the user adds it.

## 3. Plan and approval

Print each group with one proposed subject:

```
Group 2 (2 commits):
  474fdcf fix: improve tar archive paths
  9ade9d4 fix: set default path var to secrets
  → Proposed message: "fix: improve tar archive paths and secrets path default"
```

The message takes the strongest prefix in the group (`fix` > `chore` > `style` > `docs`), describes the whole group rather than the first commit, stays within 72 characters, and contains no single quote, because step 4 passes it inside single quotes.

`--dry-run` stops here.

Otherwise ask with the `question` tool: `Squash as proposed`, `Edit messages or exclude groups`, `Cancel`. Without that tool, print the plan, say `Reply "squash" to run it`, and end the turn. Never run step 4 without explicit approval.

## 4. Squash

No editor can be typed into, so never start one: `git rebase -i` without `GIT_SEQUENCE_EDITOR`, a `reword` line, and `git commit` without `-m` all wait for input and hang.

**The whole range is one group**, so skip the rebase:

```bash
git reset --soft HEAD~<N>     # N = commits in the group
git commit -m "<message>"
```

This makes the current user the author. Use it only when the group's author is the user; the rebase below keeps the author of the group's first commit, which is why it is the safe default for history someone else wrote.

**Otherwise**, do all groups in one rebase. Write a script that turns each group's later commits into `fixup` and amends the message after the last one:

```sh
#!/bin/sh
# ${1} is the rebase todo file. Repeat the pairs for each group.
sed -i \
  -e 's/^pick 431523a/fixup 431523a/' \
  -e 's/^pick d37d678/fixup d37d678/' \
  -e "/^fixup d37d678/a exec git commit --amend -m 'fix: improve YOLO export queries and mysql.sh diagnostics'" \
  "${1}"
```

Hashes come from step 2. The patterns match by prefix, so the todo and the log may abbreviate differently. Keep the braces in `${1}`: Claude Code substitutes `$1` with the skill argument.

Run it:

```bash
chmod +x <scratchpad>/squash-todo.sh
GIT_SEQUENCE_EDITOR=<scratchpad>/squash-todo.sh git rebase -i <base>
```

`<base>` is the parent of the oldest commit in the range.

On a conflict or any error: `git rebase --abort`, report the error verbatim, and stop. Do not resolve conflicts yourself.

## 5. Verify

```bash
git log --oneline <base>..HEAD
git diff "$ORIG" HEAD     # must print nothing
```

Output from `git diff` means the squash changed file contents. Stop, report it, and name the backup branch; `git reset --hard <backup-branch>` is the way back. Do not run that reset yourself.

On success, tell the user the backup branch name. Do not delete it.
