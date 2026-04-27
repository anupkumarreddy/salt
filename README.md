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
salt check . --log-level info
```

You can also run SALT directly as a module:

```bash
python -m salt check .
```

SALT writes lint results to `stdout`. Diagnostic logging is formatted and emitted to `stderr`, so JSON and text reports remain clean. Use `--log-level debug` or `--log-level info` when you want pipeline visibility.

## Run The Demo

The repository includes a small demo under `examples/demo`.

Run it with:

```bash
./.venv/bin/python -m salt check examples/demo --config examples/salt.yaml
```

Sample output:

```text
examples/demo/axiDrv.svh:1:1      : error   : NAME004  : Class name 'axiDrv' does not match required pattern
examples/demo/axiDrv.svh:1:1      : warning : UVM001   : UVM class 'axiDrv' is missing a factory registration macro
examples/demo/axiDrv.svh:1:1      : warning : UVM002   : Class 'axiDrv' should end with '_driver'
examples/demo/bad_example.sv:1:1  : error   : NAME001  : Module name 'BadModule' does not match required pattern
examples/demo/bad_example.sv:2:1  : warning : STYLE001 : Tab found
examples/demo/bad_example.sv:2:10 : warning : STYLE002 : Trailing whitespace found
examples/demo/bad_example.sv:5:5  : error   : SV003    : always_ff should use nonblocking assignments ('<=')
examples/demo/bad_example.sv:9:5  : error   : SV004    : always_comb should use blocking assignments ('=')
examples/demo/bad_example.sv:12:1 : error   : SV001    : Usage of 'casex' is not allowed
examples/demo/bad_example.sv:12:1 : error   : SV002    : case missing default
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
