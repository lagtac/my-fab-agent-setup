---
description: Push with pre-push checks
---

# Push instructions

Follow these steps in order. Stop and report on any abort condition — do not auto-resolve.

1. **Verify clean tree.** Run `git status --porcelain --untracked-files=no`. Untracked scratch files are ignored on purpose; they are not part of a push. If tracked changes exist, **stop and report** — do not auto-stash, do not commit on the user's behalf. Tell the user what's uncommitted and ask how they want to proceed.

2. **Detect upstream state.** Run `git fetch` first, so the comparison uses the remote's current state, then `git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null`.
   - **No upstream**: stop and report. Tell the user the current branch has no upstream and ask whether to push with `-u origin <branch>`. Do not set upstream automatically.
   - **Diverged from upstream** (run `git status -sb` and look for `[ahead N, behind M]` with both non-zero): stop and report. Never force-push without an explicit instruction from the user.
   - **Behind only** (`[behind M]`): stop and report. The user decides whether to pull first.

3. **Show what will be pushed.** Run `git log --oneline @{u}..HEAD`. If empty (nothing to push), tell the user and stop.

4. **Check the branch name.** If the current branch is `main` or `master`, stop and ask whether to push directly. A branch and a pull request is the default for anything larger than a small fix.

5. **Push to the remote.** Run `git push --dry-run` first and report a rejection from it. Then use plain `git push` — no `--force`, no `--force-with-lease`, no `--no-verify` unless the user has explicitly asked for them in this turn. If the push is rejected, including by a pre-push hook, report the rejection reason verbatim and stop; do not retry with force and do not try to satisfy the hook by rewriting commits.
