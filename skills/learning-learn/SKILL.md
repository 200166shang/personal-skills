---
name: learning-learn
description: "Learn through Root-guided recursive questions, preserve useful explanations, and resume any explored learning route."
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
- If the learner gives a broad unfamiliar module and no useful question, inspect it
  cheaply and create or present a Root Compass with 3–5 candidate Root Questions.
  Prefer distinct views such as end-to-end flow, core collaborators, data flow,
  concurrency, and external integration. Recommend the end-to-end Root first when it
  is useful. Do not turn the Compass into a curriculum or pre-generate child Questions.
- If the learner chooses a Root, activate it. Its Root Question becomes `q001` in an
  independent Root directory. Unselected candidates remain in `root-compass.yaml`
  without a Question directory.
- If the learner already asks a concrete question, answer immediately. When durable
  recording is requested and no Root exists, use that question as the first active
  Root instead of forcing a preliminary Compass review.
- If an existing Root workspace is supplied, resolve the named Root or the active Root,
  then read its `thread.yaml` and current note. Follow parent links only as far as the
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

Do not classify understanding into mastery or completion states. A follow-up may push
deeper, apply an idea, move sideways, or return to any earlier Question. `current` and
`parent` only preserve navigation; they do not force the next teaching action.

The learner may begin with one broad Root Question and recurse through follow-ups for
as long as the exploration remains useful. Every genuinely pursued follow-up remains an
ordinary Question in the same graph. Do not split Questions into “exploration” and
“Topic-local” types, renumber them under Topics, or force the learner to stop exploring
after a Topic Compass exists.

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

Record only Questions the learner actually pursued. Questions are local to one Root;
similar Questions under different Roots are valid because they preserve different
learning contexts. Use the immediate conversational Question as `parent` when clear.
Do not add cross-Root canonicalization, duplicate detection, or `same_as` metadata.

Do not invent a curriculum, prerequisite tree, mastery state, causal ontology, or
future questions.

An existing Topic Compass is downstream organization, not a recording boundary. New
Questions continue to receive the next local `qNNN` within their Root and stable IDs
such as `r003-q007`. Do not attach them directly to Topics or update the Compass during
Learn; `$learning-organize refresh` handles that explicit projection step later.

Recording for the turn is complete when the note preserves the useful explanation and
the Root-local `thread.yaml` can identify the current Question, its parent chain, and
Question notes without parsing prose.

## Resume

Treat each Root-local `thread.yaml` as routing metadata, not a teaching plan.

1. Resolve the requested Root or the active Root from `root-compass.yaml`.
2. Find `current` in that Root's `thread.yaml`.
3. Read that Question's note.
4. If the present request needs more context, follow parent links to the minimum
   relevant earlier notes.
5. Continue the conversation naturally from the learner's new message.

Never resume by reconstructing a workflow state machine. The learner decides whether
to continue deeper, branch, apply an idea, or return to an earlier question.

Resume is complete when enough prior context has been recovered to answer the current
message naturally.

## Boundaries

Keep review, spaced repetition, Memory Targets, Concept promotion, viewers, and
Obsidian rendering outside this core skill. They may consume the saved notes and graph
through separate explicit workflows later.

Do not maintain duplicate navigation state in Markdown. `root-compass.yaml` owns Root
status; each Root's `thread.yaml` owns its Question navigation; Markdown notes are for
readable explanations.
