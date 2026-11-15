---
description: Grill a UI or design task, then dispatch the flow on "just build it"
---

Design task: **$ARGUMENTS**

If the task is empty, ask what to design and stop. Do not guess.

If the task names a deliverable but no subject — for example "a landing page" with no "for X" — ask what it is for and stop. Do not guess.

If the task says "this" — this diff, file, or screen — run `git status` and `git diff` in the repo root first, then name what you found in one line.

Read `~/projects/my-opencode-config/docs/design-routing.md` and classify the task against its flow table. State the chosen flow in one line, with each step's owner.

If no row matches or the matching row is a gap, say "No skill for <task>. Nearest: <row>." and stop. Do not grill or improvise a design process.

Read every skill's `SKILL.md` in the chosen flow. Resolve each id across the skill roots in order (`~/.config/opencode/skills`, `~/.claude/skills`, `~/.agents/skills`) and read the first match. A designer-owned skill is read for its decision points, not loaded as a skill.

Grill in rounds. Ask only the frontier: the questions whose prerequisites are settled. Number each question and recommend an answer when you have a basis for one; if you do not, list the candidates and say you have no recommendation. Word a question so "yes" accepts your recommendation. Source the decision points from the flow's skills. Look up facts yourself, but a choice among several legitimate targets is a decision, not a fact: make one lookup, then ask. Wait for answers before the next round.

When the frontier is empty, summarise the settled decisions in one short list. Do not build.

If you are in Plan mode, do not build, load skills, or dispatch subagents. After the summary, tell the user you are in Plan mode and they must switch agents to execute, even on "just build it".

On "just build it" (or equivalent), run the flow in order. For each step:

- **build-owned:** load the skill with `skill({ name: "<id>" })` and carry it out.
- **designer-owned:** dispatch the `designer` subagent with the skill id, the sub-command if the routing cell names one (`shape`, `optimize`, `document`, `extract`, `init`, `generate`, `live`), the request, and the settled decisions. Wait for it to finish before starting the next step.

The coordinator runs as `build`. The designer-owned skills are denied to it and absent from its skill list: do not try to load them, and dispatch them by id as the table writes them. Reading their `SKILL.md` for decision points is expected.

Stop at the first step that fails or needs a decision. Do not run later steps on an unfinished earlier one. Do not grill after "just build it".
