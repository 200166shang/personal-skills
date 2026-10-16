# Host dispatch adapters

The shared skill and task files are portable; spawning is a host operation, not a Python model client. Discover the actual exposed API and available slots. Do not pin a model. The batch max-active count applies to writers and reviewers together, with no nested dispatch by children.

## Codex

Use the host's exposed spawn/create-subagent tool with a fresh context. In this desktop environment, `collaboration.spawn_agent` supports `fork_turns="none"`; use it explicitly and pass only the task path, the relevant writer/reviewer reference path and necessary skill locations. Other Codex releases may expose a different schema: verify their context-inheritance behavior rather than passing this environment's parameter blindly. No custom agent TOML is required for a generic child given these instructions.

Record the returned actual agent ID using `attach --host codex --isolation fresh`. Keep the host spawn/tool records as audit evidence. Wait/collect through the host, read the result JSON, and call `record`. Prefer brief result summaries; do not load lesson prose into the coordinator. New lesson and reviewer → new child. Repairs may resume only that lesson's writer, but fresh repair children are simplest. On interruption, inspect known child state before explicit recovery.

## Claude Code

Use the exposed Agent/subagent tool for a non-fork child with its own context. Pass the same task/reference pointers, explicitly requiring it to read the applicable skills; the parent's previously loaded skill text is not assumed inherited. Select a suitable general-purpose or custom child available in that session. A regular fork that inherits the full conversation does not meet lesson isolation. Record the actual child ID with `attach --host claude-code --isolation fresh`, then wait and collect using that host's API.

Run the coordinator at a level permitted to spawn children under the installed version's tools, nesting and concurrency settings. This skill does not install or change local agent definitions. If host limits disallow dispatch, report the gap rather than silently writing all lessons in the coordinator context. Claude Code compatibility here is an adapter design; claim live verification only after an actual run in that host.
