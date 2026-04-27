from __future__ import annotations

from salt.models import Violation


def render_text(violations: list[Violation]) -> str:
    if not violations:
        return ""

    locations = [f"{violation.file}:{violation.line}:{violation.column}" for violation in violations]
    location_width = max(len(location) for location in locations)
    rule_id_width = max(len(violation.rule_id) for violation in violations)
    severity_width = max(len(violation.severity) for violation in violations)

    lines = []
    for location, violation in zip(locations, violations):
        lines.append(
            f"{location:<{location_width}}"
            f" : {violation.severity:<{severity_width}}"
            f" : {violation.rule_id:<{rule_id_width}}"
            f" : "
            f"{violation.message}"
        )
    return "\n".join(lines)
