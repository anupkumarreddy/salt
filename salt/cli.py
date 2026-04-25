from __future__ import annotations

import argparse
from typing import Sequence

from salt.reporters.json_reporter import render_json
from salt.reporters.text_reporter import render_text
from salt.runner import run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="salt", description="SystemVerilog style linter.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="Run the linter.")
    check_parser.add_argument("paths", nargs="+", help="Files or directories to lint.")
    check_parser.add_argument("--config", help="Path to YAML config file.")
    check_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Reporter output format.",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "check":
        parser.error(f"Unsupported command: {args.command}")

    result = run(args.paths, config_path=args.config)
    output = render_json(result.violations) if args.format == "json" else render_text(result.violations)
    if output:
        print(output)
    return 1 if result.violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
