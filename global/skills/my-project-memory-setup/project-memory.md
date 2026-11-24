## Project memory

Four files record the project. Each answers one question:

- `ROADMAP.md`: where the project is going.
- `STATUS.md`: where it is now.
- `WORKLOG.md`: what happened, and why.
- `CHANGELOG.md`: what changed for users in each release.

### Route each fact

Write each fact to one file, and link it from the others.

| The fact                                | File           | Skill                     | Written when                                     |
| --------------------------------------- | -------------- | ------------------------- | ------------------------------------------------ |
| An initiative decision                  | `ROADMAP.md`   | `my-roadmap-management`   | agreed, reordered, or ships                      |
| An issue state change                   | `STATUS.md`    | `my-status`               | starts, blocks, lands, or closes                 |
| The day's work, decisions, and handoffs | `WORKLOG.md`   | `my-worklog`              | you log the day or a handoff                     |
| A user-visible change                   | `CHANGELOG.md` | `my-changelog-management` | a user-visible change lands, or a release is cut |

A roadmap row is one initiative with one outcome and a spec link, or `no spec yet`. Tickets live in the tracker. The worklog records refactors, tests, lint, and internal docs when you log the day or a handoff.

### Read the present before you plan

Before you plan work in a project with a `STATUS.md`, read it. Answer from the tracker, and re-render the view when the two differ. Done when the plan starts from the current view.
