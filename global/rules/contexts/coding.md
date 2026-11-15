# Coding

The following are specialized and extended expressions of `../principles.md` and apply when writing or editing code.

## Code Style

- Prefer functional programming over OOP
- Use OOP classes only for connectors and interfaces to external systems
- Write pure functions - only modify return values, never input parameters or global state
- Follow DRY, KISS, and YAGNI principles
- Prefer simple, native, vendor-recommended solutions and avoid premature abstractions
- Use strict typing for returns, variables, collections, and complex data; validate external/API data at runtime; require needed fields, ignore unrelated extra fields, prefer structured models over loose dictionaries, and avoid weak generic types like `Any`, `unknown`, or `List[Dict[str, Any]]`
- Check if logic already exists before writing new code
- Never use default parameter values - make all parameters explicit
- Write simple single-purpose functions - no multi-mode behavior, no flag parameters that switch logic. If the user needs multiple modes, they will ask explicitly

## Error Handling

- Always raise errors explicitly, never silently ignore them
- Use specific error types that clearly indicate what went wrong
- Avoid catch-all exception handlers that hide the root cause
- No fallbacks, symptom-masking guards, or silent recovery unless I explicitly ask for them; fix root causes and make code either succeed or fail with a clear error
- External API or service calls: use retries with warnings, then raise the last error
- Error messages must be clear, actionable, and specific: explain what failed and why, include request params, response body, status codes, and avoid generic "something went wrong"
- Logging should use structured fields instead of interpolating dynamic values into message strings

## Libraries and Dependencies

- Use modern stable, project-compatible package management, libraries, and language standards; prefer vendor-recommended patterns such as ESM when supported
- Install dependencies in project environments, not globally
- Add or update dependencies in project config files, not as one-off manual installs
- If a dependency is installed locally, read its source code when needed instead of guessing, even if it is gitignored

## Testing

- Respect the repository test strategy and add only the minimum useful tests for the requested change
- Prefer smoke, integration, and end-to-end tests over narrow unit or regression tests; do not test static text, prompts, or config unless behavior depends on them
- Do not create fake/mock-based tests by default; use real integrations when practical, even if they cost a little money
- UI tests and automations must use stable IDs, test IDs, or accessibility IDs instead of visible text, and fail fast without fallback clicks

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

- Project documentation goes to `$PROJECT/docs` unless otherwise specified.
- Files that are usually uppercase, like README.md etc, signal "meta documents about the project" and are are root-level.
- Code is the primary documentation - use clear naming, types, and docstrings
- Keep documentation in docstrings of the functions, classes, or modules they describe, not in separate files
- Separate docs files only when a concept cannot be expressed clearly in code, and only one file per topic
- Never duplicate documentation across files; reference other sources instead
- Store knowledge as current state, not as a changelog of modifications
