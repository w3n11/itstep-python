import random  # noqa: F401
from typing import Any  # noqa: F401
from test import TestCase, Procedure, NewInstance  # noqa: F401 # type: ignore


def generate(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)

    result: list[TestCase] = [
        TestCase(
            id=(1, 0),
            name="ExceptionRaiser existuje",
            func=TestCase.test_class_init,
            args=(
                "ExceptionRaiser", tuple()
            ),
            expected_return=True
        ),
        TestCase(
            id=(1, 1),
            name="Raise ArithmeticError",
            func=TestCase.test_class,
            args=(
                "ExceptionRaiser", Procedure()
                .add("raise_arithmetic_error", tuple())
            ),
            expected_exception=ValueError
        )
    ]
    return result


def generate_bonus(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)
    result: list[TestCase] = []
    return result
