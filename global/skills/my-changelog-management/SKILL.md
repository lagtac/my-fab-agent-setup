---
name: my-changelog-management
description: >
  Use when editing CHANGELOG.md: adding a user-visible change, cutting a release
  from commits, or noting a deploy or config change. Trigger on "add a changelog
  entry", "cut a release", "release notes", "we just shipped X", "X is fixed on
  main", and "the env var changed".
---

# Changelog

A changelog records what each release changed for the people who use or deploy the project. It looks backward. It is append-only and newest-first.

The unit is a **release**: a date-named section you cut when you want to report what changed. A release is not a git tag. In a project that never tags, "what reached main is released", and the date is the version.

Entries accumulate under `[Unreleased]` as merges land. Cutting a release freezes them under a date and opens a fresh `[Unreleased]`.

## Rules

### 1. Scope check — does it earn an entry?

Name the **reader**. A deployed app or service answers to operators and end users. A library or CLI answers to API consumers. A data or ML pipeline answers to whoever depends on the output.

Ask "notable to whom?" When no reader cares, the change earns no entry.

Internal work earns no entry: refactors, tests, lint, formatting, and internal docs. Say in one line that the change is internal and that `my-worklog` records it. Then stop.

Done when you have named the reader, or stopped.

### 2. Find the home

Resolve the project's conventions in this order, and let a stated convention win over every default below:

1. **Read `AGENTS.md`, then `CLAUDE.md`.** Each may declare the changelog path, an entry format, a contract heading, and which changes earn an entry.
2. **Reuse a changelog the project keeps under another name**, such as `HISTORY.md` or `CHANGES.md`. Follow the format that file uses.
3. **Fall back to the defaults**: `CHANGELOG.md` at the repo root, Keep a Changelog structure, and date-only release headings.
4. **Ask** when a file might be the changelog and nothing confirms it.

Then open the file and find the current `## [Unreleased]` block, or its equivalent. Keep the existing subsection names and date form. When the project has no changelog and the user wants one, offer a Keep a Changelog header. Add it once they accept.

Every lifecycle file opens with a front-matter block naming the skill that owns it. When you create `CHANGELOG.md`, put `skill: my-changelog-management` in that block above the title, and list the file under the `project lifecycle` heading in `AGENTS.md`.

Done when you know the file path and the block you will edit.

### 3. Write the entry

One bullet per change, past tense, in the reader's language, terse. Name the delta: the change in behaviour or contract the reader gets. Link the spec or plan when one exists, taken from the tracker or the roadmap row.

Rewrite for the reader instead of copying the linked doc. Metrics, commit SHAs, per-phase detail, and verdict reasoning stay in that doc, which remains the source of truth.

Group bullets under `### Added`, `### Changed`, `### Fixed`, `### Removed`, and `### Docs`. When no subsection fits, ask the user which one before editing.

```markdown
### Fixed

- Upload form now shows an inline message when Firefox 149 on Wayland sends an empty `DataTransfer`. See [the plan](<path to the plan>).
```

Done when the bullet names a reader-visible delta and cites its spec where one exists.

### 4. Contract and breaking changes

Deployed app: put `### Deployment Contract` at the top of `[Unreleased]`, before `### Added`. Use it for port changes, new or renamed environment variables, package-manager migrations, new runtime dependencies, and infrastructure requirements. Each bullet tells an operator what to do or know.

Library: record a breaking API change under `### Changed` or `### Removed` with a `**BREAKING**` marker. Bump semver only when the project tags.

Data or ML pipeline: follow any contract heading the project declares, such as `### Dataset Contract`.

Done when every deploy or breaking change sits under the heading its reader scans.

### 5. Cut a release

Run this when the user says "cut a release", accepts a roadmap suggestion, or picks a cadence.

1. **Find the boundary.** Read the last dated release heading. Its date is the boundary. Use the tag when one exists, otherwise `git log --since=<date> <main-branch>`. With no dated heading yet, start from the first commit.
2. **Generate a draft from Conventional Commits.** Run `git log <boundary>..HEAD --oneline` on the main branch, or `git log --since=<date> <main-branch> --oneline`. Map each commit:
   - `feat` → `### Added`
   - `fix` → `### Fixed`
   - `perf`, or a `refactor` with a user-visible effect → `### Changed`
   - `feat!` or `BREAKING CHANGE` → `### Changed` or `### Removed`, with `**BREAKING**`
   - a commit that removes a feature, route, or runtime dependency → `### Removed`
   - a user-facing `docs` change → `### Docs`
   - `test`, `chore`, `ci`, `build`, `style`, and internal `docs` → drop
3. **Rewrite for the reader.** Merge related commits into one bullet. A commit subject records what the author changed; the entry records what the reader gets.
4. **Freeze the draft.** Create a `## YYYY-MM-DD` heading and move the rewritten bullets and any existing `[Unreleased]` bullets under it. Keep the newest release first.
5. **Open a fresh `## [Unreleased]`** above it, or the project's equivalent.
6. **Name the release.** Use the tag when the project tags, otherwise the date is the version. A project that tags occasionally uses the tag on those releases and date-only headings on the rest. An entry stands without a tag.

Done when the date section holds every generated bullet and a fresh empty `[Unreleased]` sits above it.

### 6. Dated narrative for a major shipment

When one shipment needs more than three or four bullets, give it a subsection. Place it inside the release, or inside `[Unreleased]` before the cut:

```markdown
### YYYY-MM-DD — <Feature Name>

<One short paragraph: what shipped, and why.>

- <detail>
- <detail>
```

Link the spec. Done when the subsection reads as a summary and carries that link.

### 7. Link discipline

- **Same-repo targets use a relative `.md` path.** The Git host renders Markdown, so an `.html` path breaks the hosted view and the release-notes build.
- **Cross-repo targets use an absolute web URL.** A relative path that climbs out of the repo dies outside a local checkout.
- **Repoint the links of a moved, archived, or renamed doc.** Run `git grep` on the old path across `CHANGELOG.md`, `ROADMAP.md`, and `docs/`.
- **An entry for a deleted doc stays unlinked.** Keep the filename as plain text so the historical entry still reads.

### 8. Cross-check before the commit

- The entry sits under the heading its reader scans. Deploy changes go under `### Deployment Contract`, never `### Added`.
- The change has landed on the main branch. When you are unsure, ask before you commit.
- Internal work still has no entry, by rule 1.
- Run `~/.config/opencode/skills/bin/link-check.py CHANGELOG.md`. Fix every `new` problem by rule 7. List every `old` problem to the user, one line each, and leave it. If the script is missing or exits `2`, check the new links by hand.
- A broad audit of old entries runs only when the user asks for one.

Done when no `new` problem remains unresolved.

### 9. Commit

When the session asked for commits:

- **Changelog-only edit**: one commit, `docs(changelog): note <change>`.
- **A release cut**: one commit, `docs(changelog): cut release YYYY-MM-DD`.
- **Commit `CHANGELOG.md` alone.** A roadmap change lands in its own commit, so a reader who bisects `main` never needs the two together.

Use Conventional Commits. Done when `git show --stat HEAD` lists `CHANGELOG.md` and nothing else. When the session did not ask for commits, leave the edit in the working tree for the user's `/commit`.
