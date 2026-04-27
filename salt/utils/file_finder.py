from __future__ import annotations

import logging
from pathlib import Path

LOGGER = logging.getLogger("salt.finder")


def discover_files(paths: list[str], include: list[str], exclude: list[str]) -> list[Path]:
    found: set[Path] = set()
    excluded: set[Path] = set()

    for raw_path in paths:
        base_path = Path(raw_path)
        LOGGER.debug("Inspecting path %s", base_path)
        if base_path.is_file():
            found.add(base_path.resolve())
            continue
        if not base_path.exists():
            LOGGER.warning("Path does not exist: %s", base_path)
            continue

        for pattern in include:
            for match in base_path.glob(pattern):
                if match.is_file():
                    found.add(match.resolve())

        for pattern in exclude:
            for match in base_path.glob(pattern):
                if match.is_file():
                    excluded.add(match.resolve())

    discovered = sorted(path for path in found if path not in excluded)
    LOGGER.info(
        "Discovered %d file(s) from %d input path(s)",
        len(discovered),
        len(paths),
    )
    return discovered
