#!/usr/bin/env python3
import argparse
import pathlib
import re
import sys


def read_version(path: pathlib.Path) -> str:
    content = path.read_text(encoding="utf-8")
    section = None

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped.strip("[]")
            continue

        match = re.match(r'version\s*=\s*["\']([^"\']+)["\']', stripped)
        if match and section in ("project", "tool.poetry"):
            return match.group(1)

    raise ValueError(
        f"Could not find version in [project] or [tool.poetry] section of {path}"
    )


def write_version(path: pathlib.Path, target_version: str) -> None:
    content = path.read_text(encoding="utf-8")
    section = None
    found_section = False
    replaced = False
    lines = []

    for line in content.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped.strip("[]")

        if section in ("project", "tool.poetry"):
            found_section = True
            match = re.match(
                r'^(\s*version\s*=\s*["\'])([^"\']+)(["\']\s*)$',
                line.rstrip("\n"),
            )
            if match and not replaced:
                lines.append(f"{match.group(1)}{target_version}{match.group(3)}\n")
                replaced = True
                continue

        lines.append(line)

    if not found_section or not replaced:
        raise ValueError(
            f"Could not update version in [project] or [tool.poetry] section of {path}"
        )

    path.write_text("".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    read_parser = subparsers.add_parser("read")
    read_parser.add_argument("--file", required=True)

    write_parser = subparsers.add_parser("write")
    write_parser.add_argument("--file", required=True)
    write_parser.add_argument("--version", required=True)

    args = parser.parse_args()
    path = pathlib.Path(args.file)

    try:
        if args.command == "read":
            print(read_version(path))
            return 0

        write_version(path, args.version)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
