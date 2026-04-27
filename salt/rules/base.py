from __future__ import annotations

from abc import ABC, abstractmethod

from salt.config import SaltConfig
from salt.models import SourceFile, Violation


class Rule(ABC):
    rule_id: str
    name: str
    description: str
    default_severity: str = "warning"

    @abstractmethod
    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        raise NotImplementedError

    def make_violation(
        self,
        source_file: SourceFile,
        line: int,
        message: str,
        column: int = 1,
        severity: str | None = None,
    ) -> Violation:
        return Violation(
            rule_id=self.rule_id,
            rule_name=self.name,
            file=source_file.relative_path,
            line=line,
            column=column,
            message=message,
            severity=severity or self.default_severity,
        )
