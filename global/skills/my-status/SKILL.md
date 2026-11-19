---
name: my-status
description: >
  Use when the user asks where a project stands or what work comes next.
  Trigger on "where are we", "what is next", "what's next", "what's left",
  "what's in flight", "what's blocked", and "status". Owns STATUS.md, a short
  index of the present state, active work, blockers, and the hand-picked next
  items, each pointing at the tracker item or doc that holds the detail.
---

# Status

`STATUS.md` answers two questions from one small file: where the project stands, and what comes next. It is an index. A line points at the tracker item or doc that holds the detail, and copies none of it.

## The file

Resolve the path in this order:

1. **Read `AGENTS.md`, then `CLAUDE.md`.** A declared status path wins over every default here, including the section names below.
2. **Reuse a status file the project already keeps under another name.** A file that already holds present state, active work, and blockers is the status file. Keep its shape, and keep one such file.
3. **Fall back to `STATUS.md`** at the repo root.

Shape, when the project has none:

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

- `Updated:` holds the date any line last changed. It is the file's freshness mark, so a reader sees staleness at a glance.
- `Present state` is one sentence, followed by links to the roadmap and changelog where the project keeps them.
- `Active` lists work in flight.
- `Blocked` names what each item waits for.
- `Next` holds up to five hand-picked items. It is a decision, so it stays shorter than the tracker queue.

## Link, never duplicate

A fact kept in two files has two owners, and one of them goes stale. The tracker, the spec, and the changelog own their facts. `STATUS.md` owns one sentence of present state and the choice of what comes next. Every content line carries a link, and no line restates the linked item.

## The tracker

Pick the kind the project declares in `AGENTS.md` or `CLAUDE.md`. When it declares none, pick the kind the repo shows. Ask when neither is clear, because the two need different commands.

- **Local markdown.** A spec at `.scratch/<slug>/spec.md`, and issues at `.scratch/<slug>/issues/NN-<slug>.md`. Read the files.
- **GitHub issues.** `gh issue list --state open`. Read with `gh issue view <number>`.

## 1. Where are we

Read the file and print `Updated`, then every section as written. Then compare the date with the newest commit on the default branch, `git log -1 --format=%cs`. When the file is older, add one line: "The status file is older than the last commit, so it may be stale."

Done when the user has the four sections and knows the file's age.

## 2. What is next

Print the `Next` section in file order, each item with its link. When `Next` is empty, read the tracker and list its open items, in tracker order.

Offer to move an item into `Next`. Add it only on the user's word. `Next` stays a short decision.

Done when the user has the next items and the link to each.

## 3. Record a change

Edit lines in place:

- **Started:** move the item from `Next` to `Active`.
- **Blocked:** move the item to `Blocked`, and name what it waits for.
- **Finished:** delete the line. The tracker and the worklog hold the record.
- **New candidate:** add it to `Next` on the user's word only.

Set `Updated:` to today on every edit.

Done when every line in the four sections links, and `Present state` is still one sentence.

## 4. Create the file

When the project has none, create it on the first **edit** request. Write the heading, the `Updated:` line, and the four sections. A question gets an answer from the tracker plus an offer to create the file.

Outside a repo, say "no project here" and stop.
