# Topic quality contract

A Topic is a long-form explanation around one coherent larger question or mechanism. It must let a learner reconstruct the understanding without opening the original Question history, including why each important step exists and how the steps connect.

## Reasoning spine

State the overall mental model near the beginning. Prefer a causal or logical chain such as:

```text
input
→ transformation
→ intermediate representation
→ next subsystem
→ output
```

Then explain the important stages and reconnect them at the end: **whole → parts → whole**. For every material stage, make clear what information changes, why the stage exists, and why its result enables the next stage. Include those explanations where they repair understanding rather than mechanically adding a “why” paragraph everywhere.

Preserve the reasoning spine; remove conversational redundancy. Compress duplicate definitions, repeated analogies, chat transitions, repeated introductions, and earlier wording superseded by a clearer later explanation. Retain important intermediate reasoning, useful mental models, material caveats, small examples that connect stages, source-code mappings, and places where understanding commonly breaks.

## Integration

Reconstruct the article from the combined understanding. Choose the best explanatory order regardless of Question chronology. Do not concatenate source Notes or create `## Q001` sections unless the learner explicitly requested a question-indexed format.

A Topic must add integration value beyond its sources: it should expose how scattered facts form one mechanism, why one stage leads to the next, and what the complete chain accomplishes. A list of correct definitions is not an integrated explanation.

Use a title that names the larger question or mechanism, such as “How wheel encoder data becomes robot pose,” rather than a category label such as “Encoder knowledge.”

When code matters, connect:

```text
concept
→ variable, function, or module
→ transformation performed by the code
→ why that implementation realizes the concept
```

Keep the mechanism primary; avoid a line-by-line source walkthrough. Add a small concrete example only when it materially connects stages.

## Scope and boundaries

One Topic should have one identifiable reasoning spine. Merge fragments that only make sense as stages of one mechanism. Split a Topic whose distinct mechanisms cannot share a clear spine.

Cover the learned substance needed for the larger question, not every detail from every source. Small bridging explanations are allowed. A new prerequisite tree, domain survey, or unrequested advanced theory is outside scope.

Synthesize learned understanding; do not invent a curriculum.

## Required review

Revise a Topic before finishing when any material answer below is no:

- Does it answer one clear larger question?
- Can it be understood without the original Questions?
- Is the overall mental model visible early?
- Is there an identifiable reasoning spine with important intermediate steps and why-reasoning?
- Are the sources integrated rather than appended, and repeated explanation compressed?
- Does the ending reconnect the parts into the whole mechanism?
- When code matters, are concept and implementation connected?
- Does it provide more integrated understanding than reading the source Questions separately?

Then review the Organization as a whole. Fix clear cases where Topics substantially duplicate one another, appear in an order that hides prerequisites, should be merged into one mechanism, should be split to recover a clear spine, or omit an important scoped Question.

When generation is governed by an approved Topic Compass, this review must not silently
change Topic boundaries, order, Question placement, includes, or exclusions. Complete
the requested Topic when the defect can be repaired within its contract. Otherwise stop,
report the specific Compass defect, and recommend returning to the planning stage.
