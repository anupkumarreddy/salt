from __future__ import annotations

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


class NoTabsRule(Rule):
    rule_id = "STYLE001"
    name = "no_tabs"
    description = "Disallow tab characters."
    default_severity = "warning"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        violations: list[Violation] = []
        for line_number, line in enumerate(source_file.raw_lines, start=1):
            column = line.find("\t")
            if column >= 0:
                violations.append(self.make_violation(source_file, line_number, "Tab found", column=column + 1, config=config))
        return violations
