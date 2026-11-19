# Workflow skills handoff

Date: 2026-11-19
Scope: commits `e9471e9..172c8a7`, the four workflow skills.
State: conclusion revised. No skill edits. Working tree clean.

## Conclusion

Rewrite `my-roadmap-management` and `my-changelog-management` from scratch. The current models answer the wrong question. The tracker and ADR already have owners in Matt Pocock's skills.

## Why

The reader-decision-lifetime split decides each artifact. A roadmap supports an investment decision for the team and stakeholders, over a rolling horizon. Its unit is an initiative or outcome. The current skill models a per-feature status machine (💭 📋 🚧 ✅) with permanent ✅ rows. That is a work tracker, and `to-tickets` and `triage` already own that job.

A changelog supports an upgrade decision for users and operators. Its unit is a release, and its source is the commits and tags that make up that release. The current skill hand-writes one entry per change. That duplicates git at change granularity.

## Already handled

- Issue tracker: `to-tickets`, `triage`, and `setup-matt-pocock-skills` for the tracker config and triage labels.
- Domain docs: `domain-modeling` owns `GLOSSARY.md` and `docs/adr/`.
- Spec and execution: `to-spec` and `implement-spec`.
- All live under `~/.agents/skills/`. `to-tickets`, `triage`, `to-spec`, `implement-spec`, and `setup-matt-pocock-skills` are user-invoked (`disable-model-invocation: true`).

## What the rewrite changes

Roadmap:

- Unit: initiative or outcome, not a feature ticket.
- Status: a horizon or confidence level, not 💭 📋 🚧 ✅.
- Links: the spec or epic in the tracker.
- Drop: ✅ rows, promotion rules, and dependency-as-order. Tickets carry blocking edges.
- Keep: short rows, links over copies, one owner per fact.

Changelog:

- Unit: release.
- Source: commits and tags, grouped and rewritten for users.
- Flow: curate at release time, or generate and then edit.
- Drop: per-change hand entries as the primary flow.
- Keep: user and operator language, internal work excluded, links to detail.

## Consequence

The current hard dependency, roadmap to changelog at the 🚧 → ✅ promotion, disappears. Strategy and releases decouple.

## Open decisions

1. Roadmap horizon: now/next/later, or themes with no dates.
2. Row link target: spec, epic, or the ticket set.
3. Changelog source: generated from Conventional Commits, or hand-curated at release.
4. Archive policy for old releases.
5. Whether `my-status` survives the tracker dashboard. Secondary.

## Next action

Rewrite the two skills against this model. No edits made.
