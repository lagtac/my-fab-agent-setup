#!/usr/bin/env python3
"""Regenerate skills-audit.md, or check the skill corpus for collisions.

Report mode (default) writes the markdown file.
Check mode (--check) writes nothing and exits 1 on any problem, 2 on a usage error.

Load      = tokens to read the whole SKILL.md when the skill is invoked.
Catalogue = tokens of the always-on `<name>: <description>` entry.

Both are byte length / 4. That is an approximation, not a tokenizer.
"""

from __future__ import annotations

import argparse
import math
import os
import re
import sys
from pathlib import Path

DEFAULT_ROOTS = [
    Path("~/.config/opencode/skills"),
    Path("~/.claude/skills"),
    Path("~/.agents/skills"),
]

DEFAULT_OUT = Path(__file__).resolve().parent.parent / "docs" / "skills-audit.md"

FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
BYTES_PER_TOKEN = 4

# Function words only. A tuning change here is a decision, recorded in
# docs/specs/skills-audit.md, not a drift.
STOPWORDS = frozenset(
    """a an and are as at be been but by can could do does did for from had has
    have how if in into is it its may might must of on or our so than that the
    their them then there these they this those to use used uses using via was
    we were what when where which will with would you your""".split()
)


class Skill:
    def __init__(
        self,
        name: str,
        description: str,
        path: Path,
        root: Path,
        *,
        hidden: bool,
    ) -> None:
        self.name = name
        self.description = description
        self.path = path
        self.root = root
        self.hidden = hidden
        self.load = len(path.read_bytes()) // BYTES_PER_TOKEN
        line = f"{name}: {description}\n"
        self.catalogue = len(line.encode("utf-8")) // BYTES_PER_TOKEN
        self.shadowed: list[Path] = []

    @property
    def source(self) -> str:
        return display(self.root)


def display(path: Path) -> str:
    home = str(Path.home())
    text = str(path)
    return "~" + text[len(home) :] if text.startswith(home) else text


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _block_scalar(header: str, lines: list[str]) -> str:
    """Unfold a `|` or `>` block scalar body."""
    folded = header.startswith(">")
    body = [line for line in lines]
    indents = [len(line) - len(line.lstrip()) for line in body if line.strip()]
    cut = min(indents) if indents else 0
    body = [line[cut:] if line.strip() else "" for line in body]

    if not folded:
        return "\n".join(body).strip()

    paragraphs: list[str] = []
    current: list[str] = []
    for line in body:
        if line.strip():
            current.append(line.strip())
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n".join(paragraphs)


def _frontmatter_keys(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}

    lines = match.group(1).splitlines()
    keys: dict[str, str] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        field = re.match(r"^([A-Za-z_][\w-]*):[ \t]*(.*)$", line)
        index += 1
        if not field:
            continue

        key, rest = field.group(1), field.group(2).strip()
        if rest[:1] in {"|", ">"}:
            # Block scalar: consume the indented lines that follow.
            block: list[str] = []
            while index < len(lines) and (
                not lines[index].strip() or lines[index][:1] in " \t"
            ):
                block.append(lines[index])
                index += 1
            rest = _block_scalar(rest, block)
        elif rest and index < len(lines) and lines[index][:1] in " \t":
            # Plain scalar wrapped over several lines: YAML folds them with spaces.
            parts = [rest]
            while (
                index < len(lines)
                and lines[index][:1] in " \t"
                and lines[index].strip()
            ):
                parts.append(lines[index].strip())
                index += 1
            rest = " ".join(parts)
        elif not rest and index < len(lines) and lines[index][:1] in " \t":
            # An indented block under an empty value: expose its scalar
            # children as `parent/child`. Sequences simply yield no keys.
            while index < len(lines) and lines[index][:1] in " \t":
                child = re.match(r"^[ \t]+([A-Za-z_][\w-]*):[ \t]*(.*)$", lines[index])
                index += 1
                if child:
                    keys[f"{key}/{child.group(1)}"] = _strip_quotes(
                        child.group(2).strip()
                    )
            continue

        keys[key] = _strip_quotes(rest)
    return keys


def discover(root: Path) -> list[Skill]:
    root = root.expanduser()
    if not root.is_dir():
        print(f"warning: skipping missing root {display(root)}", file=sys.stderr)
        return []

    skills: list[Skill] = []
    visited: set[tuple[int, int]] = set()
    for directory, subdirs, filenames in os.walk(root, followlinks=True):
        subdirs.sort()
        try:
            stats = os.stat(directory)
        except OSError as error:
            print(f"warning: cannot stat {directory}: {error}", file=sys.stderr)
            subdirs[:] = []
            continue
        marker = (stats.st_dev, stats.st_ino)
        if marker in visited:
            # A symlink back into the tree we already walked: stop descending.
            subdirs[:] = []
            continue
        visited.add(marker)

        if "SKILL.md" not in filenames:
            continue
        path = Path(directory) / "SKILL.md"
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as error:
            print(f"warning: cannot read {path}: {error}", file=sys.stderr)
            continue

        fields = _frontmatter_keys(text)
        name = fields.get("name") or Path(directory).name
        hidden = (
            fields.get("disable-model-invocation", "").lower() == "true"
            or fields.get("opencode/autoinvoke", "").lower() == "false"
        )
        skills.append(
            Skill(name, fields.get("description", ""), path, root, hidden=hidden)
        )
    return skills


def collect(roots: list[Path]) -> list[Skill]:
    by_name: dict[str, Skill] = {}
    for root in roots:
        for skill in discover(root):
            winner = by_name.get(skill.name)
            if winner is None:
                by_name[skill.name] = skill
            elif winner.root != skill.root:
                # Root order decides; the earlier root wins.
                winner.shadowed.append(skill.path)
            elif (len(skill.path.parts), str(skill.path)) < (
                len(winner.path.parts),
                str(winner.path),
            ):
                # Same root, shallower copy: a nested snapshot is not the installed skill.
                skill.shadowed = winner.shadowed + [winner.path]
                by_name[skill.name] = skill
            else:
                winner.shadowed.append(skill.path)

    for skill in by_name.values():
        skill.shadowed.sort()

    return sorted(by_name.values(), key=lambda skill: (-skill.load, skill.name))


def cell(value: str) -> str:
    """Escape a value so it cannot break the pipe-delimited table."""
    return value.replace("|", "\\|").replace("\n", " ")


def tokens(description: str) -> set[str]:
    """Case-insensitive description words, stopwords dropped."""
    return {
        word
        for word in re.split(r"[^a-z0-9]+", description.lower())
        if word and word not in STOPWORDS
    }


def similarity(left: Skill, right: Skill) -> float:
    """Jaccard: shared description tokens over all tokens."""
    left_tokens = tokens(left.description)
    right_tokens = tokens(right.description)
    union = left_tokens | right_tokens
    if not union:
        return 0.0
    return len(left_tokens & right_tokens) / len(union)


def overlaps(skills: list[Skill], threshold: float) -> list[tuple[float, Skill, Skill]]:
    """Every pair at or above the threshold, by score then name."""
    pairs = []
    for index, left in enumerate(skills):
        for right in skills[index + 1 :]:
            score = similarity(left, right)
            if score >= threshold:
                first, second = sorted((left, right), key=lambda skill: skill.name)
                pairs.append((score, first, second))
    pairs.sort(key=lambda pair: (-pair[0], pair[1].name, pair[2].name))
    return pairs


def threshold_arg(text: str) -> float:
    """A Jaccard score cut-off, which is always a number in 0..1."""
    value = float(text)
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise argparse.ArgumentTypeError("must be a number between 0 and 1")
    return value


def advertised_lines(skills: list[Skill], advertised: list[str]) -> list[str]:
    """One line per required ID that is missing or hidden by its frontmatter."""
    by_name = {skill.name: skill for skill in skills}
    lines = []
    for name in sorted(set(advertised)):
        skill = by_name.get(name)
        if skill is None:
            lines.append(f"missing: {name}")
        elif skill.hidden:
            lines.append(f"hidden: {name} at {display(skill.path)}")
    return lines


def problem_lines(
    skills: list[Skill], threshold: float, advertised: list[str]
) -> list[str]:
    """One line per problem, classed and deterministically ordered."""
    lines = [
        f"collision: {first.name} / {second.name} ({score:.2f})"
        for score, first, second in overlaps(skills, threshold)
    ]
    for skill in sorted(skills, key=lambda skill: skill.name):
        for path in skill.shadowed:
            lines.append(
                f"shadowed: {skill.name} at {display(path)} "
                f"(winner {display(skill.path)})"
            )
    lines += advertised_lines(skills, advertised)
    return lines


def render(skills: list[Skill], roots: list[Path], threshold: float) -> str:
    scanned = ", ".join(f"`{display(root.expanduser())}`" for root in roots)
    lines = [
        "# Skills audit",
        "",
        "Generated by `scripts/skills_audit.py`. Do not edit.",
        "",
        f"Scanned: {scanned}.",
        "",
        "**Load** = approximate tokens to load the full `SKILL.md` when invoked (bytes / 4).",
        "**Catalogue** = approximate tokens of the always-on `<name>: <description>` entry (bytes / 4).",
        "",
        "| # | Skill | Source | Load (tok) | Catalogue (tok) | Shadowed |",
        "|---:|---|---|---:|---:|---|",
    ]

    for position, skill in enumerate(skills, start=1):
        shadowed = "<br>".join(f"`{cell(display(path))}`" for path in skill.shadowed)
        lines.append(
            f"| {position} | {cell(skill.name)} | {cell(skill.source)} | "
            f"{skill.load:,} | {skill.catalogue:,} | {shadowed} |"
        )

    total_load = sum(skill.load for skill in skills)
    total_catalogue = sum(skill.catalogue for skill in skills)
    lines += [
        "",
        f"**Skills:** {len(skills)} · "
        f"**Total load:** {total_load:,} tok · "
        f"**Catalogue (always on):** {total_catalogue:,} tok",
        "",
        "## Trigger collisions",
        "",
        f"Threshold {threshold:.2f}. Jaccard overlap of description tokens, "
        "case-insensitive, stopwords dropped.",
        "",
    ]

    pairs = overlaps(skills, threshold)
    if not pairs:
        lines += [f"No pair at or above threshold {threshold:.2f}.", ""]
    else:
        lines += [
            "| Score | Skill A | Skill B |",
            "|---:|---|---|",
        ]
        for score, first, second in pairs:
            lines.append(f"| {score:.2f} | {cell(first.name)} | {cell(second.name)} |")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        action="append",
        type=Path,
        dest="roots",
        help="Skill directory to scan; repeatable, replaces the defaults.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Markdown file to write (default: {display(DEFAULT_OUT)}).",
    )
    parser.add_argument(
        "--threshold",
        type=threshold_arg,
        default=0.4,
        help="Report description pairs scoring at or above this (default: 0.4).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Print problems to stderr and exit 1 on any; write no file.",
    )
    parser.add_argument(
        "--require-advertised",
        action="append",
        default=[],
        metavar="ID",
        dest="advertised",
        help="Skill ID that must be model-invoked; repeatable, requires --check.",
    )
    args = parser.parse_args(argv)

    if args.advertised and not args.check:
        parser.error("--require-advertised requires --check")

    roots = args.roots or DEFAULT_ROOTS
    skills = collect(roots)
    if not skills:
        print("error: no skills found", file=sys.stderr)
        return 2

    if args.check:
        found = problem_lines(skills, args.threshold, args.advertised)
        for line in found:
            print(line, file=sys.stderr)
        return 1 if found else 0

    output = args.out.expanduser()
    try:
        output.write_text(render(skills, roots, args.threshold), encoding="utf-8")
    except OSError as error:
        print(f"error: cannot write {display(output)}: {error}", file=sys.stderr)
        return 2
    print(f"wrote {display(output)}: {len(skills)} skills", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
