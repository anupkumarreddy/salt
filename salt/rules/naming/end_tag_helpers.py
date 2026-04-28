from __future__ import annotations

import re

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule


def check_named_end_tag(
    *,
    rule: Rule,
    source_file: SourceFile,
    config: SaltConfig,
    declaration_kind: str,
    end_keyword: str,
    display_name: str,
) -> list[Violation]:
    del config

    pattern = re.compile(
        rf"^\s*{declaration_kind}\s+([A-Za-z_]\w*)\b.*?\b{end_keyword}\b(?:\s*:\s*([A-Za-z_]\w*))?",
        re.MULTILINE | re.DOTALL,
    )

    violations: list[Violation] = []
    for match in pattern.finditer(source_file.clean_text):
        declared_name = match.group(1)
        end_name = match.group(2)
        line = source_file.clean_text.count("\n", 0, match.start()) + 1

        if end_name is None:
            violations.append(
                rule.make_violation(
                    source_file,
                    line,
                    f"{display_name} '{declared_name}' is missing a named {end_keyword} tag",
                )
            )
            continue

        if end_name != declared_name:
            violations.append(
                rule.make_violation(
                    source_file,
                    line,
                    (
                        f"{display_name} '{declared_name}' has mismatched {end_keyword} tag "
                        f"'{end_name}'"
                    ),
                )
            )

    return violations
