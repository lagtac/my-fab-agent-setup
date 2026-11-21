# `/implement` skips TDD because the seams agreed in `/to-spec` are dropped by `/to-tickets`

**Type:** bug
**Impact:** TDD is silently skipped. An agent that follows the text literally writes tests after the code, because the precondition "pre-agreed seams" is never met.
**Target:** `mattpocock/skills`
**Source:** Observed in a ticket implementation session.

## Summary

The skills negotiate test seams in `/to-spec`, but that list never reaches `/implement`. `/to-tickets` writes tickets with no seam field. `/implement` then reads "where possible, at pre-agreed seams" and treats TDD as not possible.

## Reproduction

1. Run `/to-spec`. It asks you to agree the seams (`to-spec/SKILL.md:15-17`).
2. Run `/to-tickets`. The ticket template has no seam field (`to-tickets/SKILL.md:69-103`), so the seams are not written to the ticket.
3. Start a fresh session and run `@implement <ticket>`. The conversation context is gone, and the ticket carries no seams.
4. The agent reads `implement/SKILL.md:11`: "Call the Skill tool with 'tdd' where possible, at pre-agreed seams." No seam is pre-agreed.

## Expected

The agent stops and agrees seams first, per `tdd/SKILL.md:22`: "Before writing any test, write down the seams under test and confirm them with the user."

## Actual

The agent skips TDD silently and writes tests after the implementation.

## Root cause

The seam list has no owner across three files.

- `to-spec/SKILL.md:15-17` asks for seams, but the spec template (lines 21-75) has no dedicated seam section. "Testing Decisions" asks for "which modules will be tested," not the agreed seam names.
- `to-tickets/SKILL.md:69-103` publishes tickets with only "What to build," "Blocked by," and "Acceptance criteria." Seams are not carried forward.
- `implement/SKILL.md:11` assumes seams already exist and gives no instruction for when they do not. `implement-spec/SKILL.md:31` has the same gap: it tells each implementer subagent to call `tdd` but never says where the seams come from.

## Proposed fix

- Add a "Seams" subsection to the spec template in `to-spec/SKILL.md`, so the agreed seams are written down.
- Add a "Seams to test" line to both templates in `to-tickets/SKILL.md`, copied from the spec.
- In `implement/SKILL.md:11`, add the fallback: "If the ticket has no pre-agreed seams, stop and agree them with the user before writing any test."
- In `implement-spec/SKILL.md:31`, state that the ticket's seams are passed to each implementer, and must be agreed with the parent when missing.

## Environment

Skills installed under `~/.agents/skills` from `mattpocock/skills`. Agent: OpenCode. Add the install date or commit.
