# Media operator: video notes

The two video skills are independent of Learning workflows. Install their complete directories, preserving scripts, runtime locks, references and assets. `video-notes` locates `video-frames` through host skill discovery or a caller-supplied path. Existing downloads and ASR are reusable inputs.

Default content mode is `faithful`: preserve the full lecture in the speaker's voice and original order, cleaning speech without summarization. Set `prepare --mode summary` only for an explicit condensation request. Use a new job when changing modes; an old summary is not a source for the faithful rewrite.

## Agent instruction addition

Add this intent branch to the media agent's instructions:

> For an illustrated video-note request, resolve the exact source and part, reuse verified local media/transcripts, and use the existing acquisition or ASR skills only for missing inputs. Use video-notes for content organization, screenshot selection, Markdown and portable HTML. Use video-frames for previews and captures. The calling model writes the note and views images; no secondary model API is required. Complete source matching, scoped window review, final-image review, assembly, rendering and structural validation, then report the deliverables and limitations. Video-note tasks use the note skill's completion criteria. Dubbing JSON and audio-render completion gates apply only to dubbing tasks.

Register both skills using the installed absolute paths. Example configuration shape (resolve placeholders locally; TOML does not expand them):

```toml
[[skills.config]]
path = "<installed video-frames directory>/SKILL.md"
enabled = true

[[skills.config]]
path = "<installed video-notes directory>/SKILL.md"
enabled = true
```

The repository does not own the user's external agent configuration. Apply only these additions; keep download, ASR and TTS behavior unchanged. Installed copies are generated artifacts; maintain changes in this repository and reinstall only the two affected skills. Avoid global force replacement of unrelated skills.

## Input preparation

1. Resolve the supplied URL with its part parameter. Keep source URL, part ID and local path separate.
2. Reuse matching media. Obtain video with the existing download skill if absent; download success returns the actual path.
3. Reuse readable matching subtitles after source verification. If absent, use the existing local ASR skill and validate its output.
4. Invoke `video-notes` with explicit work and delivery directories outside the repository.

For Bilibili, preserve `p=2` throughout inspection, download and source-time links. Do not use a similarly named file from another part. The current default downloader may select 360p; inspect actual frame readability and report any remaining source-detail limitation.

## Review and recovery

The agent reads the normalized source segments and matching previews, writes one recoverable chunk per window, and records actual review with the `review` subcommand. Merge chunks before assembly; a window boundary is not a required section boundary. Final captures require visual inspection and accepted hashes. The job and exported report distinguish these caller attestations from automatic checks.

Use the source's original time axis for samples. Re-running prepare with the same inputs reuses state; changed source inputs require a new job. CSS-only changes rerender the note. No catalog registration, topic generation or learning-state update is part of delivery.

## Local verification commands

Run tests from a checkout using cache/temporary environments, never a runtime `.venv` inside a skill:

```sh
UV_PROJECT_ENVIRONMENT=/tmp/video-frames-test-env uv run --frozen \
  --project skills/video-frames/runtime python -B -m unittest discover -s skills/video-frames/tests
UV_PROJECT_ENVIRONMENT=/tmp/video-notes-test-env uv run --frozen \
  --project skills/video-notes/runtime python -B -m unittest discover -s skills/video-notes/tests
CODEX_HOME=/tmp/personal-skills-install-test node bin/install.mjs
```

Use fresh temporary paths when needed. Run both installed launchers and an end-to-end fixture there. Generic skill instructions remain in `SKILL.md`; these host integration notes are optional documentation.
