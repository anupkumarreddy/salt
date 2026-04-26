from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(slots=True)
class Declaration:
    kind: str
    name: str
    line: int


@dataclass(slots=True)
class Block:
    kind: str
    start_line: int
    end_line: int
    text: str


@dataclass(slots=True)
class SourceFile:
    path: str
    raw_text: str
    clean_text: str
    lines: list[str]
    declarations: list[Declaration] = field(default_factory=list)
    blocks: list[Block] = field(default_factory=list)

    @property
    def raw_lines(self) -> list[str]:
        return self.raw_text.splitlines()

    @property
    def relative_path(self) -> str:
        path = Path(self.path)
        try:
            return path.relative_to(Path.cwd()).as_posix()
        except ValueError:
            return path.as_posix()


@dataclass(slots=True)
class Violation:
    rule_id: str
    rule_name: str
    file: str
    line: int
    column: int
    message: str
    severity: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
