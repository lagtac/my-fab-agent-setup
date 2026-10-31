# Port notes

`my-deep-research` is a copy of the `deep-research` skill, changed only where OpenCode names a tool differently.

- Source: `~/.claude/skills/synced/<id>/deep-research`, a synced copy that will be replaced on the next sync.
- Ported: 2026-10-29.
- Diff against the source: 13 lines, all listed below.

## Substitutions

| Source | Port |
|---|---|
| `name: deep-research` | `name: my-deep-research` |
| "(the Agent or Task tool)" | "(the `subagent` tool)" |
| "(for example TodoWrite, or TaskCreate and TaskUpdate)" | "(for example `todowrite`)" |
| "the AskUserQuestion tool" | "the `question` tool" |
| "the Agent tool (named Task in some versions) with subagent_type=\"general-purpose\" and run_in_background=false" | "the `subagent` tool with `agent=\"general\"` and foreground mode, which is the default" |
| the `Agent(` call blocks | `subagent(`, with `agent="general"` in place of the two keyword lines |
| "calls to the Agent tool" | "calls to the `subagent` tool" |
| "(for example SendUserFile)" | "(for example a tool that presents files)" |
| `WebSearch` | `websearch` |
| `WebFetch` | `webfetch` |
| "the Read tool" | "the `read` tool" |

Nothing else changed. The output paths, the researcher-count table, the title rules, step 5 and the coordinator's ban on reading the reference files are all as written upstream.

## Known consequences

- `subagent` takes a `description` field, so the call blocks keep one. The upstream blocks also pass it.
- OpenCode has no file-sending tool. Step 7 falls through to its own fallback and leaves the report at `reports/<title>.md`.
- Reports and notes land in `reports/` and `research_notes/` in the working directory. This differs from the `docs/` conventions in this repo, and that is deliberate: the port does not change behaviour.

## Re-porting

Copy the source over this folder and apply the table above. Every entry is a literal string, so `diff -r` should show only these lines.
