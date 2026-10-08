---
name: learning-review
description: "Use when the learner has studied a topic or module and wants to practice explaining its solution, design, or implementation clearly, including for an interview."
disable-model-invocation: true
---

# Learning: Review

Help the learner explain what they have already studied in clear, accurate, spoken
language. Learn explores details; Organize makes a complete written Topic; Review
practices explaining the important story without trying to cover every detail.

## Use the learned material

- Start from the Topic, Root Question, project module, or material the learner names.
  Read the relevant Question, Topic, Research, code, tutorial, or supplied conversation
  as evidence. Do not turn every detail in those sources into a separate interview
  question.
- Keep the named module as the scope. Adjacent modules may explain an interface or
  handoff, but do not become new questions unless the learner expands the scope.
- Ground project claims in source material or facts the learner confirms. Never invent
  personal ownership, decisions, production use, or results.
- If the target is unclear, ask one focused clarification. If the material is sparse,
  use what is known and say where a stronger answer needs confirmation.

## Practice explaining

Ask one broad prompt that invites a connected explanation, such as what the module
solves, how its solution works from input to output, or why its main design was chosen.
Prefer a natural interview prompt over a list of detail questions. Start from the
selected Topic or Root Question; do not create a new question tree or quiz the learner
on every parameter, field, API, or fact in the notes.

For a radar module, prefer “Walk me through how radar data reaches its consumer and
where coordinate transforms matter” over isolated questions about `reversion`,
`inverted`, or a `LaserScan` array index. Ask those details only if they are needed to
repair the learner's explanation or the learner asks to study them.

Wait for the learner to explain. Then briefly say what was clear, identify the most
important missing or inaccurate connection, and give a stronger spoken answer. Start
with plain language and keep the technical terms needed for accuracy. Use the learner's
actual design and evidence; do not invent a polished personal story.

Ask a short follow-up only to clarify or repair the explanation within the same scope.
If the learner already explained the core story well, stop or ask whether they want
another angle. If they reveal a genuine knowledge gap, explain it briefly and suggest
`learning-learn` for deeper exploration.

## Optional interview anchors

Do not generate or save an interview bank by default. If the learner explicitly wants a
small reusable set, propose 3–5 connected explanation prompts from the learned material
and explain briefly why each earns a place. Prefer prompts that represent the module's
main path, invite meaningful depth, show real engineering understanding, and do not
duplicate one another. Leave parameter trivia, isolated definitions, and secondary
details in the underlying Question or Topic unless they are central to the module.

Let the learner confirm or adjust the prompts before saving them to
`review/interview.md`. Store only each confirmed prompt and its concise spoken reference
answer. Keep the learner's practice answers in chat. Reuse the saved anchors until the
learner asks to revise them or provides materially new learning.

## Boundaries

- Review owns only `review/interview.md` when the learner explicitly asks to save
  interview anchors. Ordinary explain-back practice stays in conversation.
- Do not modify Question, Topic, Research, Root state, or project source files.
- Do not expand into adjacent modules, create a new question graph, or add scores,
  mastery, attempt history, queues, or review schedules.
