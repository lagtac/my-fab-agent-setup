# Workflow skills

Four skills answer four questions about the files in a project. You ask in plain words. The agent picks the skill. Say the skill's name when you want it directly. A fifth skill, `my-name-pane`, labels the tmux pane with the title of the row you picked and owns no file.

| You ask | Skill | File it owns |
|---|---|---|
| Where are we? What is next? What is blocked? | `my-status` | `STATUS.md` |
| Log the day, or read it back | `my-worklog` | `WORKLOG.md` |
| Update the roadmap, mark a feature shipped | `my-roadmap-management` | `ROADMAP.md` |
| Add a changelog entry for a change with no roadmap row | `my-changelog-management` | `CHANGELOG.md` |

## A normal day

1. **Start with "what is next".** `my-status` prints the `Next` section with a link for each item. When `Next` is empty, it lists the open tracker items from `.scratch/<slug>/` or GitHub issues. You pick the work.
2. **Mark the item started**: say "move X to active". `my-status` moves it from `Next` to `Active`. For a roadmap feature, also promote its row `📋 → 🚧` when the plan exists and the work is underway. `Active` and `🚧` track the same work: a status line and a roadmap row.
3. **Work.** Changes during the work go to the roadmap: a reframe, a split, or a new spec link. The agent commits only when you ask. Say when you want a commit.
4. **Ship and finish.** "Mark X shipped" moves the roadmap row to `✅` and writes the changelog entry in the same commit. "Finish X" deletes the item from `Active`. The two edits complete the same piece of work.
5. **End with "log the day".** `my-worklog` appends today's heading and the session's bullets. A `Decision:` line records a choice and its reason. A `Handoff:` line names the work the next session must continue.
6. **Next morning**, "where are we" shows the status file, its age, and which items wait for other items. The worklog holds yesterday's reasoning.

The day is a loop. "Next morning" returns to the first step.

```mermaid
flowchart LR
    A["1 what is next"] --> B["2 mark started<br/>Next to Active"]
    B -->|roadmap feature| R["promote row to 🚧"]
    B -->|plain item| C["3 work"]
    R --> C
    C --> D["4 ship and finish<br/>roadmap ✅ + changelog"]
    D --> E["5 log the day"]
    E -->|next morning| A
```

## What each file holds

- **`STATUS.md`** is an index, not a record. It holds one sentence of present state, then active work, blockers, and selected next items. Every line links to the tracker item or doc that explains it. The `Updated:` date tells you how fresh the file is.
- **`WORKLOG.md`** is the narrative, one heading per day, newest last. It is append-only, so earlier days stay as written. It holds what you did, the decisions, and the handoffs.
- **`ROADMAP.md`** is the forward view of features, from 💭 to ✅. A row gets `💭` after you agree to the idea. It gets `📋` when its spec exists. It gets `🚧` when its plan exists and the work is underway. A row is short and links to its spec and plan. The file expresses dependencies as order, not as a graph.
- **`CHANGELOG.md`** is the backward view of what reached the main branch. It records contract and behaviour changes for users and operators. Internal work gets no entry.

## The two lifecycles

The roadmap row and the status item each pass through a fixed set of states. A state diagram shows every state, the moves out of it, and the condition for each move.

### Roadmap row

```mermaid
stateDiagram-v2
    state "💭 discussed" as D
    state "📋 planned" as P
    state "🚧 in progress" as W
    state "✅ shipped" as S
    [*] --> D: idea agreed
    D --> P: spec exists
    P --> W: plan exists and work started
    W --> S: merged to main, changelog in the same commit
```

A row enters at `💭` only after you agree to the idea. Each later move needs its linked document, or the merge to main for `✅`.

### Status item

```mermaid
stateDiagram-v2
    [*] --> Next: new candidate agreed
    Next --> Active: start
    Active --> Blocked: a blocker appears
    Blocked --> Active: the blocker clears
    Active --> [*]: finish
```

`Next` and `Active` are the two current states. `Blocked` is a temporary state before the item returns to `Active`. Finishing deletes the line, because the tracker and worklog keep the record.

## Where does this go?

- A refactor, test, lint pass, or internal doc note → the worklog.
- A user-visible fix, a changed default, or a deploy change such as an env var or port → the changelog.
- A removed feature → the changelog `### Removed` entry. The `✅` roadmap row stays.
- A whole feature → the roadmap, plus the changelog when it ships. Route a shipment through `my-roadmap-management`, so both files change in one commit. A changelog entry alone is for changes with no roadmap row.
- A decision → the worklog `Decision:` line, with a link to the doc that argues for it.
- A blocked item → `STATUS.md` under `Blocked`, naming what it waits for.
- A started or finished item → `STATUS.md`, moved to `Active` or deleted.

## Adopting the skills in a project

Nothing to install. The skills are global. They work in any repo, with a local-markdown tracker or GitHub issues.

1. **Run "where are we" in the project.** When no status file exists, the agent answers from the tracker and offers to create `STATUS.md`. Accept, or ask for the first edit.
2. **Log the first day.** "Log the day" creates `WORKLOG.md` with today's heading.
3. **Keep the defaults or declare your own.** Put the paths in `AGENTS.md` or `CLAUDE.md` when they differ:

   ```markdown
   ## Workflow files

   - Status: `docs/STATUS.md`
   - Worklog: `docs/WORKLOG.md`
   - Roadmap: `ROADMAP.md`
   - Changelog: `CHANGELOG.md`
   ```

4. **Name the tracker when it is not obvious.** A local-markdown tracker keeps specs and issues under `.scratch/<slug>/`. A GitHub-issue tracker uses `gh issue list`. The agent asks when the repo shows no tracker.

A project that already keeps a status file, worklog, roadmap, or changelog under another name keeps it. The skills reuse that file and its shape, and never create a second file.

## Habits that keep the files useful

- Ask the skill instead of editing the files by hand, so the shape stays consistent.
- Keep `STATUS.md` lines as links. A copied fact goes stale in one of its two homes.
- Log the day before you stop. A handoff written tomorrow loses the detail you had today.
- Set `Updated:` to today whenever you touch the status file.
- Promote a roadmap row to ✅ only after the change reaches the main branch.
