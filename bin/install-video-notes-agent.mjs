#!/usr/bin/env node
import { copyFile, mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { randomUUID } from "node:crypto";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const skillNames = ["yt-dlp-download", "xiaoetong-download", "local-whisper", "video-frames", "video-notes"];
const args = process.argv.slice(2);
let skillsDir;
let force = false;
let dryRun = false;

async function install() {
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--help" || arg === "-h") {
      console.log("Usage: personal-video-notes-agent [--skills-dir PATH] [--dry-run] [--force]");
      console.log("Installs video_notes_operator into $CODEX_HOME/agents (default: ~/.codex/agents).");
      console.log("Requires the five media skills already installed; --force backs up and replaces only this agent.");
      return;
    }
    if (arg === "--force") force = true;
    else if (arg === "--dry-run") dryRun = true;
    else if (arg === "--skills-dir" && args[i + 1] && !args[i + 1].startsWith("--")) skillsDir = args[++i];
    else throw new Error(`Unknown or incomplete option: ${arg}`);
  }
  const codexHome = resolve(process.env.CODEX_HOME || join(homedir(), ".codex"));
  const root = resolve(skillsDir || join(codexHome, "skills"));
  const missing = [];
  for (const name of skillNames) {
    try {
      const content = await readFile(join(root, name, "SKILL.md"), "utf8");
      if (!new RegExp(`^name:\\s*["']?${name}["']?\\s*$`, "m").test(content)) missing.push(name);
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
      missing.push(name);
    }
  }
  if (missing.length) throw new Error(`Missing or mismatched skills under ${root}: ${missing.join(", ")}. Install these dependencies first, or pass --skills-dir.`);
  const templatePath = fileURLToPath(new URL("../agents/video_notes_operator.toml.in", import.meta.url));
  const template = await readFile(templatePath, "utf8");
  const content = template.replaceAll("@SKILLS_ROOT@", JSON.stringify(root).slice(1, -1));
  const destination = join(codexHome, "agents/video_notes_operator.toml");
  let previous;
  try { previous = await readFile(destination, "utf8"); }
  catch (error) { if (error.code !== "ENOENT") throw error; }
  if (dryRun) {
    console.log(JSON.stringify({ status: "dry-run", destination, skills: root, config: content }));
    return;
  }
  if (previous === content) {
    console.log(JSON.stringify({ status: "unchanged", destination }));
    return;
  }
  if (previous !== undefined && !force) throw new Error("Agent already exists with different content; use --force to back it up and replace only this agent");
  let backup;
  if (previous !== undefined) {
    backup = join(codexHome, "agent-backups", `video_notes_operator-${randomUUID()}.toml`);
    await mkdir(dirname(backup), { recursive: true });
    await copyFile(destination, backup);
  }
  await mkdir(dirname(destination), { recursive: true });
  const temporary = `${destination}.${randomUUID()}.tmp`;
  await writeFile(temporary, content, { flag: "wx" });
  await rename(temporary, destination);
  console.log(JSON.stringify({ status: "installed", destination, ...(backup ? { backup } : {}) }));
}

install().catch(error => {
  console.error(error.message);
  process.exitCode = 1;
});
