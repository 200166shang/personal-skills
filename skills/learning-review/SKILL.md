---
name: learning-review
description: "Use when generating or practicing a fixed-scope technical interview bank for a learning topic, project, or module."
disable-model-invocation: true
---

# Learning: Review

Build a small, source-grounded interview bank for one target scope, then practice it
one question at a time. Keep the scope fixed. The learner's answers stay in chat; the
bank contains only questions and reference answers.

## Resolve scope and material

- Start from the topic, project, or module the learner names. If its boundary is
  unclear, ask one focused question before building the bank.
- Read relevant Question notes, Topic articles, Research, tutorials, README, supplied
  materials, and source code. Materials may come from a larger workspace, but select
  only what supports the target scope; do not scan unrelated project areas.
- Adjacent modules may explain the target's boundary or data handoff. Use them as
  context, not as new review scope. If the learner mentions another module in an
  answer, evaluate only the part relevant to the target and do not switch topics unless
  the learner explicitly expands the scope.
- Ground project-specific answers in evidence or facts the learner confirms. Use
  general technical knowledge to clarify mechanisms and check accuracy; do not invent
  personal ownership, production use, or results.

## Build the bank

If a bank already exists for the exact scope, reuse it. Create one when it is missing;
refresh it only when the learner asks or provides materially new sources. Prefer a
stable set of about 10–15 useful questions when the material supports it; make fewer
when evidence or scope is limited. Cover the target's role, how it works (flow and key
mechanisms), why it is designed that way, and likely implementation or failure
questions. These are priorities, not required categories. Prefer project-grounded
explanation over generic definitions.

Save the bank at `review/interview-bank.md` in the clearly identified Learning
Workspace. Keep one file per workspace. Group entries under a scope heading when the
workspace has several modules; otherwise keep the file flat. Use only numbered
questions and their reference answers:

```markdown
# Interview Bank

## Radar Module

### Q1. What does the radar module contribute to the robot?

The radar provides two-dimensional distance measurements around the robot. Its driver
publishes them as `/scan`; downstream consumers can use those measurements with the
relevant coordinate transforms for tasks such as obstacle handling.
```

Do not store the learner's answers, follow-up questions, key-point lists, scores,
attempts, dates, or mastery state. Update existing questions when refreshing the same
scope; do not keep duplicate versions. If no durable workspace is identified, build a
temporary bank in context without inventing a file path.

## Drill

Use the fixed bank as the main sequence. Start by showing only the first question and
wait for the learner's answer; do not reveal its reference answer or the remaining
questions. After each answer, briefly say what is right and what important point is
missing or incorrect, then give the reference answer from the bank in clear spoken
language. Present the next bank question and wait.

If an answer exposes a clear misunderstanding, ask a brief temporary follow-up to
repair it, then return to the next bank question. Keep the follow-up inside the locked
scope; do not add it to the bank unless it is promoted to a formal question during an
explicit bank refresh. Evaluate understanding, not exact wording. Do not add headings
or scoring structure to routine feedback; keep it to the question, a concise assessment,
and the reference answer.

## Boundaries

- Questions must stay within the named scope. Adjacent systems can appear only to
  explain an interface or handoff; do not turn them into independent questions.
- Review owns only `review/interview-bank.md`. Do not modify Question, Topic, or
  Research material, Root state, or project source code.
- If practice reveals a broader knowledge gap, explain it briefly and suggest
  `learning-learn` for exploration without changing the current scope.
- Do not create a separate Point artifact or interview workflow, dynamic question
  queue, mode, scoring system, mastery state, attempt history, or review schedule.
