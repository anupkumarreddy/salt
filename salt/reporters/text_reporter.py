from __future__ import annotations

from salt.models import Violation


def render_text(violations: list[Violation]) -> str:
    lines = [
        (
            f"{violation.file}:{violation.line}:{violation.column}: "
            f"{violation.rule_id} {violation.severity}: {violation.message}"
        )
        for violation in violations
    ]
    return "\n".join(lines)
