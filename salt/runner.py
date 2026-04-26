from __future__ import annotations

from dataclasses import dataclass
from salt.config import SaltConfig, load_config
from salt.models import SourceFile, Violation
from salt.registry import build_rules
from salt.scanner import scan_file
from salt.utils.file_finder import discover_files


@dataclass(slots=True)
class RunResult:
    config: SaltConfig
    files: list[SourceFile]
    violations: list[Violation]


def run(paths: list[str], config_path: str | None = None) -> RunResult:
    config = load_config(config_path)
    discovered_paths = discover_files(paths, config.include, config.exclude)
    source_files = [scan_file(path) for path in discovered_paths]

    rules = [rule for rule in build_rules() if config.is_rule_enabled(rule.name)]
    violations: list[Violation] = []
    for source_file in source_files:
        for rule in rules:
            violations.extend(rule.check(source_file, config))

    violations.sort(key=lambda item: (item.file, item.line, item.column, item.rule_id))
    return RunResult(config=config, files=source_files, violations=violations)


def run_for_paths(paths: list[str], config_path: str | None = None) -> list[Violation]:
    return run(paths, config_path).violations
