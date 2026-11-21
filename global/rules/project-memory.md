# Project memory

Project memory is four root-level files. Each answers one question:

- `ROADMAP.md` — where the project is going.
- `STATUS.md` — where it is now.
- `WORKLOG.md` — what happened, and why.
- `CHANGELOG.md` — what changed for users in each release.

Four skills own the files: `my-roadmap-management`, `my-status`, `my-worklog`, and `my-changelog-management`. This rule routes a fact to its file. The skill holds the file's shape.

## Steps

**1. Read the present before you plan.** Read `STATUS.md` when the user asks where the project stands, what is next, or what is blocked, and before you plan work in a project that has the file. Answer from the tracker, and re-render the view when the two differ.

Done when the answer names the tracker items with links.

**2. Track the work.** When work starts, claim the ticket. When work blocks, add the blocker. When work lands, comment the commit on the issue and re-render `STATUS.md`; the item shows under Active as "landed, open for verification". Close the issue on the user's word, then re-render the view.

Done when the tracker holds the change and the view matches it.

**3. Write the landed fact.** Write each fact from the session to one file, using the table below. The other files link to it.

Done when every fact from the session has one home.

## Which file gets the fact

| The fact                                     | File           | Skill                     |
| -------------------------------------------- | -------------- | ------------------------- |
| What the session did, decided, or tried      | `WORKLOG.md`   | `my-worklog`              |
| A change a host, guest, or operator can see  | `CHANGELOG.md` | `my-changelog-management` |
| An issue starts, blocks, lands, or closes    | `STATUS.md`    | `my-status`               |
| An initiative is agreed, reordered, or ships | `ROADMAP.md`   | `my-roadmap-management`   |

A ticket belongs in the tracker. A roadmap row is an initiative. Internal work earns no changelog entry.

## Authority

- The tracker is the source for `STATUS.md`. The view holds no fact of its own.
- The code on `main` is the source for `CHANGELOG.md`.
- The session is the source for `WORKLOG.md`.
- The investment decision is the source for `ROADMAP.md`.

The tracker is the project's issue tracker: GitHub issues when the repo has them, local files under `.scratch/` otherwise.

## Tracker writes

You may claim, label, and comment. You close an issue on the user's word.

## Creating a missing file

Create a project-memory file only when the user asks. The skill that owns it says what to create.

## Commits

Leave project-memory edits uncommitted unless the session asked for commits. When it did, commit each file on its own, as its skill says.
