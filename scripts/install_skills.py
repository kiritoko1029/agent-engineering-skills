#!/usr/bin/env python3
"""Plan or copy complete skill folders; apply is explicit and overwrites are refused."""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path

# A dry run must not create an import cache in the source repository either.
sys.dont_write_bytecode = True
from validate_repo import valid_name, validate_skill


def is_link_or_reparse(path: Path) -> bool:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def reject_link_ancestors(path: Path) -> None:
    for item in [path, *path.parents]:
        if is_link_or_reparse(item):
            raise ValueError(f"symbolic links and Windows reparse points are not allowed: {item}")


def inspect_source(source: Path) -> None:
    reject_link_ancestors(source)
    if not source.is_dir():
        raise ValueError(f"skill does not exist: {source.name}")
    for parent, directories, files in os.walk(source, followlinks=False):
        for name in directories + files:
            item = Path(parent) / name
            if is_link_or_reparse(item):
                raise ValueError(f"skill source contains a symbolic link or reparse point: {item}")
            if not item.is_dir() and not item.is_file():
                raise ValueError(f"skill source contains a special file: {item}")
    errors = validate_skill(source)
    if errors:
        raise ValueError("; ".join(errors))


def build_plan(repo: Path, target: Path, names: list[str] | None) -> list[tuple[Path, Path]]:
    skills_dir = repo / "skills"
    reject_link_ancestors(skills_dir)
    reject_link_ancestors(target)
    if target.exists() and not target.is_dir():
        raise ValueError(f"target is not a directory: {target}")
    for parent in target.parents:
        if parent.exists() and not parent.is_dir():
            raise ValueError(f"target ancestor is not a directory: {parent}")
    if names is None:
        if not skills_dir.is_dir():
            raise ValueError(f"missing skills directory: {skills_dir}")
        names = sorted(item.name for item in skills_dir.iterdir() if item.is_dir() or is_link_or_reparse(item))
    names = list(dict.fromkeys(names))
    if not names:
        raise ValueError("no skills selected")
    plan = []
    for name in names:
        if not valid_name(name):
            raise ValueError(f"invalid skill name: {name!r}; use kebab-case shorter than 64 characters")
        source = skills_dir / name
        destination = target / name
        inspect_source(source)
        if target == source or target.is_relative_to(source):
            raise ValueError(f"target must not be inside a selected source skill: {source}")
        if os.path.lexists(destination):
            raise ValueError(f"conflict: destination already exists; nothing was installed: {destination}")
        plan.append((source, destination))
    return plan


def apply_plan(target: Path, plan: list[tuple[Path, Path]]) -> None:
    reject_link_ancestors(target)
    target.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    # Stage every complete source before claiming any destination folder.
    with tempfile.TemporaryDirectory(prefix=".agent-skills-install-", dir=target) as staging:
        staging_path = Path(staging)
        for source, _ in plan:
            inspect_source(source)
            shutil.copytree(source, staging_path / source.name)
        reject_link_ancestors(target)
        try:
            # Exclusive creation refuses even an empty folder that appeared since planning.
            for _, destination in plan:
                destination.mkdir()
                created.append(destination)
            for source, destination in plan:
                shutil.copytree(staging_path / source.name, destination, dirs_exist_ok=True)
        except Exception:
            for destination in reversed(created):
                if not is_link_or_reparse(destination):
                    shutil.rmtree(destination)
            raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path, help="destination skills directory (no default home-directory writes)")
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--skill", action="append", help="skill name; may be repeated")
    selection.add_argument("--all", action="store_true", help="select every skill in this repository")
    parser.add_argument("--apply", action="store_true", help="copy files; without this flag only print the plan")
    args = parser.parse_args()
    try:
        raw_target = args.target.expanduser()
        if not raw_target.is_absolute():
            raw_target = Path.cwd() / raw_target
        # Inspect original components before abspath removes '..'; otherwise
        # a link/../ segment could hide a symbolic link or Windows junction.
        reject_link_ancestors(raw_target)
        target = Path(os.path.abspath(raw_target))
        reject_link_ancestors(target)
        repo = Path(__file__).absolute().parents[1]
        plan = build_plan(repo, target, None if args.all else args.skill)
        print("APPLY" if args.apply else "DRY RUN (no files will be changed)")
        for source, destination in plan:
            print(f"  {source} -> {destination}")
        if args.apply:
            apply_plan(target, plan)
            print(f"Installed {len(plan)} skill(s).")
        else:
            print("Add --apply to copy these complete skill directories.")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
