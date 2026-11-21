# Workflow skills handoff

Date: 2026-11-19
Revised: 2026-11-20
Scope: the four workflow skills, from `e9471e9..172c8a7` to the rewrite in `d267623..8b8a4d5`.
State: rewrite landed. No open skill edits.

## Conclusion

The roadmap and changelog were rebuilt around the reader-decision-lifetime split. The tracker and ADR stay with Matt Pocock's skills.

## Current model

- `my-roadmap-management` holds the investment decision: one row per initiative under `Now`, `Next`, or `Later`, with optional confidence. It has no lifecycle machine, no ✅ rows, and no done-list. A shipped row is removed, and the skill suggests a release cut. The tracker owns blocking edges.
- `my-changelog-management` holds the release record. Entries accumulate under `[Unreleased]`; a cut freezes them under a date and opens a fresh block. The draft comes from Conventional Commits on the main branch, then is rewritten for the reader. A release needs no git tag.
- `my-status` is a rendered view over the tracker. It holds no fact of its own.
- `my-worklog` holds the narrative, decisions, and handoffs.
- Strategy and releases are decoupled. No commit edits both the roadmap and the changelog.

## Ownership

- Issue tracker: `to-tickets`, `triage`, and `setup-matt-pocock-skills`.
- ADR and glossary: `domain-modeling`.
- Spec and execution: `to-spec` and `implement-spec`.
- All under `~/.agents/skills/`. The tracker and spec skills are user-invoked.

## Verification

`python3 scripts/skills_audit.py --check --root global/skills` exits 0. The named-trigger check finds no trigger that names another skill.

Three description collisions exist elsewhere in the installed set: `deep-research` / `my-deep-research`, `built-in-browser` / `chrome-browser`, and `grill-me` / `grill-with-docs`. None involve these four.

## Open

Archive policy for old releases. The changelog is append-only and newest-first, with no rule to archive or split an old release.

## Next action

Decide the archive policy, or close the handoff.
