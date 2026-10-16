# Keep media capabilities composable

Status: accepted. Recorded 2026-10-16 from the implemented design.

Download, local ASR, frame extraction and single-lesson note production remain independent Skills. `video-notes-batch` manages independent note tasks for prepared local lessons; the user's calling agent composes preparation and production, and each lesson writer/reviewer uses its own context. This permits downloading a course first and processing it later, with concurrency at the useful task boundaries, while reducing cross-lesson context carryover. A mandatory end-to-end orchestrator or dedicated named agent would couple those stages unnecessarily; file ownership and persisted attempts support cooperation but do not provide an OS sandbox.

See [batch design](../video-notes-batch/design.md) and [integration](../video-notes/integration.md) for the current boundaries.
