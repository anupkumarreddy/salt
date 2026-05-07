from __future__ import annotations

import re

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


CLASS_EXTENDS_PATTERN = re.compile(
    r"^\s*class\s+([A-Za-z_]\w*)\s+extends\s+([A-Za-z_]\w*)\b", re.MULTILINE
)

EXPECTED_SUFFIXES = {
    "uvm_driver": "_driver",
    "uvm_monitor": "_monitor",
    "uvm_sequencer": "_sequencer",
    "uvm_agent": "_agent",
    "uvm_env": "_env",
}


class ComponentSuffixRule(Rule):
    rule_id = "UVM002"
    name = "component_suffix"
    description = "Enforce suffixes for common UVM component types."
    default_severity = "warning"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        violations: list[Violation] = []
        for match in CLASS_EXTENDS_PATTERN.finditer(source_file.clean_text):
            class_name = match.group(1)
            parent_name = match.group(2)
            expected_suffix = _infer_suffix(parent_name)
            if expected_suffix and not class_name.endswith(expected_suffix):
                line = source_file.clean_text.count("\n", 0, match.start()) + 1
                violations.append(
                    self.make_violation(
                        source_file,
                        line,
                        f"Class '{class_name}' should end with '{expected_suffix}'",
                        config=config,
                    )
                )
        return violations


def _infer_suffix(parent_name: str) -> str | None:
    for prefix, suffix in EXPECTED_SUFFIXES.items():
        if parent_name.startswith(prefix):
            return suffix
    return None
