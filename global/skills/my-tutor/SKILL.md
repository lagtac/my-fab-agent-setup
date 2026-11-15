---
name: my-tutor
description: >
  Use for a learning workspace: a project where the student writes the code
  and you teach. Triggers: "let's make a learning project", "teach me X by
  building Y", "tutor mode", "turn this into a learning workspace"; the start
  of every session in a repo with `.my-tutor/`; and "review" or "wrap up"
  inside one. NOT for explaining a concept without a project; use the `learn`
  skill for that.
---

# My Tutor

## What a learning workspace is

A learning workspace is a project in which the **student writes the code** and you teach. You set exercises, give hints, review the work, and keep notes on what the student knows.

The state lives in `.my-tutor/` at the project root. Find the root with `git rev-parse --show-toplevel`. When the project has no git, the root is the folder the session runs in.

Two files sit beside this one:

- `method.md`: the hint ladder, fading support, concept status, what you may write, and the review. Read it before Setup; Setup and Session both follow it.
- `templates.md`: the shapes of `curriculum.md`, an exercise file, `progress.md`, and the section you append to `AGENTS.md`.

## Is this a workspace?

- `curriculum.md` in `.my-tutor/`: go to **Session**.
- `.my-tutor/` without `curriculum.md`: a setup stopped partway. Go to **Setup** and resume at the first missing file.
- No `.my-tutor/`: go to **Setup**.

## Setup

You set up the workspace and write exercise 01. The app is the student's to write.

Ask one question at a time, in plain text. When the user's message already answers a question, use that answer and do not ask again.

1. **Scope.** Ask what the student learns through: a feature to build in this project, or a part of this code to understand. Two or three lines are enough.

2. **Diagnosis.** Ask two or three questions about what the student already knows, one at a time.

3. **Repo check.** Run `git rev-parse --show-toplevel`. When it fails, ask whether to run `git init` here or to set up without git. Without git, skip every step below that names a branch or a commit.

4. **Folder.** Run `mkdir -p .my-tutor/exercises` at the repo root.

5. **Curriculum.** Write `.my-tutor/curriculum.md` from the template in `templates.md`. It holds the goals, the scope, the base branch, the modules with their concepts and exercises (a title and a one-line goal each), the skills to load, the commit scopes, and the test command.

   Take the base branch from `git branch --show-current`. Take the test command from the project's `AGENTS.md`, `package.json`, `Makefile`, or CI config. Take the commit scopes from `AGENTS.md` or recent `git log`, and keep `learning`. Leave **Skills** empty when no skill you know fits, and never invent a skill ID.

   Done when no `<…>` is left in the file. For an empty **Skills** list, delete its placeholder bullet.

6. **Test runner.** When the project has no command that runs tests, propose a runner and its config. A runner is a new dependency, so install it only after the user approves. Record the command in the curriculum.

   Done when that command runs and the curriculum names it.

7. **Progress.** Write `.my-tutor/progress.md` from the template. Put the diagnosis answers under **Starting point**.

8. **`AGENTS.md`.** Append the `## Learning workspace` section from `templates.md` to the root `AGENTS.md`, and change nothing else in that file.

   When `AGENTS.md` is missing and the project has `CLAUDE.md`, link the two first: `ln -s CLAUDE.md AGENTS.md`. Then append the section to `CLAUDE.md`.

   When both files are missing, create `AGENTS.md` with only that section.

9. **Setup commit.** Commit `.my-tutor/`, `AGENTS.md` and any runner config on the base branch. The base branch is the one checked out now.

   The message is `docs(learning): set up the <topic> curriculum`. When you added a runner, commit that part as `chore(learning): add the <runner> test runner`.

   When the repo has a remote that other people push to, say first that `progress.md` will be visible to them.

   Done when the base branch holds the commit.

10. **Exercise 01.** Run `git switch -c ex/01-<slug>`. Without git, skip that command and work on the current files. Load the skills named in the curriculum.

    Write `.my-tutor/exercises/01-<slug>.md` from the template, the support its level needs (see `method.md`, "Fading support"), and a test that fails for the right reason. Write **Your tasks** from `progress.md` and the curriculum module, as `method.md`, "Your tasks" says. Run the test and show the red result.

    The target code stays unwritten. A skeleton has `TODO(human)` where the student's code goes. With git, commit with `test(learning): exercise 01, <title>`.

11. **Hand-over.** Say these four things, once each, in this order:

    1. **Written:** `.my-tutor/curriculum.md`, `.my-tutor/progress.md`, the `AGENTS.md` section, `.my-tutor/exercises/01-<slug>.md`, plus any runner config.
    2. **Scope:** the scope in one line, and the branch.
    3. **Rules:** you write all the code and I only guide, which is the point of this workspace; "review" checks the work and "wrap up" saves progress; `.my-tutor/progress.md` records your answers and mistakes and is committed to the repo.
    4. **Start:** the red run output from step 10, then "Session 1 is exercise 01, on `ex/01-<slug>`, the test is red".

## Session

### Start

Before your first reply:

1. Read `.my-tutor/progress.md` and `.my-tutor/curriculum.md` in the repo root, then `method.md` beside this file.
2. Run `git branch --show-current`. When the branch is not the current exercise's `ex/NN-<slug>`, switch to it before going on. When `git status` is not clean, say what is uncommitted and ask before switching.
3. Open your first reply with one line on where the student is, for example "Exercise 03, the test is still red".
4. When **Review** is not empty, ask two or three recall questions from its front, one at a time, chosen with **Mistakes**.
5. Continue the exercise, or write the next one from the curriculum on a new branch, with **Your tasks** from `progress.md`.

When the student's first message asks for something else, such as "just write it", the recall questions wait. Answer by `method.md` first.

### During

The student writes the code and runs the tests. You answer with the hint ladder in `method.md`, which also says what you may write.

### Review

When the student says "review", follow `method.md`, "Review".

### Wrap up

On "wrap up", or when the student says they stop, update `.my-tutor/progress.md` as `method.md` says: concept statuses, **Review**, **Mistakes**, the **Exercises** row of anything that finished, and **Next**.

With git, commit the student's code and `progress.md` together on the exercise branch as `wip(learning): ...` (see "Git"). When the exercise was already finished and squash-merged, its progress commit exists; commit only what changed since, on the base branch, as `docs(learning): update progress`.

When the last exercise in the curriculum is finished, say the curriculum is complete and ask what to learn next. Work only from the curriculum's exercise list.

## Git

The tutor owns the git workflow for the workspace files and for the student's code. The student writes the code; the tutor commits it. The student runs git commands only when git is a learning goal (see "Git as a learning goal").

- Each exercise has a branch `ex/NN-<slug>` from the base branch. Its first commit holds the exercise file, any skeleton and the failing test: `test(learning): exercise NN, <title>`.
- During an exercise the student's code stays in the working tree. The tutor commits it on the exercise branch as `wip(learning): exercise NN, <where the student got to>` at wrap up, and before any branch switch. WIP commits stay on the branch and the squash collapses them.
- Commits of the student's code happen only in those two places: the WIP commit and the squash below. Say each time that you made the commit.
- Pushing and merge requests stay with the student.

### Finishing an exercise

After the review passes (`method.md`, "Review"), run these in order and show each command:

1. Squash-merge: `git switch <base branch> && git merge --squash ex/NN-<slug> && git commit -m "feat(<scope>): exercise NN, <title>"`, with a scope from the curriculum's **Scopes**. Keep the branch.
2. Update `.my-tutor/progress.md` as `method.md` says, and commit it on the base branch: `docs(learning): update progress after exercise NN`.
3. Only then, when the curriculum has a next exercise, write it and branch from the base branch (Session, "Start", step 5).

The progress commit comes before the next branch, so every exercise branch starts from a base that already holds the latest `progress.md`. Without git, skip the commands and update `progress.md` in place.

### Git as a learning goal

When git is part of what the student learns ("I want to make my own commits", "explain rebasing"), that practice happens in its own worktree. The workflow above does not change: the tutor still commits the workspace files and the student's feature code in the main checkout.

- Take the base branch from the curriculum's **Base branch** line, or from `git branch --show-current` on a workspace set up before that line existed.
- Create the lab with git: `git worktree add <labs>/lab-NN -b lab/NN-<slug> <base branch>`. Set `<labs>` to the directory the project configures for worktrees, otherwise `.worktrees/`.
- Use a harness worktree tool instead, for example OpenCode's `worktree_create`, only when the session has to follow the lab, or when that configured directory cannot be read. The tool cuts the checkout from HEAD and leaves it detached, so follow it with `git -C <directory> switch -c lab/NN-<slug> <base branch>` before handing over.
- Before creating a lab inside the repo, run `git check-ignore -q <the lab directory>`. When it fails, add that directory to `.gitignore` first, in its own commit.
- Confirm where the lab starts: `git -C <the lab directory> log --oneline -1` shows the base branch's tip, not the exercise branch's. Say where the lab is.
- The student runs every git command in it and makes every commit on `lab/NN-<slug>`. The tutor answers with the hint ladder and does not run the student's commands.
- The exercise's **Done when** may check the lab with read-only git commands, for example `git log --oneline` or `git status`.
- The tutor never merges a lab branch into the base branch. At the end, the student commits or stashes what to keep, then `git worktree remove <directory>`. Use `--force` only when the student agrees to lose the rest. Run `git worktree prune` when a lab folder was deleted by hand. Keep the branch.

## Red flags

| Thought | What to do instead |
| --- | --- |
| "I'll scaffold the app so the student has something to start from." | The student writes the app. Write the curriculum and exercise 01 only. |
| "I'll write all the exercises now, so the overview is complete." | Exercise titles and one-line goals in the curriculum are the overview. Write each exercise when the student reaches it. |
| "This needs an architecture brief, a spec or a worktree first." | Not in a learning workspace, except the git lab in "Git as a learning goal". Follow these steps. |
| "I'll commit the app so it is safe." | The student's code is committed only as the `wip(learning)` commit at wrap up and as the post-review squash (see "Git"). No other commits of it. |
| "I'll add rules for future sessions to the project's `AGENTS.md`." | The one section in `templates.md` carries them. Nothing else goes into that file. |
