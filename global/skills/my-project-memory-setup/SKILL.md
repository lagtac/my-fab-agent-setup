---
name: my-project-memory-setup
description: "Install the project-memory routing rule in this project's AGENTS.md or CLAUDE.md. Run it once per project. The four project-memory skills keep the roadmap, status, worklog, and changelog in sync."
disable-model-invocation: true
---

# Project memory setup

Install the project-memory routing rule into the project where you run this skill. The four project-memory skills work in every project. This skill adds their routing rule to the project.

Run this skill once from the project root.

## 1. Explore

Read the project root and find these facts:

- Which of `CLAUDE.md` and `AGENTS.md` exists, and whether either file holds a `## Project memory` section.
- Whether the project keeps a `.scratch/` tracker, a `docs/agents/` setup, or a `STATUS.md`.

Done when you know which file to edit and whether the rule is present.

## 2. Confirm

Show the user the file you will edit and the block you will write. Let the user edit the block before you write.

When a `## Project memory` section exists, propose to replace that section. Do not append a second section.

Done when the user accepts the block and the target file.

## 3. Write

Pick the file:

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither file exists, ask the user which one to create. Do not pick for the user.

Never create `AGENTS.md` when `CLAUDE.md` exists. Never create `CLAUDE.md` when `AGENTS.md` exists.

Append [project-memory.md](./project-memory.md) to the end of the file. Put one blank line before the block. Write the file verbatim. The file starts at `##`, so the block becomes a section under the project's title.

To replace an existing section, delete it from its `## Project memory` heading to the next `##` heading. If no later `##` heading exists, delete to the end of the file. Then write the new block there.

Done when the chosen file ends with the rule block, and the block appears once.

## 4. Report

Tell the user which file now holds the rule. Name the four skills the rule routes to: `my-status`, `my-worklog`, `my-roadmap-management`, and `my-changelog-management`. They work in every project. Nothing else needs installing.

Re-running this skill is only needed to repair the block or move it to another file.
