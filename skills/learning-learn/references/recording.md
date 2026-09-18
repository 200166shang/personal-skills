# Recording contract

Use this contract only for durable recording or resume. Teaching quality must not be
changed to make recording easier.

## Workspace shape

Use one directory per Learning Thread:

```text
<thread>/
├── thread.yaml
└── questions/
    ├── q001.md
    ├── q002.md
    └── ...
```

`thread.yaml` is the single source of truth for routing and relationships. Question
Markdown is the readable learning artifact. Do not duplicate graph state in notes.

## Minimal schema

Keep the schema intentionally small:

```yaml
version: 1

thread:
  title: <human-readable title>
  root: q001
  current: q003

nodes:
  q001:
    title: <question in learner language>
    file: questions/q001.md
  q002:
    title: <question in learner language>
    file: questions/q002.md
  q003:
    title: <question in learner language>
    file: questions/q003.md

edges:
  - from: q001
    to: q002
    type: deepens
  - from: q002
    to: q003
    type: applies
```

Required top-level keys are `version`, `thread`, `nodes`, and `edges`. Keep
`version: 1`. `thread` contains only `title`, `root`, and `current`. Each node contains
only `title` and `file`. Each edge contains only `from`, `to`, and `type`.

Do not add fields speculatively. In particular, do not add Active Path, Blocking Gap,
Return Point, completion evidence, mastery, review state, source boundaries, generated
prerequisites, tags, or graph ontology fields.

## IDs

Use simple thread-local sequential IDs: `q001`, `q002`, and so on. IDs are stable after
creation. A renamed or improved question title keeps its ID and file.

## Record a turn

Record only a question the learner actually pursued and for which a useful explanation
was produced.

For a new thread:

1. Create `q001` from the learner's actual question.
2. Save the useful explanation to `questions/q001.md`.
3. Set both `root` and `current` to `q001`.
4. Start with an empty `edges` list.

For a later pursued question:

1. Reuse an existing node when the learner is plainly continuing the same question
   rather than creating a distinct question.
2. Otherwise allocate the next sequential ID and save a new question note.
3. Add at most one direct edge that best captures how the new question arose from a
   previously pursued question. Prefer the immediate conversational parent when it is
   clear. Do not manufacture ancestry when it is not clear.
4. Use only `deepens`, `applies`, or `related`.
5. Set `thread.current` to the question the learner is now pursuing.

When the learner explicitly returns to an existing question, set `current` to that
existing node instead of creating a duplicate node.

## Build a note for relearning

A Question note is a reconstructed explanation optimized for **relearning**. It is not
a chat transcript and not a terse knowledge summary. Conversation may discover ideas
in a messy order; the note may reorganize them into the order that best rebuilds the
understanding later.

Use this minimum shape, without forcing any additional section template:

```markdown
# <question>

<a self-contained explanation organized for understanding this question again>
```

Preserve **learning value, not wording**. When integrating or restructuring a note,
retain the parts that made the idea understandable: important `why` reasoning, useful
mental models, intermediate mechanism, connections to prior concepts, concrete
examples or counterexamples, concept-to-code mappings, material caveats, and source
references. Rewrite wording, reorder sections, merge repetition, and remove chat-only
transitions when that makes the explanation better.

**Compress redundancy, not reasoning.** Do not turn a rich explanation into a list of
correct conclusions by deleting the intermediate reasoning that lets the learner
reconstruct why those conclusions follow.

When later turns improve the same Question, integrate the new understanding into the
existing note. Prefer local integration when the article remains coherent; restructure
the whole note when accumulated additions, corrections, or changed understanding make
a different explanatory order substantially clearer. Do not preserve conversation
chronology merely because it happened first.

Let the question determine the shape of the note:

- For a standalone concept, make the explanation self-contained. Explain the concept,
  motivation, mechanism, useful example, distinctions, or boundaries only as they help
  understanding; do not invent project context.
- For a source- or project-specific question, anchor source-specific claims in the
  supplied material and explicitly connect the general concept to the relevant code,
  data, or project behavior. General knowledge may still be used to make the mechanism
  understandable.
- For an end-to-end system question, establish the overall mental model and organize
  the stages in causal order, using concrete data or code where it helps the learner
  see how one stage produces the next.

These are quality guides, not mandatory Markdown sections. Do not manufacture
`Background`, `Principle`, `Example`, `Source`, `Common mistakes`, or `Summary`
sections when the question does not benefit from them. Let complexity determine the
length and structure.

## Sources

When an explanation depends on supplied code, documentation, PDFs, or prepared notes,
keep useful source locators close to the relevant prose in the Markdown note. Source
metadata is explanatory evidence, not graph routing state, so it does not belong in
`thread.yaml` version 1.

General conceptual explanation does not require pretending it came from the supplied
sources. Make the distinction clear when it matters.

## Resume

Read `thread.current` and its note first. If the new user message depends on earlier
context, inspect only the relevant connected nodes needed to understand it. Do not
parse Markdown to reconstruct relationships already represented in YAML.

A graph is a projection of learning that already happened. Never use it to force the
learner down a predetermined path.

## Determinism boundary

Be deterministic about persistence:

- valid minimal YAML;
- stable node IDs;
- existing nodes are not duplicated;
- only the three relation values are used;
- `current` points to an existing node;
- every edge endpoint exists;
- every node file exists;
- Markdown contains no second copy of graph routing state.

Be flexible about teaching and note composition. The recorder may improve explanatory
structure, but it must preserve the learning value that made the understanding useful.
