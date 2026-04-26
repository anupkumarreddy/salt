from __future__ import annotations

from salt.rules.base import Rule
from salt.rules.naming.class_name import ClassNameRule
from salt.rules.naming.interface_name import InterfaceNameRule
from salt.rules.naming.module_name import ModuleNameRule
from salt.rules.naming.package_name import PackageNameRule
from salt.rules.style.max_line_length import MaxLineLengthRule
from salt.rules.style.no_tabs import NoTabsRule
from salt.rules.style.trailing_whitespace import TrailingWhitespaceRule
from salt.rules.sv.always_comb_blocking import AlwaysCombBlockingRule
from salt.rules.sv.always_ff_nonblocking import AlwaysFfNonblockingRule
from salt.rules.sv.case_default import CaseDefaultRule
from salt.rules.sv.no_casex import NoCasexRule
from salt.rules.uvm.component_suffix import ComponentSuffixRule
from salt.rules.uvm.factory_macro import UvmFactoryMacroRule


RULES: list[type[Rule]] = [
    NoTabsRule,
    TrailingWhitespaceRule,
    MaxLineLengthRule,
    ModuleNameRule,
    InterfaceNameRule,
    PackageNameRule,
    ClassNameRule,
    NoCasexRule,
    CaseDefaultRule,
    AlwaysFfNonblockingRule,
    AlwaysCombBlockingRule,
    UvmFactoryMacroRule,
    ComponentSuffixRule,
]


def build_rules() -> list[Rule]:
    return [rule_class() for rule_class in RULES]
