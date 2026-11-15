---
description: Cleans up all git branches marked as [gone] (branches that have been deleted on the remote but still exist locally), including removing associated worktrees.
---

## Your Task

Delete local branches whose upstream branch was deleted on the remote (`[gone]`), and remove their worktrees. Run this only because the user asked for it: merged branches are otherwise kept as a record, so never run it as a side step of other work.

Deleting a branch and removing a worktree cannot be undone from this command. So it lists first, asks, and removes nothing that has uncommitted work.

## Steps

1. **Refresh the remote state.** Without this, `[gone]` reflects the last fetch, which may be stale.

   ```bash
   git fetch --prune
   ```

2. **List the candidates.**

   ```bash
   git branch -v | grep '\[gone\]'
   git worktree list
   ```

   A `+` before a branch name means a worktree has it checked out. A `*` means it is the current branch.

   For each candidate, count the commits that are not in the current branch:

   ```bash
   git log --oneline HEAD.."<branch>" | wc -l
   ```

   Anything above zero is work that `git branch -D` destroys. A count above zero can also be squash-merged work: check `git log --oneline -20 HEAD` for a matching subject and note it in the table.

   If there are no `[gone]` branches, report `No [gone] branches; nothing to clean.` and stop.

3. **Check each worktree for uncommitted work.** For each `[gone]` branch with a worktree at `<path>`:

   ```bash
   git -C "<path>" status --porcelain
   ```

   A worktree with any output is **dirty**. It and its branch are skipped in step 5.

4. **Show the plan and ask.** Print one table: branch, last commit, unmerged commit count, worktree path or `none`, and the action. Use `delete`, `skip: current branch`, `skip: dirty worktree`, or `skip: unmerged commits`.

   A branch with a count above zero defaults to `skip: unmerged commits`. The user must name that branch in their reply before it can be deleted.

   Then ask with the `question` tool: `Delete as listed` or `Cancel`. If the `question` tool is not available, print the table, say `Reply "delete" to run it`, and end the turn. Delete nothing without an explicit approval, and never a `skip` row.

5. **Delete, one branch at a time.** For each branch marked `delete`:

   ```bash
   git worktree remove "<path>"     # only when it has a worktree; never --force
   git branch -d "<branch>"         # safe delete; refuses unmerged work
   ```

   Try `git branch -d` first. A squash-merged branch never looks merged to git, so it refuses that one. Use `git branch -D` only on a branch the user named in step 4, and report the commit it pointed at. If `git worktree remove` fails, report the error, skip that branch's deletion, and continue with the next branch.

6. **Report.** List the worktrees removed, the branches deleted and the branches skipped, each with its reason.
