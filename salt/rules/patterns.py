from __future__ import annotations

from dataclasses import dataclass
import re

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


@dataclass(frozen=True, slots=True)
class PatternRuleSpec:
    rule_id: str
    name: str
    description: str
    message: str
    pattern: str
    severity: str = "warning"
    mode: str = "forbidden_line"
    required_pattern: str | None = None
    flags: int = re.MULTILINE


class PatternRule(Rule):
    spec: PatternRuleSpec

    @property
    def rule_id(self) -> str:
        return self.spec.rule_id

    @property
    def name(self) -> str:
        return self.spec.name

    @property
    def description(self) -> str:
        return self.spec.description

    @property
    def default_severity(self) -> str:
        return self.spec.severity

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        if self.spec.mode == "required_file_if":
            return self._check_required_file_if(source_file, config)
        if self.spec.mode == "forbidden_file":
            return self._check_forbidden_file(source_file, config)
        return self._check_forbidden_line(source_file, config)

    def _check_forbidden_line(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        violations: list[Violation] = []
        pattern = re.compile(self.spec.pattern)
        for line_number, line in enumerate(source_file.lines, start=1):
            match = pattern.search(line)
            if match:
                violations.append(
                    self.make_violation(source_file, line_number, self.spec.message, column=match.start() + 1, config=config)
                )
        return violations

    def _check_required_file_if(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        trigger = re.compile(self.spec.pattern, self.spec.flags)
        required = re.compile(self.spec.required_pattern or r"$^", self.spec.flags)
        violations: list[Violation] = []
        for match in trigger.finditer(source_file.clean_text):
            if required.search(source_file.clean_text):
                continue
            line = source_file.clean_text.count("\n", 0, match.start()) + 1
            violations.append(self.make_violation(source_file, line, self.spec.message, column=1, config=config))
            break
        return violations

    def _check_forbidden_file(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        pattern = re.compile(self.spec.pattern, self.spec.flags)
        violations: list[Violation] = []
        for match in pattern.finditer(source_file.clean_text):
            line = source_file.clean_text.count("\n", 0, match.start()) + 1
            column = match.start() - source_file.clean_text.rfind("\n", 0, match.start())
            violations.append(self.make_violation(source_file, line, self.spec.message, column=column, config=config))
        return violations


def build_pattern_rule_class(spec: PatternRuleSpec) -> type[PatternRule]:
    class_name = "".join(part.capitalize() for part in spec.name.split("_")) + "Rule"
    return type(class_name, (PatternRule,), {"spec": spec})
