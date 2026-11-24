# Project memory skills

The vocabulary shared by the project-memory skills that manage a project's roadmap, changelog, status, and worklog. It keeps strategy, execution, and the release record from collapsing into one another.

## Language

**Roadmap**:
A forward-looking index of initiatives over a rolling horizon.
_Avoid_: feature tracker, backlog, ticket list

**Initiative**:
One outcome the team intends to deliver, written as a single roadmap row.
_Avoid_: feature, ticket, task

**Horizon**:
The investment bucket a roadmap row sits in: `Now`, `Next`, or `Later`. `Now` mirrors a ticket's `Active` state; the other horizons are investment order, not execution state.
_Avoid_: status, phase, tier

**Ticket state**:
The tracker's execution state for a ticket: `Active` (started and unblocked), `Blocked` (waits on something else), or `Next` (open, unblocked, unclaimed). It is not a horizon.
_Avoid_: status, phase

**Confidence**:
An optional note on how sure it is that an initiative ships as described.
_Avoid_: status, priority

**Tracker**:
The system that owns specs, tickets, blocking edges, and triage state.
_Avoid_: roadmap, backlog

**Changelog**:
A backward-looking, append-only record of what each release changed for users and operators.
_Avoid_: history, commit log

**Release**:
A date-named, human-cut window in the changelog. It is not a git tag.
_Avoid_: version, tag, deploy
