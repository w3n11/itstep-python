from dataclasses import dataclass, field
import random
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

    result.append(
        TestCase(
            name="hello() < \"John\"",
            func="hello",
            inputs=["John"],
            expected_print="Hello John!\n"
        )
    )

    result.append(
        TestCase(
            name="hello() < \"Jane\"",
            func="hello",
            inputs=["Jane"],
            expected_print="Hello Jane!\n"
        )
    )

    result.append(
        TestCase(
            name="hello() < \"World\"",
            func="hello",
            inputs=["World"],
            expected_print="Hello World!\n"
        )
    )

    result.append(
        TestCase(
            name="hello() < \"\"",
            func="hello",
            inputs=[""],
            expected_print="Hello everyone!\n"
        )
    )

    result.append(
        TestCase(
            name="age_verification(21) < \"18\"",
            func="age_verification",
            inputs=["18"],
            expected_return=False,
            args=(21,)
        )
    )

    result.append(
        TestCase(
            name="age_verification(21) < \"21\"",
            func="age_verification",
            inputs=["21"],
            expected_return=True,
            args=(21,)
        )
    )

    result.append(
        TestCase(
            name="age_verification(21) < \"35\"",
            func="age_verification",
            inputs=["35"],
            expected_return=True,
            args=(21,)
        )
    )

    random_test_amount: int = 7
    for i in range(random_test_amount):
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        result.append(
            TestCase(
                name=f"age_verification({a}) < \"{b}\" (random)",
                func="age_verification",
                inputs=[str(b)],
                expected_return=b >= a,
                args=(a,)
            )
        )

    result.append(
        TestCase(
            name="dice_roll()",
            func="dice_roll",
            iterations=20,
            expected_return=lambda results: (
                all(isinstance(x, int) and 1 <= x <= 6 for x in results)
                and len(set(results)) > 1
            )
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
                name=f"is_prime({candidates[i]}) (random)",
                func="is_prime",
                expected_return=candidates[i] in PRIMES,
                args=(candidates[i],)
            )
        )

    result.append(
        TestCase(
            name="is_prime(0) (edge case)", func="is_prime", expected_return=False, args=(0,)
        )
    )
    result.append(
        TestCase(
            name="is_prime(1) (edge case)", func="is_prime", expected_return=False, args=(1,)
        )
    )
    result.append(
        TestCase(
            name="is_prime(-1) (edge case)", func="is_prime", expected_return=False, args=(-1,)
        )
    )

    return result


def generate_bonus() -> list[TestCase]:
    result: list[TestCase] = []
    result.append(
        TestCase(
            name="hello() < \"  \"",
            func="hello",
            expected_print="Hello everyone!\n",
            inputs=["  "]
        )
    )

    result.append(
        TestCase(
            name="age_verification(15) < \"fifteen\"",
            func="age_verification",
            expected_return=False,
            inputs=["fifteen"],
            args=(15,)
        )
    )

    result.append(
        TestCase(
            name="age_verification(15) < \"\"",
            func="age_verification",
            expected_return=False,
            inputs=[""],
            args=(15,)
        )
    )

    result.append(
        TestCase(
            name="dice_roll() (fair rolls)",
            func="dice_roll",
            iterations=6000,
            expected_return=lambda results: all(800 < results.count(i) < 1200 for i in range(1, 7)),
            timeout=5.0
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
