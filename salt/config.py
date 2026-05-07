from __future__ import annotations

from dataclasses import dataclass, field
import logging
from pathlib import Path
from typing import Any

import yaml

LOGGER = logging.getLogger("salt.config")


DEFAULT_INCLUDE = ["**/*.sv", "**/*.svh"]
DEFAULT_EXCLUDE = ["**/build/**", "**/sim/**"]
VALID_SEVERITIES = frozenset({"error", "warning", "info"})

DEFAULT_RULES: dict[str, dict[str, Any]] = {
    "no_tabs": {"enabled": True},
    "trailing_whitespace": {"enabled": True},
    "max_line_length": {"enabled": True, "max": 100},
    "module_name": {"enabled": True, "pattern": r"^[a-z][a-z0-9_]*$"},
    "interface_name": {"enabled": True, "pattern": r"^[a-z][a-z0-9_]*_if$"},
    "package_name": {"enabled": True, "pattern": r"^[a-z][a-z0-9_]*_pkg$"},
    "class_name": {"enabled": True, "pattern": r"^[a-z][a-z0-9_]*$"},
    "module_end_tag": {"enabled": True},
    "interface_end_tag": {"enabled": True},
    "package_end_tag": {"enabled": True},
    "class_end_tag": {"enabled": True},
    "no_casex": {"enabled": True},
    "case_default": {"enabled": True},
    "always_ff_nonblocking": {"enabled": True},
    "always_comb_blocking": {"enabled": True},
    "uvm_factory_macro": {"enabled": True},
    "component_suffix": {"enabled": True},
}


@dataclass(slots=True)
class SaltConfig:
    include: list[str] = field(default_factory=lambda: list(DEFAULT_INCLUDE))
    exclude: list[str] = field(default_factory=lambda: list(DEFAULT_EXCLUDE))
    rules: dict[str, dict[str, Any]] = field(
        default_factory=lambda: {key: value.copy() for key, value in DEFAULT_RULES.items()}
    )

    def rule_config(self, name: str) -> dict[str, Any]:
        rule_data = self.rules.get(name, {})
        base = DEFAULT_RULES.get(name, {}).copy()
        base.update(rule_data)
        return base

    def is_rule_enabled(self, name: str) -> bool:
        return bool(self.rule_config(name).get("enabled", True))


def load_config(config_path: str | None = None) -> SaltConfig:
    config = SaltConfig()
    if not config_path:
        LOGGER.debug("No config path provided; using default configuration")
        return config

    path = Path(config_path)
    LOGGER.info("Loading config from %s", path)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    if "include" in data:
        config.include = list(data["include"] or [])
    if "exclude" in data:
        config.exclude = list(data["exclude"] or [])
    if "rules" in data:
        merged_rules = {key: value.copy() for key, value in DEFAULT_RULES.items()}
        for rule_name, rule_config in (data["rules"] or {}).items():
            base = merged_rules.get(rule_name, {}).copy()
            base.update(rule_config or {})
            if "severity" in base:
                severity = base["severity"]
                if severity not in VALID_SEVERITIES:
                    raise ValueError(
                        f"Invalid severity '{severity}' for rule '{rule_name}'. "
                        f"Valid values: {', '.join(sorted(VALID_SEVERITIES))}"
                    )
            merged_rules[rule_name] = base
        config.rules = merged_rules

    LOGGER.debug(
        "Loaded config: include=%d exclude=%d rules=%d",
        len(config.include),
        len(config.exclude),
        len(config.rules),
    )
    return config
