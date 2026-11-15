# Git

- Use Conventional Commits: `type(scope): sentence`.
- Keep one logical change per commit. Do not bundle unrelated files.
- Read the staged diff before each commit.
- Use a branch and pull request for larger changes. Small fixes may go to main.
- Never create a git commit unless the user explicitly asks for one
- Prefer `git merge` over `git squash` whenever possible, unless the user explicitly asks for squash.
- Uncommitted changes are the user's review state - they read the diff before deciding what to commit
- Keep changes uncommitted until asked, so the diff stays clean and reviewable
