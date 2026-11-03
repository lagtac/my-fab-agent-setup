# Templates

The shapes of the files under `.my-tutor/`, and of the section you append to `AGENTS.md`. Replace every `<…>`.

## curriculum.md

`.my-tutor/curriculum.md`, committed on the base branch. It is a map that may change, not a plan. Exercises are a title and a one-line goal here; each file is written when the student reaches it.

```markdown
# Curriculum: <topic> through <project>

## Goals

<What the student wants to be able to do at the end, two or three lines.>

## Scope

<What the app does and what it leaves out. Or: the part of this code the
student learns through.>

## Modules

1. <Module title>
   - Concepts: <concept>, <concept>
   - Exercises: 01 <short title> — <one-line goal>, 02 <short title> — <one-line goal>
2. <Module title>
   - Concepts: <concept>
   - Exercises: 03 <short title> — <one-line goal>

## Skills

The skill IDs the session loads before writing each exercise. Leave this
list empty when no skill fits.

- `<skill id, for example docx>`

## Scopes

Commit scopes for this workspace.

- `<scope>`: <the part of the code>
- `learning`: exercise files, tests and curriculum edits

## Test command

`<the command that runs the tests, for example npm test>`
```

## Exercise file

`.my-tutor/exercises/NN-<slug>.md`. Commit it, with any skeleton and the failing test, in the exercise branch's first commit: `test(learning): exercise NN, <title>`.

It holds no hints: hints are given live. **Your tasks** lists outcomes the student can check, never code or solution steps.

```markdown
# Exercise NN: <title>

**Goal:** <one sentence>

**Concepts:** <concept>, <concept>

**Support:** <worked example | skeleton | test only>

**Files:** `<path>`, `<path>`

## Your tasks

1. <what the student does>
2. <what the student does>

**Done when:** `<test command>` passes `<test name>`, `<test name>`.

**Read:** <documentation link>, <documentation link>
```

## progress.md

`.my-tutor/progress.md`, committed with the rest of the workspace. It is the record of what the student knows, so it belongs in the history.

```markdown
# Progress

## Starting point

- <diagnosis answer>

## Concepts

| Concept | Status |
| --- | --- |
| <concept> | new |

## Review

Practised concepts for recall questions, oldest first.

- <concept>

## Mistakes

- <repeated mistake, in the student's words where possible>

## Exercises

| Exercise | Date | Highest hint | Note |
| --- | --- | --- | --- |
| NN <title> | <YYYY-MM-DD> | <0-5> | <one line> |

## Next

<What the next session starts with.>
```

## The `AGENTS.md` section

Append this to the root `AGENTS.md`, once, and change nothing else in the file:

```md
## Learning workspace

- Workspace state: `.my-tutor/`.
- The student writes the code.
- New session: read `.my-tutor/progress.md`, then `.my-tutor/curriculum.md`, then load the `my-tutor` skill and follow it.
```
