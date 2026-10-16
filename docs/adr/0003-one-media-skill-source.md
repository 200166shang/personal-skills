# Maintain media Skills in this collection

Status: accepted. Recorded 2026-10-16 after migration PR #16.

The download wrapper and local Whisper Skill are maintained in personal-skills alongside the note Skills, retaining their independent entry points. Keeping them in separate source repositories made coordinated maintenance and installation harder; one collection makes those changes reviewable together without combining the capabilities or vendoring their upstream packages/models. The original main histories and Whisper license were imported intact, so the migration was merged with a merge commit. Old repositories were not archived as part of that operation; they are historical sources, not additional active maintenance locations.

See [migration provenance](../media-skills-migration/design.md). Installed copies remain deployments of this source, not a second editing location.
