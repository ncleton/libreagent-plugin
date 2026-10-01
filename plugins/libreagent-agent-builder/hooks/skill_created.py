#!/usr/bin/env python3
"""PostToolUse: prompt after a local skill or agent project file is written; never read or upload contents."""

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from libreagent_hook_state import agent_sessions, data_dir, emit, load_json, save_json, session_key  # noqa: E402

RECENT_SECONDS = 120
SKIPPED_DIRS = {".git", "node_modules", "target", "dist", "__pycache__", ".venv", "venv"}


def scan_skill_files(root):
    if not root.is_dir():
        return
    for current, dirs, files in os.walk(root, followlinks=True):
        if len(Path(current).relative_to(root).parts) >= 2:
            dirs[:] = []
        else:
            dirs[:] = [name for name in dirs if name not in SKIPPED_DIRS and not name.startswith(".")]
        if "SKILL.md" in files:
            yield Path(current) / "SKILL.md"


def recent(path, now):
    try:
        modified = path.stat().st_mtime_ns
    except OSError:
        return None
    if now - modified / 1_000_000_000 > RECENT_SECONDS:
        return None
    return modified


def main():
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        return
    directory = data_dir()
    if directory is None:
        return
    state_path = directory / "skill-created-seen.json"
    seen = load_json(state_path, {})
    now = time.time()
    cwd = Path(event.get("cwd") or os.getcwd())
    home = Path.home()
    roots = [cwd / ".agents/skills", cwd / ".claude/skills", cwd / ".codex/skills",
             home / ".agents/skills", home / ".codex/skills", home / ".claude/skills"]
    changed = []
    for root in roots:
        for path in scan_skill_files(root):
            modified = recent(path, now)
            if modified is None:
                continue
            key = str(path.resolve())
            if seen.get(key) == modified:
                continue
            seen[key] = modified
            changed.append(key)
    for name in ("AGENTS.md", "CLAUDE.md"):
        path = cwd / name
        modified = recent(path, now)
        if modified is not None and seen.get(str(path)) != modified:
            seen[str(path)] = modified
            changed.append(str(path))
    if not changed:
        return
    save_json(state_path, seen)
    _, sessions = agent_sessions(directory)
    paths = ", ".join(sorted(set(changed))[:4])
    if session_key(event) in sessions:
        context = (
            f"LibreAgent: skill or agent project files changed during agent creation: {paths}. "
            "Keep them as real directories in the agent project's .agents/skills, then continue "
            "create-organization-agent until the agent is created, shared as chosen, backed up "
            "and hosted H24 when requested."
        )
    else:
        context = (
            f"LibreAgent: a local skill or agent project file was just created, installed or updated: {paths}. "
            "If the conversation is building an agent, apply create-organization-agent. Otherwise, once the "
            "skill is finished, apply capture-created-skill: offer to keep it local or import it into "
            "LibreAgent. Do not upload any skill contents before the user chooses import."
        )
    emit("PostToolUse", context)


if __name__ == "__main__":
    main()
