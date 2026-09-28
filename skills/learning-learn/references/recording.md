# Recording contract

Use this contract only for durable recording or resume. Teaching quality must not be
changed to make recording easier.

## Workspace shape

One learning workspace may contain several independent Root explorations:

```text
<workspace>/
├── root-compass.yaml
├── questions/
│   ├── r001-end-to-end/
│   │   ├── thread.yaml
│   │   ├── q001.md
│   │   └── q002.md
│   └── r003-concurrency/
│       ├── thread.yaml
│       └── q001.md
└── organized/
    ├── compass.md
    ├── compass.yaml
    └── topics/
```

`root-compass.yaml` owns Root candidates and status. A Root directory exists only after
activation. Each Root-local `thread.yaml` owns Question navigation for that Root.
Question Markdown is the readable learning artifact.

For a legacy workspace with one top-level `thread.yaml` and flat `questions/`, migrate
on the next durable mutation: create Root `r001`, move the thread and notes under one
Root directory, qualify its IDs with `r001-`, and preserve titles, note content, order,
and relationships as parent links where the immediate ancestry is unambiguous. Never
maintain both layouts as writable state.

## Root Compass

Use this minimal schema:

```yaml
version: 1
roots:
  r001:
    title: How does one request travel through the whole system?
    status: explored
    path: questions/r001-end-to-end
  r002:
    title: How do the core objects collaborate?
    status: candidate
  r003:
    title: How does concurrency work in this system?
    status: active
    path: questions/r003-concurrency
```

Allowed status values are `candidate`, `active`, and `explored`. Keep at most one Root
active. A candidate has no `path` and no directory. To activate a candidate, assign a
stable path, create its directory and Root Question, mark the previously active Root
`explored`, and mark the selected Root `active`. Never delete another Root's graph when
switching.

When creating a Root Compass for a broad unfamiliar module, propose only 3–5 broad,
chain-forming views. Do not create Question directories until the learner selects a
Root. When the learner starts with a concrete durable question, it may directly become
`r001` without first proposing unused candidates.

## Root-local thread

Each activated Root uses:

```yaml
version: 1
root:
  id: r003
  title: How does concurrency work in this system?
current: r003-q003
nodes:
  r003-q001:
    seq: 1
    title: How does concurrency work in this system?
    file: q001.md
    parent: null
    status: explored
  r003-q002:
    seq: 2
    title: Why does TTS use a separate worker?
    file: q002.md
    parent: r003-q001
    status: explored
  r003-q003:
    seq: 3
    title: Can function execution block playback?
    file: q003.md
    parent: r003-q002
    status: active
```

Required keys are `version`, `root`, `current`, and `nodes`. A node contains only
`seq`, `title`, `file`, `parent`, and `status`. Question status is `active` or
`explored`; exactly one node is active and equals `current`.

File names and visible sequence numbers restart within every Root (`q001.md`,
`q002.md`). Machine-stable Question IDs always include the Root (`r003-q001`). IDs and
paths remain stable after creation.

## Record and navigate

For an activated Root, its Root Question is always local `q001`. Save each genuinely
pursued later Question as the next local sequence. Use the current Question as parent
when the follow-up arose from it; use another existing Question only when the learner
explicitly returned there. Do not manufacture ancestry.

On a push to a new Question, mark the previous node explored, create the new active
node, and update `current`. On an explicit return or pop, mark the old current explored,
mark the selected existing node active, and update `current`; do not create a duplicate.
Navigation never means the learner has mastered or completed the material.

Similar Questions in different Roots remain separate. The Question layer preserves why
the learner reached each question in that view. Do not block a question because it
resembles an earlier one and do not add cross-Root identity metadata. Topic organization
is responsible for later semantic aggregation.

## Build a note for relearning

Use the minimum note shape:

```markdown
# <question>

<a self-contained explanation organized for understanding this question again>
```

Preserve learning value, not chat wording. Retain important why-reasoning, mental
models, intermediate mechanisms, examples, caveats, concept-to-code mappings, and
useful source locators. Compress repetition, not reasoning. Integrate later improvements
into the same note when the learner is still pursuing the same Question.

Let the question determine structure and length. Do not force template sections. For
source-specific questions, distinguish evidence from general explanation and reconnect
concepts to the relevant code or data. Markdown must not duplicate Root status,
Question parent links, or current-position metadata.

## Topics and continued learning

Topics are replaceable projections across one or many Roots. Learn never mutates
`organized/`. After a Compass exists, continue appending Questions to the appropriate
Root. Only explicit `$learning-organize refresh` compares those Questions with its
snapshot.

## Determinism boundary

Be deterministic about persistence:

- valid minimal YAML;
- one active Root at most and one active Question per activated Root;
- stable Root-qualified IDs and Root-local sequence numbers;
- every `current`, parent, path, and note file resolves;
- candidate Roots have no directories;
- Markdown contains no duplicate navigation state.

Be flexible about teaching and note composition. The graph records learning that
already happened; it never prescribes a curriculum.
