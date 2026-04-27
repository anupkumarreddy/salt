from __future__ import annotations

from pathlib import Path


def discover_files(paths: list[str], include: list[str], exclude: list[str]) -> list[Path]:
    found: set[Path] = set()
    excluded: set[Path] = set()

    for raw_path in paths:
        base_path = Path(raw_path)
        if base_path.is_file():
            found.add(base_path.resolve())
            continue
        if not base_path.exists():
            continue

        for pattern in include:
            for match in base_path.glob(pattern):
                if match.is_file():
                    found.add(match.resolve())

        for pattern in exclude:
            for match in base_path.glob(pattern):
                if match.is_file():
                    excluded.add(match.resolve())

    return sorted(path for path in found if path not in excluded)
