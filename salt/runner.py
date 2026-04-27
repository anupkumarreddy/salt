from __future__ import annotations

from dataclasses import dataclass
import logging

from salt.config import SaltConfig, load_config
from salt.models import SourceFile, Violation
from salt.registry import build_rules
from salt.scanner import scan_file
from salt.utils.file_finder import discover_files

LOGGER = logging.getLogger("salt.runner")


@dataclass(slots=True)
class RunResult:
    config: SaltConfig
    files: list[SourceFile]
    violations: list[Violation]


def run(paths: list[str], config_path: str | None = None) -> RunResult:
    LOGGER.info("Running SALT on %d path(s)", len(paths))
    config = load_config(config_path)
    discovered_paths = discover_files(paths, config.include, config.exclude)
    LOGGER.info("Scanning %d discovered file(s)", len(discovered_paths))
    source_files = [scan_file(path) for path in discovered_paths]

    rules = [rule for rule in build_rules() if config.is_rule_enabled(rule.name)]
    LOGGER.info("Applying %d enabled rule(s)", len(rules))
    violations: list[Violation] = []
    for source_file in source_files:
        LOGGER.debug("Applying rules to %s", source_file.relative_path)
        for rule in rules:
            rule_violations = rule.check(source_file, config)
            violations.extend(rule_violations)
            if rule_violations:
                LOGGER.debug(
                    "Rule %s reported %d violation(s) for %s",
                    rule.name,
                    len(rule_violations),
                    source_file.relative_path,
                )

    violations.sort(key=lambda item: (item.file, item.line, item.column, item.rule_id))
    LOGGER.info("Run finished with %d violation(s)", len(violations))
    return RunResult(config=config, files=source_files, violations=violations)


def run_for_paths(paths: list[str], config_path: str | None = None) -> list[Violation]:
    return run(paths, config_path).violations
