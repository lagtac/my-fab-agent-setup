# Global Rules

## identity

- my name is dimitris chrysomallis
- i was born on Dec 30 1975 in Athens, Greece where i still live with my wife and son
- i have several non life-threatening medical conditions, e.g. depression. I regulate all of them.
- i do fullstack web dev. js, ts, html5, python, php, node, react.
- i work on the linux cli and tmux most of the time
- code and projects live in `~/src` and `~/projects` respectively
- i am currently looking for work
- i am looking for business opportunities as a tech entrepreneur
- as a self-taught developer i have to apply extra effort to keep my programming and engineering skills updated. currently i fail all leetcode tests.
- i have BS in philosophy and MS in cognitive science

## Rule files

The rules live in `rules/` next to this file. Each harness loads them through its own adapter under `harnesses/<harness>/`. OpenCode, for example, points its `instructions` list at `~/.config/opencode/rules/*.md`, which symlinks to this directory.

### Universal rules

These load in every project.

- `rules/principles.md`: universal principles.
- `rules/critical-thinking.md`: checking claims, scoping requests, handling faults.
- `rules/communication.md`: the 17 writing rules and the review pass.
- `rules/skills.md`: skill roots and the audit script.
- `rules/plan.md`: where plans go.
- `rules/git.md`: commits, branches, merge.

### Context rules

These apply to one kind of project. They live in `rules/contexts/` and do not load on their own. A project opts in per harness; see `docs/rule-contexts.md` for the snippet to add.

- `rules/contexts/coding.md`: code style, errors, dependencies, tests, terminal use, workflow, docs.
- `rules/contexts/research.md`: investigating, comparing, citing.
- `rules/contexts/writing.md`: drafting and editing prose.
