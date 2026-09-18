---
name: learning-review
description: "Run active recall from an existing explanation or Learning Thread, revealing the saved explanation only after the learner attempts an answer."
---

# Learning: Review

Run a short active-recall session against material the learner has already studied.
The learner attempts recall before seeing the saved explanation. Review observes
memory; it does not silently rewrite learning history or decide what the learner has
mastered.

## Select review material

Use one of these inputs:

- a question or explanation the learner supplies;
- a Question note explicitly selected from a `learning-learn` thread;
- a small set of existing Question notes from which the learner chooses.

When a thread is supplied, treat `thread.yaml` as routing metadata. Read the selected
Question note only far enough to prepare the recall prompt and retain its path so the
same saved explanation can be revealed later. Do not invent a past question,
explanation, review history, or schedule when none exists.

If the user asks for a general review without selecting an item, offer a small number
of real candidates. Prefer the current question and older questions that have not
been reviewed recently when reliable local review facts exist. Explain the reason
briefly and let the learner choose or skip. Candidate selection itself records
nothing.

## Ask before revealing

Create one prompt that tests the important mechanism, connection, distinction, or
application captured by the selected explanation. Avoid trivia and avoid merely
asking the learner to repeat the title.

Ask the prompt without showing or paraphrasing the saved answer. Do not reveal hidden
parts of the note while the attempt is pending. If the learner asks for help, give at
most one minimal hint at a time and remember the hints actually used.

Accept an answer, an explicit non-answer, or a skip. Judge whether the learner
reconstructed the important reasoning, not whether their wording matches the note.
Distinguish:

- recalled: the central mechanism and relevant boundary are present;
- partial: an important causal step, distinction, or condition is missing;
- not recalled: the answer does not recover the central idea;
- not scored: the learner skipped or did not answer.

State that this is a conversational judgment when the evidence is borderline. Let
the learner correct the evaluation.

## Reveal and teach

After the attempt or skip, reveal the relevant saved explanation and compare it with
the learner's answer. Focus on the missing or distorted connection rather than
re-teaching everything. General knowledge may clarify the material, but distinguish
it from what the saved note actually said when that difference matters.

If recall exposes a factual error or ambiguity in the explanation, identify it as a
learning-note correction. Do not score the learner against a claim that appears
wrong. Update the Question note only when the learner asks or when the current request
already includes maintaining the durable learning workspace.

## Optional lightweight record

Do not require a backend, card engine, scheduler, delivery service, or external
account. When the learner asks to save reviews or the supplied learning workspace
already has a review log, append one compact local record after the outcome is known.
Use `reviews.yaml` beside `thread.yaml` unless the workspace already defines another
location.

Keep each event limited to:

```yaml
- question: q001
  reviewed_at: 2026-09-18T12:00:00+08:00
  prompt: <prompt actually asked>
  answer: <learner's actual answer or null>
  hints: []
  evaluation: recalled | partial | not_recalled | not_scored
  correction: <learner correction or null>
```

Use an ISO 8601 timestamp with the actual local offset. Preserve the learner's answer
and any correction in their own words; do not fabricate a concise answer for them.
Append exactly one event for one completed attempt or skip, and do not record candidate
suggestions.

Review never changes `thread.yaml`, the current learning question, question
relationships, or understanding feedback. Scheduling, reminders, flash-card
generation, and delivery belong to separate explicitly requested workflows.
