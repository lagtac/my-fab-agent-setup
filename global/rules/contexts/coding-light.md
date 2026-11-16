# Coding Light

The following apply when writing or editing small scripts and repo tooling.

## Code Style

- Write simple single-purpose functions; no multi-mode behavior or flag parameters
- Follow DRY, KISS, and YAGNI
- Prefer simple, native, vendor-recommended solutions; avoid premature abstractions
- Add type hints where cheap and helpful; validate external input at runtime
- Check if logic already exists before writing new code

## Error Handling

- Raise errors explicitly; never silently ignore them
- Use specific error types and clear, actionable messages
- No catch-all handlers or silent fallbacks

## Libraries and Dependencies

- Install dependencies in the project environment, not globally; record them in the project config

## Testing

- Add a minimal test only when behavior is worth locking; no mocks for your own code

## Terminal Usage

- Prefer non-interactive commands with flags over interactive ones
- Always use non-interactive git diff: `git --no-pager diff` or `git diff | cat`

## Workflow

- Read the existing code and relevant project instructions before editing
- Keep changes minimal and tightly scoped to the current request: make the smallest useful diff, change only the lines needed to solve the problem, and avoid unrelated improvements unless the user asks for them
- Match the existing style of the repository even if it differs from my personal preference; new code must look like it was written by the same author
- Keep files small and cohesive; split by feature or responsibility when the project has no established structure
- Do not revert unrelated changes
- If you are unsure, inspect the codebase instead of inventing patterns
- When project instructions include test or lint commands, run them before finishing if the task changed code

## Documentation

- Keep documentation in docstrings where the code lives; add a separate doc file only when a concept cannot be expressed in code
