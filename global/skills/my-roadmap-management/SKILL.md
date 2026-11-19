---
name: my-roadmap-management
description: >
  Use when updating ROADMAP.md — adding a feature, promoting between status
  tiers (💭 → 📋 → 🚧 → ✅), splitting or reframing a row, or marking
  something shipped. Trigger on phrases like "update the roadmap", "mark X
  as shipped", "X is done", "move X to in progress", "we just merged Y", or
  whenever a feature transitions lifecycle stages. Owns the roadmap;
  delegates the CHANGELOG half of a 🚧 → ✅ promotion to the
  `my-changelog-management` skill.
---

# Roadmap Management

A roadmap is **forward-looking** — what's next, in flight, or shipped recently. It is an index of the feature lifecycle: rows grouped by area, each one a tier, a spec or plan link, and a short body. It does not answer where the project is now, what happened on a given day, or what is queued. The status file, the worklog, and the tracker own those.

A CHANGELOG is **backward-looking** — what reached `main` and changed contract or behaviour. They couple at one moment: the integration (squash-merge by default) that promotes a row from 🚧 to ✅. At that moment both files update in the same commit (rule 6).

This skill owns the roadmap. The companion `my-changelog-management` skill owns the CHANGELOG. When a 🚧 → ✅ promotion happens, this skill drives the commit and delegates the CHANGELOG half to `my-changelog-management`.

## Adapting to the project

This skill works for any software project. The paths, git workflow, and legend below are **defaults**, not law. Resolve a project's real setup in this order:

1. **Read `AGENTS.md` or `CLAUDE.md`.** It declares the roadmap path, the tracker kind, and the git workflow: worktrees or not, the main/release branch name, and squash versus PR versus direct merge. Honour it over every default in this skill, including the commit rules. A project may keep more than one roadmap, so edit the one it names for this kind of change. Ask when it names none.
2. **Reuse a roadmap the project already keeps under another name.** A file that already holds this project's feature index is the roadmap. Never create a second one.
3. **Fall back to the defaults** in this skill: `ROADMAP.md` at the project root, the legend below, and the git workflow and tracker kind you find in the repo.

Ask when a file might be the roadmap but nothing confirms it. Never guess a convention into existence.

When an existing roadmap uses a different shape, such as a flat checklist or a done-log: in a project you do not control, follow it as-is. In your own projects, stop and report the mismatch. The user decides whether to edit it as-is or migrate it separately. Ask when you cannot tell which case applies.

When the project has no roadmap, create `ROADMAP.md` on the first **edit** request: the legend below, a one-line intro, and the row. A question about the roadmap gets an answer and an offer to create it.

## Files

- `ROADMAP.md` — project root by default, or the file `AGENTS.md` or `CLAUDE.md` names (for example `docs/frontend-roadmap.md`). Everywhere below, `ROADMAP.md` means that file. Living index of features. Owned by this skill.
- The row's spec and plan — held by the project's tracker. A local-markdown tracker keeps them at `.scratch/<slug>/spec.md` and `.scratch/<slug>/issues/NN-<slug>.md`. A GitHub-issue tracker keeps them in issues, listed with `gh issue list`. Use the links a row already carries. Ask when neither the row nor the tracker names one.
- `CHANGELOG.md` — project root. Touched only via `my-changelog-management` (delegated at rule 6).
- dev-report folder — `docs/dev-reports/` by default, used only when a dev report is written. Internal work (refactors / tests / lint / internal docs) gets no roadmap or changelog edit: `my-changelog-management` rule 2.

## Status legend

Default — match a project's own legend if its `ROADMAP.md` already uses one:

`✅ shipped` · `🚧 in progress` · `📋 planned` · `💭 discussed, not scheduled`

## Decision table

Look up the situation, then jump to the rule. Bold rows are the easy ones to get wrong.

| Situation | Files touched | Rule |
|---|---|---|
| Idea raised but user hasn't agreed yet | None — wait | — |
| User agreed to add an idea | ROADMAP only — new row, status `💭`, no link | 3 |
| Spec landed | ROADMAP only — `💭 → 📋`, link spec | 4 |
| Plan landed + work started | ROADMAP only — `📋 → 🚧`, link plan | 5 |
| **Integration to the main/release branch just landed** (squash, PR, or direct merge) | **ROADMAP + CHANGELOG in the same commit** — `🚧 → ✅` and add changelog entry | 6 |
| Scope or framing changed mid-flight | ROADMAP only — edit row in place, note pivot | 7 |
| One row growing into multiple sub-tasks | ROADMAP only — suffixed numbering (`1`, `1b`, `1c`) | 7 |
| **One row blocks another** | ROADMAP only — express as order, never as a graph | 12 |
| Speculative `💭` / `📋` row now off-table | ROADMAP only — delete row | 7 |
| Already-shipped feature later removed from `main` | The ✅ row **stays**; CHANGELOG gets the `### Removed` entry | 7 + `my-changelog-management` |
| **Any CHANGELOG-only edit** (deploy change, hotfix, removal, behaviour change with no roadmap row) | CHANGELOG only — use **`my-changelog-management`** | `my-changelog-management` |
| **Refactor, test, lint, formatting, internal-only docs** | **Neither** — see `my-changelog-management` rule 2 | `my-changelog-management` rule 2 |
| Plan file renamed or moved | Both files where the path is linked | 8 |

If a request fits no row, ask the user — premature roadmap entries and speculative changelog lines are noise.

## Rules

The rules are sequential and keyed by the decision table above.

### 1. Read ROADMAP.md before editing it

Open `ROADMAP.md` and find the area section the row belongs to (the `##` sections the file already has) plus the row's existing numbering context. Don't open `CHANGELOG.md` from this skill — if the edit pairs with a CHANGELOG entry (rule 6), `my-changelog-management` owns that file.

**Old rows.** While you read, check the open rows (💭, 📋, 🚧). If some of them do not follow rule 11's order — most often, the body does not open with the kind of work, such as `bug in …` or `feature in …` — ask the user once, before the requested edit: "N open rows do not follow the row order, so they are hard to read cold. Rewrite them now, in a separate commit?" Ask at most once per session.

- **On yes:** rewrite every open row to rule 11's order, in one commit of its own (`docs: rewrite ROADMAP rows in the row order`), before the requested edit. Read a row's linked document when the row alone does not say its kind or what the user sees. Never drop a fact that no linked document holds (rule 11). Keep every number. Change a title only when it names an internal step and not what changes for the user, and then update every reference to it. ✅ rows stay as they are: they are records.
- **On no:** do the requested edit only. The trim trigger in rule 11 still moves each row you touch.

### 2. Identify the lifecycle transition

Look up the user's request in the decision table above and jump to the rule it points to. The table is the source of truth for which files to touch — don't edit anything until the situation matches a row.

### 3. New row — idea → 💭

A new row goes in only **after** the user has agreed to the idea in conversation. Casual mentions and brainstorm tangents do not earn a row.

- Pick the area section that fits (or propose a new `## Section` if none does — confirm with the user).
- Choose the next free number, in the scheme the roadmap already uses: per table, the section's next `#`; with one sequence for the whole file, the next number the roadmap names (raise it by one in the same edit), or else the highest number in the file plus one. Use a suffix form like `1b`, `1c` when the row clearly extends a previous one. Never change or reuse a number, also when a row ships or is deleted.
- In a bullet roadmap, the number goes between the icon and the title: `- 💭 12 **<Short Name>** — …`. Tools that read the roadmap find it there.
- Status: `💭`. Spec/plan column: `—`. No link required at this stage.
- Title format: `**<Short Name>** — <body>`. The short name says what changes, in the words a user of the tool would use, not the name of an internal step. The body follows the order in rule 11.

### 4. Promote 💭 → 📋 — spec landed

Verify that the row's spec exists (see "Files"). If it doesn't, refuse the promotion — `📋` means "spec is written," not "we plan to write a spec."

- Update the status cell to `📋`.
- Add a markdown link to the spec in the Spec / Plan column: `[spec](<path to the spec>)`.
- In a project that routes its work, replace `route not set` with the route that was picked (rule 11).
- If the row body needs to grow (e.g., the spec materially reframed the feature), edit the short name and the row body to match — never leave the row contradicting its linked spec.

### 5. Promote 📋 → 🚧 — plan written and work started

Two preconditions, both required:

- The row's plan exists (see "Files").
- Implementation has actually started in an isolated workspace appropriate to the project's git workflow. If the project uses worktrees (see its `AGENTS.md` or `CLAUDE.md`), a worktree exists; if it uses branches, the feature branch exists; if it legitimately works on the main branch, "started" is enough. The point is real work underway — not a worktree per se. Don't withhold 🚧 in a project that doesn't use worktrees.

Then:

- Status → `🚧`.
- Spec / Plan column → `[spec](...), [plan](...)`. Keep both links if both exist.
- Do **not** touch the CHANGELOG yet. In-progress work has not changed any contract.

### 6. Promote 🚧 → ✅ — integrated to the main/release branch (couples with CHANGELOG)

This is the only transition that touches both files. **Both edits go in the same commit.**

Preconditions:

- The integration to the project's main/release branch has already happened — squash-merge, PR merge, or direct, whatever the project uses (verify with `git log` on that branch if uncertain — do not pre-emptively mark ✅ before it lands).
- The plan/spec links in the Spec / Plan column still resolve.

Roadmap edit:

- Status → `✅`.
- In a project that routes its work, a row that still says `route not set` gets its route here: a change whose route writes no spec skips the 📋 edit that would have set it (rule 11).
- Update the row body if the implementation diverged from the plan (this is common — the row should describe what shipped, not what was planned). Keep it in rule 11's order (kind, place and route; what the user sees; the fix; verdict; pointer); deep narrative belongs in the CHANGELOG and the linked docs, not the row (rule 11).

CHANGELOG edit (in the **same commit**): hand off to the `my-changelog-management` skill for scope, structure, dating, and linking. Both edits land in one commit (rule 9 below).

Commit message:

```
docs: mark <feature> shipped on roadmap and changelog
```

If multiple shipments land in one go, list them in the body.

### 7. Reframes, splits, deletions

- **Reframe** (scope or framing changed mid-flight): edit the row in place. Add one short clause to the row body explaining the pivot ("originally framed as X; reframed to Y after Z became clear"). Do **not** re-date the row.
- **Split** (one row grew into multiple sub-tasks): keep the parent's number, give children suffixed numbers (`1`, `1b`, `1c`). Match the existing pattern in the file — do not invent new numbering schemes.
- **Delete a 💭 / 📋 row**: allowed when the row is speculative and the user has agreed it's off the table. Note the deletion briefly in the next CHANGELOG entry's `### Removed` (or `### Docs`) section if a follow-up reader would otherwise wonder where it went.
- **Delete a ✅ row**: don't. Shipped rows are historical record. They stay even if the feature was later removed — note the removal as a fresh CHANGELOG entry under `### Removed`.

### 8. Linking discipline (roadmap side)

- Every roadmap row in `📋`, `🚧`, or `✅` status **must** link to its spec and/or plan. A row without a link is by definition `💭`.
- **Same-repo targets → relative `.md` paths** (such as `<path to the plan>`, written relative to the roadmap file); never hardcode `.html`. A relative `.md` link renders on the Git host's web UI (GitHub/GitLab serve the rendered Markdown), resolves in the repo, and opens in editors. If the project also exports docs to standalone HTML, the `.md`→`.html` extension is rewritten at *build* time — so authoring `.html` in source breaks the hosted and raw-repo views to "fix" a view the build already handles. Keep source links `.md`.
- **Out-of-repo / cross-repo targets → absolute web URLs**, not relative `../other-repo/...` paths. A path that climbs out of the repo only resolves on a local checkout that happens to have the sibling repo beside it — it is dead on the Git host's web UI and in any exported HTML. Link the hosted URL instead (e.g. `https://<git-host>/<group>/<repo>/-/blob/<default-branch>/<path>`); verify the target's default branch rather than assuming `main`/`master`.
- If a plan is **moved, archived (e.g. into an `archive/` folder), or renamed**, repoint *every* link to it — a move silently breaks the link in all views, the Git host included. Run `git grep` on the old path across `ROADMAP.md`, `CHANGELOG.md`, and `docs/`. CHANGELOG-side updates are owned by `my-changelog-management`.

CHANGELOG-side linking lives in `my-changelog-management`. The two files are tied together by their shared links to the row's spec and plan, not to each other directly.

### 9. Commit discipline (roadmap side)

- Roadmap-only edits (rules 3–5, 7): one commit. Message: `docs: <verb> ROADMAP for <feature>`.
- Roadmap + CHANGELOG paired edits (rule 6): **one commit**, never two. Message: `docs: mark <feature> shipped on roadmap and changelog`. Splitting them breaks atomicity — a reader bisecting `main` should never see a ✅ row whose CHANGELOG entry hasn't landed yet, or vice versa.
- CHANGELOG-only edits: see `my-changelog-management` rule 9.
- Run rule 10's link check first.

Use Conventional Commits in all cases (project rule).

### 10. Cross-check the row you just touched

Edit-scoped only — no full-file audits:

- The status reflects reality (the integration has actually landed for ✅; plan file actually exists for 🚧; spec file actually exists for 📋).
- Before the commit in rule 9, run `/home/dchris/.config/opencode/skills/bin/link-check.py ROADMAP.md`. Fix every `new` problem by rule 8: `html` → the `.md` twin's path; `climbs` → the absolute web URL on the Git host; `dead` → the moved file's path, or ask the user when no moved file exists. List every `old` problem to the user, one line each, and leave it. If `/home/dchris/.config/opencode/skills/bin/link-check.py` is not on `PATH`, or it exits `2`, show its stderr line (or say it is missing) and check by hand that the links in the row you touched resolve. In a paired edit (rule 6), run it once with both files, `/home/dchris/.config/opencode/skills/bin/link-check.py ROADMAP.md CHANGELOG.md`, and fix the changelog's `new` problems by `my-changelog-management` rule 8.
- The row body is still index-level and in rule 11's order (kind, place and route; what the user sees; the fix; verdict; pointer) — you didn't append numbers, SHAs, or play-by-play that a linked doc already owns (rule 11).
- The markdown table is still well-formed (no broken pipes, no missing cells).

Skip broad audits (stale-💭 sweeps, orphan-row scans). Run those only when the user explicitly asks for a roadmap audit. The link check reads the whole file, but fixing old links is audit work.

### 11. Row-body content discipline — index, not archive

A roadmap row is an **index entry**, not the record of the work. The linked spec / plan / experiment-log / briefing is the source of truth; the row points at it. The same fact must not be maintained in both places — when the linked doc is later corrected, a duplicated row silently goes stale and ends up contradicting its own link.

Keep in the row body, in this order, so that a reader who opens the roadmap cold knows what the row is without opening a link. Target: one sentence each for the first three parts, then the verdict and the pointer as short fragments (≤ ~5 lines in all):

- **Kind, place and route** — the kind of work (`bug`, `feature`, `rule` for a change to instruction text, or another kind the roadmap already uses), where it happens (the skill, file or area), and the route when it is already known. In a project whose rules route its work, the row names its route as those rules say, and `route not set` until one is picked. In a project that does not route its work, leave the route out. Examples: `bug in the export command.` and `feature in the settings page, route not set.`
- **What the user sees** — for a bug, what goes wrong for the person using the tool; for a feature, what they can do once it ships. Start from that effect, not from its cause in the code. Replace or define every term a reader may not know.
- **The fix or the goal** — one sentence. When no linked document holds the facts a fixer needs (the cause, the chosen approach), this sentence keeps them, because the row is their only record.
- **Current bottom line** — one line: shipped / NO-GO / blocked-on-X. Include a single figure *only when that figure is itself the verdict* (e.g. a NO-GO whose crux is "background-FP 51 vs 12") — one decisive number, not a metrics dump.
- **A pointer** — "detail in the linked X" when the row links somewhere.

Push to the linked doc, never copied into the row:

- Metrics and numbers (mAP, AUC, counts, thresholds, dates beyond the row's own status), commit SHAs, per-phase / per-experiment play-by-play, mechanism explanations, full verdict reasoning, supersession chains.

The one exception: a cause or a chosen approach that no linked document holds stays in the fix sentence, as above.

**Trim trigger** (applies whenever you write or edit a body — rules 3–7): if the body would run past the target above (~5 lines), or you're about to paste a figure or SHA that already lives in a linked doc, **compress instead of appending**. When you touch a row that has already accumulated history, trim it to the order above (kind, effect, fix, verdict, pointer) in the *same* edit — never add one more clause to an already-oversized cell. (Markdown table cells can't contain paragraph breaks, so an over-long cell can't even be reformatted into readable prose — the only available fix is less content.)

Why this is a rule and not a style preference: the row and the linked doc are two copies of one fact, and only the linked doc is maintained as ground truth. Most `ROADMAP.md` files state this contract in their own intro ("Keep this short — details live in the linked docs"). Enforce it on every edit, not just new rows.

### 12. Dependencies are expressed as order, not as a graph

A roadmap says what and roughly when. Blocking relations are execution detail — a tracker's job (issue relations), where they are structural rather than narrated. A roadmap absorbs a dependency by **making it an order**: if A blocks B, B sits in a later tier. Do not build a `Depends on` column. A roadmap that needs a real graph is telling you the work belongs in issues.

What to write instead, in escalating order of need:

- **Nothing.** If the priority/status tiers already put the blocker first, the dependency is expressed. Stop here — a prose edge that only restates the tier is pure decay surface.
- **One clause, one direction.** Where an edge genuinely changes the order, name the blocker *from the blocked row*: `Blocked by row 4b.` For a blocker outside the roadmap, such as a client's answer or a missing file, write `Waits for <what>.` in the same place. Never mix directions — "raises the ceiling on row 5" in one row and "the keying half is row 4b" in another forces the reader to parse each sentence for which way the arrow runs.

Two failure modes to watch:

- **Split-rot.** When rule 7 splits a row, inherited edge clauses keep pointing at numbers that no longer mean what they meant. A split keeps the parent's number, so an edge that now means a child still names the parent. Re-read every prose edge that names the parent, and point it at the parent or the child it now means.
- **Duplicate orderings.** A durable doc elsewhere may already sequence the work, such as an action plan's phases or a spec's phasing. Do not maintain a second copy. Keep one live ordering and link to it from the roadmap.

## Common mistakes

- Promoting 📋 → 🚧 just because a workspace was created — the plan file must exist first.
- Promoting 🚧 → ✅ before the integration has actually landed on the main/release branch (`git log` not yet showing it).
- Editing only the roadmap on a shipment, forgetting the CHANGELOG entry — or vice versa. The same-commit rule (9) is the safety net.
- Putting a refactor or a test addition in CHANGELOG. It gets no entry (see `my-changelog-management` rule 2).
- Deleting a ✅ row when the feature was later removed. Add a `### Removed` CHANGELOG entry instead; the historical row stays.
- Adding a 💭 row for a casual brainstorm tangent. Wait for explicit user agreement first.
- Narrating a dependency the priority tier already implies, adding a `Depends on` column, or leaving an edge pointing at a parent row whose work a split moved to a child (rule 12).
- Pasting metrics, commit SHAs, or per-phase history into a row body that the linked doc already records, or appending one more clause to an already-bloated cell. The row points at detail; it doesn't duplicate it (rule 11).
- Hardcoding `.html` in a link, or pointing at a cross-repo file with a relative `../other-repo/...` path. The first breaks the Git host's rendered view; the second is dead anywhere but a local checkout. Same-repo → relative `.md`; cross-repo → absolute URL (rule 8).
