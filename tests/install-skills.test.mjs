import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, readFile, readdir, cp, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

async function fixture(t) {
  const root = await mkdtemp(join(tmpdir(), 'media-skill-install-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const repo = join(root, 'repo');
  const home = join(root, 'codex');
  await mkdir(join(repo, 'bin'), { recursive: true });
  await cp(new URL('../bin/install.mjs', import.meta.url), join(repo, 'bin/install.mjs'));
  for (const name of ['local-whisper', 'yt-dlp-download', 'other']) {
    const skill = join(repo, 'skills', name);
    await mkdir(join(skill, 'scripts'), { recursive: true });
    await writeFile(join(skill, 'SKILL.md'), `---\nname: ${name}\ndescription: Test fixture\n---\n`);
    await writeFile(join(skill, 'scripts/run.sh'), '#!/bin/sh\necho source\n');
  }
  const run = (...args) => spawnSync(process.execPath, [join(repo, 'bin/install.mjs'), ...args], {
    env: { ...process.env, CODEX_HOME: home }, encoding: 'utf8',
  });
  return { root, repo, home, run };
}

test('selected installation copies only the requested standalone skills', async t => {
  const f = await fixture(t);
  const result = f.run('--skill', 'local-whisper', '--skill', 'yt-dlp-download');
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual((await readdir(join(f.home, 'skills'))).sort(), ['local-whisper', 'yt-dlp-download']);
  assert.equal(await readFile(join(f.home, 'skills/local-whisper/scripts/run.sh'), 'utf8'), '#!/bin/sh\necho source\n');
  assert.equal(existsSync(join(f.home, 'agents')), false);
});

test('invalid selection is rejected before any destination writes', async t => {
  const f = await fixture(t);
  for (const args of [['--skill', 'missing'], ['--skill'], ['--unknown'], ['--skill', 'local-whisper', '--skill', '../other']]) {
    const result = f.run(...args);
    assert.notEqual(result.status, 0, result.stdout);
    assert.equal(existsSync(f.home), false);
  }
});

test('listing is read-only and default installation still installs all skills', async t => {
  const f = await fixture(t);
  const listed = f.run('--list');
  assert.equal(listed.status, 0, listed.stderr);
  assert.match(listed.stdout, /local-whisper/);
  assert.equal(existsSync(f.home), false);
  assert.equal(f.run().status, 0);
  assert.equal((await readdir(join(f.home, 'skills'))).length, 3);
  await writeFile(join(f.home, 'skills/local-whisper/local-change.txt'), 'keep');
  assert.equal(f.run().status, 0);
  assert.equal(await readFile(join(f.home, 'skills/local-whisper/local-change.txt'), 'utf8'), 'keep');
});

test('forced selected replacement preserves old copy and unrelated installed skills', async t => {
  const f = await fixture(t);
  await mkdir(join(f.home, 'skills/local-whisper'), { recursive: true });
  await mkdir(join(f.home, 'skills/other'), { recursive: true });
  await writeFile(join(f.home, 'skills/local-whisper/old.txt'), 'previous version');
  await writeFile(join(f.home, 'skills/other/keep.txt'), 'untouched');
  const result = f.run('--skill', 'local-whisper', '--force');
  assert.equal(result.status, 0, result.stderr);
  assert.equal(existsSync(join(f.home, 'skills/local-whisper/old.txt')), false);
  assert.equal(await readFile(join(f.home, 'skills/other/keep.txt'), 'utf8'), 'untouched');
  const backups = await readdir(join(f.home, 'skill-backups'));
  assert.equal(backups.length, 1);
  assert.equal(await readFile(join(f.home, 'skill-backups', backups[0], 'local-whisper/old.txt'), 'utf8'), 'previous version');
  assert.equal(existsSync(join(f.home, 'skills/yt-dlp-download')), false);
});

test('runtime environments, locks and caches are excluded from installation', async t => {
  const f = await fixture(t);
  const source = join(f.repo, 'skills/yt-dlp-download');
  for (const path of ['runtime/.venv', 'scripts/__pycache__', '.pytest_cache', 'runtime/.setup-lock']) {
    await mkdir(join(source, path), { recursive: true });
    await writeFile(join(source, path, 'cached'), 'temporary');
  }
  await writeFile(join(source, 'runtime/.setup-complete'), 'old machine');
  await writeFile(join(source, 'scripts/generated.pyc'), 'bytecode');
  const result = f.run('--skill', 'yt-dlp-download');
  assert.equal(result.status, 0, result.stderr);
  const dest = join(f.home, 'skills/yt-dlp-download');
  for (const path of ['runtime/.venv', 'scripts/__pycache__', '.pytest_cache', 'runtime/.setup-lock', 'runtime/.setup-complete', 'scripts/generated.pyc']) {
    assert.equal(existsSync(join(dest, path)), false, path);
  }
  assert.equal(existsSync(join(dest, 'scripts/run.sh')), true);
});
