from __future__ import annotations

import re

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


class NoCasexRule(Rule):
    rule_id = "SV001"
    name = "no_casex"
    description = "Disallow casex."
    default_severity = "error"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        violations: list[Violation] = []
        for line_number, line in enumerate(source_file.lines, start=1):
            match = re.search(r"\bcasex\b", line)
            if match:
                violations.append(
                    self.make_violation(source_file, line_number, "Usage of 'casex' is not allowed", match.start() + 1, config=config)
                )
        return violations
