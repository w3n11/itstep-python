from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class TestCase:
    name: str
    func: str
    inputs: list[str] = field(default_factory=list)
    expected_print: str | None = None
    expected_return: Any | Callable[[Any], bool] = None
    args: tuple = ()
    kwargs: dict | None = None
    timeout: float = 2.0
    iterations: int = 1
    expected_exception: type[Exception] | None = None


def generate() -> list[TestCase]:
    result: list[TestCase] = []
    return result


def generate_bonus() -> list[TestCase]:
    result: list[TestCase] = []
    return result
