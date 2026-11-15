"""Tests for hooks/method-settings.py.

Run from plugins/my: python3 -m unittest discover tests

Each test builds a temporary folder, most often a new git repo, and runs the
script as a subprocess, the way Claude Code runs a SessionStart hook. The
environment has no GIT_* variables, no CLAUDE_PROJECT_DIR unless a test sets
it, and no global or system git config, so the user's own setup cannot change
a result.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "hooks" / "method-settings.py"
HOOKS = SCRIPT.parent
HEADER = "Project settings for the my method, from .claude/my.md:\n\n"
WARNING = ("Warning: git ignores .claude/my.md, so clones and new worktrees do not get it. "
           "In .gitignore, ignore the folder's contents with .claude/* rather than .claude/, "
           "and add !.claude/*.md.")
MD = "## Parallel runs\n\n- **Max runs:** 2\n"


def clean_env():
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_") and k != "CLAUDE_PROJECT_DIR"}
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return env


class MethodSettingsTest(unittest.TestCase):
    def folder(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name) / "project"

    def write_md(self, root, md):
        (root / ".claude").mkdir(parents=True, exist_ok=True)
        (root / ".claude" / "my.md").write_text(md)

    def repo(self, md=None, gitignore=None, track=False):
        root = self.folder()
        root.mkdir()
        subprocess.run(["git", "init", "-q", str(root)], check=True, env=clean_env(),
                       capture_output=True)
        if md is not None:
            self.write_md(root, md)
        if gitignore is not None:
            (root / ".gitignore").write_text(gitignore)
        if track:
            subprocess.run(["git", "-C", str(root), "add", "-f", ".claude/my.md"],
                           check=True, env=clean_env())
        return root

    def plain_folder(self, md):
        root = self.folder()
        root.mkdir()
        self.write_md(root, md)
        return root

    def run_hook(self, project_dir, cwd=None):
        env = clean_env()
        if project_dir is not None:
            env["CLAUDE_PROJECT_DIR"] = str(project_dir)
        return subprocess.run([sys.executable, str(SCRIPT)], env=env,
                              cwd=cwd or project_dir, capture_output=True, text=True,
                              timeout=20)

    def context(self, result):
        self.assertEqual(result.returncode, 0)
        out = json.loads(result.stdout)
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "SessionStart")
        return out["hookSpecificOutput"]["additionalContext"]

    def test_prints_header_and_file(self):
        root = self.repo(md=MD)
        self.assertEqual(self.context(self.run_hook(root)), HEADER + MD.rstrip("\n"))

    def test_finds_the_file_from_a_subfolder(self):
        root = self.repo(md=MD)
        sub = root / "src" / "deep"
        sub.mkdir(parents=True)
        self.assertEqual(self.context(self.run_hook(sub)), HEADER + MD.rstrip("\n"))

    def test_finds_the_file_from_cwd_without_project_dir(self):
        root = self.repo(md=MD)
        sub = root / "src"
        sub.mkdir()
        self.assertEqual(self.context(self.run_hook(None, cwd=sub)), HEADER + MD.rstrip("\n"))

    def test_warns_when_git_ignores_the_file(self):
        root = self.repo(md=MD, gitignore=".claude/*\n")
        self.assertEqual(self.context(self.run_hook(root)),
                         HEADER + MD.rstrip("\n") + "\n" + WARNING)

    def test_warns_when_git_ignores_the_whole_folder_and_the_advice_works(self):
        root = self.repo(md=MD, gitignore=".claude/\n")
        self.assertEqual(self.context(self.run_hook(root)),
                         HEADER + MD.rstrip("\n") + "\n" + WARNING)
        (root / ".gitignore").write_text(".claude/*\n!.claude/*.md\n")
        self.assertNotIn("Warning:", self.context(self.run_hook(root)))

    def test_no_warning_when_the_file_is_tracked(self):
        root = self.repo(md=MD, gitignore=".claude/*\n", track=True)
        self.assertNotIn("Warning:", self.context(self.run_hook(root)))

    def test_no_warning_when_unignored(self):
        root = self.repo(md=MD, gitignore=".claude/*\n!.claude/*.md\n")
        self.assertNotIn("Warning:", self.context(self.run_hook(root)))

    def test_missing_file_prints_nothing(self):
        root = self.repo()
        r = self.run_hook(root)
        self.assertEqual((r.returncode, r.stdout), (0, ""))

    def test_unreadable_file_prints_nothing(self):
        root = self.repo()
        (root / ".claude" / "my.md").mkdir(parents=True)
        r = self.run_hook(root)
        self.assertEqual((r.returncode, r.stdout), (0, ""))

    def test_outside_a_repo_prints_file_without_warning(self):
        folder = self.plain_folder(md=MD)
        self.assertEqual(self.context(self.run_hook(folder)), HEADER + MD.rstrip("\n"))

    def test_hooks_json_registers_it_at_session_start(self):
        hooks = json.loads((HOOKS / "hooks.json").read_text())["hooks"]
        found = [(h["command"], h["timeout"]) for e in hooks["SessionStart"] for h in e["hooks"]
                 if "method-settings" in h["command"]]
        self.assertEqual(found, [('python3 "$CLAUDE_PLUGIN_ROOT/hooks/method-settings.py"', 10)])


if __name__ == "__main__":
    unittest.main()
