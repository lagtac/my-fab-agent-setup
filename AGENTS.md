# my-agent-skills

This repo is the source of my agent configuration. Shared content lives in `global/`. Each harness's adapter and plugins live in `harnesses/<harness>/`.

## Layout

- `global/` — shared, harness-agnostic content read by every harness: `AGENTS.md` (identity and rule index), `rules/`, `skills/`, `commands/`, `agents/`.
- `harnesses/` — one directory per harness, holding that harness's config files and plugins.
- `docs/` — repo-local docs, including the generated skills audit.
- `scripts/` — repo-local maintenance scripts, such as `skills_audit.py`.
- `tests/` — repo-local tests.

## Editing the global rules

Change universal rules in `global/rules/` and context rules in `global/rules/contexts/`. A universal rule file loads in every project on the next config change. A context rule file loads only where a project opts in, per `docs/rule-contexts.md`. Keep `global/AGENTS.md` harness-neutral; loading instructions belong in the harness adapter.

## Agent skills

### Issue tracker

Issues live as markdown files under `.scratch/<feature>/` in this repo. See `docs/agents/issue-tracker.md`.

### Triage labels

The default five triage roles keep their names: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
