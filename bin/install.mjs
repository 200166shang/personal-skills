#!/usr/bin/env node

import { cp, mkdir, readdir, readFile, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { join, resolve } from "node:path";
import { homedir } from "node:os";
import { fileURLToPath } from "node:url";

const packageRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));
const sourceRoot = join(packageRoot, "skills");
const codexHome = process.env.CODEX_HOME || join(homedir(), ".codex");
const destinationRoot = join(codexHome, "skills");
const args = new Set(process.argv.slice(2));

if (args.has("--help") || args.has("-h")) {
  console.log("Usage: personal-skills [--force]");
  console.log("Installs the bundled skills into $CODEX_HOME/skills (default: ~/.codex/skills).");
  process.exit(0);
}

const force = args.has("--force");
const skillNames = (await readdir(sourceRoot, { withFileTypes: true }))
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name);

await mkdir(destinationRoot, { recursive: true });

for (const skillName of skillNames) {
  const source = join(sourceRoot, skillName);
  const destination = join(destinationRoot, skillName);
  const manifest = join(source, "SKILL.md");

  if (!existsSync(manifest)) continue;
  if (existsSync(destination) && !force) {
    console.log(`skip ${skillName} (already installed; use --force to replace)`);
    continue;
  }

  if (force) await rm(destination, { recursive: true, force: true });
  await cp(source, destination, { recursive: true });
  const frontmatter = await readFile(manifest, "utf8");
  const name = frontmatter.match(/^name:\s*(.+)$/m)?.[1]?.trim() || skillName;
  console.log(`installed ${name}`);
}

console.log(`Skills are available in ${destinationRoot}`);
