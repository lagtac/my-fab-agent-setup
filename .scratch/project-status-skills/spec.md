# Spec: Project status skills (`my-status`, `my-worklog`)

Status: ready-for-agent

## Problem Statement

An agent cannot reliably answer "what is next" or "where are we" in a project. The `my-todo` skill claims the phrase "what is next" but reads a `TODO.md` that many projects do not have. No skill reads a project's status file or its work queue. Each project tracks work differently: `my-agent-skills` uses local markdown, `anook` uses GitHub issues. The user wants one reusable, project-agnostic way to answer both questions.

## Solution

Add two skills to `my-agent-skills`: `my-status` and `my-worklog`. Reword `my-todo` so it stops claiming "what is next". Retire `my-dev-reports`.

`my-status` answers "where are we" and "what is next" from the project's status file and its work queue. `my-worklog` writes and reads a daily worklog. Both adapt to a project's existing setup and support both local-markdown and GitHub-issue trackers.

## User Stories

1. As a developer, I want to ask "where are we" and get the answer from the project's status file, so I do not rebuild state by reading the repo.
2. As a developer, I want to ask "what is next" and get the project's next work items, so I do not hunt through the tracker.
3. As a developer, I want "what is next" to read a GitHub-issue queue, so the answer is correct for `anook`.
4. As a developer, I want "what is next" to read a local-markdown queue, so the answer is correct for `my-agent-skills`.
5. As a developer, I want the skill to learn the tracker from `AGENTS.md` or `CLAUDE.md`, so I do not edit the skill per project.
6. As a developer, I want the skill to reuse a project's status file when it already has one under another name, so it does not create a duplicate.
7. As a developer, I want the skill to create `STATUS.md` when the project has none, so I can adopt it with one command.
8. As a developer, I want the status file to carry an "Updated" date, so stale state is visible at a glance.
9. As a developer, I want the status file to link to the tracker and docs, so it never duplicates their content.
10. As a developer, I want "what is next" to stop invoking `my-todo`, so it does not look for a missing `TODO.md`.
11. As a developer, I want `my-todo` to keep add, remove, mark-done, and list, so I can still manage a todo list when a project keeps one.
12. As a developer, I want to log the work day in `WORKLOG.md`, so the narrative record outlives the session.
13. As a developer, I want each worklog entry dated, so I can find a specific day's notes.
14. As a developer, I want the worklog to append and never rewrite, so past notes are preserved.
15. As a developer, I want `my-dev-reports` retired, so generated git reports stop competing with the worklog.
16. As a developer, I want the skills audit to pass, so I know the skill descriptions do not collide.
17. As a developer, I want both new skills model-invoked, so they trigger from a bare question.
18. As a developer, I want the skill to work in a project with no `AGENTS.md`, so adoption is not blocked.
19. As a developer, I want the skill to honour a project whose `AGENTS.md` names a different tracker path, so it respects the project.
20. As a developer, I want the status file to point to the product roadmap and changelog, so "where are we" can fan out to the right detail.
21. As an agent, I want a single rule "link, never duplicate", so I do not copy tracker state into `STATUS.md`.
22. As an agent, I want the project to tell me its tracker kind, so I run the right command.
23. As a developer, I want the skills installed through the existing linker, so they appear in both OpenCode and Claude.
24. As a developer, I want the same skills to work in any repo, so the effort pays off beyond one project.
25. As a developer, I want the worklog to hold decisions and handoffs, so the next session can pick up where this one stopped.
26. As a developer, I want "blocked" recorded in the status file with a link, so I see what waits on what.
27. As a developer, I want the status file to list only hand-picked "next" items, so it stays a decision and not a second queue.

## Implementation Decisions

- Two new skill directories under `global/skills/`: `my-status` and `my-worklog`, each with a `SKILL.md`.
- `my-status` triggers on "where are we", "what is next", "what's next", "what's left", "what's in flight", "what's blocked", "status". It owns the status file, default `STATUS.md` at the repo root.
- `my-worklog` triggers on "log the day", "worklog", "what did we do today", "end of day notes". It owns `WORKLOG.md` at the repo root.
- `my-todo` description is reworded: drop "what is next", "what's next", "what's left". Keep add, remove, mark-done, and list. It owns `TODO.md`.
- `my-dev-reports` is retired by marking it hidden (`disable-model-invocation: true` in its frontmatter). The files stay on disk. If `skills-lock.json` records the skill, update it.
- **Project flexibility.** Both new skills resolve a project's setup in this order: (1) read `AGENTS.md` or `CLAUDE.md` for the declared tracker, status file, and worklog paths; (2) reuse a file the project already keeps under another name; (3) fall back to the defaults `STATUS.md`, `WORKLOG.md`, and the tracker kind inferred from what exists.
- **Two tracker kinds are supported.** Local markdown (`.scratch/<slug>/spec.md` plus `issues/NN-<slug>.md`) and GitHub issues (`gh issue list`). The skill names both and picks by what the project declares or what exists on disk.
- `STATUS.md` has four sections: `Present state` (one line), `Active`, `Blocked`, `Next`. Each line links to a tracker item or doc. A dated "Updated" line sits at the top, and the file is edited in place.
- `WORKLOG.md` is append-only, one `## YYYY-MM-DD` heading per day, with short bullets for work done, decisions, and handoffs.
- The "link, never duplicate" rule lives in the `my-status` skill body and governs every section of the status file.
- Installation goes through `link_harnesses.py`. If the OpenCode skills directory is a plain copy rather than the symlink the linker wants, refresh it so the new skills appear.

## Testing Decisions

- There is one automated seam, the existing `skills_audit.py --check` script. The check is `python3 scripts/skills_audit.py --check --require-advertised my-status --require-advertised my-worklog`. It asserts both skills exist, are model-invoked, and that no description pair scores at or above the 0.4 Jaccard threshold.
- A good test covers external behaviour only. Here that is the audit script's collision, shadowing, and advertised checks; it never inspects skill prose.
- Live behavioural testing, such as asking "where are we" in a real project and confirming the answer, is out of scope. It is later work.
- Prior art: the existing `my-todo` and `my-roadmap-management` skills are audited by the same script. No unit tests exist for skill prose.

## Out of Scope

- Applying the skills to `anook`: creating its `STATUS.md`, `WORKLOG.md`, `CHANGELOG.md`, or editing its `AGENTS.md`.
- An `anook` ADR and glossary. An anook glossary is product-domain, not the status mechanism.
- Reconciling with the superpowers `status` and `handoff` skills.
- Live or runtime testing in any project.
- Editing any project's `AGENTS.md` to add a routing table. That is adoption, and later.

## Further Notes

- The two repos demonstrate the two tracker kinds: `my-agent-skills` uses local markdown under `.scratch/`, and `anook` uses GitHub issues. The skills must handle both without per-project forks.
- Reading `AGENTS.md` or `CLAUDE.md` first matches the existing `my-*` pattern, "match what exists".
- Run the audit after writing, because two skills that both mention "status" or "next" can trip the 0.4 collision threshold.
