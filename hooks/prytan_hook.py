#!/usr/bin/env python3
"""Prytan's hook for agent apps (P1, 9 October 2026). Python 3.8+, standard library only; no installation.

A plugin's hooks run this on the person's own computer:
  prompt   before each message is answered: a short task line (made here, at most 300 characters, never the whole
           message) goes to Prytan, and what the person saved that fits comes back as context for the AI.
  start    when a session starts: the same, with the folder's name as the task.
  stop     when an answer ends: if the answer sent no checkpoint, one small reminder to send one.

Usage:  prytan_hook.py <prompt|start|stop> [--host claude|codex|gemini|cursor|cline|vscode] [--app "Claude Code"]
Input:  the host's JSON on stdin.   Output: the host's JSON on stdout, or nothing.

The key (read-only; made on My Prytan under "Keys for agent apps") is read from, in this order:
  the environment variable PRYTAN_HOOK_KEY; CLAUDE_PLUGIN_OPTION_PRYTAN_KEY (the Claude plugin's own setting);
  a file named prytan-key in the plugin's data folder (CLAUDE_PLUGIN_DATA or PLUGIN_DATA); ~/.prytan/key.
PRYTAN_URL overrides Prytan's address. If Prytan is slow or down, or there is no key, the hook prints nothing and the
chat goes on unchanged: it exits 0 whatever happens, within the time limit below.
"""
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

PRYTAN_URL = "https://staging.prytan.ai"
TASK_MAX = 300
HTTP_TIMEOUT = 6                # seconds for Prytan to answer; the hook's own limit in each host is a little longer
VERSION = "0.1.0"

HEADER = ("Prytan, what this person saved about themselves that fits this message. Apply it quietly where it fits, "
          "as a friend who knows them would; their words today come first.")
REMIND = ("Prytan: this answer sent no checkpoint. If the person's message told you anything about them (a preference, "
          "a decision, a plan, an interest, a change), call checkpoint once with it now; if there was nothing new, "
          "there is nothing to do.")


def key() -> str:
    for name in ("PRYTAN_HOOK_KEY", "CLAUDE_PLUGIN_OPTION_PRYTAN_KEY"):
        v = (os.environ.get(name) or "").strip()
        if v:
            return v
    places = [Path(os.environ[d]) / "prytan-key" for d in ("CLAUDE_PLUGIN_DATA", "PLUGIN_DATA") if os.environ.get(d)]
    places.append(Path.home() / ".prytan" / "key")
    for p in places:
        try:
            v = p.read_text(encoding="utf-8").strip()
            if v:
                return v
        except OSError:
            pass
    return ""


def task_line(text: str, limit: int = TASK_MAX) -> str:
    """The short line that leaves the computer: the first paragraph, one line, emails and long numbers taken out,
    cut at a word boundary. Never the full message."""
    text = (text or "").strip()
    if not text:
        return ""
    first = re.split(r"\n\s*\n", text, maxsplit=1)[0]
    first = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", " ", first)          # an email address
    first = re.sub(r"\d[\d \-]{5,}\d", " ", first)                     # a phone or card number
    first = re.sub(r"https?://\S+", " ", first)                        # a link (it can carry a token)
    first = re.sub(r"\s+", " ", first).strip()
    if len(first) <= limit:
        return first
    cut = first[:limit]
    if " " in cut[limit // 2:]:
        cut = cut[:cut.rfind(" ")]
    return cut.rstrip(" ,;:.")


def recall(task: str, app: str, test: bool = False) -> list:
    k = key()
    if not k or len(task) < 3:
        return []
    body = json.dumps({"task": task, "app": app}).encode("utf-8")
    req = urllib.request.Request(os.environ.get("PRYTAN_URL", PRYTAN_URL).rstrip("/") + "/hooks/recall", data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Bearer " + k)
    req.add_header("User-Agent", "prytan-hook/%s (%s)" % (VERSION, app))
    if test:
        req.add_header("X-Prytan-Test", "1")                           # the builder's own runs are never counted
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:        # noqa: S310 - Prytan's own address
        answer = json.loads(r.read().decode("utf-8"))
    return [str(x) for x in (answer.get("lines") or [])][:15]


def context_text(lines: list) -> str:
    return HEADER + "\n" + "\n".join("- " + x for x in lines)


def output(host: str, event: str, text: str) -> dict:
    """The shape each host reads. `event` is the host's own event name for the hook that ran."""
    if host == "cursor":
        return {"followup_message": text} if event == "stop" else {"additional_context": text}
    if host == "cline":
        return {"cancel": False, "contextModification": text}
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}


EVENT_NAMES = {   # (host, ours) -> the host's event name, for the output
    ("claude", "prompt"): "UserPromptSubmit", ("claude", "start"): "SessionStart", ("claude", "stop"): "Stop",
    ("codex", "prompt"): "UserPromptSubmit", ("codex", "start"): "SessionStart", ("codex", "stop"): "Stop",
    ("vscode", "prompt"): "UserPromptSubmit", ("vscode", "start"): "SessionStart", ("vscode", "stop"): "Stop",
    ("gemini", "prompt"): "BeforeAgent", ("gemini", "start"): "SessionStart", ("gemini", "stop"): "AfterAgent",
    ("cline", "prompt"): "UserPromptSubmit", ("cline", "start"): "TaskStart", ("cline", "stop"): "TaskComplete",
    ("cursor", "prompt"): "prompt", ("cursor", "start"): "start", ("cursor", "stop"): "stop",
}


def prompt_from(data: dict) -> str:
    for k in ("prompt", "user_prompt", "userPrompt", "message", "text"):
        v = data.get(k)
        if isinstance(v, str):
            return v
    for k in ("userPromptSubmitInfo", "input"):
        v = data.get(k)
        if isinstance(v, dict) and isinstance(v.get("prompt"), str):
            return v["prompt"]
    return ""


# Words that make a message likely to carry something about the person: a liking, a choice, a plan, a change. The
# reminder after an answer comes only for such a message, so the chat is not followed by "nothing new to save" after
# every answer (seen in Claude Code, 9 Oct 2026). Read on this computer; nothing of the message leaves it for this.
_ABOUT_ME = re.compile(r"\b(i|i'd|i'm|i've|i'll|we|we'd|we're|we've|let's|my|our|me)\b", re.I)
_TELLS = re.compile(r"\b(prefer|like|love|hate|dislike|rather|think|decid|choos|chose|pick|plan|going to|want|need|usually|"
                    r"always|never|changed|instead|no longer|from now|switch|moved|rule out|go with|let's|agree|settle|favourite|favorite)\w*", re.I)


def says_something_about_the_person(text: str) -> bool:
    return bool(text) and bool(_ABOUT_ME.search(text)) and bool(_TELLS.search(text))


def last_turn(transcript_path: str) -> tuple:
    """Read the host's transcript on this computer (Claude Code's JSON lines): (the person's last message, whether the
    assistant's turn after it called a checkpoint tool). Nothing of the transcript leaves the computer."""
    try:
        lines = Path(transcript_path).read_text(encoding="utf-8").splitlines()
    except (OSError, TypeError):
        return "", False
    said, found = "", False
    for raw in lines[-400:]:
        try:
            row = json.loads(raw)
        except ValueError:
            continue
        msg = row.get("message") if isinstance(row.get("message"), dict) else row
        role, content = msg.get("role") or row.get("type"), msg.get("content")
        if role == "user" and isinstance(content, str):               # the person's message, not a tool result
            said, found = content, False
        elif role == "user" and isinstance(content, list) and content and isinstance(content[0], dict) and content[0].get("type") == "text":
            said, found = str(content[0].get("text") or ""), False
        elif role == "assistant" and isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "tool_use" and "checkpoint" in str(part.get("name", "")).lower():
                    found = True
    return said, found


def reminded_recently(session_id: str, within: int = 90) -> bool:
    """One reminder per answer: a tiny marker per session in the plugin's data folder (or the temp folder)."""
    if not session_id:
        return False
    folder = Path(os.environ.get("CLAUDE_PLUGIN_DATA") or os.environ.get("PLUGIN_DATA") or os.environ.get("TMPDIR") or "/tmp") / "prytan-reminders"
    try:
        folder.mkdir(parents=True, exist_ok=True)
        mark = folder / re.sub(r"[^\w.-]", "_", session_id)[:80]
        if mark.exists() and time.time() - mark.stat().st_mtime < within:
            return True
        mark.touch()
    except OSError:
        return False
    return False


def run(event: str, host: str, app: str, data: dict, test: bool = False) -> dict:
    """The hook's answer for one event, or {} for nothing. Never raises."""
    try:
        name = EVENT_NAMES.get((host, event), event)
        if event == "stop":
            if host == "gemini":                                        # AfterAgent takes no context: the skill asks instead
                return {}
            if data.get("stop_hook_active"):
                return {}
            said, sent = last_turn(data.get("transcript_path", ""))
            if sent or not says_something_about_the_person(said):
                return {}
            if reminded_recently(str(data.get("session_id") or data.get("conversation_id") or "")):
                return {}
            return output(host, name, REMIND)
        if event == "start":
            task = "starting to work in the folder " + (os.path.basename(str(data.get("cwd") or os.getcwd())) or "home")
        else:
            task = task_line(prompt_from(data))
        lines = recall(task, app, test)
        return output(host, name, context_text(lines)) if lines else {}
    except Exception:  # noqa: BLE001 - whatever happens, the chat goes on unchanged
        return {}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    event = argv[0] if argv and not argv[0].startswith("--") else "prompt"
    host, app = "claude", "Claude Code"
    i = 1
    while i < len(argv):
        if argv[i] == "--host" and i + 1 < len(argv):
            host = argv[i + 1]; i += 2
        elif argv[i] == "--app" and i + 1 < len(argv):
            app = argv[i + 1]; i += 2
        else:
            i += 1
    try:
        raw = sys.stdin.read() if not sys.stdin.isatty() else ""
        data = json.loads(raw) if raw.strip() else {}
        if not isinstance(data, dict):
            data = {}
    except ValueError:
        data = {}
    answer = run(event, host, app, data, test=os.environ.get("PRYTAN_TEST") == "1")
    if answer:
        sys.stdout.write(json.dumps(answer))
    return 0


if __name__ == "__main__":
    sys.exit(main())
