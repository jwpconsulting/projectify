#!/usr/bin/env python3
"""Rename a svelte component."""
import argparse
import itertools
import logging
import pathlib
import shutil
from dataclasses import (
    dataclass,
)


logging.basicConfig(level=logging.INFO)

extensions = "ts", "svelte"
src = pathlib.Path("src/")


@dataclass
class ReplacementContext:
    """Store rename relevant context."""

    src_lib_path: str
    dst_lib_path: str
    src_component_name: str
    dst_component_name: str


def process_line(ctx: ReplacementContext, line: str) -> str:
    """Process and return an individual line."""
    line2 = line.replace(ctx.src_lib_path, ctx.dst_lib_path)
    line3 = line2.replace(ctx.src_component_name, ctx.dst_component_name)
    return line3


def main(args: argparse.Namespace) -> None:
    """Move from to, make sure all files track the path change."""
    src_cmp = pathlib.Path(args.src_cmp)
    dst_cmp = pathlib.Path(args.dst_cmp)
    if not src_cmp.exists():
        if dst_cmp.exists():
            logging.warning("Has this already been performed?")
            logging.warning("%s does not exist", src_cmp)
            logging.warning("%s exists", dst_cmp)
            return
    shutil.move(src_cmp, dst_cmp)

    ctx = ReplacementContext(
        src_lib_path=str(src_cmp.relative_to(src)),
        dst_lib_path=str(dst_cmp.relative_to(src)),
        src_component_name=src_cmp.stem,
        dst_component_name=dst_cmp.stem,
    )

    rename_candidates = list(
        itertools.chain.from_iterable(
            src.glob(f"**/*.{e}") for e in extensions
        )
    )

    for candidate in rename_candidates:
        lines = candidate.read_text().splitlines()
        if not lines:
            continue
        # Cool UNIX fact: An empty file contains no trailing new line
        # I guess that makes sense: A new line after every line, but if there
        # are no lines, then no new line?
        out_lines = [process_line(ctx, line) for line in lines]
        out = "\n".join(out_lines) + "\n"
        candidate.write_text(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src_cmp", type=str)
    parser.add_argument("dst_cmp", type=str)
    args = parser.parse_args()
    main(args)
