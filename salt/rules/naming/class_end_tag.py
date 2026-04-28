from __future__ import annotations

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule
from salt.rules.naming.end_tag_helpers import check_named_end_tag


class ClassEndTagRule(Rule):
    rule_id = "NAME008"
    name = "class_end_tag"
    description = "Require class end tags to be declared and match the class name."
    default_severity = "error"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        return check_named_end_tag(
            rule=self,
            source_file=source_file,
            config=config,
            declaration_kind="class",
            end_keyword="endclass",
            display_name="Class",
        )
