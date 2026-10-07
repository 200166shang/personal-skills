---
name: learning-review
description: "Use when reviewing saved or supplied learning material, rehearsing technical explanations, or conducting an engineering interview or project deep-dive."
disable-model-invocation: true
---

# Learning: Review

Run an AI-led, source-grounded technical review. The learner gives a topic, module, or
project scope; ask one useful question at a time, evaluate the answer, and save only
high-value reusable Q&A. Review is the activity; `review-bank.md` is its optional
durable output.

## Resolve material

- Use the Learning Workspace, topic, project, or source files the learner names or
  supplies. Consider relevant Question notes, Topic articles, Research notes, README,
  tutorials, code, and the current conversation; do not limit review to Question notes.
- Read enough relevant material to ask a grounded question. For a project, inspect the
  files that show the key path or design rather than scanning an unrelated source tree.
- Base questions on the learner's real material whenever possible. Use general
  technical knowledge to check, explain, deepen, or extend it—not to replace it with a
  generic trivia quiz. Distinguish evidence from inference and never invent ownership,
  production use, or performance results.
- If the requested scope or source is unclear, ask one focused clarification. If no
  usable material is available, say what is missing rather than inventing project facts.

## Ask

Default to an engineering interview or project deep-dive style. Choose questions that
test understanding of the supplied material, especially:

- end-to-end flow and causal mechanisms;
- architecture and design choices, including alternatives and trade-offs;
- failure handling, edge cases, and implementation details;
- scaling, extension, and project-specific reasoning.

Use these as priorities, not a checklist. Avoid isolated definitions or trivia unless
they expose a deeper gap. Ask one meaningful question, then wait. Deepen progressively
based on the learner's answer; skip ahead when they have already explained a layer well.
Do not generate a long question list or reveal the answer in the prompt.

## Evaluate

Judge the technical connections, causal reasoning, completeness, and consistency with
the supplied evidence—not memorized wording. Say whether the answer is correct, mostly
correct but incomplete, or contains a key error. Acknowledge correct parts, identify
the important gap, and give a concise, accurate reference answer suitable for speaking
aloud. Ground project claims in the material or the learner's confirmed experience;
never polish an unsupported claim into a fact. Offer one focused retry when useful, or
choose a follow-up that responds to what the learner actually said.

## Record

Save only questions worth explaining again: important mechanisms, core project flows,
architectural choices, meaningful trade-offs, failure cases, or likely deep interview
questions. Do not save every diagnostic, definition, or clarification question.

When a durable Learning Workspace is clearly identified, keep its Review Bank at:

```text
review/
  review-bank.md
```

Use one Markdown file per workspace, creating it only for a high-value entry. Keep
entries concise and update an existing entry when the same question recurs. Preserve
the learner's current natural answer and a stronger reference answer, with key points
and useful follow-ups when they add value:

```markdown
# Review Bank

## Why does this module use gRPC instead of making the SDK depend directly on ROS 2?

### My answer
<the learner's current explanation>

### Reference
<a technically grounded answer the learner can say aloud>

### Key points
- <important mechanism or trade-off>

### Follow-ups
- <one useful deeper question>
```

Update the file after the learner has answered and the reusable entry is clear. If no
durable workspace is identified, keep the review in conversation; do not invent a path.

## Boundaries

- Review owns only `review/review-bank.md`. Do not mutate Root status, `root-compass.yaml`,
  `thread.yaml`, Question notes, Topic articles, or Research notes.
- If review exposes a real knowledge gap, explain it briefly and suggest `learning-learn`
  for recursive exploration; do not create or edit Questions here.
- Do not add a Point skill or Point file, interview modes, scores, mastery, attempt
  history, spaced-repetition state, queues, or schedules.
