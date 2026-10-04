#!/usr/bin/env python3
"""UserPromptSubmit: remind the model to run the LibreAgent skill matching the prompt:
install-libreagent for an installation, create-organization-agent for an agent being built."""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from libreagent_hook_state import (  # noqa: E402
    agent_sessions, data_dir, emit, mentions_agent_creation, mentions_libreagent_install,
    save_json, session_key,
)

INSTALL = (
    "LibreAgent: this prompt asks to install LibreAgent, join a team's LibreAgent "
    "space or add a computer. Apply the libreagent-agent-builder install-libreagent "
    "skill now: start with its interactive questions (goal, operating system, this "
    "computer or another) using the session's question tool, and do not answer with "
    "a generic installation guide. Ignore this if the user is only developing "
    "LibreAgent itself."
)
DETECTED = (
    "LibreAgent: this conversation is building an agent. Apply the "
    "libreagent-agent-builder create-organization-agent skill now, before "
    "dual-provider-agents, skill-installer or skill-creator: keep the agent's "
    "skills in its project directory, ask audience and H24 together early, then "
    "create, publish when shared, back up and host it through the LibreAgent MCP "
    "tools. Research and skill installation are steps of this procedure, not a "
    "replacement. When an existing project must become the agent, apply "
    "convert-project-to-agent first. Ignore this if the user is only developing "
    "LibreAgent itself."
)
CONTINUING = (
    "LibreAgent: agent creation was detected earlier in this conversation. Keep "
    "applying create-organization-agent: before ending a turn that adds or changes "
    "the agent's content, check agents_list, publication, agent_backup_status and "
    "H24 hosting, and resume the first incomplete step or ask the decision it needs."
)


def main():
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        return
    prompt = str(event.get("prompt") or "")
    if mentions_libreagent_install(prompt) and not mentions_agent_creation(prompt):
        emit("UserPromptSubmit", INSTALL)
        return
    key = session_key(event)
    directory = data_dir()
    path, sessions = (None, {}) if directory is None else agent_sessions(directory)
    if mentions_agent_creation(prompt):
        if path is not None and key:
            sessions[key] = time.time()
            save_json(path, sessions)
        emit("UserPromptSubmit", DETECTED)
    elif key and key in sessions:
        sessions[key] = time.time()
        save_json(path, sessions)
        emit("UserPromptSubmit", CONTINUING)


if __name__ == "__main__":
    main()
