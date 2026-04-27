from __future__ import annotations

import re

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


class CaseDefaultRule(Rule):
    rule_id = "SV002"
    name = "case_default"
    description = "Require a default branch in every case block."
    default_severity = "error"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        violations: list[Violation] = []
        for block in source_file.blocks:
            if block.kind != "case":
                continue
            if not re.search(r"\bdefault\s*:", block.text):
                violations.append(
                    self.make_violation(source_file, block.start_line, "case missing default")
                )
        return violations
