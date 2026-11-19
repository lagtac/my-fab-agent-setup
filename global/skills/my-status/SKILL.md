---
name: my-status
description: >
  Status: `STATUS.md`, the rendered view over the project tracker. Trigger on
  "where are we", "what's next", "what's left", "what's in flight", "what's blocked",
  and "status", or when work starts, blocks, or finishes.
---

# Status

`STATUS.md` answers two questions from one small file: where the project stands, and what comes next. It is a **view** of the tracker, so it holds no fact of its own. Every line is read from a spec, ticket, or issue, and links to it.

## The file

Resolve the path in this order:

1. **Read `AGENTS.md`, then `CLAUDE.md`.** A declared status path wins over every default here, including the section names below.
2. **Reuse a status file the project already keeps under another name.** A file that already holds present state, active work, and blockers is the status file. Keep its shape, and keep one such file.
3. **Fall back to `STATUS.md`** at the repo root.

## The tracker

Resolve the kind from `AGENTS.md` or `CLAUDE.md`. When it declares none, pick the kind the repo shows. Ask when neither is clear, because the two need different commands.

- **Local markdown.** Specs at `.scratch/<slug>/spec.md`, tickets at `.scratch/<slug>/issues/NN-<slug>.md`. A ticket's `Status:` line and `Blocked by:` line drive `Active`, `Blocked`, and `Next`.
- **GitHub issues.** `gh issue list --state open`, and `gh issue view <number>`.

When the tracker cannot answer a section, say so in one line. Do not invent state to fill it.

## 1. Where are we

Read the tracker and render the four sections. Print them, then the `Updated` date.

Compare `Updated` with the newest commit on the default branch, `git log -1 --format=%cs`. When the file is older, add one line: "The status file is older than the last commit, so it may be stale."

Done when the four sections print with their `Updated` date and the stale line, when it applies.

## 2. What is next

Print the `Next` section in tracker order, each item with its link. When `Next` is empty, read the tracker and list its open, unblocked items.

`Next` is the frontier, not a separate decision list. To change it, change the tracker: unblock an item or reprioritize it. Then render the view again.

Done when every next item is printed with its link.

## 3. Refresh after a change

When the user starts, blocks, or finishes work, update the **tracker** first. Then render `STATUS.md` from it.

- **Started:** claim the ticket in the tracker, or take the user's word. It appears under `Active`.
- **Blocked:** add the blocker to the ticket's `Blocked by:` line or the issue. It appears under `Blocked`.
- **Finished:** close or resolve the ticket. It leaves the view.
- **New candidate:** add it to the tracker. It enters `Next` when it is unblocked.

Set `Updated:` to today on every render. Do not hand-edit a state line that the tracker contradicts.

Done when the tracker holds every change, the view is rendered after it, and every line links.

## 4. Create the file

When the project has none, create it on the first **edit** request. Use the shape below, and render it from the tracker.

A question gets an answer from the tracker plus an offer to create the file. Outside a repo, say "no project here" and stop.

Done when the file exists at the resolved path with all four sections rendered from the tracker.

## The shape

```markdown
# Status

Updated: YYYY-MM-DD

## Present state

<One sentence: what the project does and whether it works today.> [Roadmap](ROADMAP.md) · [Changelog](CHANGELOG.md)

## Active

- <Item> — [<tracker reference>](<path or URL>)

## Blocked

- <Item> — waits for <what> — [<tracker reference>](<path or URL>)

## Next

- <Item> — [<tracker reference>](<path or URL>)
```

- `Updated:` is the date the view was last rendered.
- `Active` lists claimed tickets or the user's word. `Blocked` names what each item waits for.
- `Next` lists the frontier: open, unblocked, unclaimed, in tracker order. Keep it short.
