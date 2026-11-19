---
name: my-changelog-management
description: >
  Use when editing CHANGELOG.md or cutting a release — recording a user-visible
  change, generating a release section from commits, or noting a deploy or
  config change. Trigger on "add a changelog entry", "cut a release", "release
  notes", "we just shipped X", "X is fixed on main", and "the env var changed".
  Owns the changelog scope, structure, dating, and commit discipline. Works
  without git tags: a release is a date-named section you cut by hand.
---

# Changelog

A changelog records what each release changed for the people who use or deploy the project. It looks backward. It is append-only and newest-first.

The unit is a **release**: a date-named section you cut when you want to report what changed. A release is not a git tag. In a project that never tags, "what reached main is released", and the date is the version.

Entries accumulate under `[Unreleased]` as merges land. Cutting a release freezes them under a date and opens a fresh `[Unreleased]`.

Internal work earns no entry: refactors, tests, lint, formatting, and internal docs. The worklog records those.

## Adapting to the project

Resolve a project's conventions in this order, and never impose one it contradicts:

1. **Read `AGENTS.md`, then `CLAUDE.md`.** It may declare the changelog path, an entry format, a contract heading, and which changes earn an entry. Its word wins over every default here, including the commit rules.
2. **Reuse a changelog the project already keeps under another name**, such as `HISTORY.md` or `CHANGES.md`. Follow the format that file already uses.
3. **Fall back to the defaults**: `CHANGELOG.md` at the repo root, Keep a Changelog structure, and date-only release headings.
4. **Ask when a file might be the changelog and nothing confirms it.**

Scale each entry to whoever consumes the main branch:

- **Deployed app or service** → operators and end users. Operator-facing changes go under `### Deployment Contract`.
- **Library, SDK, or CLI** → API consumers. Mark breaking changes with `**BREAKING**` under `### Changed` or `### Removed`. Use semver only when the project tags.
- **Data or ML pipeline** → whoever depends on the output. Follow any contract heading the project declares, such as `### Dataset Contract`.

When the project has no changelog and the user wants one, offer a Keep a Changelog header. Do not scaffold it silently.

## Files

- `CHANGELOG.md` — the path `AGENTS.md` or `CLAUDE.md` names, else a file under another name, else `CHANGELOG.md` at the repo root.
- The commits and tags that make up a release: `git log`, `git tag`.
- The spec or plan a change links to, taken from the tracker or the roadmap row.

## Decision table

| Situation | Where it goes | Rule |
|---|---|---|
| A user-visible change merged to main | `[Unreleased]` under `### Added`, `### Changed`, `### Fixed`, `### Removed`, or `### Docs` | 3 |
| A deploy or config change (port, env var, runtime dep, package manager) | `### Deployment Contract` at the top of `[Unreleased]` | 4 |
| A breaking API change (library) | `### Changed` or `### Removed`, with `**BREAKING**` | 4 |
| The user asks to cut a release | A new `## YYYY-MM-DD` section, built from the generated draft | 5 |
| A major coherent shipment (more than a few bullets) | A `###` subsection inside the release | 6 |
| Refactor, test, lint, formatting, internal docs | No entry — point to `my-worklog` | 2 |

If a change fits no row, ask the user before editing.

## Rules

### 1. Find the `[Unreleased]` block

Read the changelog and find the current `## [Unreleased]` block, or the project's equivalent. Keep the file's existing subsection names and date form.

### 2. Scope check — does it earn an entry?

Apply the decision table. Internal work gets no entry. Name it as internal in one line and tell the user that `my-worklog` records it. The test: would an operator deploying this, or a user reading release notes, care? When the answer is no, stop.

### 3. Add an entry

One bullet per change, in the past tense, in user and operator language, terse. Link the spec or plan when one exists.

```markdown
### Fixed
- Upload form now shows an inline message when Firefox 149 on Wayland sends an empty `DataTransfer`. See [the plan](<path to the plan>).
```

Group entries under `### Added`, `### Changed`, `### Fixed`, `### Removed`, and `### Docs`.

### 4. Contract and breaking changes

For a deployed app, place `### Deployment Contract` at the top of `[Unreleased]`, before `### Added`. Use it for port changes, new or renamed environment variables, package-manager migrations, new runtime dependencies, and infrastructure requirements. Each bullet tells an operator what to do or know.

For a library, record a breaking API change under `### Changed` or `### Removed` with a `**BREAKING**` marker. Bump semver only when the project tags.

### 5. Cut a release

The core flow. Run it when the user says "cut a release", or accepts the roadmap skill's suggestion.

1. **Find the boundary.** Read the last dated release heading. Its date is the boundary. Use the tag when one exists, otherwise `git log --since=<date> <main-branch>`. When there is no dated heading yet, start from the first commit.
2. **Generate a draft from Conventional Commits.** Run `git log <boundary>..HEAD --oneline` on the main branch, or `git log --since=<date> <main-branch> --oneline`. Map each commit:
   - `feat` → `### Added`
   - `fix` → `### Fixed`
   - `perf`, or a `refactor` with a user-visible effect → `### Changed`
   - `feat!` or `BREAKING CHANGE` → `### Changed` or `### Removed`, with `**BREAKING**`
   - a commit that removes a feature, route, or runtime dependency → `### Removed`
   - a user-facing `docs` change → `### Docs`
   - `test`, `chore`, `ci`, `build`, `style`, and internal `docs` → drop
3. **Rewrite each surviving commit into user and operator language.** Merge related commits into one bullet. Never paste a raw commit subject.
4. **Create a new `## YYYY-MM-DD` heading and place the rewritten draft there.** Merge in any `[Unreleased]` bullets that were already logged. Put the newest release first.
5. **Open a fresh `## [Unreleased]`** above it, or the project's equivalent.
6. **Name the release.** Use the tag when the project tags. Otherwise the date is the version.

Commit: `docs(changelog): cut release YYYY-MM-DD`.

### 6. Dated narrative for a major shipment

When one shipment needs more than three or four bullets, give it a subsection inside the release, or inside `[Unreleased]` before the cut:

```markdown
### YYYY-MM-DD — <Feature Name>

<One short paragraph: what shipped, and why.>

- <detail>
- <detail>
```

Link the spec. Keep it a summary, not a copy of the spec.

### 7. Generate, then edit

The generated draft is input, not output. A commit subject records what the author changed; the changelog records what the reader gets. Drop internal work, merge noise, and rewrite for the reader. This edit pass is the whole point of the flow.

### 8. Link discipline

- **Same-repo targets use a relative `.md` path.** The Git host renders Markdown, so an `.html` path breaks the hosted view and the release-notes build.
- **Cross-repo targets use an absolute web URL.** A relative path that climbs out of the repo dies outside a local checkout.
- **A moved, archived, or renamed doc gets its links repointed.** Run `git grep` on the old path across `CHANGELOG.md`, `ROADMAP.md`, and `docs/`.
- **An entry for a deleted doc is unlinked.** Keep the filename as plain text so the historical entry still reads.

### 9. Commit discipline

- **Changelog-only edits**: one commit, `docs(changelog): note <change>`.
- **A release cut**: one commit, `docs(changelog): cut release YYYY-MM-DD`.
- **No paired roadmap commit.** The two files are decoupled. A reader who bisects `main` never needs them to land together.

Use Conventional Commits.

### 10. Cross-check the entry you wrote

- The entry sits in the right subsection. Deploy changes go under `### Deployment Contract`, not `### Added`.
- The change has landed on the main branch. When you are unsure, ask before you commit.
- Rule 2 still holds: internal work gets no entry.
- Before the commit, run `~/.config/opencode/skills/bin/link-check.py CHANGELOG.md`. Fix every `new` problem by rule 8. List every `old` problem to the user, one line each, and leave it. If the script is missing or exits `2`, check the new links by hand.

Skip broad scans unless the user asks for a changelog audit.

### 11. Entry content discipline — summarise, link the detail

An entry records what changed for whoever consumes the branch. It is not a copy of the spec, plan, or experiment log. State the contract or behaviour delta in user and operator language, and link the detail.

Metrics, commit SHAs, per-phase play-by-play, and full verdict reasoning stay in the linked doc, which remains the source of truth.

### 12. No tags, no problem

When the project never tags, the date is the version. "Cut a release" means "report what changed since the last dated section", on whatever cadence the user chooses.

When the project tags occasionally, use the tag as the version for those releases and date-only headings for the rest. Never require a tag to add an entry.

## Common mistakes

- Logging a refactor or a test addition because it feels notable. Notable to whom? It gets no entry (rule 2).
- Burying a deploy-affecting change under `### Changed`. `### Deployment Contract` exists so operators see it.
- Adding an entry before the change lands on the main branch.
- Pasting raw commit subjects into a release instead of rewriting them for the reader.
- Requiring a tag or semver in a project that never tags.
- Forcing a same-commit pair with the roadmap.
- Transplanting an experiment log's metrics, SHAs, or verdict reasoning into an entry.
