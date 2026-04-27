from __future__ import annotations

import json

from salt.models import Violation


def render_json(violations: list[Violation]) -> str:
    return json.dumps([violation.to_dict() for violation in violations], indent=2)
