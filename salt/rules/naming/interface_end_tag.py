from __future__ import annotations

from salt.config import SaltConfig
from salt.models import SourceFile, Violation
from salt.rules.base import Rule
from salt.rules.naming.end_tag_helpers import check_named_end_tag


class InterfaceEndTagRule(Rule):
    rule_id = "NAME006"
    name = "interface_end_tag"
    description = "Require interface end tags to be declared and match the interface name."
    default_severity = "error"

    def check(self, source_file: SourceFile, config: SaltConfig) -> list[Violation]:
        return check_named_end_tag(
            rule=self,
            source_file=source_file,
            config=config,
            declaration_kind="interface",
            end_keyword="endinterface",
            display_name="Interface",
        )
