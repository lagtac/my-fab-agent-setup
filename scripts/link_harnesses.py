#!/usr/bin/env python3
"""Check each harness config directory, and link this repo's resources into it.

Report mode (default) prints one line per link and the `ln` command that fixes it.
Apply mode (--apply) creates missing links and repairs dangling ones. It never
overwrites a real file or a link that points somewhere else.
Check mode (--check) prints problems to stderr and exits 1 on any, 2 on a config
error, and changes nothing.

The map lives in `harnesses/<name>/links.json`. See `docs/linking.md`.

Exit codes:
    0  report mode finished, or nothing is left to fix
    1  --check found a problem, or --apply left one it will not fix
    2  a usage error, or a manifest that cannot be read or validated
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Roots this repo used to link into and no longer does. A symlink here that
# resolves into the repo is reported with the command that removes it.
RETIRED_ROOTS = ["~/.agents"]

KINDS = ("file", "dir", "children")

VARIABLE = re.compile(r"\$(?:\{([A-Za-z_][A-Za-z0-9_]*)\}|([A-Za-z_][A-Za-z0-9_]*))")


class ManifestError(Exception):
    """A manifest is unreadable, or it describes a link that cannot exist."""


class Link:
    """One manifest entry: a source in the repo and where it belongs."""

    def __init__(
        self, source: Path, target: str, kind: str, exclude: list[str]
    ) -> None:
        self.source = source
        self.target = target
        self.kind = kind
        self.exclude = exclude


class Manifest:
    """The link map for one harness."""

    def __init__(
        self,
        name: str,
        path: Path,
        candidates: list[str],
        binary: str | None,
        links: list[Link],
    ) -> None:
        self.name = name
        self.path = path
        self.candidates = candidates
        self.binary = binary
        self.links = links


class Entry:
    """One symlink that should exist, and its current state."""

    def __init__(self, harness: str, source: Path, target: Path, kind: str) -> None:
        self.harness = harness
        self.source = source
        self.target = target
        self.kind = kind
        self.status = status_of(source, target)

    @property
    def fixable(self) -> bool:
        return self.status in ("missing", "dangling")


class LinkReport:
    """One manifest entry, expanded into the entries it expects."""

    def __init__(self, link: Link, entries: list[Entry]) -> None:
        self.link = link
        self.entries = entries


class HarnessReport:
    """One harness, its resolved root, and the state of every link."""

    def __init__(
        self,
        manifest: Manifest,
        root: Path,
        signals: list[str],
        links: list[LinkReport],
    ) -> None:
        self.manifest = manifest
        self.root = root
        self.signals = signals
        self.links = links


def display(path: Path) -> str:
    home = str(Path.home())
    text = str(path)
    if text == home:
        return "~"
    if text.startswith(home + os.sep):
        return "~" + text[len(home) :]
    return text


def expand_candidate(text: str) -> Path | None:
    """Expand `~` and `$VARS`; None when a referenced variable is unset."""
    unset = False

    def replace(match: re.Match[str]) -> str:
        nonlocal unset
        value = os.environ.get(match.group(1) or match.group(2), "")
        if not value:
            unset = True
            return ""
        return value

    expanded = VARIABLE.sub(replace, text)
    return None if unset else Path(expanded).expanduser()


def resolve_root(candidates: list[str]) -> Path:
    """First candidate that exists, else the first the environment names.

    Falls back to the last candidate when no variable is set.
    """
    expanded = [expand_candidate(text) for text in candidates]
    for path in expanded:
        if path is not None and path.exists():
            return path
    for path in expanded:
        if path is not None:
            return path
    return Path(candidates[-1]).expanduser()


def status_of(source: Path, target: Path) -> str:
    if os.path.islink(target):
        if not target.exists():
            return "dangling"
        if os.path.realpath(target) == os.path.realpath(source):
            return "ok"
        return "wrong-target"
    return "blocked" if target.exists() else "missing"


def require(condition: bool, path: Path, message: str) -> None:
    if not condition:
        raise ManifestError(f"{display(path)}: {message}")


def load_manifest(path: Path, repo: Path) -> Manifest:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ManifestError(f"{display(path)}: {error}") from error

    require(isinstance(data, dict), path, "top level must be an object")
    name = data.get("harness")
    require(
        isinstance(name, str) and name == path.parent.name,
        path,
        f"harness must be {path.parent.name!r}",
    )

    candidates = data.get("root")
    require(
        isinstance(candidates, list)
        and bool(candidates)
        and all(isinstance(item, str) for item in candidates),
        path,
        "root must be a non-empty list of strings",
    )

    binary = data.get("binary")
    require(binary is None or isinstance(binary, str), path, "binary must be a string")

    raw_links = data.get("links")
    require(
        isinstance(raw_links, list) and bool(raw_links),
        path,
        "links must be a non-empty list",
    )

    links: list[Link] = []
    for position, item in enumerate(raw_links, start=1):
        where = f"links[{position}]"
        require(isinstance(item, dict), path, f"{where} must be an object")

        source = item.get("source")
        target = item.get("target")
        kind = item.get("kind")
        exclude = item.get("exclude", [])
        require(
            isinstance(source, str) and bool(source),
            path,
            f"{where}.source must be a string",
        )
        require(
            isinstance(target, str) and bool(target),
            path,
            f"{where}.target must be a string",
        )
        require(kind in KINDS, path, f"{where}.kind must be one of {', '.join(KINDS)}")
        require(
            isinstance(exclude, list)
            and all(isinstance(entry, str) for entry in exclude),
            path,
            f"{where}.exclude must be a list of strings",
        )

        resolved = (repo / source).resolve()
        require(resolved.exists(), path, f"{where}.source {source} does not exist")
        if kind in ("dir", "children"):
            require(
                resolved.is_dir(), path, f"{where}.source {source} must be a directory"
            )
        else:
            require(resolved.is_file(), path, f"{where}.source {source} must be a file")

        links.append(Link(resolved, target, kind, exclude))

    return Manifest(name, path, candidates, binary, links)


def load_manifests(repo: Path) -> list[Manifest]:
    folder = repo / "harnesses"
    paths = sorted(folder.glob("*/links.json"))
    if not paths:
        raise ManifestError(f"no manifests under {display(folder)}")
    return [load_manifest(path, repo) for path in paths]


def inspect(manifest: Manifest) -> HarnessReport:
    root = resolve_root(manifest.candidates)
    signals = []
    found = shutil.which(manifest.binary) if manifest.binary else None
    if found:
        signals.append(f"binary {found}")
    if root.exists():
        signals.append(f"config {display(root)}")

    reports: list[LinkReport] = []
    for link in manifest.links:
        target = root / link.target
        if link.kind == "children":
            entries = [
                Entry(manifest.name, child, target / child.name, "child")
                for child in sorted(link.source.iterdir())
                if child.name not in link.exclude
            ]
        else:
            entries = [Entry(manifest.name, link.source, target, link.kind)]
        reports.append(LinkReport(link, entries))
    return HarnessReport(manifest, root, signals, reports)


def find_stale(repo: Path) -> list[tuple[Path, Path]]:
    """Symlinks in a retired root that point into the repo, or point nowhere."""
    stale: list[tuple[Path, Path]] = []
    for text in RETIRED_ROOTS:
        root = Path(text).expanduser()
        if not root.is_dir():
            continue
        for entry in sorted(root.iterdir()):
            if not entry.is_symlink():
                continue
            real = Path(os.path.realpath(entry))
            inside = real == repo or repo in real.parents
            if inside or not entry.exists():
                stale.append((entry, real))
    return stale


def command(entry: Entry) -> str:
    flag = "-sfn" if entry.status == "dangling" else "-sn"
    return (
        f"ln {flag} {shlex.quote(str(entry.source))} {shlex.quote(str(entry.target))}"
    )


def problem_line(entry: Entry) -> str:
    return (
        f"{entry.status}: {entry.harness} {display(entry.target)} "
        f"-> {display(entry.source)}"
    )


def stale_line(path: Path, real: Path) -> str:
    return f"stale: {display(path)} -> {display(real)}"


def label(report: LinkReport) -> str:
    return report.link.target + ("/" if report.link.kind == "children" else "")


def status_text(report: LinkReport) -> str:
    if report.link.kind != "children":
        return report.entries[0].status
    total = len(report.entries)
    ok = sum(1 for entry in report.entries if entry.status == "ok")
    return f"ok ({total})" if ok == total else f"{ok}/{total} ok"


def print_report(
    harnesses: list[HarnessReport], stale: list[tuple[Path, Path]]
) -> None:
    commands: list[str] = []
    for harness in harnesses:
        if harness.signals:
            print(f"{harness.manifest.name}: installed ({', '.join(harness.signals)})")
        else:
            print(
                f"{harness.manifest.name}: not installed "
                f"(no binary {harness.manifest.binary!r}, "
                f"no config {display(harness.root)})"
            )
        for report in harness.links:
            print(f"  {label(report):<20} {status_text(report)}")
            commands += [command(entry) for entry in report.entries if entry.fixable]
        print()

    if commands:
        print("Link commands:")
        for line in commands:
            print(f"  {line}")
        print()

    if stale:
        print("Stale links into this repo:")
        for path, real in stale:
            print(f"  {display(path)} -> {display(real)}")
            print(f"    rm {shlex.quote(str(path))}")
        print()

    if not commands and not stale:
        print("Nothing to link.")


def apply_entry(entry: Entry) -> bool:
    """Create or repair one link. Returns False when the filesystem refused."""
    if not entry.fixable:
        return False
    try:
        entry.target.parent.mkdir(parents=True, exist_ok=True)
        if entry.status == "dangling":
            entry.target.unlink()
        entry.target.symlink_to(entry.source)
    except OSError as error:
        print(f"error: {display(entry.target)}: {error}", file=sys.stderr)
        return False
    return True


def apply_all(manifests: list[Manifest], repo: Path) -> int:
    linked: list[Entry] = []
    for manifest in manifests:
        for report in inspect(manifest).links:
            for entry in report.entries:
                if apply_entry(entry):
                    linked.append(entry)

    for entry in linked:
        print(f"linked: {display(entry.target)} -> {display(entry.source)}")

    problems = [
        problem_line(entry)
        for manifest in manifests
        for report in inspect(manifest).links
        for entry in report.entries
        if entry.status != "ok"
    ]
    stale = find_stale(repo)
    for line in problems:
        print(line, file=sys.stderr)
    for path, real in stale:
        print(stale_line(path, real), file=sys.stderr)

    if not linked and not problems and not stale:
        print("nothing to do")
    return 1 if problems or stale else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help=f"repository to link from (default: {display(REPO_ROOT)})",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--apply",
        action="store_true",
        help="create missing links and repair dangling ones; never overwrite",
    )
    mode.add_argument(
        "--check",
        action="store_true",
        help="print problems to stderr and exit 1 on any; change nothing",
    )
    args = parser.parse_args(argv)

    repo = args.repo_root.expanduser().resolve()
    try:
        manifests = load_manifests(repo)
    except ManifestError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if args.apply:
        return apply_all(manifests, repo)

    harnesses = [inspect(manifest) for manifest in manifests]
    stale = find_stale(repo)

    if args.check:
        problems = [
            problem_line(entry)
            for harness in harnesses
            for report in harness.links
            for entry in report.entries
            if entry.status != "ok"
        ]
        problems += [stale_line(path, real) for path, real in stale]
        for line in problems:
            print(line, file=sys.stderr)
        return 1 if problems else 0

    print_report(harnesses, stale)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
