---
name: learning-review
description: "Review an existing learning workspace by reconstructing the important mechanism before seeing the saved explanation."
disable-model-invocation: true
---

# Learning: Review

Use this Skill only for explicit review of an existing multi-Root learning workspace.

Review consumes saved learning; it does not own learning state. Do not create a thread,
change its graph, or record review status merely because review happened.

## Resolve

- Use the workspace and Root supplied or clearly identified by the learner.
- If no valid `root-compass.yaml` and activated Root thread exist, say that durable review material is unavailable and
  stop. Do not invent questions or create a thread.
- If the learner names a Root-qualified Question, resolve it through that Root's
  `thread.yaml`. If they name a local `qNNN`, require a clear Root context.
- Otherwise use the active Root and its `current`; if no Root is active, ask which
  explored Root to review.
- Read the selected Question note first. Read only the minimum parent notes needed
  to understand the mechanism being reviewed.

## Retrieve before reveal

Ask the learner to reconstruct the important mechanism, causal connection, or
concept-to-code relationship before showing the saved explanation.

Prefer one meaningful prompt at a time. Do not quiz on wording, filenames, or trivia
when the saved note supports a more important connection.

Do not reveal the answer in the prompt. If the learner asks for a hint, give the
smallest hint that preserves retrieval effort.

## Evaluate

Compare the learner's answer with the durable note and any relevant source evidence.
Judge the technical connection, not exact wording.

- If the reasoning is correct in equivalent language, say why it is correct.
- If it is incomplete, identify the missing connection without treating the whole
  answer as wrong.
- If it is incorrect, name the broken connection and explain the correction clearly.
- When useful, allow one focused retry after the repair.

Do not infer permanent mastery from one successful response.

## Stop

Stop after the learner's requested review scope. Do not silently generate a curriculum,
review queue, schedule, or additional quiz set.

Ordinary review is read-only with respect to the learning workspace:

- do not change Root status or a Root's `current`;
- do not add, remove, or rewrite nodes or parent links;
- do not store scores, mastery, due dates, intervals, streaks, review status, or attempt
  history in `thread.yaml`;
- do not rewrite Question notes simply to record a review result.

If review reveals a likely factual error in a saved explanation, report it clearly and
recommend correcting it through `learning-learn`; do not silently mutate Learn-owned
artifacts during ordinary review.
