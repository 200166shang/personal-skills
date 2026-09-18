---
name: learning-practice
description: "Turn a learned idea into one small runnable exercise, let the learner attempt it first, and preserve useful attempts without requiring a learning backend."
---

# Learning: Practice

Help the learner implement one small mechanism they are currently trying to
understand. Keep the exercise subordinate to learning: it should expose the
mechanism clearly, not grow into a realistic application or a hidden assessment.

## Choose the exercise

Start from the learner's stated question, an explanation they provide, or the
current Question note in a `learning-learn` thread. If none of those identify the
mechanism, ask one focused question before creating files.

Define:

- the single mechanism being practised;
- what the learner will implement or change;
- a concrete completion check;
- any simulation boundary that makes the exercise differ from a real system.

Prefer an exercise that can be completed in one short sitting. Do not turn it into
a full project, add unrelated architecture, or claim that simulated behavior proves
production, timing, hardware, network, or concurrency reliability.

## Prepare an isolated workspace

Use a new, clearly scoped directory unless the learner explicitly asks to work in
an existing project. Never alter the source project merely to create an exercise.
Keep example code, the editable task, checks, and any reference solution separate.
The editable task must remain incomplete: the learner writes first.

Do not install dependencies, contact external services, or access devices without
the authorization normally required for those effects. Prefer dependencies already
available in the environment and deterministic local checks.

Before inviting an attempt, verify that:

- the starter files are coherent and do not contain the answer;
- the completion check fails for the intended missing behavior rather than for
  broken scaffolding;
- any example demonstrates the idea without solving the editable task;
- a reference solution, if useful, is outside the learner's task directory and is
  not revealed prematurely.

## Coach the attempt

Let the learner attempt the task before providing a solution. Answer ordinary
clarifying questions directly. Give hints only when requested or when the learner
explicitly asks for help, increasing specificity gradually:

1. point to the relevant concept or observation;
2. identify the local decision or code area;
3. outline the next implementation step;
4. show a solution only when requested.

When execution is requested, run only the scoped local checks needed for the
exercise. Report observed results as observations; do not invent passes, timing, or
environment behavior. Preserve learner edits and do not replace their approach with
the reference answer merely because it differs.

## Finish and optionally record

Explain what the attempt demonstrates about the mechanism and distinguish remaining
issues in the exercise from limitations of its simulation.

Classify the outcome only when useful:

- completed independently;
- completed with hints;
- understood from the example or solution but not completed;
- incomplete, with the next concrete step.

If the learner is using a durable learning workspace or asks to save the practice,
write a short `practice.md` inside the exercise directory or another location they
choose. Preserve the task, the learner's meaningful attempts, hints actually used,
observed checks, outcome, and next step. Do not copy the full conversation or every
keystroke.

Practice does not silently change `learning-learn` graph position, relationships, or
Question notes. If the exercise reveals that an explanation is wrong, report the
correction and update learning material only when the learner asks.
