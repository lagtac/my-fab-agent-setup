---
name: my-roadmap-management
description: >
  Use when updating ROADMAP.md — adding an initiative, moving it between the
  Now/Next/Later horizons, or recording that an initiative shipped. Trigger on
  "update the roadmap", "add to the roadmap", "move X to next", "X shipped",
  "we finished X", and "what are we investing in". Owns the roadmap as a
  forward-looking index of initiatives. The tracker owns specs, tickets, and
  execution state; the changelog owns the release record.
---

# Roadmap Management

A roadmap answers one question: what are we investing in over the next while? It is a forward-looking index of **initiatives** over a rolling **horizon**. It is not a work tracker.

Three artifacts split the job:

- **Roadmap** — the investment decision. One row per initiative, ordered by horizon.
- **Tracker** — execution. Specs, tickets, blocking edges, and triage state.
- **Changelog** — the release record. What each release changed for users.

A roadmap row links its spec, or the tracker epic that holds it. It does not copy ticket state, and it never becomes a done-list.

## Adapting to the project

The paths and horizon names below are defaults. Resolve a project's real setup in this order:

1. **Read `AGENTS.md` or `CLAUDE.md`.** It may declare the roadmap path, the tracker kind, and the git workflow. Its word wins over every default here, including the commit rules.
2. **Reuse a roadmap the project already keeps under another name.** A file that already holds the project's forward index is the roadmap. Never create a second one.
3. **Fall back to `ROADMAP.md`** at the project root, with the horizons below.

Ask when a file might be the roadmap and nothing confirms it.

An existing roadmap may use a different shape: a feature-status machine (💭 📋 🚧 ✅), a done-log, or a flat checklist. In a project you do not control, follow it as-is. In your own projects, stop and report the mismatch. The user decides whether to keep it or migrate it.

When the project has no roadmap, create `ROADMAP.md` on the first **edit** request. Use this shape: a one-line intro, the horizon headings, and the row. A question gets an answer and an offer to create it.

```markdown
# Roadmap

What we are investing in over the next while.

## Now

- **<Initiative>** — <one sentence: what changes for the user>. [spec](<path to the spec>)

## Next

## Later
```

## Files

- `ROADMAP.md` — project root by default, or the path `AGENTS.md` or `CLAUDE.md` names. Everywhere below, `ROADMAP.md` means that file.
- The row's spec — held by the project's tracker. A local-markdown tracker keeps it at `.scratch/<slug>/spec.md`. A GitHub-issue tracker keeps it in an issue. Use the link a row already carries, and ask when neither the row nor the tracker names one.
- `CHANGELOG.md` — owned by `my-changelog-management`. This skill only suggests a release cut; it never edits that file.

## Horizons

Default: `Now` · `Next` · `Later`. A row sits in exactly one. Match a project's own horizon names when its roadmap already uses them, such as "This quarter / Next quarter / Later".

- **Now** — the team is actively investing. Being worked, or next in line.
- **Next** — agreed and queued. Not started.
- **Later** — worth doing, not scheduled.

**Confidence** is an optional annotation, not a horizon. Add `[confidence: low]` (or `medium`, `high`) only when a row's commitment is genuinely uncertain, usually in `Later`. Omit it when it adds nothing.

## Decision table

Look up the situation, then jump to the rule.

| Situation | Edit | Rule |
|---|---|---|
| User agrees to a new initiative | Add a row under a horizon; link the spec if one exists | 3 |
| Priority shifts | Move the row between horizons | 4 |
| Spec written for a queued row | Add the spec link | 5 |
| The initiative's work landed on main | Remove the row; suggest cutting a release | 6 |
| Scope or framing changed | Edit the row in place | 7 |
| One initiative splits into separate outcomes | Split into rows | 7 |
| An idea is dropped before work starts | Delete the row | 7 |
| One ticket blocks another | Nothing — the tracker owns it | 8 |
| Refactor, test, lint, or internal docs | Neither file | `my-changelog-management` rule 2 |
| A user-visible change with no initiative | Changelog only | `my-changelog-management` |

If a request fits no row, ask the user. A speculative roadmap row is noise.

## Rules

### 1. Read the roadmap before editing

Open `ROADMAP.md` and find the horizon section the row belongs to. Check the open rows against rule 9's row order. If some rows do not follow it, ask once, before the requested edit: "N open rows do not follow the row order, so they are hard to read cold. Rewrite them now, in a separate commit?" Ask at most once per session.

- **On yes:** rewrite every open row to rule 9's order, in one commit of its own, before the requested edit. Read a row's linked spec when the row alone does not say the outcome. Keep every number.
- **On no:** do the requested edit only. Trim each row you touch to rule 9's order.

### 2. Identify the change

Look up the user's request in the decision table and jump to the rule it points to. The table is the source of truth for which file to touch.

### 3. Add an initiative

A row goes in only after the user has agreed to the initiative in conversation. Casual mentions and brainstorm tangents do not earn a row.

- Choose the horizon. Default to `Next` unless the user says otherwise.
- Number the row only when the roadmap already numbers rows. Never reuse a number.
- Write the title in outcome language: what changes for the user, not the name of an internal step.
- Write one sentence of what the user gets.
- Link the spec if it exists. A row without a spec says `no spec yet`; the spec is the next step, not a precondition for the row.
- Add `[confidence: low]` only when the commitment is genuinely uncertain.

```markdown
- **<Initiative name>** — <one sentence: what changes for the user>. [spec](<path to the spec>)
- **<Initiative name>** — <one sentence>. no spec yet [confidence: low]
```

An icon is optional. Keep the one the file already uses, or use none.

### 4. Move a row between horizons

Edit the horizon and nothing else. A row moving to `Now` without a spec is allowed, but say so in one line: "This is now active without a spec. Write one?" Discovery work in `Now` is legitimate.

### 5. Add a spec link

When a spec exists, add the link. Link discipline:

- **Same-repo targets use a relative `.md` path.** The Git host renders Markdown, so an `.html` path breaks the hosted view.
- **Cross-repo targets use an absolute web URL.** A relative path that climbs out of the repo dies outside a local checkout.
- **A moved or renamed spec gets its links repointed.** Run `git grep` on the old path across `ROADMAP.md` and `docs/`.

### 6. Ship and roll off

When the initiative's work has landed on the main branch (verify with `git log` if unsure), **remove the row**. The changelog release is the record. There is no ✅ row and no done-list.

Then say one line: "An initiative shipped. Cut a release?" This is a suggestion, not a mandate.

If the user says yes, hand off to `my-changelog-management`. This skill does not edit `CHANGELOG.md`, and it does not require a same-commit pair.

### 7. Reframes, splits, and deletions

- **Reframe** — edit the row in place. Change the title only when it named an internal step rather than the outcome.
- **Split** — one initiative becomes two independently valuable outcomes. Give each its own row. When the pieces only make sense together, it is one initiative with several tickets, and the split belongs in the tracker.
- **Delete** — drop a `Next` or `Later` row that is off the table. No changelog note; the work never shipped.

### 8. Dependencies belong to the tracker

The tracker owns blocking edges: `Blocked by:` lines in local tickets, or native issue links. The roadmap expresses priority only, through the horizon.

Do not add a `Depends on` column. Do not write prose edges such as "blocked by row 4b". Do not reorder horizons to encode a dependency. When a reader needs the blocking relation, link the spec and let the tracker answer.

### 9. Row content discipline — index, not archive

A roadmap row is an index entry. The linked spec is the source of truth. Keep each row to:

- **Outcome** — what changes for the user, in one sentence.
- **Link** — the spec, or `no spec yet`.
- **Confidence** — only when it matters.

Target one outcome sentence, the link, and confidence when it matters. When a rendered row runs past three lines, trim it. Metrics, commit SHAs, per-phase history, and full verdict reasoning stay in the linked spec.

Why this is a rule: the row and the spec are two copies of one fact. Only the spec is maintained as ground truth. An oversized row silently goes stale and contradicts its own link.

### 10. Commit discipline

Roadmap-only edits get one commit:

- `docs(roadmap): add <initiative>`
- `docs(roadmap): move <initiative> to <horizon>`
- `docs(roadmap): drop <initiative>`

Use Conventional Commits. There is no paired changelog commit; strategy and releases are decoupled.

### 11. Cross-check the row you touched

Edit-scoped only:

- The horizon is one of the defined names.
- The spec link resolves. Before the commit, run `~/.config/opencode/skills/bin/link-check.py ROADMAP.md`. Fix every `new` problem by rule 5. List every `old` problem to the user, one line each, and leave it. If the script is missing or exits `2`, check the new links by hand.
- The row is outcome plus link, at index level.
- No ✅ row or done-list has crept back in.
- The markdown table or list is still well-formed.

Skip broad audits unless the user asks for a roadmap audit.

### 12. Suggest a release cut; never perform it

When an initiative ships (rule 6), the roadmap's only link to the changelog is the one-line suggestion. The user decides. If they accept, `my-changelog-management` cuts the release.

This keeps the two files decoupled. A reader who bisects `main` never needs a roadmap row and a changelog entry to land together.

## Common mistakes

- Treating the roadmap as a tracker: per-feature status, ✅ rows, or a permanent done-list.
- Requiring a spec before a row can exist. The spec is a link, not a gate.
- Adding a `Depends on` column or prose edges. The tracker owns blockers.
- Editing `CHANGELOG.md` from this skill, or forcing a same-commit pair.
- Keeping a shipped initiative on the roadmap. It rolls off; the changelog is the record.
- Pasting metrics, SHAs, or play-by-play into a row.
- Creating a second roadmap when one already exists under another name.
