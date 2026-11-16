# Rule contexts

Context rules apply to one kind of project. They live in `global/rules/contexts/` and do not load automatically. A project opts in with one reference, using the mechanism for its harness.

Pick the file that matches the project. `global/AGENTS.md` describes what each one covers.

- `global/rules/contexts/coding.md`
- `global/rules/contexts/coding-light.md`
- `global/rules/contexts/research.md`
- `global/rules/contexts/writing.md`

Use `coding.md` for applications and services, `coding-light.md` for small scripts and repo tooling.

## OpenCode

Add the context file to the project's `instructions` array in `opencode.json` or `.opencode/opencode.json`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["~/projects/my-agent-skills/global/rules/contexts/coding.md"]
}
```

`instructions` injects the file into the instruction stream, like `AGENTS.md`. A `references` entry only advertises a directory for the agent to read on demand, so it can miss rules that must always apply.

## Claude Code

Add an `@` import to the project's `CLAUDE.md` or `.claude/CLAUDE.md`:

```md
@~/projects/my-agent-skills/global/rules/contexts/coding.md
```

The import expands at launch. An absolute `~` path keeps the reference stable across worktrees.

## More than one context

A project that spans two kinds, such as a coding project with a docs site, can list both. Put both paths in the same array:

```jsonc
"instructions": [
  "~/projects/my-agent-skills/global/rules/contexts/coding.md",
  "~/projects/my-agent-skills/global/rules/contexts/writing.md"
]
```
