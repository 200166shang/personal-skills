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

## Reuse prior learning context

When the learner starts a new module, explicitly asks to reuse earlier learning, or
asks a question that clearly builds on another studied module, look for relevant
Learning Workspaces in the current learning collection. Use a path or collection the
learner supplied; otherwise infer the collection only when the current workspace's
parent directory clearly groups Learning Workspaces. Check direct candidates for
existing Learning markers such as `root-compass.yaml`. If the collection boundary or
candidate locations are unclear, continue with the available context instead of
searching the repository or filesystem broadly. A learner-named workspace may be
looked up outside the current collection.

Discover progressively: use workspace names and `organized/compass.md` to narrow the
search, read only relevant Topic articles, and use `root-compass.yaml`, the matching
Root's `thread.yaml`, and its Question notes when no suitable Topic exists. Do not
load every Question or use `review/interview.md` as a default knowledge source. Reuse
what is useful as background, focus integrated questions on the new mechanism and
connections, and respect requests to start fresh or avoid prior material. A concrete
question remains answerable without a discovery preamble; prior notes may inform the
answer when they materially help. Similarity alone never blocks a repeat explanation,
deeper exploration, or Question recording.

Keep cross-workspace reuse contextual: do not add global indexes, dependency graphs,
cross-workspace IDs, or new fields to the Root and Question data. Historical workspaces
are read-only during the current learning task. If useful, cite an existing note using
the ordinary Markdown link rules in [the recording contract](references/recording.md).

## Use the current workspace Library

The `learning-library` Skill owns `library/**`; Learn reads its catalog and original
sources but does not edit them.

When the learner asks to use registered materials, refers to a newly added source, or
requests a source-led Root Compass, read the current workspace's `library/index.md` and
inspect only the relevant original files or URLs. The index locates sources; it does
not establish their detailed contents. A concrete question can still be answered from
a directly supplied source without first creating a Library entry.

When the learner asks to expand an existing Root Compass from Library materials:

1. Resolve the specified `M###` entries or the new sources identified in the current
   conversation. Do not infer newness by scanning files or timestamps.
2. Read the existing `root-compass.yaml`. Use Root titles, relevant Root-local
   `thread.yaml` files, and the Topic Compass when present to understand current scope.
   Read Question notes or Topic articles only where needed to decide whether the
   material adds a distinct learning direction.
3. Decide whether the material opens a new direction, deepens an existing Root, or
   supports a concrete Question without changing the Root Compass. A new source alone
   does not require a new Root.
4. Present proposed Root candidates with a short reason and explain which existing
   Root could cover the material. After the learner accepts, append candidates to
   `root-compass.yaml` using the next unused stable Root IDs and `status: candidate`.
   Preserve all existing IDs, paths, statuses, and Question graphs. Candidate Roots
   have no `path` and no directory until the learner selects and activates one under
   the [recording contract](references/recording.md).

Adding Library material does not itself create a Question, activate a Root, or update
`organized/`. Record only questions the learner actually pursues. When a recorded
explanation relies on a Library source, cite its original file or URL and the useful
section or location; a Library ID alone is only a catalog reference.

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

When explaining behavior from source code, put the relevant real source in fenced code
blocks in the teaching answer, then explain each excerpt beside it in execution or data-
flow order. A file path and line number are useful locators, but are not a substitute
for showing the code the learner needs to understand. For a cross-file path, include the
important producer, handoff, and consumer excerpts, and connect them in prose (caller →
message/state → receiver → callee). Use complete relevant functions when they are
reasonably sized; otherwise include the smallest contiguous blocks that preserve the
important conditions, arguments, and handoff. Do not paste entire large files or pad
the answer with unrelated code. Keep source text faithful, label the language, and place
a clickable file-and-line locator with or immediately after each excerpt. Never invent
or silently rewrite an excerpt. If the source is unavailable, say so and explain the
limitation instead of presenting guessed code.

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
