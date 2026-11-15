---
description: Load a plan from the plan path and execute it
---

PLAN_PATH=`${PROJECT_PLAN_PATH:-docs/plans}`

Plan files live only in $PLAN_PATH

Argument: `$ARGUMENTS`

If the argument is empty, list $PLAN_PATH

If the argument contains `/` or `..`, print the path rule and stop. Do not read anything.

Otherwise read $PLAN_PATH

Then execute its steps in order in this session, and report each step as done, skipped or blocked. Change nothing the plan does not name.

If you are in Plan mode, review the plan against the current project instead of editing it, then tell the user to run the same command again after switching to the build agent.
