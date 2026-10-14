---
name: daily-journal
description: "Record, correct, or read daily Markdown in an Obsidian Vault, with deep-learning time totals and lazy monthly archiving."
disable-model-invocation: true
---

# Daily Journal

Use `$daily-journal` with natural language to add, correct, or read a diary. Keep the
user's voice and record only supplied events and feelings; do not add evaluations.

## Resolve the diary

Use the Vault path explicitly supplied or established in this conversation. If it is
unknown or ambiguous, ask for it before accessing files. Diaries belong in that
external Vault, never in this skill repository. Resolve relative dates using the
user's local date and timezone; default to today only when no other day is indicated.

For each date, check both `Journal/YYYY-MM-DD.md` and
`Journal/Archive/YYYY/MM/YYYY-MM-DD.md` before creating anything. Use the existing
file wherever it is. If both exist, report the conflict and ask which file to use;
do not merge them or choose silently. New current-month diaries go in `Journal/`;
new past-month diaries go directly in the matching archive directory. Ask about an
apparently future date before creating a diary.

Read requests only inspect existing files and answer from their content. A missing
diary is a missing record, not an empty diary to create. Do not create directories,
recalculate saved totals, edit files, or archive during a read-only request.

## Record and correct

Read the entire existing diary before editing. New diaries use exactly these three
H2 sections, with no YAML, ratings, progress bars, or extra sections:

```markdown
# 2026-10-14

## 时间线

- 09:00–11:00｜📚 深度学习：CNN 卷积
- 14:00–16:00｜💻 项目开发：ROS 2

## 今日记录

今天理解了多通道卷积。

## 学习统计

**深度学习：2h / 4h**
```

The example is a format, not content to prefill. Leave empty timeline/record sections
empty and start the total at `0h / 4h` when no qualifying intervals are known.

- Put clearly timed activities in 时间线, in time order. Normalize unambiguous times
  to `HH:MM–HH:MM`; retain explicit dates for intervals crossing midnight and split
  their counted minutes across the corresponding diaries. Clarify ambiguous dates,
  AM/PM, or end-before-start intervals before assigning times.
- Put untimed events, reflections, and feelings in 今日记录. Preserve uncertain time
  wording there without inventing an interval; ask only if a precise interval is
  needed for the requested calculation or correction. Project work is not deep
  learning unless the user explicitly marks it as such.
- Append only new information. Compare meaning, date, activity, and interval with
  existing entries so repeating the same request is a no-op. An explicitly distinct
  event may share wording or time with another; clarify if duplication is uncertain.
- Correct only the uniquely identified entry and any resulting learning total. If
  several entries match, ask which one before changing them. Preserve unrelated
  wording, links, spacing, and manual edits; use targeted edits rather than rewriting
  the diary. If an existing structure conflicts with the three-section format, ask
  before restructuring or discarding manual content.

## Learning time

Count only intervals explicitly labeled `📚 深度学习` (including activities the user
explicitly asks to label that way). Read all such intervals, including manual entries.
Merge overlapping intervals into their union, then subtract the union of explicitly
timed breaks that applies to that learning, clipped to the counted intervals. Shared
minutes and breaks are counted once. Do not subtract breaks belonging only to project
work. Clarify a break's timing or scope when it affects the requested total; do not
guess. Untimed learning has no countable duration.

Calculate in minutes, then divide by 60. Display only
`**深度学习：Xh / 4h**` in 学习统计: use a compact decimal (up to two decimal places,
no trailing zeros), a fixed 4h target, and no cap. For example, 09:00–12:00 plus
11:00–14:30 with a 12:00–12:30 break is `5h / 4h`. Recalculate after relevant edits;
if existing ambiguous learning entries prevent a reliable total, clarify before
changing that total. Do not infer study time from project work or prose.

## Lazy monthly archive

On a write invocation, after resolving any ambiguity that blocks the requested edit,
inspect root-level `Journal/YYYY-MM-DD.md` files. Archive only regular, non-symlink
files whose basename is a valid calendar date strictly before the user's current
month. Leave current/future months, invalid dates, and other files alone.

Before each move, check the destination and Obsidian link risks:

- Destination: `Journal/Archive/YYYY/MM/YYYY-MM-DD.md`. If anything already occupies
  that path, skip and report the conflict, even if the contents look identical.
- Inspect Vault Markdown and relevant Obsidian configuration for links/embeds to the
  old path (wiki links, Markdown links, encoded paths, and heading/block suffixes),
  relative links inside the diary that would resolve differently after the move,
  and configured daily-note paths. Check basename-only links for ambiguity. External
  filesystem moves do not guarantee Obsidian backlink updates. If a link may break
  or the check cannot establish safety, leave that file in place, report the risk,
  and ask about the move only if needed; continue other safe writes and moves.

Create archive directories only when moving or writing there. Move each eligible
file without overwriting, merging, or rewriting its bytes; recheck the destination
at move time and use an operation that fails if it exists. A rerun leaves archived
files alone. Resolve the requested diary again after moves so a historical edit uses
its current location and cannot create a duplicate. Make only the requested content
edit there; archival itself never rewrites content or updates links/configuration.

Finish with a brief confirmation of the date, changed content, learning total when
relevant, and any skipped archive conflicts or link risks. Keep everything as local
Markdown; this skill needs no scripts, plugins, database, scheduler, or monthly report.
