#!/usr/bin/env node

import { cp, mkdir, readdir, readFile, rm, rename, mkdtemp, lstat } from 'node:fs/promises';
import { join, resolve, basename } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { randomUUID } from 'node:crypto';

const packageRoot = resolve(fileURLToPath(new URL('..', import.meta.url)));
const sourceRoot = join(packageRoot, 'skills');
const codexHome = process.env.CODEX_HOME || join(homedir(), '.codex');
const destinationRoot = join(codexHome, 'skills');
const excluded = new Set(['.git', '.venv', '__pycache__', '.pytest_cache', '.DS_Store', '.setup-complete', '.setup-lock']);

async function exists(path) {
  try {
    await lstat(path);
    return true;
  } catch (error) {
    if (error.code === 'ENOENT') return false;
    throw error;
  }
}

function options(argv) {
  const result = { force: false, list: false, skills: [] };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--force') result.force = true;
    else if (arg === '--list') result.list = true;
    else if (arg === '--skill') {
      const name = argv[++i];
      if (!name || name.startsWith('-')) throw new Error('--skill requires a skill name');
      result.skills.push(name);
    } else throw new Error(`Unknown argument: ${arg}`);
  }
  return result;
}

async function install(name, force) {
  const source = join(sourceRoot, name);
  const destination = join(destinationRoot, name);
  if (await exists(destination) && !force) {
    console.log(`skip ${name} (already installed; use --force to replace)`);
    return;
  }
  // Prepare the new copy outside skill discovery before moving any installed copy.
  const stagingRoot = join(codexHome, 'skill-install-staging');
  await mkdir(stagingRoot, { recursive: true });
  const staging = await mkdtemp(join(stagingRoot, 'install-'));
  let backup;
  try {
    const prepared = join(staging, name);
    await cp(source, prepared, {
      recursive: true,
      filter: path => !excluded.has(basename(path)) && !path.endsWith('.pyc'),
    });
    if (await exists(destination)) {
      if (!force) {
        console.log(`skip ${name} (installed by another process)`);
        return;
      }
      backup = join(codexHome, 'skill-backups', `${Date.now()}-${randomUUID()}`, name);
      await mkdir(resolve(backup, '..'), { recursive: true });
      await rename(destination, backup);
    }
    try {
      await rename(prepared, destination);
    } catch (error) {
      if (backup && !await exists(destination)) await rename(backup, destination);
      throw error;
    }
    if (backup) console.log(`backup ${name}: ${backup}`);
    console.log(`installed ${name}`);
  } finally {
    await rm(staging, { recursive: true, force: true });
  }
}

async function main() {
  const argv = process.argv.slice(2);
  if (argv.includes('--help') || argv.includes('-h')) {
    console.log('Usage: personal-skills [--skill NAME ...] [--force] [--list]');
    console.log('Installs into $CODEX_HOME/skills (default: ~/.codex/skills).');
    console.log('Without --skill, selects every bundled skill. --force backs up replaced copies.');
    return;
  }
  const args = options(argv);
  const available = [];
  for (const entry of await readdir(sourceRoot, { withFileTypes: true })) {
    if (entry.isDirectory() && await exists(join(sourceRoot, entry.name, 'SKILL.md'))) available.push(entry.name);
  }
  available.sort();
  const selected = args.skills.length ? [...new Set(args.skills)] : available;
  for (const name of selected) {
    if (!available.includes(name)) throw new Error(`Unknown skill: ${name}. Use --list to see available skills.`);
    // Fail before any destination writes if a selected definition is unreadable.
    await readFile(join(sourceRoot, name, 'SKILL.md'), 'utf8');
  }
  if (args.list) {
    console.log(selected.join('\n'));
    return;
  }
  await mkdir(destinationRoot, { recursive: true });
  for (const name of selected) await install(name, args.force);
  console.log(`Skills are available in ${destinationRoot}`);
}

main().catch(error => {
  console.error(`Install failed: ${error.message}`);
  process.exitCode = 1;
});
