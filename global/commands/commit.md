---
description: Structured commit workflow with conventional commits
model: opencode-go/deepseek-v4.1-flash#low
---

# Commit

The project's `AGENTS.md`, `CLAUDE.md` and `CLAUDE.local.md` set the rules for types, scopes, trailers and CHANGELOG entries. Read them and let them win over anything here. Run `git log --oneline -20` to see whether this project uses scopes.

**Group.** One commit per coherent change. When the diff covers unrelated work, split it.

**Show the plan first.** List the groups with their exact commit messages before the first commit. Then commit without asking again.

**Stage by explicit path.** `git add <paths>` only. No `-A`, no `.`, and no `-p` because it waits for input. If one file holds changes for two groups, stop and ask how to split it.

**Check each commit before writing it.** Run `git diff --cached` and read it in full. Confirm that only this group is staged, that the edit is intact, and that the message matches the diff.

**Hooks stay on.** Never `--no-verify` or `--no-gpg-sign`. When a hook fails, fix the cause and make a new commit. Do not `--amend` past it.

**Finish.** Run `git status` and `git log --oneline -n <N>`, where N is the number of commits you made.
