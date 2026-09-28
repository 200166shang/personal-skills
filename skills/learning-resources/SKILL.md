---
name: learning-resources
description: "Find and curate high-quality external materials for a technical subject, Learning Question, or Organized Topic."
disable-model-invocation: true
---

# Learning: Resources

Find things worth learning from; do not learn them on the learner's behalf. Return a
small, verified list of external materials the learner can inspect personally, not an
investigation report or replacement textbook.

Use this Skill for official documentation, tutorials, source code, demos, example
projects, technical articles, talks, videos, or courses. The context may be a free-form
subject, the current or named Question in a multi-Root workspace, or an Organized Topic.

## Understand the context

Determine what the learner is studying, what they already understand, the material
types they want, and the appropriate depth. Do not assume beginner level.

When a learning workspace is available, read only enough context to curate relevant
materials:

- for the current Question, read `root-compass.yaml`, the active Root's `thread.yaml`,
  its current note, and only the parent Questions materially needed;
- for named Questions, resolve Root-qualified IDs such as `r003-q002` through their
  Root-local thread; a local `qNNN` requires a clear Root context;
- for an Organized Topic, read `organized/compass.yaml`, the named Topic, and its
  contributing Question notes only when needed.

A durable workspace is optional. Ask one concise direction question only when two
materially different interpretations would produce substantially different resources
and the request does not choose between them.

## Find, verify, and curate

Search broadly enough to discover strong candidates, then return about 3–6 core
resources by default. Quality and complementary roles matter more than count. Prefer
primary or official sources for authoritative claims, and add strong explanatory or
real-world material when it serves a distinct learning purpose.

Open or inspect every recommended resource enough to verify that it exists, covers the
claimed subject, and is credible for the role assigned to it. Mention a section, class,
function, file, demo, or video chapter only after verifying that entry point. Never
invent coverage or navigation details.

Avoid redundant links. Useful complementary roles may include an official reference,
official tutorial, source implementation, minimal demo, real-world repository, strong
explanatory article, or system walkthrough. Do not force every role into every result.

## Return the resource list

For each recommendation provide:

- title, direct link, and source type;
- why it is worth inspecting now;
- the exact section, concept, code entry point, or passage to focus on;
- how it connects to the learner's Question, Topic, or stated subject.

Include a reading order when sequencing matters. A brief note about a useful follow-up
concept is allowed, but do not turn it into gap analysis or a generated curriculum.

Do not create or update Questions, Topics, Learning Notes, research notes, manifests,
or runtime state. Do not write `research/rNNN.md`, produce a long investigation report,
recursively research every unfamiliar term, or rewrite the sources into a new chapter.
If a resource raises a real question, the learner may later pursue it explicitly with
`$learning-learn`.
