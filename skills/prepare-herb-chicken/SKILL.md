---
name: prepare-herb-chicken
description: Plan and execute the herb chicken recipe using the available kitchen MCP tools. Use when asked to prepare, cook, or simulate an herb chicken main course, or when assembling a chicken dinner that specifically calls for herb chicken.
---

# Prepare Herb Chicken

## Execute the Recipe

1. Read [references/recipe.json](references/recipe.json).
2. Confirm that every recipe step contains a step number, tool name, and arguments object.
3. Confirm that each named tool is available before beginning execution.
4. Execute the steps in ascending numerical order.
5. Pass each step's `arguments` object directly to its named MCP tool.
6. Record every tool result, including its action number and status.
7. Do not begin a dependent step until the preceding step succeeds.

## Handle Variations

- Follow the recipe as written unless the request explicitly requires a substitution or adjustment.
- Preserve the tool argument names defined in `recipe.json`.
- Do not invent missing ingredients, arguments, temperatures, or cooking durations.
- Report an unsupported substitution or missing requirement instead of silently changing the recipe.
- Do not assume that scaling servings requires proportionally scaling cooking time.

## Handle Failures

Stop execution when:

- A required MCP tool is unavailable.
- A recipe step contains invalid or missing arguments.
- A tool returns a failure.
- A tool invocation raises an exception.

Report the failed step, tool name, completed actions, and failure reason. Do not continue to later steps when their prerequisites may be incomplete.

## Report Completion

Return a concise summary containing:

- The recipe name
- The requested or default serving count
- The actions completed in execution order
- Any requested substitutions or deviations
- The final completion status

Treat MCP results as simulated kitchen actions. Do not claim that real food has reached a safe temperature or is physically ready to eat without real-world verification.
