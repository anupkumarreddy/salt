from __future__ import annotations

import re

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


class InterfaceNameRule(Rule):
    rule_id = "NAME002"
    name = "interface_name"
    description = "Enforce a naming convention for interfaces."
    default_severity = "error"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        pattern = re.compile(config.rule_config(self.name).get("pattern", r"^[a-z][a-z0-9_]*_if$"))
        violations: list[Violation] = []
        for declaration in source_file.declarations:
            if declaration.kind == "interface" and not pattern.fullmatch(declaration.name):
                violations.append(
                    self.make_violation(
                        source_file,
                        declaration.line,
                        f"Interface name '{declaration.name}' does not match required pattern",
                    )
                )
        return violations
