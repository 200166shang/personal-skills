---
name: learning-point
description: "Use when capturing, recalling, rehearsing, or refining a small knowledge point, project detail, or interview answer without recursive exploration."
disable-model-invocation: true
---

# Learning: Point

A Point is the smallest useful piece of understanding the learner can explain
independently. Use it for active recall, quick review, tutorial or project details, and
interview answers—not to explore an unresolved subject or summarize a whole Topic.

## Choose the mode

- **Capture or refine:** The learner wants to save or improve a small point. Help make
  its prompt and answer clear, then update the Point document when using a durable
  Learning Workspace.
- **Recall or interview:** Ask for the learner's answer before showing saved wording.
  After they respond, compare it with the saved Point, clarify gaps, and let them retry
  when useful.
- **Unclear knowledge gap:** If the learner cannot explain a mechanism or needs
  recursive follow-up questions, answer the immediate question if possible and suggest
  continuing with `learning-learn`. Do not turn the Point into an exploration thread.

## Store Points

Use the supplied or clearly identified Learning Workspace. Keep Points independent of
Question Roots and Topic articles; a Point may be useful even when no matching Topic
exists.

The default layout is:

```text
learning-workspace/
  points/
    points.md
```

Keep one `points.md` for the whole Learning Workspace by default. Add or update entries
there; do not create one file per Point, require a Topic association, or split the file
into categories. If the learner later asks for more records or a different layout,
follow that request.

Use one second-level heading per Point. Write a direct prompt as the heading and a
concise answer that can be spoken without opening the Topic or Question notes. Include
an optional project connection or interview phrasing only when it helps the learner
explain the point. Preserve the learner's own project facts and wording; do not invent
experience or details. Avoid turning an entry into a multi-section article.

Example:

```markdown
# Points

## How do the device SDK and ROS driver divide responsibility?

The SDK handles device communication and vendor-protocol parsing. The ROS driver
converts the resulting measurements into ROS messages such as `sensor_msgs/LaserScan`
and publishes them. In an interview, I can summarize this as: the SDK handles the
device protocol; the driver integrates the device with ROS.
```

When recalling a Point, use its heading as the cue and keep the answer hidden until the
learner has tried. Accept a technically sound answer in the learner's own words rather
than requiring a memorized script. Explain only material gaps, then reveal or refine the
saved version.

## Boundaries

- `learning-learn` owns recursive exploration, Root Questions, and durable explanations.
- `learning-organize` owns Topic Compasses and coherent Topic articles.
- `learning-point` owns concise recall and spoken explanations. It does not own a
  Question graph, Topic structure, mastery score, schedule, or spaced-repetition state.
- A Point is independent: do not move it under a Topic or make it contingent on having
  completed a Topic.

If a recall attempt reveals a real gap, preserve the small Point and follow the gap in
`learning-learn`; update the Point after the learner understands the answer.
