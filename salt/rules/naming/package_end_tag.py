from __future__ import annotations

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule
from salt.rules.naming.end_tag_helpers import check_named_end_tag


class PackageEndTagRule(Rule):
    rule_id = "NAME007"
    name = "package_end_tag"
    description = "Require package end tags to be declared and match the package name."
    default_severity = "error"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        return check_named_end_tag(
            rule=self,
            source_file=source_file,
            config=config,
            declaration_kind="package",
            end_keyword="endpackage",
            display_name="Package",
        )
