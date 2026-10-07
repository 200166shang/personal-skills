---
name: learning-plan
description: "Maintain a small Markdown learning state page with the learner's goal, current direction, bookmark, next step, and deferred topics."
disable-model-invocation: true
---

# Learning: Plan

Keep one short, human-readable Markdown page that helps the learner remember why they
are learning, which direction they are following, where they stopped, and what to do
next. The page is both the source of truth and the view the learner can open directly
in Obsidian.

## State page

Use `learning-state.md` at the root of the supplied or clearly identified Learning
Workspace. Keep its structure to these five sections:

```markdown
# Learning State

## Goal

...

## Current Direction

...

## Bookmark

...

## Next

...

## Later

...
```

- **Goal**: the stable, plain-language reason for learning and the intended long-term
  outcome.
- **Current Direction**: the main learning thread and why it matters now. Describe it
  naturally; do not split it into phases or sprints.
- **Bookmark**: the concise point where the learner stopped, enough to resume after a
  break. Link to learning notes when useful; do not copy them.
- **Next**: one natural first step for the next session.
- **Later**: important topics intentionally deferred for now.

## Read

When the learner asks what they are studying, where they stopped, or what to continue,
read `learning-state.md` and answer from **Current Direction**, **Bookmark**, and
**Next**. Keep the response brief and grounded in the page. A read request leaves the
file unchanged unless the same request also asks to record new state; in that case,
follow **Update** for the affected sections. If the page is missing, say that no saved
state page is available.

## Update

When the learner asks to record progress or change the learning direction, read the
existing page first. Create it with the fixed structure if it does not exist. Use only
information the learner has supplied or confirmed; leave unknown sections brief rather
than filling them by assumption. Ask one focused question only when it is impossible to
tell what they want recorded.

Change only the sections affected by the update and preserve the rest. Progress usually
changes **Bookmark** and **Next**. A temporary change of focus may also change **Current
Direction** and **Later**. Change **Goal** only when the learner explicitly changes the
long-term outcome. When the learner pauses a direction, preserve its useful bookmark
and next step in one concise **Later** item. If the new direction has no supplied
bookmark or next step, write `尚未记录` in those sections instead of carrying over the
old direction's state or guessing. Keep **Next** to one action and **Later** to a short
list.

## Boundaries

This Skill owns only `learning-state.md`. `learning-learn` owns Questions, explanations,
Question Graphs, and Learning Notes. `learning-organize` owns Topic Compasses and Topic
articles. Link to those materials when useful, while keeping this page about orientation
rather than knowledge content.

Keep the state in Markdown. Do not add YAML, JSON, checkpoint history, a generated view,
curriculum, roadmap, phases, sprints, daily plans, task lists, mastery, streaks, due
dates, deadlines, or schedules. Do not create or edit Questions, Root/thread state, or
Topic files. A break alone does not call for a new learning direction; restore the
Bookmark and Next from the page.
