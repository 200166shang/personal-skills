# Issue tracker

Status: current project convention, 2026-10-16.

Tracker: [200166shang/personal-skills GitHub Issues](https://github.com/200166shang/personal-skills/issues). This is the default for future cross-Skill or multi-session work; a small fix can go directly to a PR. This documentation change creates no issues, labels or project automation. PRs are delivery/review artifacts, not an automatic intake queue for third-party work.

Create one parent spec issue describing the problem, outcome, relevant decisions, acceptance and exclusions. Split it into independently verifiable tickets only when useful. Each ticket links its parent, has its own acceptance criteria and lists `Blocked by` issue references, or `None`. Use native dependencies where the available tracker supports them; explicit body references remain readable and portable. Dispatch tickets whose blockers are complete. Link their PR and verification before closing them.

Use existing labels when appropriate; inspect the repository's available labels before applying them. No triage-label vocabulary is established by this lightweight setup. A task is ready when its scope, inputs, acceptance and blockers are explicit, not merely because it has a label.

Local Markdown tasks are an explicit alternative when requested: use one file per task under `.scratch/<feature>/issues/`, with numbered blockers. `.scratch` is temporary work state, not the durable design archive. Preserve any needed handoff until its result has been incorporated. Accepted decisions/designs and final evidence go to docs; private scratch material stays out of Git.

See [the workflow and task outline](../development.md) for what to include. Referencing a tracker in instructions does not by itself authorize sending messages or changing external projects; perform mutations within the user's requested task scope.
