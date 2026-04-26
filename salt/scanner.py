from __future__ import annotations

import re
from pathlib import Path

from salt.models import Block, Declaration, SourceFile
from salt.utils.comment_stripper import strip_comments


DECLARATION_PATTERNS: dict[str, re.Pattern[str]] = {
    "module": re.compile(r"^\s*module\s+([A-Za-z_]\w*)\b", re.MULTILINE),
    "interface": re.compile(r"^\s*interface\s+([A-Za-z_]\w*)\b", re.MULTILINE),
    "package": re.compile(r"^\s*package\s+([A-Za-z_]\w*)\b", re.MULTILINE),
    "class": re.compile(r"^\s*class\s+([A-Za-z_]\w*)\b", re.MULTILINE),
}

TOKEN_PATTERN = re.compile(r"\b(always_ff|always_comb|begin|end|case[xz]?|endcase)\b")


def scan_file(path: Path) -> SourceFile:
    raw_text = path.read_text(encoding="utf-8")
    clean_text = strip_comments(raw_text)
    lines = clean_text.splitlines()

    return SourceFile(
        path=path.as_posix(),
        raw_text=raw_text,
        clean_text=clean_text,
        lines=lines,
        declarations=_extract_declarations(clean_text),
        blocks=_extract_blocks(clean_text),
    )


def _extract_declarations(text: str) -> list[Declaration]:
    declarations: list[Declaration] = []
    for kind, pattern in DECLARATION_PATTERNS.items():
        for match in pattern.finditer(text):
            declarations.append(
                Declaration(
                    kind=kind,
                    name=match.group(1),
                    line=text.count("\n", 0, match.start()) + 1,
                )
            )
    return sorted(declarations, key=lambda item: item.line)


def _extract_blocks(text: str) -> list[Block]:
    blocks: list[Block] = []
    lines = text.splitlines()

    for match in re.finditer(r"\balways_ff\b|\balways_comb\b", text):
        kind = match.group(0)
        start_line = text.count("\n", 0, match.start()) + 1
        start_index = _line_start_offset(lines, start_line)
        end_index = _find_always_block_end(text, match.start())
        end_line = text.count("\n", 0, end_index) + 1
        blocks.append(
            Block(
                kind=kind,
                start_line=start_line,
                end_line=end_line,
                text=text[start_index:end_index],
            )
        )

    case_stack: list[tuple[int, int]] = []
    for token_match in TOKEN_PATTERN.finditer(text):
        token = token_match.group(1)
        if token.startswith("case"):
            case_stack.append((token_match.start(), token_match.end()))
            continue
        if token == "endcase" and case_stack:
            start_index, _ = case_stack.pop()
            start_line = text.count("\n", 0, start_index) + 1
            end_line = text.count("\n", 0, token_match.end()) + 1
            blocks.append(
                Block(
                    kind="case",
                    start_line=start_line,
                    end_line=end_line,
                    text=text[start_index:token_match.end()],
                )
            )

    return sorted(blocks, key=lambda item: (item.start_line, item.kind))


def _find_always_block_end(text: str, start_index: int) -> int:
    remaining = text[start_index:]
    begin_match = re.search(r"\bbegin\b", remaining)
    semicolon_match = re.search(r";", remaining)

    if semicolon_match and (not begin_match or semicolon_match.start() < begin_match.start()):
        return start_index + semicolon_match.end()

    if not begin_match:
        return _line_end_index(text, start_index)

    block_start = start_index + begin_match.start()
    depth = 0
    for token_match in TOKEN_PATTERN.finditer(text, block_start):
        token = token_match.group(1)
        if token == "begin":
            depth += 1
        elif token == "end":
            depth -= 1
            if depth == 0:
                return token_match.end()

    return len(text)


def _line_start_offset(lines: list[str], line_number: int) -> int:
    if line_number <= 1:
        return 0
    return sum(len(line) + 1 for line in lines[: line_number - 1])


def _line_end_index(text: str, start_index: int) -> int:
    newline_index = text.find("\n", start_index)
    return len(text) if newline_index == -1 else newline_index
