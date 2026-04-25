# SALT

SALT stands for **SystemVerilog Analysis & Linting Tool**.

SALT is a lightweight Python-based linter for SystemVerilog codebases. It is focused on style enforcement, naming conventions, and basic RTL/UVM best-practice checks. It is not a compiler and it is not intended to be a full syntax checker or parser.

## Goals

- Enforce coding style
- Enforce naming conventions
- Enforce basic RTL/UVM best practices
- Stay lightweight and fast
- Remain easy to configure and extend

## Features

- Python 3.11+
- `argparse` CLI
- YAML configuration via `PyYAML`
- Modular rule architecture
- Regex-based lightweight scanner
- Text and JSON reporting

## Current MVP Rules

- Style: `no_tabs`, `trailing_whitespace`, `max_line_length`
- Naming: `module_name`, `interface_name`, `package_name`, `class_name`
- SystemVerilog: `no_casex`, `case_default`, `always_ff_nonblocking`, `always_comb_blocking`
- UVM: `uvm_factory_macro`, `component_suffix`

## Install

```bash
python3 -m venv .venv
./.venv/bin/pip install -e .
```

## Usage

```bash
salt check <path>
salt check . --config salt.yaml
salt check ./tb ./rtl
salt check . --format json
```

You can also run SALT directly as a module:

```bash
python -m salt check .
```

## Configuration

Example `salt.yaml`:

```yaml
include:
  - "**/*.sv"
  - "**/*.svh"

exclude:
  - "**/build/**"
  - "**/sim/**"

rules:
  no_tabs:
    enabled: true

  max_line_length:
    enabled: true
    max: 100

  module_name:
    enabled: true
    pattern: "^[a-z][a-z0-9_]*$"
```

## Architecture

The SALT pipeline is:

1. Discover files
2. Scan files into a lightweight model
3. Apply enabled rules
4. Collect violations
5. Render output

Core modules live under [salt/](/Users/anupreddy/PycharmProjects/salt/salt).

## Status

This repository currently contains the MVP implementation of SALT with a modular foundation for adding new rules and reporters.
