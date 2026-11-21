# Code Mode

The `execute` tool runs JavaScript that calls other tools. This harness also offers top-level tools, and several names exist in both places in a different form.

## Calling tools

`read`, `write`, `edit`, `shell`, `glob` and `grep` are top-level tools. Call them directly, as in `read({ path })`.

Inside `execute`, call `search` first, then call `tools.<namespace>["<tool>"]` with the exact paths it returns. Those top-level tools have no `tools.` entry, so the guessed name fails.

## Slash commands

`/name` runs `~/.config/opencode/commands/<name>.md`. When the first message names a command and no such file exists, say so in one sentence before doing anything else.

Then read `~/.agents/skills/<name>/SKILL.md` and follow it when it exists. That covers the user-invoked skills, which this harness does not advertise. `@<name>` loads the same skill.
