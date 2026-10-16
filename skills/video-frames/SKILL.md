---
name: video-frames
description: Create time-labelled video contact sheets or extract single frames at specified times. Use for browsing a local video visually or preparing screenshots for illustrated notes.
---

# Video Frames

Use `scripts/video-frames` relative to this skill. Requires `uv`, FFmpeg and FFprobe; the launcher prepares its locked Python environment in the user cache. Read [the CLI contract](references/cli-contract.md) before constructing commands.

- **Browse:** provide a local video, absolute source-time range and output directory. Start with 6–12 second sampling and a 2×2 or 3×3 grid; adjust density when important transitions are missing. Open the returned contact sheets with the host's image-viewing tool. A generated file is not evidence that its contents were viewed.
- **Capture:** provide a JSON figure plan with unique IDs and timestamps in seconds. Extract the original single frames, then open the actual images to judge readability and context. Previews select candidates; final captures belong in the deliverable.

Keep source aspect ratio and original time coordinates. Short final groups remain visible. Preview sampling stops at the video stream's end when audio continues longer. Capture results report requested time; frame PTS is null unless measured.

Use a separate directory per task/range. Reuse an unchanged preview manifest; changed inputs require a new directory. Report failed captures from `captures.json`; only existing, decoded images count as successful results. Return manifest paths and any limitations in the source resolution. Summarization and semantic frame selection belong to the caller.
