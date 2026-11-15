# Skills

- Skill roots: `~/.config/opencode/skills`, `~/.claude/skills`, and `~/.agents/skills`.
- Use `npx skills` cli command to manage skills installed in `~/.agents/skills`.
- Run `python3 ~/projects/my-agent-skills/scripts/skills_audit.py --check --require-advertised interface-review` to audit installed skills. Use it before installing a new skill. EXPERIMENTAL.
- On a `collision:` line, ask the user to demote (stop advertising) or reword one of the two skills.
