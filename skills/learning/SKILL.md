---
name: learning
description: "Choose the explicit Learning workflow that best matches the learner's current intent."
disable-model-invocation: true
---

# Learning: Router

Use this Skill only when the learner is unsure which explicit Learning workflow fits.
Recommend one primary Skill and stop.

- Record, inspect, or update the learner's long-term learning direction, current focus,
  resume bookmark, next step, or intentionally deferred topics -> recommend
  `learning-plan`.
- New question, continue understanding, source/code explanation, or correction of saved
  learning -> recommend `learning-learn`.
- Review, quiz, technical interview, project deep-dive, active recall, or ask the learner
  questions about saved or supplied learning material -> recommend `learning-review`.
- Apply saved understanding in an exercise, code task, trace, prediction, or reasoning
  problem -> recommend `learning-practice`.
- Find external documentation, source code, demos, articles, talks, videos, courses, or
  other learning materials -> recommend `learning-resources`.
- Snapshot or refresh a Question graph into a Topic Compass, or generate coherent Topic
  articles from an approved Compass -> recommend `learning-organize`.
- Turn course or lecture ASR files into a faithful, readable Markdown lecture script
  without adding new teaching content -> recommend `learning-transcript`.

When the request genuinely mixes two intentions, name the primary Skill first and one
alternative only if the distinction helps the learner choose.

Do not perform the downstream work, inspect a large source tree, read or mutate Learning
Thread state for ordinary routing, or auto-invoke another Skill. All downstream Skills
are explicitly user-invoked. If the learner already invoked one directly, no router hop
is required.
