from __future__ import annotations

import re

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


class ClassNameRule(Rule):
    rule_id = "NAME004"
    name = "class_name"
    description = "Enforce a naming convention for classes."
    default_severity = "error"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        pattern = re.compile(config.rule_config(self.name).get("pattern", r"^[a-z][a-z0-9_]*$"))
        violations: list[Violation] = []
        for declaration in source_file.declarations:
            if declaration.kind == "class" and not pattern.fullmatch(declaration.name):
                violations.append(
                    self.make_violation(
                        source_file,
                        declaration.line,
                        f"Class name '{declaration.name}' does not match required pattern",
                    )
                )
        return violations
