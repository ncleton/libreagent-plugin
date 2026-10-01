#!/usr/bin/env python3
"""Prompt after a local skill file is written; never read or upload its contents."""

import json
import os
import sys
import time
from pathlib import Path


def scan_skill_files(root: Path):
    if not root.is_dir():
        return
    for current, dirs, files in os.walk(root, followlinks=False):
        relative_depth = len(Path(current).relative_to(root).parts)
        dirs[:] = [
            name for name in dirs
            if name not in {".git", "node_modules", "target", "dist"}
            and relative_depth < 5
        ]
        if "SKILL.md" in files:
            yield Path(current) / "SKILL.md"


def main():
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        return
    tool_name = str(event.get("tool_name", ""))
    command = str((event.get("tool_input") or {}).get("command", ""))
    if tool_name == "Bash" and not any(
        marker in command for marker in ("SKILL.md", "skill-creator", "init_skill.py")
    ):
        return
    if tool_name == "apply_patch" and "SKILL.md" not in command:
        return

    if not os.environ.get("PLUGIN_DATA"):
        return
    data_dir = Path(os.environ["PLUGIN_DATA"])
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return
    state_path = data_dir / "skill-created-seen.json"
    try:
        seen = json.loads(state_path.read_text()) if state_path.exists() else {}
    except (ValueError, OSError):
        seen = {}
    now = time.time()
    roots = [Path.cwd() / ".agents/skills", Path.cwd() / ".codex/skills",
             Path.home() / ".agents/skills", Path.home() / ".codex/skills"]
    changed = []
    for root in roots:
        for path in scan_skill_files(root):
            try:
                modified = path.stat().st_mtime_ns
            except OSError:
                continue
            if now - modified / 1_000_000_000 > 90:
                continue
            key = str(path.resolve())
            if seen.get(key) == modified:
                continue
            seen[key] = modified
            changed.append(key)
    try:
        state_path.write_text(json.dumps(seen))
    except OSError:
        pass
    if changed:
        paths = ", ".join(changed[:3])
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"A local skill was just created or updated: {paths}. "
                "Once the local skill is finished, apply the capture-created-skill workflow: "
                "offer to keep it local or import into LibreAgent. "
                "Do not upload any skill contents before the user chooses import."
            )
        }}))


if __name__ == "__main__":
    main()
