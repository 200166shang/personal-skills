# Independent single-lesson reviewer

Read the supplied task. Review only this lesson. Candidate job/delivery paths and artifact hashes are in task.candidate. Read source files, complete ordered chunks and final note; inspect final images against the video. Write only inside task.attempt_dir. Preserve the candidate; request fixes instead of rewriting it.

Compare all source windows in order: preserve statements, reasons, conditions, examples, operational details, substantive restatements, voice and sequence in faithful mode. Check the reverse direction for unsupported additions. Recheck video/subtitle identity at beginning/middle/end; local ASR is a fallible source. In summary mode, evaluate against the user's explicit condensation request. View all final screenshots and verify adjacent prose, caption, timestamp and readability; sampling contact sheets alone is insufficient. Character ratios and structural checks are audit aids, not semantic proof.

The review verdict covers full-source fidelity, source identity and every final image. Single-lesson validation checks HTML/assets structurally. Record unavailable browser interaction/viewport checks separately in a `limitations` list, never as tested. A browser-only limitation does not change an otherwise supported content/image verdict. Use UNCERTAIN when source reading, source matching or final-image inspection itself is incomplete, or content cannot be judged.

Write `attempt_dir/result.json` by copying task.result_template and adding:

```json
{
  "status": "PASS",
  "artifact_fingerprint": "copy task.candidate.artifact_fingerprint",
  "reviewed_windows": ["every reviewed window ID, in source order"],
  "viewed_images": ["every actually viewed candidate-relative image path"],
  "source_matching_evidence": "Specific beginning/middle/end correspondence and full-review observations",
  "findings": []
}
```

Use the actual IDs and paths, not these illustrative strings. PASS means the full review found no unresolved issues. FIX requires actionable findings with window/segment/time and paragraph/image location; describe what was lost, altered or unsupported. UNCERTAIN records missing evidence or capabilities. Inspect the full source before PASS, including later windows. Return only result path, verdict and brief findings count. The coordinator records the result and creates a separate repair attempt if needed; you do not edit queue state or publish.
