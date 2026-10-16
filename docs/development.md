# Development workflow

Status: current project convention, 2026-10-16. This adapts Matt Pocock's persistent context and self-contained ticket practices to a small Skill collection; it does not require a framework or a multi-agent run for every edit.

## Small changes

Use this path for a prompt correction, bounded parameter change or local bug: identify the intended behavior, create a worktree/branch, implement, verify the affected behavior and open a PR. Preserve unrelated local files. No separate spec issue or ticket graph is required when the change fits one context and has a clear completion condition.

## Larger changes

Use a spec for cross-Skill behavior, significant scope decisions or work spanning sessions. Before implementing, make the expected behavior and acceptance concrete with the user; an already agreed plan need not be approved again. Save it to the [configured tracker](agents/issue-tracker.md), linking relevant current design, ADRs and research rather than copying whole documents.

A spec records the problem, proposed outcome, user-facing scenarios, accepted decisions, testing approach and exclusions. Keep rapidly changing file lists and long code snippets out of requirements. Each ticket should deliver one complete, verifiable behavior, sized for a fresh context, with:

```text
Parent: <spec issue>
Outcome: <observable behavior>
Blocked by: <issue references or None>
Acceptance: <checkable conditions>
Context: <current design, relevant ADRs and source/test pointers>
Verification: <command or evidence needed>
```

Work only the ready frontier. Use fresh sessions or task-scoped child agents when useful; concurrency requires independent responsibilities and sufficient host capacity. For code-writing children, assign disjoint ownership and isolated worktrees/branches as appropriate, then integrate and verify. Carry paths, accepted results and precise checkpoints, not the preceding task's full exploratory conversation. A sequential fresh-context run is valid. Video-note runtime child creation is a separate capability governed by its own Skill.

Before opening/finishing a PR, review both accepted scope and repository conventions, fix actionable findings and record actual verification. A PR links its spec/tickets when present, explains the final behavior and states unverified portions. Do not create completed spec/ticket records retroactively for past features. Creating a PR does not authorize merging it; on requested merge, synchronize local main and clean up merged development branches/worktrees after preserving needed work. History-import PRs need merge commits to preserve original ancestry.

## Documentation and validation

Update the relevant current design with behavior changes. Add ADRs sparingly for consequential choices; put dated results in validation documents, source investigation in research and obsolete plans under a clearly marked history directory. Use [the index](README.md); runtime instructions remain in the Skills. This separates intent, implementation contracts and dated evidence without copying an entire Skill into docs.

Verify proportionally, using fresh temporary output/cache directories and no credentials/media in Git:

| Affected area | Verification entry |
| --- | --- |
| Installer or packaging | `node --test tests/*.test.mjs`; inspect `npm pack --dry-run --json` for missing references or caches |
| Local Whisper interfaces | `python3 -B -m unittest discover -s skills/local-whisper/tests -v` (offline, no model inference) |
| Download wrapper | `uv run --frozen --project skills/yt-dlp-download/runtime --group dev python -B -m pytest skills/yt-dlp-download/tests -q` |
| Batch note state | `python3 -B -m unittest discover -s skills/video-notes-batch/tests -v` |
| Note/frame tools | Use `uv run --frozen --project skills/<name>/runtime` to run that Skill's unittest suite; point `UV_PROJECT_ENVIRONMENT` to a temporary/cache directory |
| Documentation only | Resolve relative Markdown links, verify status/authority and inspect package contents after path changes; no model run or new media generation |

Test counts in prior reports are historical, not a permanent quality threshold. Tests that generate files or install Skills use temporary directories; real model inference, platform downloads and browser interactions are separate checks and are reported only when actually executed.
