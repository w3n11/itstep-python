from dataclasses import dataclass, field
from typing import Any


@dataclass
class TestCase:
    name: str
    func: str
    inputs: list[str] = field(default_factory=list)
    expected_print: str | None = None
    expected_return: Any = None
    args: tuple = ()
    kwargs: dict | None = None
    timeout: float = 2.0


def generate() -> list[TestCase]:
    result: list[TestCase] = []
    return result


def generate_bonus() -> list[TestCase]:
    result: list[TestCase] = []
    return result
