---
name: learning-plan
description: "Maintain long-horizon learning direction, current execution focus, checkpoints, and resume state."
disable-model-invocation: true
---

# Learning: Plan

Maintain the learner's long-horizon direction and short-horizon execution state. Keep
the current plan easy to resume after an interruption and light enough to maintain
without daily reporting.

## Choose one operation

- `init`: establish the Mission and current execution state for a new planning
  workspace.
- `status`: show the saved state and the single most useful next action.
- `checkpoint`: record where a learning session or Sprint stopped.
- `resume`: restore context after an interruption from the current plan and latest
  checkpoint.
- `replan`: adjust the current Phase or Sprint when goals or real-world conditions
  have materially changed.

Choose from the learner's intent. If no operation is named, use the matching operation
above. If the request combines planning with a concrete learning question, resource
search, review, practice, or Topic organization, recommend the relevant Skill for that
separate intent; do not perform or invoke it automatically.

## Maintain a rolling direction

Use four scales:

```text
Mission → current Phase → current Sprint → one Next Action
```

The Mission describes why the learner is investing in this period and the outcome they
want, usually over months or longer. The Phase names the current capability to build,
often over two to six weeks. The Sprint describes a small outcome to move over roughly
three to ten days. The Next Action is concrete enough to begin in the next session
without another planning pass. Keep `now` to a few current focuses and put worthwhile
distractions in `later`.

Keep only the current Phase and Sprint. Let the learner adapt as conditions change;
never expand the Mission into a fixed multi-week course or a daily schedule.

## Run the operation

### `init`

Use explicit goals and constraints already present in the conversation. Establish the
Mission, current Phase, Sprint, `now`, one `next_action`, `later`, and `open_loops`. Ask
one focused question only when the Mission cannot reasonably be inferred. Create the
durable state described in [the state contract](references/state-contract.md). Base
success criteria and Sprint outcomes on evidence the learner supplied or confirmed;
leave unknown criteria empty and keep unknown context in `open_loops`. Do not invent
portfolio deliverables, timelines, or weekly capacity to make the plan look complete.

### `status`

Read the plan and latest checkpoint as needed. This operation is read-only. Briefly
show Mission, current Phase and Sprint, **NOW**, **NEXT ACTION**, Later, open loops, and
the last checkpoint. Put NOW and NEXT ACTION first; omit empty sections.

### `checkpoint`

Capture the progress, current state, next action, and open loops supplied by the
learner. `learned` is optional and should stay brief. Create a new checkpoint and
update the current plan's state and checkpoint pointer. Keep it a navigation record,
not a copy of learning notes.

### `resume`

Read `plan.yaml` and its referenced latest checkpoint. Restore the Mission, Phase,
Sprint, where the learner stopped, and one natural Next Action. Resume first; an
interruption alone is not a reason to replan. If the saved direction appears obsolete,
explain the mismatch and let the learner choose `replan`.

### `replan`

Use only when the learner's goal, constraints, project direction, or current Sprint
outcome has materially changed. Adjust the current Phase, Sprint, `now`, `next_action`,
`later`, or `open_loops` as needed. Keep the Mission stable unless the learner explicitly
changes the long-term goal. Update the current plan without rewriting checkpoint
history.

## Keep ownership clear

- This Skill owns Direction and execution state: Mission, current Phase and Sprint,
  Now / Next / Later, open loops, and checkpoints.
- `learning-learn` owns Questions and explanations.
- `learning-organize` owns Topic projections.
- `learning-review`, `learning-practice`, and `learning-resources` own their explicit
  downstream workflows.

Keep planning data in `planning/` only. Read other Learning files only when the current
plan needs that context, and never copy a Question Graph into the plan. Do not create
Questions, edit Question notes or Topic files, track mastery or streaks, or turn the
plan into a task manager, calendar, or spaced-repetition system. The state contract
defines the file schema and read/write boundaries.
