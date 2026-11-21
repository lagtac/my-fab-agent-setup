# `/implement` calls `/code-review` with no fixed point, and the prescribed diff cannot see uncommitted work

**Type:** bug
**Impact:** The review either misses the ticket's changes or fails on an empty diff. The agent then improvises a diff target instead of asking.
**Target:** `mattpocock/skills`
**Source:** Observed in a ticket implementation session.

## Summary

`implement/SKILL.md:15` calls code-review "once done," then commits at `:17`. The work is therefore uncommitted at review time. `code-review/SKILL.md:19` says to ask for a fixed point (the commit you diff against) if none was supplied. `/implement` never supplies or asks for one.

## Reproduction

1. Run `@implement <ticket>` without committing first, because the skill commits last.
2. It reaches code-review with no fixed point and with uncommitted changes.
3. Use a correct fixed point such as `main`. `git diff main...HEAD` then shows only committed work, so the ticket changes are invisible.
4. `code-review/SKILL.md:23` says an empty diff should fail there. It does, but the skill offers no path for reviewing uncommitted work.

## Expected

Either `/implement` passes the branch base as the fixed point and the review diffs against the working tree, or `/implement` commits before review so `...HEAD` includes the work.

## Actual

No fixed point is passed, and the skill has no instruction for the uncommitted case.

## Proposed fix

- Pick one ordering and state it. Either commit before review, or change the review to `git diff <fixed-point>` without `...HEAD`, which includes the working tree.
- In `implement/SKILL.md:15`, name the fixed point to pass, for example the merge-base with `main`.
- In `code-review/SKILL.md:19`, add the uncommitted case explicitly.

## Environment

Skills installed under `~/.agents/skills` from `mattpocock/skills`. Agent: OpenCode. Add the install date or commit.
