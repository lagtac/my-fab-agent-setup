---
name: my-changelog-management
description: >
  Use when editing CHANGELOG.md — recording a shipped feature, a deployment or
  config change, a user-visible bug fix, or a removed capability. Trigger on
  "add a changelog entry", "note the deploy change", "we just shipped X", "X is
  fixed on main", and "the env var changed". Owns the changelog scope,
  structure, dating, and commit discipline. A 🚧 → ✅ roadmap promotion is
  driven by my-roadmap-management; this skill writes the changelog half.
---

# Changelog

A CHANGELOG records the contract and behaviour changes that reached `main`. It is written for the people who deploy the project, use it, or depend on its output. Internal work earns no entry: refactors, tests, lint, formatting, and internal docs belong in the worklog.

A changelog looks backward. A roadmap looks forward. They meet at one moment: the integration that promotes a roadmap row from 🚧 to ✅. That edit touches both files in one commit.

## Adapting to the project

Resolve a project's conventions in this order, and never impose one it contradicts:

1. **Read `AGENTS.md`, then `CLAUDE.md`**, and `CLAUDE.local.md` when present. It may declare the changelog path, a custom contract heading, an entry format, and which changes earn an entry. It may also declare the git workflow. Its word wins over every default here, including the bold rows of the decision table and the commit rules. A project may want refactors logged, or the entry inside the feature's own commit.
2. **Reuse a changelog the project already keeps under another name**, such as `HISTORY.md` or `CHANGES.md`. Follow the format that file already uses.
3. **Fall back to the defaults**: `CHANGELOG.md` at the repo root, Keep a Changelog 1.1.0, and the headings in this skill.
4. **Ask when a file might be the changelog and nothing confirms it.** Never guess a convention into existence.

Scale each entry to whoever consumes the main branch:

- **Deployed app or service** → operators and end users. Operator-facing changes go under `### Deployment Contract`.
- **Library, SDK, or CLI** → API consumers. Mark breaking changes with `**BREAKING**` under `### Changed` or `### Removed`, and respect semver.
- **Data or ML pipeline** → whoever depends on the output. The project may define its own heading, such as `### Dataset Contract`. Follow what it declares.

When the project has no changelog and the user wants one, offer a Keep a Changelog header. Do not scaffold it silently.

## Files

- `CHANGELOG.md` — the path `AGENTS.md` or `CLAUDE.md` names, else a file under another name, else `CHANGELOG.md` at the repo root. Everywhere below, `CHANGELOG.md` means that file.
- The spec and plan for a shipped row. A local-markdown tracker keeps them at `.scratch/<slug>/spec.md` and `.scratch/<slug>/issues/NN-<slug>.md`. A GitHub-issue tracker keeps them in issues, listed with `gh issue list`. Take the links from the roadmap row or from the tracker, and ask when neither names one.

## Decision table

| Situation | Where it goes | Rule |
|---|---|---|
| Roadmap row promoted 🚧 → ✅ | Dated narrative entry inside `[Unreleased]`, in the same commit as the roadmap edit | 6, 9 |
| Deployment or config change (port, env var, runtime dep, package manager) | `### Deployment Contract` at the top of `[Unreleased]` | 5 |
| User-visible feature shipped without a roadmap row | `### Added` bullet | 4 |
| Behaviour or contract changed (route, response shape, default) | `### Changed` bullet | 4 |
| Bug fix to user-visible behaviour on `main` | `### Fixed` bullet | 4 |
| Feature, route, or runtime dep removed | `### Removed` bullet | 4 |
| Notable docs reorg (cross-referenced specs, audits) | `### Docs` bullet | 4 |
| Major coherent shipment (multi-aspect, several paragraphs) | `### YYYY-MM-DD — Title` dated narrative | 6 |
| **Refactor, test, lint, formatting, internal-only docs** | **No entry** — point the user to `my-worklog` | 2 |

If a change fits no row, ask the user before editing.

## Rules

### 1. Locate the `[Unreleased]` block

Read the changelog and find the current `## [Unreleased]` block. Some projects date it (`## [Unreleased] — YYYY-MM-DD`) and some do not. Keep the form the file already uses, with its subsection names.

### 2. Scope check — does it earn an entry?

Apply the decision table. Internal work gets no entry. Name it as internal in one line and tell the user that `my-worklog` records it. The test: would an operator deploying this, or a user reading release notes, care? When the answer is no, stop.

### 3. Pick a structure

Three forms coexist inside `[Unreleased]`:

- **Categorised bullet** (rule 4) for atomic changes.
- **Deployment Contract** (rule 5) for operator-facing config and deploy changes.
- **Dated narrative** (rule 6) for major coherent shipments.

Pick the form that fits the shape of the change.

### 4. Categorised bullet

Use one of `### Added`, `### Changed`, `### Fixed`, `### Removed`, `### Docs`. One bullet per change, in the past tense, in user-facing language, terse. Link the spec or plan when one exists:

```markdown
### Fixed
- Upload form now shows an inline message when Firefox 149 on Wayland sends an empty `DataTransfer`. See [the plan](<path to the plan>).
```

### 5. Contract heading — consumer-facing changes first

For a deployed app, place `### Deployment Contract` at the top of `[Unreleased]`, before `### Added`. Use it for port changes, new or renamed environment variables, package-manager migrations, new runtime dependencies, infrastructure requirements, and pipeline additions. Each bullet tells an operator what to do or know.

Follow the project type (see Adapting): use its own contract heading when it declares one. A library records a breaking API change under `### Changed` or `### Removed` with a `**BREAKING**` marker.

### 6. Dated narrative — major coherent shipments

When one feature needs more than three or four bullets, give it a subsection inside `[Unreleased]`:

```markdown
### YYYY-MM-DD — <Feature Name> (<Roadmap Reference>)

<One short paragraph: what shipped, and why.>

- <detail>
- <detail>
```

A roadmap promotion (🚧 → ✅) usually takes this form. Carry the roadmap reference, such as `Checkout #2b`, so a reader can find the row.

### 7. Update the `[Unreleased]` date

When the heading carries a date and that date is older than today, bump it to today. Never add a date to an undated heading. The date marks the latest contribution to the unreleased window.

### 8. Link to specs and plans

An entry whose change has a spec or a plan links to it inline. Roadmap rows and changelog entries meet through those shared links, and not through a link to each other.

Link discipline:

- **Same-repo targets use a relative `.md` path.** A changelog is read on the Git host and often exported to HTML for release notes. The host renders Markdown, and the build rewrites the extension, so an `.html` path in source breaks both views.
- **Out-of-repo targets use an absolute web URL.** A relative path that climbs out of the repo dies outside a local checkout that holds the sibling repo. Verify the target's default branch before you write the URL.
- **A moved, archived, or renamed doc gets its links repointed.** Run `git grep` on the old path across `CHANGELOG.md`, `ROADMAP.md`, and `docs/`.
- **An entry for a deleted doc is unlinked.** Keep the filename as plain text so the historical entry still reads.

### 9. Commit discipline

- **Changelog-only edits**: one commit, `docs(changelog): note <change>`.
- **Paired with a roadmap promotion (🚧 → ✅)**: one commit covers both files. `my-roadmap-management` rule 6 owns the message, usually `docs: mark <feature> shipped on roadmap and changelog`. A reader bisecting `main` must never see half of the pair.
- Run rule 10's link check first.

Use Conventional Commits in all cases.

### 10. Cross-check the entry you just wrote

- The entry sits in the right subsection. Deployment-contract changes go at the top of `[Unreleased]`, not under `### Added`.
- The change has landed on `main`. When you are unsure, ask before you commit.
- Rule 2 still holds: internal work gets no entry.
- Before the commit, run `/home/dchris/.config/opencode/skills/bin/link-check.py CHANGELOG.md`. Fix every `new` problem by rule 8: `html` → the `.md` twin's path; `climbs` → the absolute web URL; `dead` → the moved file's path, or unlink a deleted document and keep its name as plain text. Ask when you cannot tell which. List every `old` problem to the user, one line each, and leave it. If the script is missing or exits `2`, show its stderr line and check the new links by hand. Skip this run when the entry is the changelog half of a paired edit: `my-roadmap-management` rule 10 runs the check once on both files.

Skip broad scans such as orphan-entry sweeps. Run those only when the user asks for a changelog audit.

### 11. Entry content discipline — summarise the change, link the detail

An entry records what changed for whoever consumes the branch. It is not a copy of the spec, plan, experiment log, or worklog entry that explains the change. State the contract or behaviour delta in user and operator language, and link the detail (rule 8). Metrics, commit SHAs, per-phase play-by-play, and full verdict reasoning stay in the linked doc, which remains the source of truth.

A dated narrative (rule 6) is still a short framing paragraph plus bullets of what changed. Cut a figure that only re-proves a point the linked doc already makes. Keep the link. The companion `my-roadmap-management` rule 11 applies the same rule to roadmap rows.

## Common mistakes

- Logging a refactor or a test addition because it feels notable. Notable to whom? It gets no entry (rule 2).
- Burying a deployment-affecting change under `### Changed`. `### Deployment Contract` exists so operators see it.
- Adding an entry before the change lands on the main branch. Wait for the merge.
- Promoting a roadmap row to ✅ without the changelog half, or the reverse (rule 9).
- Renaming a plan file and repointing the changelog link while the roadmap link stays stale. Use `git grep` on the old path.
- Transplanting an experiment log's metrics, SHAs, or verdict reasoning into an entry (rule 11).
- Hardcoding `.html`, linking a cross-repo file by a relative path, or leaving a link to a deleted doc (rule 8).
