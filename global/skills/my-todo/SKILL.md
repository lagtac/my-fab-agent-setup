---
name: my-todo
description: >
  Use when the user asks what is next, what is left, or what is on their todo
  list; marks an item done, adds one, or removes one. Trigger on "what is
  next", "what's next", "what's left", "what's on my todo", "show todo",
  "mark X done", "check off X", "X is done", "complete X", "add X to my
  todo", "todo: X", "remove X from my todo". Owns the project's TODO.md, a
  flat list of short-lived tasks; roadmap features stay in ROADMAP.md under
  my-roadmap-management.
---

# Todo

`TODO.md` is the project's flat list of short-lived, immediate tasks — the small
stuff that would clutter `ROADMAP.md`. This skill lists the open items, checks
one off, adds one, and removes one.

## The file

- Default path: `TODO.md` at the repo root.
- Match what exists: when the project's `AGENTS.md` or `CLAUDE.md` names a todo
  path, use that; when the repo already keeps a todo file under another name,
  use that.
- Format: Markdown checkboxes — `- [ ]` open, `- [x]` done — optionally grouped
  under `##` headings. Keep the file's own format.
- The file is tracked. Edit it in place and leave it; the user's own commit flow
  decides when it lands.

## 1. List — "what is next"

Read the file and print every open item (`- [ ]`), grouped under its `##`
heading where the file has them, in file order. When nothing is open, say
"nothing open".

When the project has no todo file, say so and offer to create an empty one; do
not create it until the user agrees.

## 2. Mark done — "mark X done", "X is done"

Find the item by its text and flip `- [ ]` to `- [x]`, in place. Leave it in the
file. When two items match the text, ask which one.

## 3. Add — "add X to my todo", "todo: X"

Append `- [ ] <X>` to the bottom of the section the user names, else to the
bottom of the file. Create `TODO.md` on the first add when it does not exist.

## 4. Remove — "remove X from my todo"

Find the item by its text and delete the whole line. When two match, ask which
one.

Outside a project (no repo root), say "no project here" and stop; there is no
home-wide list.
