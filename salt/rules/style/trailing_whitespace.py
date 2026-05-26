from __future__ import annotations

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


class TrailingWhitespaceRule(Rule):
    rule_id = "STYLE002"
    name = "trailing_whitespace"
    description = "Disallow trailing whitespace."
    default_severity = "warning"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        violations: list[Violation] = []
        for line_number, line in enumerate(source_file.raw_lines, start=1):
            stripped = line.rstrip(" \t")
            if stripped != line:
                violations.append(
                    self.make_violation(
                        source_file,
                        line_number,
                        "Trailing whitespace found",
                        column=len(stripped) + 1,
                        config=config,
                    )
                )
        return violations
