#!/usr/bin/env python3
"""Rename a svelte component."""
import csv
import difflib
import itertools
import pathlib
import re
import shutil
import subprocess
from dataclasses import (
    dataclass,
)
from typing import (
    List,
)

import click


extensions = "ts", "svelte"
src = pathlib.Path("src/")
a_path = pathlib.Path("a/")
b_path = pathlib.Path("b/")
# Subtract src/lib and add src/stories path back
component_lib_path = pathlib.Path("src/lib")
src_stories_prefix = pathlib.Path("src/stories")
stories_suffix = ".stories.ts"

CHECK = "npm", "run", "check"
FIX = "npm", "run", "fix"
GIT_ADD = "git", "add", str(src)
GIT_COMMIT = "git", "commit", "-e", "-m"
GIT_RESET = "git", "reset", str(src)
GIT_CHECKOUT = "git", "checkout"
GIT_APPLY = "git", "apply"
GIT_APPLY_REVERSE = "git", "apply", "--reverse"


@dataclass
class ReplacementInvocation:
    """Store all information needed for a single invocation."""

    src_cmp: str
    dst_cmp: str


@dataclass(kw_only=True, frozen=True)
class ReplacementContext:
    """Store rename relevant context."""

    src_cmp: pathlib.Path
    dst_cmp: pathlib.Path
    src_stories_path: pathlib.Path
    dst_stories_path: pathlib.Path
    src_lib_path: pathlib.Path
    dst_lib_path: pathlib.Path
    src_component_name: str
    dst_component_name: str


@dataclass(kw_only=True, frozen=True)
class FileDiff:
    """Contain the diff for one file."""

    original: List[str]
    changed: List[str]
    fromfile: pathlib.Path
    tofile: pathlib.Path
    diff: List[str]


@dataclass(kw_only=True, frozen=True)
class DestructiveResult:
    """Return all changes as part of the destructive operation."""

    deleted_file: pathlib.Path
    new_file: pathlib.Path
    deleted_stories_file: pathlib.Path
    new_stories_file: pathlib.Path
    diffs: List[FileDiff]


class CheckError(Exception):
    """Contain the data necessary to unwind the stack and return diffs."""

    exception: Exception
    diffs: List[FileDiff]

    def __init__(self, exception: Exception, diffs: List[FileDiff]):
        """Initialize with diff."""
        self.exception = exception
        self.diffs = diffs


def process_line(ctx: ReplacementContext, line: str) -> str:
    """Process and return an individual line."""
    # Imports
    line = line.replace(
        f'import {ctx.src_component_name} from "${ctx.src_lib_path}";',
        f'import {ctx.dst_component_name} from "${ctx.dst_lib_path}";',
    )
    # Tags
    line = re.sub(
        f"<{ctx.src_component_name}(?P<suffix>$|\\s)",
        f"<{ctx.dst_component_name}\\g<suffix>",
        line,
    )
    line = line.replace(
        f"</{ctx.src_component_name}>",
        f"</{ctx.dst_component_name}>",
    )

    # Stories
    line = re.sub(
        rf"(?P<prefix>Meta|StoryObj)<{ctx.src_component_name}>",
        rf"\g<prefix><{ctx.dst_component_name}>",
        line,
    )
    line = line.replace(
        f"component: {ctx.src_component_name}",
        f"component: {ctx.dst_component_name}",
    )
    return line


def create_diffs(
    ctx: ReplacementContext, rename_candidates: List[pathlib.Path]
) -> List[FileDiff]:
    """Process all candidate files."""
    diffs = []
    for candidate in rename_candidates:
        fromfile = a_path / candidate
        tofile = b_path / candidate
        original = candidate.read_text().splitlines(True)
        if not original:
            continue
        changed = []
        for line in original:
            result = process_line(ctx, line)
            changed.append(result)
        diff = list(
            difflib.unified_diff(
                original,
                changed,
                str(fromfile),
                str(tofile),
            )
        )
        if len(diff) == 0:
            continue
        diffs.append(
            FileDiff(
                original=original,
                changed=changed,
                fromfile=fromfile,
                tofile=tofile,
                diff=diff,
            )
        )
    return diffs


def apply_diffs(diffs: List[FileDiff]) -> None:
    """Apply diffs."""
    for diff in diffs:
        click.echo(f"Patching {diff.tofile}")
        patch = "".join(diff.diff).encode()
        subprocess.run(GIT_APPLY, input=patch, check=True)


def revert_diffs(diffs: List[FileDiff]) -> None:
    """Revert the diffs."""
    for diff in diffs:
        patch = "".join(diff.diff).encode()
        click.echo(f"Unapplying {patch.decode()}")
        subprocess.run(GIT_APPLY_REVERSE, input=patch, check=True)


def attempt_cleanup(destructive_result: DestructiveResult) -> None:
    """Attempt to clean up the mess."""
    click.echo("Attempting cleanup")
    subprocess.run(GIT_RESET, check=True)
    subprocess.run(
        (*GIT_CHECKOUT, destructive_result.deleted_file),
        check=True,
    )
    destructive_result.new_file.unlink()
    subprocess.run(
        (*GIT_CHECKOUT, destructive_result.deleted_stories_file),
        check=True,
    )
    destructive_result.new_stories_file.unlink()
    revert_diffs(destructive_result.diffs)


def make_msg_prefix(dst_lib_path: pathlib.Path) -> str:
    """Make a git commit message prefix."""
    parent = dst_lib_path.parent
    return "/".join([p.capitalize() for p in parent.parts])


def _destructive(ctx: ReplacementContext) -> List[FileDiff]:
    diffs: List[FileDiff] = []
    ctx.dst_cmp.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(ctx.src_cmp, ctx.dst_cmp)
    ctx.dst_stories_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(ctx.src_stories_path, ctx.dst_stories_path)

    rename_candidates = list(
        itertools.chain.from_iterable(
            src.glob(f"**/*.{e}") for e in extensions
        )
    )
    diffs = create_diffs(ctx, rename_candidates)
    apply_diffs(diffs)

    try:
        subprocess.run(FIX, check=True)
        subprocess.run(CHECK, check=True)
    except subprocess.CalledProcessError as e:
        raise CheckError(e, diffs)

    subprocess.run(GIT_ADD, check=True)
    msg_prefix = make_msg_prefix(ctx.dst_lib_path)
    msg = (
        f"{msg_prefix}: {ctx.src_component_name} -> "
        f"{ctx.dst_component_name}"
    )
    subprocess.run(
        (
            *GIT_COMMIT,
            msg,
        ),
        check=True,
    )
    return diffs


def destructive(ctx: ReplacementContext) -> DestructiveResult:
    """Perform all destructive actions."""
    diffs: List[FileDiff]
    try:
        diffs = _destructive(ctx)
    except CheckError as e:
        diffs = e.diffs
        click.echo(f"Something went wrong: {e.exception}")
        attempt_cleanup(
            DestructiveResult(
                deleted_file=ctx.src_cmp,
                new_file=ctx.dst_cmp,
                deleted_stories_file=ctx.src_stories_path,
                new_stories_file=ctx.dst_stories_path,
                diffs=diffs,
            )
        )
        raise e.exception
    return DestructiveResult(
        deleted_file=ctx.src_cmp,
        new_file=ctx.dst_cmp,
        deleted_stories_file=ctx.src_stories_path,
        new_stories_file=ctx.dst_stories_path,
        diffs=diffs,
    )


def main(args: ReplacementInvocation) -> None:
    """Move from to, make sure all files track the path change."""
    src_cmp = pathlib.Path(args.src_cmp)
    dst_cmp = pathlib.Path(args.dst_cmp)
    if not src_cmp.exists():
        if dst_cmp.exists():
            click.echo("Move has already been performed")
            return
        else:
            raise ValueError(f"Source file {src_cmp} does not exist")

    # Guess the stories path
    src_stories_path: pathlib.Path = (
        src_stories_prefix / src_cmp.relative_to(component_lib_path)
    ).with_suffix(stories_suffix)
    dst_stories_path: pathlib.Path = (
        src_stories_prefix / dst_cmp.relative_to(component_lib_path)
    ).with_suffix(stories_suffix)
    if not src_stories_path.exists():
        if dst_stories_path.exists():
            click.echo(
                f"A stories file was found at {dst_stories_path}. "
                f"Move already performed?"
            )
            return
        raise ValueError(
            f"Could not find corresponding story {src_stories_path} for "
            f"component at {src_cmp}"
        )

    ctx = ReplacementContext(
        src_cmp=src_cmp,
        dst_cmp=dst_cmp,
        src_lib_path=src_cmp.relative_to(src),
        dst_lib_path=dst_cmp.relative_to(src),
        src_stories_path=src_stories_path,
        dst_stories_path=dst_stories_path,
        src_component_name=src_cmp.stem,
        dst_component_name=dst_cmp.stem,
    )

    destructive_result = destructive(ctx)

    click.echo(
        f"Renamed {destructive_result.deleted_file} to "
        f"{destructive_result.new_file}",
    )
    for p in destructive_result.diffs:
        click.echo(f"Modified {p.tofile}")


@click.group()
def cli() -> None:
    """Group all commands."""
    pass


@cli.command()
@click.argument("src_cmp", type=click.Path(exists=True))
@click.argument("dst_cmp", type=click.Path())
def single(src_cmp: str, dst_cmp: str) -> None:
    """Do a single run."""
    main(
        ReplacementInvocation(
            src_cmp=src_cmp,
            dst_cmp=dst_cmp,
        )
    )


@cli.command()
@click.argument("csv_path", type=click.File())
def multiple(csv_path: str) -> None:
    """Do multiple."""
    fieldnames = "src_cmp", "dst_cmp"
    reader = csv.DictReader(csv_path, fieldnames=fieldnames)
    todo: List[ReplacementInvocation] = []
    # Skip first row
    next(reader)
    for row in reader:
        todo.append(
            ReplacementInvocation(
                src_cmp=row["src_cmp"],
                dst_cmp=row["dst_cmp"],
            )
        )
    for t in todo:
        main(t)


if __name__ == "__main__":
    cli()
