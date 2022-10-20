#!/usr/bin/env python3
"""Rename a svelte component."""
import argparse
import difflib
import itertools
import logging
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


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


extensions = "ts", "svelte"
src = pathlib.Path("src/")
a_path = pathlib.Path("a/")
b_path = pathlib.Path("b/")

CHECK = "npm", "run", "check"
FORMAT = "npm", "run", "format"
GIT_ADD = "git", "add", str(src)
GIT_COMMIT = "git", "commit", "-e", "-m"
GIT_RESET = "git", "reset", str(src)
GIT_CHECKOUT = "git", "checkout"
GIT_APPLY = "git", "apply"
GIT_APPLY_REVERSE = "git", "apply", "--reverse"


@dataclass
class ReplacementContext:
    """Store rename relevant context."""

    src_cmp: pathlib.Path
    dst_cmp: pathlib.Path
    src_lib_path: pathlib.Path
    dst_lib_path: pathlib.Path
    src_component_name: str
    dst_component_name: str


@dataclass
class FileDiff:
    """Contain the diff for one file."""

    original: List[str]
    changed: List[str]
    fromfile: pathlib.Path
    tofile: pathlib.Path
    diff: List[str]


@dataclass
class DestructiveResult:
    """Return all changes as part of the destructive operation."""

    deleted_file: pathlib.Path
    new_file: pathlib.Path
    diffs: List[FileDiff]


def process_line(ctx: ReplacementContext, line: str) -> str:
    """Process and return an individual line."""
    src_import_stmt = (
        f'import {ctx.src_component_name} from "${ctx.src_lib_path}";'
    )
    dst_import_stmt = (
        f'import {ctx.dst_component_name} from "${ctx.dst_lib_path}";'
    )

    src_tag = f"<{ctx.src_component_name}(?P<suffix>$|\\s)"
    dst_tag = f"<{ctx.dst_component_name}\\g<suffix>"

    line2 = line.replace(src_import_stmt, dst_import_stmt)
    line3 = re.sub(src_tag, dst_tag, line2)
    return line3


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
        logging.info("Patching %s", diff.tofile)
        patch = "".join(diff.diff).encode()
        subprocess.run(GIT_APPLY, input=patch, check=True)


def revert_diffs(diffs: List[FileDiff]) -> None:
    """Revert the diffs."""
    for diff in diffs:
        patch = "".join(diff.diff).encode()
        logger.info("Unapplying %s", patch.decode())
        subprocess.run(GIT_APPLY_REVERSE, input=patch, check=True)


def attempt_cleanup(destructive_result: DestructiveResult) -> None:
    """Attempt to clean up the mess."""
    logger.info("Attempting cleanup")
    subprocess.run(GIT_RESET, check=True)
    subprocess.run(
        (*GIT_CHECKOUT, destructive_result.deleted_file),
        check=True,
    )
    destructive_result.new_file.unlink()
    revert_diffs(destructive_result.diffs)


def destructive(ctx: ReplacementContext) -> DestructiveResult:
    """Perform all destructive actions."""
    diffs: List[FileDiff] = []
    try:
        shutil.move(ctx.src_cmp, ctx.dst_cmp)

        rename_candidates = list(
            itertools.chain.from_iterable(
                src.glob(f"**/*.{e}") for e in extensions
            )
        )
        diffs = create_diffs(ctx, rename_candidates)
        apply_diffs(diffs)
        subprocess.run(CHECK, check=True)
        subprocess.run(FORMAT, check=True)
        subprocess.run(GIT_ADD, check=True)
        msg_prefix = ctx.dst_lib_path.parent
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
    except Exception as e:
        logger.error("Something went wrong", exc_info=e)
        attempt_cleanup(
            DestructiveResult(
                deleted_file=ctx.src_cmp,
                new_file=ctx.dst_cmp,
                diffs=diffs,
            )
        )
        raise e
    return DestructiveResult(
        deleted_file=ctx.src_cmp,
        new_file=ctx.dst_cmp,
        diffs=diffs,
    )


def main(args: argparse.Namespace) -> None:
    """Move from to, make sure all files track the path change."""
    src_cmp = pathlib.Path(args.src_cmp)
    dst_cmp = pathlib.Path(args.dst_cmp)
    if not src_cmp.exists():
        if dst_cmp.exists():
            logger.info("Move has already been performed")
            return
        else:
            raise ValueError("Source file does not exist")

    ctx = ReplacementContext(
        src_cmp=src_cmp,
        dst_cmp=dst_cmp,
        src_lib_path=src_cmp.relative_to(src),
        dst_lib_path=dst_cmp.relative_to(src),
        src_component_name=src_cmp.stem,
        dst_component_name=dst_cmp.stem,
    )

    destructive_result = destructive(ctx)

    logger.info(
        "Renamed %s to %s",
        destructive_result.deleted_file,
        destructive_result.new_file,
    )
    for p in destructive_result.diffs:
        logger.info("Modified %s", p.tofile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src_cmp", type=str)
    parser.add_argument("dst_cmp", type=str)
    args = parser.parse_args()
    main(args)
