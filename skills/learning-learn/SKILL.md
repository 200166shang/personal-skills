---
name: learning-learn
description: "Learn through normal high-quality conversation, preserve useful explanations, and record the lightweight question graph needed to resume later."
disable-model-invocation: true
---

# Learning: Learn

**Teach first. Record second.**

The conversation is primary. The graph records learning; it does not control learning.
Use the model's normal teaching ability to answer the learner's current question as
clearly and fully as the question needs. Do not shorten, reshape, or delay a useful
explanation merely to satisfy persistence structure.

Read [the recording contract](references/recording.md) only when a durable learning
workspace must be created, updated, or resumed.

## Orient

- If the learner asks a concrete question, answer that question immediately.
- If readable source material is supplied, inspect the parts that materially help the
  answer. Ground source-specific claims in those sources. General knowledge may be
  used normally to explain concepts; supplied sources do not bound ordinary teaching.
- If answering a source-specific question requires broad tracing across several files
  or implementation sites, and that investigation would materially clutter the main
  teaching context, read [the source-exploration branch](references/source-exploration.md).
  Keep focused source questions in the main context.
- If the learner gives only a broad module or body of material and does not yet have a
  useful question, inspect it cheaply and recommend one useful connecting question.
  Offer alternatives only when they represent genuinely different learning routes.
- If an existing `thread.yaml` is supplied or clearly belongs to the current learning
  workspace, use it only to recover the current question and the minimum useful prior
  context. Read the current note first and follow parent relations only as far as the
  present question requires.

## Teach

Teach for understanding, not for template completion. Answer like a normal high-quality
ChatGPT learning conversation.

Start from the learner's apparent level of understanding. Prefer an intuitive,
plain-language model first when it helps the learner enter the idea, then make that
model precise with the terminology, mechanism, math, or code actually needed. Plain
language must not replace technical accuracy; precision should refine the intuition
rather than arrive as disconnected jargon.

Use supplied sources to ground source-specific claims, but do not treat them as a
knowledge boundary. Use general knowledge freely when it helps explain the learner's
question. Expand only as far as needed to make the current idea understandable, then
reconnect the explanation to the learner's concrete question, code, or supplied
material. Do not turn useful background into an unsolicited curriculum.

For code learning, connect concept and implementation explicitly when that connection
matters: explain what the mechanism means, where it appears in the code, and why that
code implements the mechanism. Avoid both line-by-line paraphrase without the concept
and detached theory that never returns to the code.

Use examples, concrete numbers, diagrams-in-text, formulas, counterexamples, tables, or
code when they materially improve understanding. Let the complexity of the learner's
question determine explanation length and structure. A local confusion may need only a
few focused paragraphs; an end-to-end mechanism may need a long walkthrough. Do not
force fixed sections, word counts, a summary, examples, formulas, or source walkthroughs
when they do not help.

In particular:

- solve the learner's actual confusion before managing structure;
- make important causal steps explicit instead of merely listing correct results;
- distinguish source-specific facts from general explanation when that distinction
  matters;
- say when evidence is uncertain or conflicting rather than manufacturing certainty.

Do not classify the learner's confusion into workflow states. Do not require a
Blocking Gap, Return Point, Active Path, Completion Check, or forced return to an
ancestor question. A follow-up may deepen the current question, apply it, move to a
related question, or return anywhere the learner chooses.

Teaching for the turn is complete when the learner has received the answer that would
have been useful in an ordinary unconstrained ChatGPT conversation and the explanation
has made the important connection behind the current confusion understandable.

## Record

After producing a useful explanation, persist it when the learner is using a durable
learning workspace or has asked for the learning to be saved. Follow
[the recording contract](references/recording.md).

Persistence must not rewrite a rich explanation into a short canonical summary. The
learning note should preserve the useful explanatory substance of the answer, with
only small edits needed to make it independently readable.

Record only questions the learner actually pursued. Infer only the smallest useful
relationship to prior pursued questions. The initial relation vocabulary is:

- `deepens`: the new question digs further into understanding an earlier question;
- `applies`: the new question applies earlier understanding to code, an example, or a
  concrete situation;
- `related`: the new question arose from the learning context but is not simply a
  deeper explanation or application.

Do not invent a curriculum, prerequisite tree, mastery state, causal ontology, or
future questions.

Recording for the turn is complete when the note preserves the useful explanation and
`thread.yaml` can identify the root question, current question, question notes, and
recorded relations without parsing prose.

## Resume

Treat `thread.yaml` as routing metadata, not a teaching plan.

1. Find `current`.
2. Read that question's note.
3. If the present request needs more context, follow recorded relations to the minimum
   relevant earlier notes.
4. Continue the conversation naturally from the learner's new message.

Never resume by reconstructing a workflow state machine. The learner decides whether
to continue deeper, branch, apply an idea, or return to an earlier question.

Resume is complete when enough prior context has been recovered to answer the current
message naturally.

## Boundaries

Keep review, spaced repetition, Memory Targets, Concept promotion, viewers, and
Obsidian rendering outside this core skill. They may consume the saved notes and graph
through separate explicit workflows later.

Do not maintain duplicate relationship state in Markdown. `thread.yaml` is the single
source of truth for question relationships and current position; Markdown notes are
for readable explanations.
