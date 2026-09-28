---
name: learning-organize
description: "Create, refresh, approve, and execute a cross-Root Topic Compass over durable Learning Questions."
disable-model-invocation: true
---

# Learning: Organize

Roots preserve distinct exploration views. Questions preserve the learner's real
recursive paths. Topics preserve the current best explanation across one or many Roots.
Never reshape or deduplicate the Question layer to make the Topic structure prettier.

Separate exploration, structural judgment, and article generation:

`Question Graph → SNAPSHOT → COMPASS → REVIEW → APPROVE → GENERATE`

The approved Compass is the content contract for generation. New Questions continue
to accumulate normally; they affect Topics only through an explicit refresh.

## Choose one operation

- `compass`: take the first snapshot and create a draft Topic Compass. Use `plan` as a
  compatibility alias.
- `refresh`: compare the current Question graph with the last snapshot and propose the
  smallest Compass change that accounts for new Questions.
- `approve`: freeze the reviewed draft for generation.
- `generate all`, `generate t004`, `generate t001-t003`, or an explicit ID list:
  generate only those Topics from an approved Compass.

If no operation is named, continue the obvious unfinished stage. Otherwise start with
`compass`. Never combine Compass planning or refresh with article generation in one
turn.

The durable Organization is:

```text
organized/
  compass.md
  compass.yaml
  topics/
    t001.md
    t002.md
```

If an older workspace has `organized/organize.yaml` but no `compass.yaml`, treat it as
the current Compass and migrate it to `compass.yaml` on the next planning mutation.
If an older workspace has one top-level `thread.yaml` and flat `questions/`, preserve
its IDs and notes while migrating it to Root `r001` on the next Learn or Organize
mutation. Do not silently mix flat and Root-qualified IDs in one Compass.

## Create the first Compass

Read `root-compass.yaml`, every `thread.yaml` belonging to an `active` or `explored`
Root, and all notes in those Roots. Ignore candidate Roots: they are navigation ideas,
not learned material. Titles alone are insufficient. If scope is materially ambiguous,
ask one focused question.

Derive the smallest coherent set of Topics supported by the Questions:

- do not invent a subject that the learner never explored;
- merge semantically repeated Questions;
- give each Topic one stable larger question or mechanism;
- prefer fewer Topics, but never force distinct mechanisms into one article;
- prefer causal reading order over Question chronology;
- define required content and explicit exclusions for every Topic.

Write `compass.md` as the complete learner-facing map. Show its draft status, revision,
source snapshot, proposed Topic count, organizing rationale, and for every Topic:

- provisional ID and title;
- purpose or larger question;
- source Question IDs;
- required content;
- excluded or deferred content;
- relationship to neighboring Topics.

Write the same contract to `compass.yaml`:

```yaml
version: 1
revision: 1
status: draft
source_snapshot:
  roots:
    r001: r001-q004
    r003: r003-q002
organization:
  title: <human-readable title>
topics:
  t001:
    title: <Topic title>
    purpose: <larger question or learning goal>
    sources:
      - r001-q004
      - r003-q002
    include:
      - <required mechanism or connection>
    exclude:
      - <boundary delegated elsewhere or intentionally omitted>
    contract_revision: 1
    file: topics/t001.md
order:
  - t001
change_set:
  unchanged: []
  regenerate: []
  added:
    - t001
  removed: []
```

The snapshot records the highest local Question considered in each activated or
explored Root. Root-qualified Question IDs remain stable. A Topic may cite Questions
from several Roots, and one Question may support several Topics. Important scoped
Questions should normally appear at least once; explicitly explain any omission.
Never assign a Topic to one Root with `root:` and never add `same_as` or canonical
Question metadata. Cross-Root semantic deduplication belongs only in Topic contracts.

Present the complete Compass in the conversation and stop for review. On feedback,
update only `compass.md` and `compass.yaml`; do not write Topic articles. Increase the
Compass revision for each accepted structural revision and keep both files consistent.

## Refresh from new Questions

Refresh never redesigns the whole Organization by default.

For low-reasoning execution, use the durable state as authority: read the existing
contracts, calculate the new per-Root Question delta, apply the smallest justified
change, save it, and stop. An approved Compass outranks a temporary alternative
organization the model might prefer.

1. Read `root-compass.yaml`, all activated Root threads, and the current Compass.
   Calculate the Root-qualified Question IDs newer than `source_snapshot.roots`, plus
   all Questions in a Root activated since the snapshot.
2. If there are no new Questions, report that the Compass is current and change no
   files.
3. Read the new Question notes. Read existing source Questions or Topic articles only
   where needed to decide which current boundary is affected.
4. Propose a minimal diff: extend an existing Topic, add a new Topic for a genuinely new
   stable cluster, or rarely merge/split when the new material proves the old boundary
   wrong. Preserve unrelated Topics exactly.
5. Update the snapshot to include all Questions considered, increment the Compass
   revision, set `status: draft`, and record the exact `change_set`.

For an unchanged Topic, preserve its ID, contract, and `contract_revision`. For a changed
Topic, increment `contract_revision` and list it under `regenerate`. New Topics begin at
`contract_revision: 1` and appear under `added`; retired IDs appear under `removed`.

Show the Question delta and proposed Compass delta to the learner, then stop for review.
Do not modify existing Topic articles during refresh.

## Approve and freeze

Clear approval changes `status` from `draft` to `approved`; do not request a second
confirmation. Make `compass.md` agree with the approved machine plan.

On approval, preserve article files for `change_set.unchanged`. Remove article files for
`change_set.regenerate` and `change_set.removed` so stale content cannot appear current.
New Topics have no article until generated. Report which Topics remain valid and which
must be generated.

Approval freezes structural judgment. Generation cannot change Topic boundaries,
Question placement, includes, exclusions, order, or contract revisions.

## Generate from the approved Compass

Refuse generation unless `status` is `approved`. Resolve the requested ID, range, list,
or `all` against `order`; reject unknown IDs instead of inventing Topics.

Before writing, read the complete [Topic quality contract](references/topic-quality.md).
For each requested Topic independently:

1. Read only its Compass contract and the full notes named by `sources`. Resolve each
   Root-qualified ID through that Root's `thread.yaml`.
2. Cover every material `include` item and do not expand the `exclude` items.
3. Use another Question only for a small bridge needed for coherence.
4. Briefly reference neighboring Topics when useful, without duplicating their detail.
5. If source material is insufficient, report the gap; do not expand the curriculum or
   silently change the contract.
6. Do not modify any other Topic or Compass field.

Start each generated article with provenance frontmatter:

```yaml
---
topic: t001
compass_revision: 3
contract_revision: 2
---
```

`contract_revision` determines freshness. A Topic remains valid across later Compass
revisions when its contract revision did not change. This lets `refresh` preserve
unaffected articles and regenerate only the delta.

## Validate

After Compass creation, refresh, or approval, confirm:

- `compass.yaml` parses and agrees with `compass.md`;
- the snapshot contains every Question considered by this revision;
- every `order` entry has a complete contract and every cited Root-qualified Question exists;
- the change set exactly describes changed, added, removed, and preserved Topics;
- important scoped Questions are covered or their omission is explained;
- draft operations did not modify Topic articles.

After generation, additionally confirm:

- every requested file exists at its planned path;
- its provenance matches the approved Compass and Topic contract revisions;
- required content is covered and excluded content is not expanded;
- the article passes the Topic quality contract without duplicating neighboring Topics;
- the Compass, Question graph, Question notes, and unrequested Topic files are unchanged.

Topics are replaceable projections. Reorganization always returns to durable Questions;
never create Topic groups, Topic-local Question systems, meta-Topics, archives, or
`organized-v2/`. Git provides history.

Learn naturally first. Organize understanding later. Synthesize learned understanding;
do not invent a curriculum.
