---
name: my-worklog
description: >
  Write, read, or search WORKLOG.md, the append-only daily record of work
  done, decisions, and handoffs. Trigger on "log the day", "worklog", "what
  did we do today", "end of day notes", and "log a handoff".
---

# Worklog

`WORKLOG.md` is the project's narrative record of work by day. It outlives the session, so it carries what the next session must pick up. Each day is appended under its own heading, and earlier days stay as written.

## The file

Resolve the path in this order:

1. **Read `AGENTS.md`, then `CLAUDE.md`.** A declared worklog path wins over every default below.
2. **Reuse a worklog the project already keeps under another name**, such as `docs/journal.md` or `NOTES.md`. A file with dated day headings is the worklog. Keep one such file.
3. **Fall back to `WORKLOG.md`** at the repo root.

Shape:

```markdown
---
skill: my-worklog
---

# Worklog

## 2026-11-19

- Wrote the status and worklog skills.
- Decision: git reports are dropped, because the worklog carries the narrative.
- Handoff: regenerate the skills audit with `python3 scripts/skills_audit.py`.
```

- One `## YYYY-MM-DD` heading per day, newest day last.
- A bullet that refers to an issue, spec, or commit carries the link, and leaves the detail there.

## 1. Log the day

Read the last heading in the file. When it is today's date, append the new bullets under it. Otherwise write a new `## <today>` heading first, then the bullets.

Draw the bullets from the session and keep them in session order. Record what changed. Record each decision as a one-line `Decision:` bullet with its reason. Record each next action as a `Handoff:` bullet with its starting point.

A missed day gets no heading of its own, because its heading would sit above a later one. Log it under today's heading, and open the bullet with the earlier date.

Done when every new bullet sits under today's heading, and every earlier line is unchanged.

## 2. Read a day

For "what did we do today", print today's heading and its bullets. For a date or range, print the heading and bullets of each requested day.

Done when every requested day appears in the reply, or the reply says that day has no entry.

## 3. Find a decision or a handoff

Search with `grep -n 'Decision:' WORKLOG.md`, and the same for `Handoff:`. Print each match under its date.

Done when every match is listed with the day it belongs to.

## 4. Create the file

When the project has none, create it on the first **edit** request, using the shape above. The front-matter names the skill that owns the file, so write it on create and keep it on every edit. When you create `WORKLOG.md`, also list it under the `project lifecycle` heading in `AGENTS.md`. A read request gets one line saying the project has no worklog yet, plus an offer to create the file. Outside a repo, say "no project here" and stop.

Done when the file exists at the resolved path under a `# Worklog` title, with today's heading and the session's bullets.
