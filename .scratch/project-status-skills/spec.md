# Spec: Status, worklog, roadmap, and changelog skills

Status: done

## Problem Statement

An agent cannot reliably answer "what is next" or "where are we" in a project. The `my-todo` skill claims "what is next" but reads a `TODO.md` that many projects do not have. No skill reads a project's status file or its work queue. The `my-dev-reports` skill generates git reports that compete with a narrative worklog. Each project tracks work differently: `my-agent-skills` uses local markdown, and `anook` uses GitHub issues. The roadmap and changelog skills are long, tightly coupled, and follow an older pattern. The user wants one project-agnostic skill suite for status, worklog, roadmap, and changelog.

## Solution

Add two skills, `my-status` and `my-worklog`. Delete `my-todo`, `my-dev-reports`, and `my-briefing`. Refactor `my-roadmap-management` and rewrite `my-changelog-management` to match the new pattern. Write every touched skill with the `writing-for-agents` skill. Install the skills through the existing linker, and prove them with the skills audit.

`my-status` answers "where are we" and "what is next" from the project's status file and work queue. `my-worklog` writes and reads a daily worklog. The roadmap and changelog skills keep their jobs and adopt the same project-resolution order. All four skills work with local-markdown and GitHub-issue trackers.

## User Stories

1. As a developer, I want to ask "where are we" and get the answer from the project's status file, so I do not rebuild state by reading the repo.
2. As a developer, I want to ask "what is next" and get the project's next work items, so I do not hunt through the tracker.
3. As a developer, I want "what is next" to read a GitHub-issue queue, so the answer is correct for `anook`.
4. As a developer, I want "what is next" to read a local-markdown queue, so the answer is correct for `my-agent-skills`.
5. As a developer, I want the skill to learn the tracker from `AGENTS.md` or `CLAUDE.md`, so I do not edit the skill per project.
6. As a developer, I want the skill to reuse a status file the project already keeps under another name, so it does not create a duplicate.
7. As a developer, I want the skill to create `STATUS.md` when the project has none, so I can adopt it with one command.
8. As a developer, I want the status file to carry an "Updated" date, so stale state is visible at a glance.
9. As a developer, I want the status file to link to the tracker and docs, so it never duplicates their content.
10. As a developer, I want "what is next" to stop invoking `my-todo`, so it does not look for a missing `TODO.md`.
11. As a developer, I want `my-todo` deleted, so no skill advertises a `TODO.md` the project may not have.
12. As a developer, I want the status "Next" section to hold hand-picked items, so it stays a decision and not a second queue.
13. As a developer, I want "blocked" recorded in the status file with a link, so I see what waits on what.
14. As a developer, I want the status file to point to the roadmap and changelog, so "where are we" can fan out to the right detail.
15. As an agent, I want a single "link, never duplicate" rule, so I do not copy tracker state into `STATUS.md`.
16. As a developer, I want to log the work day in `WORKLOG.md`, so the narrative record outlives the session.
17. As a developer, I want each worklog entry dated, so I can find a specific day's notes.
18. As a developer, I want the worklog to append and never rewrite, so past notes are preserved.
19. As a developer, I want the worklog to hold decisions and handoffs, so the next session can pick up where this one stopped.
20. As a developer, I want `my-dev-reports` deleted, so generated git reports stop competing with the worklog.
21. As a developer, I want the changelog skill to send internal work to the worklog, so the narrative record has one home.
22. As a developer, I want the roadmap skill to learn the project's conventions the same way, so the suite behaves consistently.
23. As a developer, I want the roadmap skill to create `ROADMAP.md` when the project has none, so adoption is one command.
24. As a developer, I want the roadmap and changelog skills to keep their promotion coupling, so a 🚧 → ✅ promotion still updates both files.
25. As a developer, I want the changelog skill rewritten to the same standard, so it reads like the rest of the suite.
26. As a developer, I want every touched skill written with `writing-for-agents`, so the instructions follow one writing standard.
27. As a developer, I want both new skills model-invoked, so they trigger from a bare question.
28. As a developer, I want the skills installed through the existing linker, so they appear in both OpenCode and Claude.
29. As a developer, I want the same skills to work in any repo, so the effort pays off beyond one project.
30. As a developer, I want the skills audit to pass, so I know the descriptions do not collide.
31. As a developer, I want the skill to work in a project with no `AGENTS.md`, so adoption is not blocked.
32. As a developer, I want the skill to honour a project whose `AGENTS.md` names a different path, so it respects the project.
33. As a developer, I want the deleted `my-todo` to leave no dangling link, so both harnesses stay clean.
34. As an agent, I want the project to tell me its tracker kind, so I run the right command.

## Implementation Decisions

- Two new skills under `global/skills/`: `my-status` and `my-worklog`, each with a `SKILL.md`.
- `my-status` triggers on "where are we", "what is next", "what's next", "what's left", "what's in flight", "what's blocked", and "status". It owns the status file, default `STATUS.md` at the repo root.
- `my-worklog` triggers on "log the day", "worklog", "what did we do today", and "end of day notes". It owns `WORKLOG.md` at the repo root.
- Delete the `my-todo` skill directory. TODO.md management ends, and the status "Next" section is the only todo surface.
- Delete the `my-dev-reports` and `my-briefing` directories. No retirement flag, no re-route, and no reference to either skill survives in another skill.
- Refactor `my-roadmap-management` to the new pattern: resolve the project's conventions in the shared order, and create `ROADMAP.md` when none exists.
- Rewrite `my-changelog-management` to the same standard, and keep its coupling to the roadmap promotion.
- Write every touched skill with `writing-for-agents`.
- **Project flexibility.** All four skills resolve a project's setup in this order: read `AGENTS.md` or `CLAUDE.md` for the declared paths; reuse a file the project already keeps under another name; fall back to the defaults, `STATUS.md`, `WORKLOG.md`, `ROADMAP.md`, `CHANGELOG.md`, and the tracker kind inferred from what exists.
- **Two tracker kinds.** Local markdown (`.scratch/<slug>/spec.md` plus `issues/NN-<slug>.md`) and GitHub issues (`gh issue list`). The skill names both and picks by what the project declares or what exists.
- `STATUS.md` has four sections: `Present state` (one line), `Active`, `Blocked`, `Next`. Every line in the sections links to a tracker item or doc, and copies nothing. A dated `Updated:` line sits at the top, and the file is edited in place.
- `WORKLOG.md` is append-only, with one `## YYYY-MM-DD` heading per day. Short bullets record work done, and `Decision:` and `Handoff:` bullets carry decisions and handoffs.
- The "link, never duplicate" rule lives in the `my-status` skill body and governs every section of the status file.
- The changelog skill gives internal work no entry and points the user to `my-worklog`. `my-roadmap-management` drops its dev-report bullet and names the worklog as the internal-work record.
- Installation goes through `scripts/link_harnesses.py --apply`. If the OpenCode skills directory is a plain copy, refresh it. The deleted `my-todo` leaves no dangling link in either harness.
- `skills-lock.json` is empty, so no lockfile change is needed.

## Overrides

These six decisions supersede the first draft, where they differ. Recorded 2026-11-19.

1. **Delete, with no retirement and no re-route.** `my-dev-reports` and `my-briefing` are removed with their directories, and no skill points at either.
2. **One path-resolution order.** Read `AGENTS.md` or `CLAUDE.md` first, then reuse an existing file under another name, then fall back to the default.
3. **`STATUS.md` shape.** `Updated`, `Present state`, `Active`, `Blocked`, `Next`. Every line links, and nothing is copied.
4. **`WORKLOG.md` shape.** Append-only, one dated heading per day, with `Decision:` and `Handoff:` prefixes.
5. **Internal work in the changelog.** It gets no entry, and the user is pointed to `my-worklog`.
6. **Roadmap and changelog references.** The roadmap drops its dev-report bullet, and both skills name the worklog where they named a briefing.

## Testing Decisions

- There is one automated seam, the existing `scripts/skills_audit.py --check`. The command is `python3 scripts/skills_audit.py --check --require-advertised my-status --require-advertised my-worklog`.
- The check asserts both skills exist, are model-invoked, and that no description pair scores at or above the 0.4 Jaccard threshold.
- A good test covers external behaviour only: the audit's collision, shadowing, and advertised checks. It never inspects skill prose.
- Live behavioural testing, such as asking "where are we" in a real project, is out of scope. It is later work.
- Prior art: the existing `my-*` skills are audited by the same script. No unit tests exist for skill prose.

## Out of Scope

- Applying the skills to `anook`: creating its `STATUS.md`, `WORKLOG.md`, `CHANGELOG.md`, or editing its `AGENTS.md`.
- An `anook` ADR and glossary.
- Reconciling with the superpowers `status` and `handoff` skills.
- Live or runtime testing in any project.
- Editing any project's `AGENTS.md` to add a routing table.
- TODO.md management, which ends with `my-todo`.
- Rewriting skills outside this set.

## Further Notes

- The two repos demonstrate the two tracker kinds: `my-agent-skills` uses local markdown under `.scratch/`, and `anook` uses GitHub issues.
- Reading `AGENTS.md` or `CLAUDE.md` first matches the existing `my-*` pattern, "match what exists".
- Run the audit after writing, because two skills that both mention "status" or "next" can trip the 0.4 collision threshold.
- `writing-for-agents` is the project's skill-writing skill.
