"""Process-level tests for scripts/link_harnesses.py.

The seam is the process boundary: build a fixture repo and home, run the
program, and assert on exit code, output, and the filesystem. Nothing imports
the program's internals.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "link_harnesses.py"


def build(work: Path) -> tuple[Path, Path]:
    """A repo with the shared resources, and a home with a harness root."""
    repo = work / "repo"
    home = work / "home"
    (repo / "global" / "rules").mkdir(parents=True)
    (repo / "global" / "rules" / "one.md").write_text("rule\n", encoding="utf-8")
    (repo / "global" / "AGENTS.md").write_text("# agents\n", encoding="utf-8")
    (repo / "global" / "skills" / "alpha").mkdir(parents=True)
    (repo / "global" / "skills" / "alpha" / "SKILL.md").write_text(
        "alpha\n", encoding="utf-8"
    )
    (repo / "global" / "skills" / "bin").mkdir(parents=True)
    (repo / "global" / "skills" / "bin" / "tool.py").write_text(
        "pass\n", encoding="utf-8"
    )
    (home / ".fake").mkdir(parents=True)
    return repo, home


def write_manifest(
    repo: Path,
    name: str,
    links: list[dict],
    roots: list[str] | None = None,
    binary: str | None = None,
) -> Path:
    data = {"harness": name, "root": roots or ["$FAKE_HOME"], "links": links}
    if binary is not None:
        data["binary"] = binary
    path = repo / "harnesses" / name / "links.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def run(
    repo: Path, home: Path, *args: str, extra_env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.pop("OPENCODE_CONFIG_DIR", None)
    env.pop("XDG_CONFIG_HOME", None)
    env["HOME"] = str(home)
    env["FAKE_HOME"] = str(home / ".fake")
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def line_with(output: str, needle: str) -> str:
    for line in output.splitlines():
        if needle in line:
            return line
    raise AssertionError(f"no line holds {needle!r}:\n{output}")


RULES = {"source": "global/rules", "target": "rules", "kind": "dir"}
AGENTS_MD = {"source": "global/AGENTS.md", "target": "AGENTS.md", "kind": "file"}


class ReportModeTest(unittest.TestCase):
    def test_missing_link_is_listed_with_its_command(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [RULES])

            result = run(repo, home)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("missing", line_with(result.stdout, "rules"))
            self.assertIn(
                f"ln -sn {repo / 'global' / 'rules'} {home / '.fake' / 'rules'}",
                result.stdout,
            )

    def test_installed_harness_names_its_signal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [RULES], binary=sys.executable)

            result = run(repo, home)

            self.assertIn("fake: installed", line_with(result.stdout, "fake:"))
            self.assertIn("binary", line_with(result.stdout, "fake:"))

    def test_uninstalled_harness_still_shows_its_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(
                repo,
                "fake",
                [RULES],
                roots=["$MISSING_HOME/rules"],
                binary="definitely-not-installed",
            )

            result = run(repo, home)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("not installed", line_with(result.stdout, "fake:"))
            self.assertIn("ln -sn", result.stdout)

    def test_children_link_counts_its_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(
                repo,
                "fake",
                [
                    {
                        "source": "global/skills",
                        "target": "skills",
                        "kind": "children",
                        "exclude": ["bin"],
                    }
                ],
            )

            result = run(repo, home)

            self.assertIn("0/1 ok", line_with(result.stdout, "skills/"))

    def test_stale_retired_root_link_is_reported_with_rm(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [AGENTS_MD])
            retired = home / ".agents"
            retired.mkdir()
            (retired / "AGENTS.md").symlink_to(repo / "global" / "AGENTS.md")

            result = run(repo, home)

            self.assertIn("Stale links into this repo:", result.stdout)
            self.assertIn(f"rm {retired / 'AGENTS.md'}", result.stdout)


class CheckModeTest(unittest.TestCase):
    def test_clean_run_is_silent_and_exits_zero(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [RULES])
            (home / ".fake" / "rules").symlink_to(repo / "global" / "rules")

            result = run(repo, home, "--check")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(result.stderr, "")

    def test_missing_link_is_one_line_and_exits_one(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [RULES])

            result = run(repo, home, "--check")

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(
                result.stderr.splitlines(),
                [f"missing: fake ~/.fake/rules -> {repo / 'global' / 'rules'}"],
            )

    def test_real_file_at_the_target_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [AGENTS_MD])
            (home / ".fake" / "AGENTS.md").write_text("mine\n", encoding="utf-8")

            result = run(repo, home, "--check")

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("blocked: fake", result.stderr)
            self.assertEqual(
                (home / ".fake" / "AGENTS.md").read_text(encoding="utf-8"), "mine\n"
            )

    def test_link_to_a_different_source_is_wrong_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [RULES])
            elsewhere = Path(temporary) / "elsewhere"
            elsewhere.mkdir()
            (home / ".fake" / "rules").symlink_to(elsewhere)

            result = run(repo, home, "--check")

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("wrong-target: fake", result.stderr)

    def test_stale_link_fails_the_check(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [AGENTS_MD])
            (home / ".fake" / "AGENTS.md").symlink_to(repo / "global" / "AGENTS.md")
            retired = home / ".agents"
            retired.mkdir()
            (retired / "AGENTS.md").symlink_to(repo / "global" / "AGENTS.md")

            result = run(repo, home, "--check")

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("stale: ", result.stderr)


class ApplyModeTest(unittest.TestCase):
    def test_apply_creates_the_link(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [RULES])

            result = run(repo, home, "--apply")

            self.assertEqual(result.returncode, 0, result.stderr)
            target = home / ".fake" / "rules"
            self.assertTrue(target.is_symlink())
            self.assertEqual(target.resolve(), (repo / "global" / "rules").resolve())
            self.assertIn("linked:", result.stdout)

    def test_apply_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [RULES])

            run(repo, home, "--apply")
            second = run(repo, home, "--apply")

            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(second.stdout, "nothing to do\n")

    def test_apply_keeps_a_foreign_file_in_a_children_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(
                repo,
                "fake",
                [
                    {
                        "source": "global/skills",
                        "target": "skills",
                        "kind": "children",
                        "exclude": ["bin"],
                    }
                ],
            )
            target = home / ".fake" / "skills"
            target.mkdir()
            (target / "synced").mkdir()

            result = run(repo, home, "--apply")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "alpha").is_symlink())
            self.assertTrue((target / "synced").is_dir())
            self.assertFalse((target / "bin").exists())

    def test_apply_does_not_overwrite_a_real_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [AGENTS_MD])
            target = home / ".fake" / "AGENTS.md"
            target.write_text("mine\n", encoding="utf-8")

            result = run(repo, home, "--apply")

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "mine\n")
            self.assertIn("blocked: fake", result.stderr)

    def test_apply_replaces_a_dangling_link(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [RULES])
            target = home / ".fake" / "rules"
            target.symlink_to(Path(temporary) / "gone")

            result = run(repo, home, "--apply")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(target.resolve(), (repo / "global" / "rules").resolve())

    def test_apply_creates_a_missing_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [RULES], roots=["$FRESH_ROOT"])

            result = run(
                repo,
                home,
                "--apply",
                extra_env={"FRESH_ROOT": str(home / ".fresh")},
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                (home / ".fresh" / "rules").resolve(),
                (repo / "global" / "rules").resolve(),
            )

    def test_apply_never_removes_a_stale_link(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(repo, "fake", [AGENTS_MD])
            retired = home / ".agents"
            retired.mkdir()
            stale = retired / "AGENTS.md"
            stale.symlink_to(repo / "global" / "AGENTS.md")

            result = run(repo, home, "--apply")

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertTrue(stale.is_symlink())
            self.assertIn("stale: ", result.stderr)


class ManifestTest(unittest.TestCase):
    def test_bad_json_exits_two(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            path = repo / "harnesses" / "fake" / "links.json"
            path.parent.mkdir(parents=True)
            path.write_text("{", encoding="utf-8")

            result = run(repo, home)

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("error:", result.stderr)

    def test_missing_source_exits_two(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(
                repo,
                "fake",
                [{"source": "global/absent", "target": "x", "kind": "file"}],
            )

            result = run(repo, home)

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("does not exist", result.stderr)

    def test_harness_name_must_match_the_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            path = repo / "harnesses" / "wrong" / "links.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps({"harness": "other", "root": ["~/.x"], "links": [RULES]}),
                encoding="utf-8",
            )

            result = run(repo, home)

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("harness must be 'wrong'", result.stderr)

    def test_root_falls_back_to_the_last_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(
                repo,
                "fake",
                [RULES],
                roots=["$UNSET_VARIABLE/x", "~/.config/opencode"],
            )

            result = run(repo, home)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(
                f"ln -sn {repo / 'global' / 'rules'} "
                f"{home / '.config' / 'opencode' / 'rules'}",
                result.stdout,
            )

    def test_set_environment_root_wins(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo, home = build(Path(temporary))
            write_manifest(
                repo, "fake", [RULES], roots=["$FAKE_HOME", "~/.config/opencode"]
            )

            result = run(repo, home)

            self.assertIn(
                f"ln -sn {repo / 'global' / 'rules'} {home / '.fake' / 'rules'}",
                result.stdout,
            )


if __name__ == "__main__":
    unittest.main()
