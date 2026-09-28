---
name: learning-practice
description: "Practice an existing learning workspace by applying saved understanding to one concrete task at a time."
disable-model-invocation: true
---

# Learning: Practice

Use this Skill only for explicit practice over an existing multi-Root learning workspace.

Practice consumes saved learning; it does not own learning state. Do not create a thread,
change its graph, or record practice status merely because an exercise happened.

## Resolve

- Use the workspace and Root supplied or clearly identified by the learner.
- If no valid `root-compass.yaml` and activated Root thread exist, say that durable practice material is unavailable
  and stop. Do not invent questions or create a thread.
- If the learner names a Root-qualified Question, resolve it through that Root's
  `thread.yaml`. If they name a local `qNNN`, require a clear Root context.
- Otherwise use the active Root and its `current`; if no Root is active, ask which
  explored Root to practice.
- Read the selected Question note first. Read only the minimum parent notes needed
  to design a coherent application.

## Apply before reveal

Create one concrete task that requires using the saved mechanism rather than reciting
it. Match the task to the material, for example:

- predict what a code path will do;
- trace a value through several stages;
- fill in or repair a small code fragment;
- explain why a proposed implementation is wrong;
- apply a concept to a new numeric example;
- choose between two designs and justify the mechanism-level difference;
- reconstruct an end-to-end flow from a new starting condition.

Prefer a concrete application over generic multiple choice when the material allows it.
Do not reveal the solution before the learner has a chance to attempt the task. If the
learner asks for a hint, give the smallest hint that preserves useful effort.

## Evaluate

Compare the learner's attempt with the durable note and any relevant source evidence.
Explain the mechanism behind the result, not just whether it is correct.

- If the attempt works, explain why the reasoning or implementation works.
- If it is incomplete, identify the smallest missing connection.
- If it is incorrect, identify the broken connection and repair that point without
  dumping unrelated solution detail.
- When useful, offer one smaller follow-up or focused retry.

## Stop

Stop after the learner's requested practice scope unless they explicitly ask for more.
Do not silently create an exercise backlog, score, curriculum, or schedule.

Ordinary practice is read-only with respect to the learning workspace:

- do not change Root status or a Root's `current`;
- do not add practice nodes or parent links;
- do not store scores, pass/fail, mastery, streaks, attempt logs, or practice state in
  `thread.yaml`;
- do not rewrite Question notes simply to record an exercise result.

If practice reveals a likely misconception or factual error in a saved explanation,
report it clearly and recommend correcting it through `learning-learn`; do not silently
mutate Learn-owned artifacts during ordinary practice.
