# Linking this repo into the harnesses

`scripts/link_harnesses.py` checks each harness config directory against this repo. It reports the links that are missing and prints the `ln` command for each one.

```sh
python3 scripts/link_harnesses.py            # report, print commands, change nothing
python3 scripts/link_harnesses.py --check    # exit 1 on any problem, for scripts
python3 scripts/link_harnesses.py --apply    # create missing links, repair dangling ones
```

Exit codes are `0` for a clean run, `1` for drift, and `2` for a manifest that cannot be read or validated.

## Why there is one link set per harness

`~/.agents` is not a universal config root. It is the Agent Skills directory, and each tool reads only part of it:

- OpenCode reads `~/.agents/skills` for skills, but reads `AGENTS.md`, `agents/`, `commands/`, and `instructions` only from `~/.config/opencode`.
- Claude Code reads only `~/.claude`. It does not read `~/.agents/skills`.
- Neither tool has an `~/.agents/rules` slot. Rules load through `instructions` in OpenCode and through `@` imports in `CLAUDE.md`.

So skills can be shared, but rules, the instruction file, commands, and agents need one link per harness. That is what the map below does.

## The map

Each harness declares its links in `harnesses/<name>/links.json`. Add a harness by adding a manifest; the script has no per-harness code.

| Harness | Root | Links |
|---|---|---|
| `claude` | `~/.claude` | `CLAUDE.md`, `rules/`, `commands/`, and the children of `skills/` and `agents/` |
| `opencode` | `$OPENCODE_CONFIG_DIR`, then `$XDG_CONFIG_HOME/opencode`, then `~/.config/opencode` | `AGENTS.md`, `rules/`, `skills/`, `agents/`, `commands/`, `opencode.json`, `cli.json` |

The children of `~/.claude/skills` and `~/.claude/agents` are linked one by one, because those directories also hold skills installed by `npx skills` and agents that this repo does not manage. A directory symlink would hide them.

`global/skills/bin` is excluded from the skills children. It holds helper scripts, not skills.

## Manifest fields

```json
{
  "harness": "opencode",
  "binary": "opencode",
  "root": ["$OPENCODE_CONFIG_DIR", "~/.config/opencode"],
  "links": [
    {"source": "global/rules", "target": "rules", "kind": "dir"}
  ]
}
```

- `harness` must match the folder name under `harnesses/`.
- `binary` is the command to look for on `PATH`. The harness counts as installed when the binary or the root exists.
- `root` is tried in order. The first path that exists wins, then the first path the environment names, then the last entry.
- `links[].source` is a path relative to the repo root. The script fails with exit 2 when it does not exist.
- `links[].target` is a path relative to the harness root.
- `links[].kind` is `file`, `dir`, or `children`. `children` links one entry of the source directory per name; `exclude` skips names.

## What `--apply` will and will not do

It creates a missing link, and it replaces a dangling one. It leaves a real file or directory alone, and it leaves a link that points somewhere else alone. Those are reported as `blocked` and `wrong-target`, and the run exits 1 so the person decides.

## Retired roots

`RETIRED_ROOTS` in the script lists roots this repo no longer links into: `~/.agents`. A symlink there that resolves into this repo, or points nowhere, is reported as `stale` with the `rm` command. The script never deletes it.

## Fresh machine

1. Clone this repo under `~/projects/my-agent-skills`, the path the adapters use.
2. Run `python3 scripts/link_harnesses.py` to see what each harness is missing.
3. Run it again with `--apply`.
4. Run `python3 scripts/link_harnesses.py --check` and expect exit 0.

A harness whose binary and config directory are both absent is reported as `not installed`. Its commands are still printed, so a dry run on a new machine shows the full set.
