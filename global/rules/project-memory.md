# Project memory

Four files record the project. Each answers one question:

- `ROADMAP.md`: where the project is going.
- `STATUS.md`: where it is now.
- `WORKLOG.md`: what happened, and why.
- `CHANGELOG.md`: what changed for users in each release.

## Route each fact

Write each fact to one file, and link it from the others.

| The fact                                     | File           | Skill                     |
| -------------------------------------------- | -------------- | ------------------------- |
| An initiative is agreed, reordered, or ships | `ROADMAP.md`   | `my-roadmap-management`   |
| An issue starts, blocks, lands, or closes    | `STATUS.md`    | `my-status`               |
| What the session did, decided, or tried      | `WORKLOG.md`   | `my-worklog`              |
| A change a host, guest, or operator can see  | `CHANGELOG.md` | `my-changelog-management` |

A roadmap row is one initiative with one outcome and a spec link, or `no spec yet`. Tickets live in the tracker. Refactors, tests, lint, and internal docs go to the worklog.

## Read the present before you plan

Before you plan work in a project with a `STATUS.md`, read it. Answer from the tracker, and re-render the view when the two differ. Done when the plan starts from the current view.

## Guardrails

- Claim, label, and comment as work moves. Closing an issue waits for the user's word.
- Create a project-memory file when the user asks; its skill gives the shape.
- When the session asks for commits, commit each file on its own.
