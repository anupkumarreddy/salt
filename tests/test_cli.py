from __future__ import annotations

import json
from pathlib import Path

from salt.cli import main
from salt.config import load_config, VALID_SEVERITIES


def test_cli_returns_success_for_clean_file(tmp_path: Path, capsys) -> None:
    source = tmp_path / "good_module.sv"
    source.write_text(
        "\n".join(
            [
                "`default_nettype none",
                "module good_module;",
                "  timeunit 1ns;",
                "  timeprecision 1ps;",
                "endmodule : good_module",
                "",
            ]
        ),
        encoding="utf-8",
    )

    exit_code = main(["check", str(source), "--format", "json"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert json.loads(captured.out) == []
    assert captured.err == ""


def test_cli_reports_demo_violations_as_json(capsys) -> None:
    exit_code = main(
        [
            "check",
            "examples/demo",
            "--config",
            "examples/salt.yaml",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    violations = json.loads(captured.out)
    rule_ids = {violation["rule_id"] for violation in violations}

    assert exit_code == 1
    assert {"NAME001", "STYLE001", "SV001"}.issubset(rule_ids)
    assert captured.err == ""


def test_severity_override_from_yaml(tmp_path: Path, capsys) -> None:
    """YAML severity should override the rule's default_severity."""
    source = tmp_path / "bad_module.sv"
    source.write_text(
        "module BadModule;\nendmodule\n",
        encoding="utf-8",
    )

    config = tmp_path / "salt.yaml"
    config.write_text(
        "rules:\n"
        "  module_name:\n"
        "    enabled: true\n"
        "    severity: info\n"
        "  no_tabs:\n"
        "    enabled: true\n"
        "    severity: error\n"
    )

    exit_code = main(["check", str(source), "--config", str(config), "--format", "json"])

    captured = capsys.readouterr()
    violations = json.loads(captured.out)

    name_violations = [v for v in violations if v["rule_id"] == "NAME001"]
    assert len(name_violations) == 1
    assert name_violations[0]["severity"] == "info"


def test_default_severity_when_not_in_yaml(tmp_path: Path, capsys) -> None:
    """When severity is not specified in YAML, default_severity is used."""
    source = tmp_path / "bad_module.sv"
    source.write_text("module BadModule;\nendmodule\n", encoding="utf-8")

    # Config without severity for module_name
    config = tmp_path / "salt.yaml"
    config.write_text(
        "rules:\n"
        "  module_name:\n"
        "    enabled: true\n"
        # no severity key
    )

    exit_code = main(["check", str(source), "--config", str(config), "--format", "json"])

    captured = capsys.readouterr()
    violations = json.loads(captured.out)

    name_violations = [v for v in violations if v["rule_id"] == "NAME001"]
    assert len(name_violations) == 1
    assert name_violations[0]["severity"] == "error"  # default_severity from rule class


def test_invalid_severity_raises_error(tmp_path: Path) -> None:
    """Invalid severity values in YAML should raise ValueError."""
    source = tmp_path / "module.sv"
    source.write_text("module my_module; endmodule : my_module\n", encoding="utf-8")

    config = tmp_path / "salt.yaml"
    config.write_text(
        "rules:\n"
        "  module_name:\n"
        "    enabled: true\n"
        "    severity: critical\n"  # invalid
    )

    try:
        main(["check", str(source), "--config", str(config), "--format", "json"])
        assert False, "Expected ValueError for invalid severity"
    except ValueError as e:
        assert "Invalid severity 'critical'" in str(e)
        assert "module_name" in str(e)
