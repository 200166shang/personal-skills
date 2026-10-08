---
name: learning-review
description: "Use when the learner has studied a topic or module and wants to prepare interview explanations or practice explaining its solution and implementation clearly."
disable-model-invocation: true
---

# Learning: Review

Help the learner turn an already learned module into a few strong, speakable interview
answers. Learn explores details; Organize synthesizes a complete Topic; Review selects
representative questions and practices explaining the module clearly.

## Resolve scope and material

- Work on one previously studied Topic or project module named by the learner. If the
  target is unclear, ask one focused question before selecting interview material.
- Read the relevant Questions, Topic, Research, implementation, tutorial, or supplied
  conversation. Use adjacent modules only to explain an interface or handoff; they do
  not become separate questions unless the learner expands the scope.
- Ground technical and project claims in those materials or facts the learner confirms.
  Do not invent personal ownership, design decisions, production use, or results.

## Select interview Q&A

When no saved Q&A exists for the target, propose 3–5 representative questions with
concise spoken reference answers. Briefly explain why each is worth keeping, then wait
for the learner to confirm or adjust them before saving. Prefer questions that connect
the module's main solution or implementation, invite meaningful depth, show supported
engineering understanding, and do not duplicate one another. Deliberately leave
isolated parameter facts, definitions, and secondary details in the learning material
unless they are central to explaining the module.

The learner may specify additional questions. Keep in-scope questions even if that
takes the set beyond 3–5; explain briefly why each is worth practicing, draft a strong
spoken answer from the available evidence, and confirm the complete entry before
saving. Merge duplicates. If a requested question belongs to a different module, ask
whether the learner wants to expand the scope.

Save confirmed entries in `review/interview.md`, one file per Learning Workspace,
grouped by module. Each entry contains only the question, a brief reason it is worth
practicing, and the reference answer. Do not save the learner's practice answers. If no
durable workspace is identified, keep the confirmed material in the conversation
instead of inventing a path.

Reuse saved Q&A for the same scope. Refresh only when the learner asks: compare the
existing set with the new material, propose additions or edits, and save only after the
learner confirms the changes.

## Practice

After the learner confirms a new or refreshed set, start with its first question. For
later practice, use the saved set and start at the first question unless the learner
names another one. Show one question without its answer and wait for the learner to
respond.

After each response, briefly say what was clear and identify the most important gap or
error. Then give the reference answer as a natural, accurate explanation that can be
spoken in roughly one to three minutes: start with plain language and preserve the
technical terms needed for precision. Keep the learner's actual project evidence; do
not turn the answer into a textbook entry or invented personal story. Continue with the
next question.

Use a temporary, in-scope follow-up only when it helps repair a misunderstanding, then
return to the saved questions. Do not save practice attempts or progress. Continue from
the conversation when available; in a new conversation, start at the first question or
the one the learner specifies.

## Boundaries

- Review owns only the confirmed Q&A in `review/interview.md`. Do not modify Questions,
  Topics, Research, Root state, or project source files.
- Review is for explaining learned material, not opening another recursive learning
  thread. If the learner reveals a real gap, explain it briefly and suggest
  `learning-learn` for exploration.
- Do not add scores, mastery, attempt history, queues, or review schedules.
