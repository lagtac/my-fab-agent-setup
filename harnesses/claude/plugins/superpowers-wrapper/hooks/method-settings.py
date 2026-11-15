#!/usr/bin/env python3
"""Load the project's my settings, .claude/my.md, into the session.

A SessionStart hook in my. The project root is the git top level of
$CLAUDE_PROJECT_DIR (else of the current folder), else that folder itself.
When <root>/.claude/my.md exists and can be read, it prints one JSON object
whose additionalContext is the line "Project settings for the my method, from
.claude/my.md:", a blank line and the file. When git ignores the file, a
warning line follows, because clones and new worktrees would not get it. With
no file, or an unreadable one, it prints nothing.

The hook turns off with my, so another method never sees the file. Its text
does not reach subagents. It always exits 0, so it never blocks a session.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

HEADER = "Project settings for the my method, from .claude/my.md:"
WARNING = ("Warning: git ignores .claude/my.md, so clones and new worktrees do not get it. "
           "In .gitignore, ignore the folder's contents with .claude/* rather than .claude/, "
           "and add !.claude/*.md.")


def project_root():
    folder = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path.cwd())
    try:
        top = subprocess.run(["git", "-C", str(folder), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=5)
        if top.returncode == 0 and top.stdout.strip():
            return Path(top.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        pass
    return folder


def ignored(root):
    try:
        check = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", ".claude/my.md"],
                               capture_output=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return False
    return check.returncode == 0


def main():
    root = project_root()
    try:
        text = (root / ".claude" / "my.md").read_text()
    except (OSError, UnicodeDecodeError):
        return
    body = text.rstrip("\n")
    context = f"{HEADER}\n\n{body}"
    if ignored(root):
        context += "\n" + WARNING
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart", "additionalContext": context}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
