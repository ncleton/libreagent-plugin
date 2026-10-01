"""Shared state for LibreAgent agent-creation hooks. Never reads skill contents."""

import json
import os
import re
import time
import unicodedata
from pathlib import Path

SESSION_TTL_SECONDS = 7 * 24 * 3600


def data_dir():
    value = os.environ.get("PLUGIN_DATA") or os.environ.get("CLAUDE_PLUGIN_DATA")
    if not value:
        return None
    path = Path(value)
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    return path


def load_json(path, default):
    try:
        return json.loads(path.read_text()) if path.exists() else default
    except (ValueError, OSError):
        return default


def save_json(path, value):
    try:
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(value))
        tmp.replace(path)
    except OSError:
        pass


def fold(text):
    """Lowercase and strip accents so French prompts match without accents."""
    normalized = unicodedata.normalize("NFKD", text.lower().replace("\u2019", "'"))
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def session_key(event):
    return str(event.get("session_id") or event.get("thread_id") or "")


def agent_sessions(directory):
    path = directory / "agent-creation-sessions.json"
    now = time.time()
    sessions = {
        key: value for key, value in load_json(path, {}).items()
        if isinstance(value, (int, float)) and now - value < SESSION_TTL_SECONDS
    }
    return path, sessions


def emit(event_name, context):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": event_name,
        "additionalContext": context,
    }}))


AGENT_NOUN = r"(?:agents?|assistants?|bots?|chatbots?|copilotes?|copilots?|conseillers? (?:ia|ai|virtuels?))"
CREATION = re.compile(
    r"\b(?:cree|creer|creons|creez|creation|construi\w*|developp\w*|fabriqu\w*|concevoir|conception|"
    r"mettre en place|monter|build\w*|creat\w*|make|design\w*|set up|setup|prototyp\w*)\b"
    r"[^.?!\n]{0,80}\b" + AGENT_NOUN + r"\b"
)
AGENT_DUTY = re.compile(
    r"\b" + AGENT_NOUN +
    r"\b[^.?!\n]{0,40}\b(?:devra|doit|devrait|pourra|qui fera|qui va|should|must|will|that can)\b"
)
AGENT_FOR = re.compile(
    r"\b(?:skills?|mcp|plugins?|outils?|tools?)\b[^.?!\n]{0,60}\b(?:pour|for) "
    r"(?:l'|un |une |cet |the |an |this |my |mon |notre )?" + AGENT_NOUN + r"\b"
)


def mentions_agent_creation(prompt):
    text = fold(prompt)
    return bool(CREATION.search(text) or AGENT_DUTY.search(text) or AGENT_FOR.search(text))
