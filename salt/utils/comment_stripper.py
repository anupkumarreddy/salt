from __future__ import annotations


def strip_comments(text: str) -> str:
    """Remove // and /* */ comments while preserving line structure."""
    result: list[str] = []
    i = 0
    in_block_comment = False
    in_string = False
    string_delimiter = ""
    length = len(text)

    while i < length:
        char = text[i]
        next_char = text[i + 1] if i + 1 < length else ""

        if in_block_comment:
            if char == "*" and next_char == "/":
                in_block_comment = False
                result.extend("  ")
                i += 2
                continue
            result.append("\n" if char == "\n" else " ")
            i += 1
            continue

        if in_string:
            result.append(char)
            if char == "\\" and i + 1 < length:
                result.append(text[i + 1])
                i += 2
                continue
            if char == string_delimiter:
                in_string = False
                string_delimiter = ""
            i += 1
            continue

        if char in {'"', "'"}:
            in_string = True
            string_delimiter = char
            result.append(char)
            i += 1
            continue

        if char == "/" and next_char == "/":
            result.extend("  ")
            i += 2
            while i < length and text[i] != "\n":
                result.append(" ")
                i += 1
            continue

        if char == "/" and next_char == "*":
            in_block_comment = True
            result.extend("  ")
            i += 2
            continue

        result.append(char)
        i += 1

    return "".join(result)
