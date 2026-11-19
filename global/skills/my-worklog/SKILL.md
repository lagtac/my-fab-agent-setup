---
name: my-worklog
description: >
  Use when the user wants a day's work written down or read back. Trigger on
  "log the day", "worklog", "what did we do today", "end of day notes", and
  "handoff". Owns WORKLOG.md, an append-only daily record of work done,
  decisions, and handoffs.
---

# Worklog

`WORKLOG.md` is the project's narrative record of work by day. It holds what a session did, which decisions it made, and what the next session must pick up. It outlives the session. Each day is appended under its own heading, and earlier days stay as written.

## The file

Resolve the path in this order:

1. **Read `AGENTS.md`, then `CLAUDE.md`.** A declared worklog path wins over every default here.
2. **Reuse a worklog the project already keeps under another name**, such as `docs/journal.md` or `NOTES.md`. A file with dated day headings is the worklog. Keep one such file.
3. **Fall back to `WORKLOG.md`** at the repo root.

Shape:

```markdown
# Worklog

## 2026-11-19

- Wrote the status and worklog skills.
- Decision: git reports are dropped, because the worklog carries the narrative.
- Handoff: regenerate the skills audit with `python3 scripts/skills_audit.py`.
```

- One `## YYYY-MM-DD` heading per day, newest day last.
- A plain bullet records work done, in the active past tense.
- A `Decision:` bullet records a choice and its reason, in one line.
- A `Handoff:` bullet names the next action and where to start it.
- A bullet that refers to an issue, spec, or commit carries the link, and leaves the detail there.

## 1. Log the day

Read the file's last heading.

- When it is today's date, append the new bullets under it.
- Otherwise append a new `## <today>` heading at the end, then the bullets.

Draw the bullets from the session. Record what changed, each decision with its reason, and each next action with its starting point. Keep the bullets in session order.

A missed day gets no heading of its own, because that would insert a heading above a later one. Append the note under today's heading and open it with the earlier date.

Done when every new bullet sits under today's heading, and every earlier line is unchanged.

## 2. Read a day

For "what did we do today", print today's heading and its bullets. For a date or range, print those headings.

Done when every requested day is printed, or the user is told the day has no entry.

## 3. Find a decision or a handoff

Search with `grep -n 'Decision:' WORKLOG.md`, and the same for `Handoff:`. Print each match under its date.

Done when every match is listed with the day it belongs to.
