from __future__ import annotations

import re

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


NONBLOCKING_PATTERN = re.compile(r"(?<!<)<=(?!=)")


class AlwaysCombBlockingRule(Rule):
    rule_id = "SV004"
    name = "always_comb_blocking"
    description = "Require blocking assignments in always_comb blocks."
    default_severity = "error"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        violations: list[Violation] = []
        for block in source_file.blocks:
            if block.kind != "always_comb":
                continue
            for offset, line in enumerate(block.text.splitlines(), start=0):
                match = NONBLOCKING_PATTERN.search(line)
                if match:
                    violations.append(
                        self.make_violation(
                            source_file,
                            block.start_line + offset,
                            "always_comb should use blocking assignments ('=')",
                            column=match.start() + 1,
                            config=config,
                        )
                    )
        return violations
