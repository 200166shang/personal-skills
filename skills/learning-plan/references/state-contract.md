# Learning Plan State Contract

This contract defines the file state owned by `learning-plan` in a Learning Workspace.
The only durable Planning paths are:

```text
planning/
  plan.yaml
  checkpoints/
    c001.md
    c002.md
```

Do not add a database, runtime service, daily log, or parallel plan format.

## `plan.yaml`

Use this version 1 schema without adding fields:

```yaml
version: 1

mission:
  statement: ""
  success_criteria: []
  constraints: []

phase:
  title: ""
  outcome: ""
  why_now: ""

sprint:
  title: ""
  started_on: "YYYY-MM-DD"
  outcomes: []

now: []

next_action: ""

later: []

open_loops: []

linked_learning:
  workspaces: []

last_checkpoint:
  id: null
  date: null
  file: null

updated_on: "YYYY-MM-DD"
```

- `mission.statement` records the longer-term reason and desired result. Keep success
  criteria few and observable when the learner supplied or confirmed them; an empty
  list is valid. Record real-world limits in `constraints`.
- `phase` and `sprint` describe only the current work. `sprint.outcomes` are results,
  grounded in the learner's stated direction, not a list of lessons or tasks.
- `now` holds a small set of current focuses, normally one to three. `next_action` is
  exactly one session-sized action. `later` holds useful items intentionally deferred.
- `open_loops` records concrete unresolved questions or engineering state that may need
  attention again.
- `linked_learning.workspaces` contains paths to related Learning Workspaces when
  useful; it never contains copied Questions or notes.
- Dates use `YYYY-MM-DD`. `last_checkpoint` remains null until the first checkpoint.
  `updated_on` changes whenever `plan.yaml` changes.

## Checkpoint files

Create checkpoints at `planning/checkpoints/cNNN.md`, with zero-padded, lowercase IDs:

```markdown
---
checkpoint: c001
date: YYYY-MM-DD
---

# Checkpoint

## Progressed

- ...

## Current State

- ...

## Next Action

...

## Open Loops

- ...

## Learned

- ...
```

`Learned` is optional. Keep every section focused on navigation; link to existing
learning notes when needed instead of copying them.

Allocate the next ID by incrementing the highest existing numeric ID. Never reuse an
ID or overwrite a checkpoint. A checkpoint is historical: ordinary resume and replan
leave earlier checkpoint files unchanged.

## Read and write ownership

`learning-plan` may read `planning/` to perform its operations. When needed to
understand the current plan, it may also read only the relevant `root-compass.yaml`, a
Root's `thread.yaml`, a small number of current Question notes, or
`organized/compass.yaml`. Read those files only when the active planning decision
depends on them.

All writes are limited to `planning/`:

- `init` creates `plan.yaml` and the checkpoint directory when absent.
- `status` reads state and writes nothing.
- `checkpoint` creates one new checkpoint, updates `plan.yaml` with the supplied
  current state, and points `last_checkpoint.id`, `.date`, and `.file` to the new file.
- `resume` reads `plan.yaml` and its referenced latest checkpoint; it writes nothing.
- `replan` updates the current `plan.yaml`; it preserves prior checkpoint files and
  leaves Mission unchanged unless the learner explicitly changes that goal.

The write boundary excludes `root-compass.yaml`, `roots/*`, `questions/*`, and
`organized/*`. Learn owns Question state; Organize owns Topic state. Planning may link
to these workspaces, but it does not duplicate or mutate them.

## Operation details

### Initialize

Use goals and constraints already stated by the learner. Populate the schema with the
current Mission, one Phase, one Sprint, `now`, a concrete `next_action`, `later`, and
`open_loops`. Ground success criteria and Sprint outcomes in the learner's stated or
confirmed evidence needs. Leave unknown criteria empty and capture unknown context in
`open_loops`; do not invent portfolio deliverables, timelines, or weekly capacity. Ask
one focused question only if the Mission cannot be inferred. Create no checkpoint until
the learner has a progress state to preserve.

### Show status

Read `plan.yaml` and, when available, the checkpoint identified by
`last_checkpoint.file`. Keep the response brief and lead with `now` and `next_action`.
Do not change timestamps or saved state.

### Checkpoint

Record the learner's actual progress, current state, next action, and open loops. Include
brief `learned` notes only when they aid future orientation. Create the next unique
checkpoint file, then update `plan.yaml` with the current state and its pointer. If the
learner has not supplied enough information to identify where they stopped or what to
do next, ask one focused question rather than inventing progress.

### Resume

Read the plan first, then the checkpoint referenced by `last_checkpoint`. If there is
no checkpoint, resume from the plan. If its referenced file is missing, state that and
use the plan's current fields; do not guess a replacement or modify the pointer. If no
plan exists, explain that there is no saved state to restore and ask for the one detail
needed to establish it.

### Replan

Change only current Planning State fields justified by the learner's changed goals or
conditions. The Mission remains stable by default. Keep one current Phase and one
current Sprint; do not generate a future Phase roadmap, daily schedule, or task list.
