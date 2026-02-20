from dataclasses import dataclass, field
from typing import Any
import random


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

    result.append(
        TestCase(
            name="is_adult() < '15'",
            func="is_adult",
            inputs=["15"],
            expected_return=False
        )
    )

    result.append(
        TestCase(
            name="is_adult() < '18'",
            func="is_adult",
            inputs=["18"],
            expected_return=True
        )
    )

    result.append(
        TestCase(
            name="is_prime(2)", func="is_prime", expected_return=True, args=(2,)
        )
    )
    result.append(
        TestCase(
            name="is_prime(3)", func="is_prime", expected_return=True, args=(3,)
        )
    )
    result.append(
        TestCase(
            name="is_prime(4)", func="is_prime", expected_return=False, args=(4,)
        )
    )
    result.append(
        TestCase(
            name="is_prime(5)", func="is_prime", expected_return=True, args=(5,)
        )
    )

    PRIMES = [
        7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97]

    random_test_amount: int = 7
    candidates: list[int] = []
    chosen_primes = random.choices([p for p in PRIMES if p >= 6], k=3)
    chosen_composites = random.choices([c for c in range(6, 97) if c not in PRIMES], k=random_test_amount - 3)

    candidates = chosen_primes + chosen_composites
    random.shuffle(candidates)

    for i in range(random_test_amount):
        result.append(
            TestCase(
                name=f"is_prime({candidates[i]}) random",
                func="is_prime",
                expected_return=candidates[i] in PRIMES,
                args=(candidates[i],)
            )
        )

    result.append(
        TestCase(
            name="is_prime(0) edge case", func="is_prime", expected_return=False, args=(0,)
        )
    )
    result.append(
        TestCase(
            name="is_prime(1) edge case", func="is_prime", expected_return=False, args=(1,)
        )
    )
    result.append(
        TestCase(
            name="is_prime(-1) edge case", func="is_prime", expected_return=False, args=(-1,)
        )
    )
    large_prime = 3400470137
    result.append(
        TestCase(
            name="is_prime() efficiency",
            func="is_prime",
            expected_return=True,
            args=(large_prime,)
        )
    )

    return result


def generate_bonus() -> list[TestCase]:
    result: list[TestCase] = []
    return result
