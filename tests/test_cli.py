from __future__ import annotations

import json
from pathlib import Path

from salt.cli import main


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
