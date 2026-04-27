from __future__ import annotations

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


class MaxLineLengthRule(Rule):
    rule_id = "STYLE003"
    name = "max_line_length"
    description = "Enforce a maximum line length."
    default_severity = "warning"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        limit = int(config.rule_config(self.name).get("max", 100))
        violations: list[Violation] = []
        for line_number, line in enumerate(source_file.raw_lines, start=1):
            if len(line) > limit:
                violations.append(
                    self.make_violation(
                        source_file,
                        line_number,
                        f"Line exceeds maximum length of {limit}",
                        column=limit + 1,
                    )
                )
        return violations
