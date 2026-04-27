from __future__ import annotations

import re

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


CLASS_BLOCK_PATTERN = re.compile(
    r"^\s*class\s+([A-Za-z_]\w*)\b.*?\bendclass\b", re.MULTILINE | re.DOTALL
)


class UvmFactoryMacroRule(Rule):
    rule_id = "UVM001"
    name = "uvm_factory_macro"
    description = "Require UVM factory registration macros inside classes."
    default_severity = "warning"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        violations: list[Violation] = []
        for match in CLASS_BLOCK_PATTERN.finditer(source_file.clean_text):
            class_name = match.group(1)
            block_text = match.group(0)
            if "uvm_" not in block_text:
                continue
            if re.search(r"`uvm_(component|object)_utils\b", block_text):
                continue
            line = source_file.clean_text.count("\n", 0, match.start()) + 1
            violations.append(
                self.make_violation(
                    source_file,
                    line,
                    f"UVM class '{class_name}' is missing a factory registration macro",
                )
            )
        return violations
