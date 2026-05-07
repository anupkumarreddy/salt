from __future__ import annotations

import re

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


ASSIGNMENT_EQ_PATTERN = re.compile(r"(?<![<>=!])=(?!=)")


class AlwaysFfNonblockingRule(Rule):
    rule_id = "SV003"
    name = "always_ff_nonblocking"
    description = "Require nonblocking assignments in always_ff blocks."
    default_severity = "error"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        violations: list[Violation] = []
        for block in source_file.blocks:
            if block.kind != "always_ff":
                continue
            for offset, line in enumerate(block.text.splitlines(), start=0):
                match = ASSIGNMENT_EQ_PATTERN.search(line)
                if not match:
                    continue
                if "==" in line or "!=" in line or ">=" in line or "<=" in line:
                    continue
                violations.append(
                    self.make_violation(
                        source_file,
                        block.start_line + offset,
                        "always_ff should use nonblocking assignments ('<=')",
                        column=match.start() + 1,
                        config=config,
                    )
                )
        return violations
