import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const installer = fileURLToPath(new URL("../bin/install-video-notes-agent.mjs", import.meta.url));
async function fixture(t) {
  const root = await mkdtemp(join(tmpdir(), 'agent "测试 '));
  t.after(() => rm(root, { recursive: true, force: true }));
  for (const name of ["yt-dlp-download", "xiaoetong-download", "local-whisper", "video-frames", "video-notes"]) {
    const dir = join(root, "skills", name);
    await mkdir(dir, { recursive: true });
    await writeFile(join(dir, "SKILL.md"), `---\nname: ${name}\n---\n`);
  }
  return root;
}
function run(root, ...args) {
  return spawnSync(process.execPath, [installer, ...args], { env: { ...process.env, CODEX_HOME: root }, encoding: "utf8" });
}

test("dry run is read-only; installation resolves paths and is idempotent", async t => {
  const root = await fixture(t);
  const dry = run(root, "--dry-run");
  assert.equal(dry.status, 0, dry.stderr);
  assert.equal(JSON.parse(dry.stdout).status, "dry-run");
  assert.deepEqual(await readdir(root), ["skills"]);
  const result = run(root);
  assert.equal(result.status, 0, result.stderr);
  const config = await readFile(join(root, "agents/video_notes_operator.toml"), "utf8");
  assert.ok(!config.includes("@SKILLS_ROOT@"));
  assert.ok(config.includes(JSON.stringify(join(root, "skills/video-notes/SKILL.md"))));
  assert.equal(JSON.parse(run(root).stdout).status, "unchanged");
});

test("missing dependencies prevent installation", async t => {
  const root = await fixture(t);
  await rm(join(root, "skills/local-whisper"), { recursive: true });
  const result = run(root);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /local-whisper/);
  assert.deepEqual(await readdir(root), ["skills"]);
});

test("replacement requires force and preserves previous content and other agents", async t => {
  const root = await fixture(t);
  await mkdir(join(root, "agents"));
  await writeFile(join(root, "agents/video_notes_operator.toml"), "previous user config");
  await writeFile(join(root, "agents/other.toml"), "keep");
  assert.notEqual(run(root).status, 0);
  assert.equal(await readFile(join(root, "agents/video_notes_operator.toml"), "utf8"), "previous user config");
  const result = run(root, "--force");
  assert.equal(result.status, 0, result.stderr);
  const { backup } = JSON.parse(result.stdout);
  assert.equal(await readFile(backup, "utf8"), "previous user config");
  assert.equal(await readFile(join(root, "agents/other.toml"), "utf8"), "keep");
});
