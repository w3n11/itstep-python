from dataclasses import dataclass, field
import random  # noqa: F401
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
    verify_print: Any | Callable[[Any], bool] = None
    max_calls: dict[str, int] = field(default_factory=dict)


def generate() -> list[TestCase]:
    result: list[TestCase] = []
    list_data = [
        (5, 0, 10),
        (8, 0, 100),
        (10, 0, 10_000),
        (10, -(10 ** 30), 10 ** 30),
        (15, 0, 1),
        (1_000, -10, 10)
    ]

    def create_validator(original_copy: list[int], passed_in_arg: list[int]) -> Callable[[Any], bool]:
        def validator(actual_return: Any) -> bool:
            if actual_return is None:
                return False
            if actual_return != sorted(original_copy):
                return False
            if passed_in_arg != original_copy:
                return False
            return True
        return validator

    for list_length, min_range, max_range in list_data:
        random_data = [random.randint(min_range, max_range) for _ in range(list_length)]
        original_copy = list(random_data)
        mutable_arg = list(random_data)

        result.append(
            TestCase(
                name=f"bubble_sort (délka {list_length})",
                func="bubble_sort",
                args=(mutable_arg,),
                expected_return=create_validator(original_copy, mutable_arg),
                timeout=5.0 if list_length == 1_000 else 2.0
            )
        )

    edge_cases = [
        ([], "prázdný seznam"),
        ([1, 2, 3, 4, 5], "již seřazený seznam"),
        ([5, 4, 3, 2, 1], "obráceně seřazený"),
        ([42, 42, 42, 42], "stejné hodnoty")
    ]

    for edge_data, desc in edge_cases:
        original_copy = list(edge_data)
        mutable_arg = list(edge_data)
        result.append(
            TestCase(
                name=f"bubble_sort ({desc})",
                func="bubble_sort",
                args=(mutable_arg,),
                expected_return=create_validator(original_copy, mutable_arg)
            )
        )

    return result


def generate_bonus() -> list[TestCase]:
    result: list[TestCase] = []
    to_search_short_odd_len = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    to_search_short_even_len = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result.extend([
        TestCase(
            name="linear_search první prvek",
            func="linear_search",
            args=(to_search_short_odd_len, 1),
            expected_return=True
        ),
        TestCase(
            name="linear_search prostřední prvek",
            func="linear_search",
            args=(to_search_short_odd_len, 5),
            expected_return=True
        ),
        TestCase(
            name="linear_search poslední prvek",
            func="linear_search",
            args=(to_search_short_odd_len, 9),
            expected_return=True
        ),
        TestCase(
            name="linear_search chybějící prvek",
            func="linear_search",
            args=(to_search_short_odd_len, 10),
            expected_return=False
        ),
        TestCase(
            name="linear_search chybějící prvek",
            func="linear_search",
            args=(to_search_short_odd_len, 0),
            expected_return=False
        )
    ])
    result.extend([
        TestCase(
            name="binary_search první prvek (lichá délka seznamu)",
            func="binary_search",
            args=(to_search_short_odd_len, 1),
            expected_return=True
        ),
        TestCase(
            name="binary_search prostřední prvek (lichá délka seznamu)",
            func="binary_search",
            args=(to_search_short_odd_len, 5),
            expected_return=True
        ),
        TestCase(
            name="binary_search poslední prvek (lichá délka seznamu)",
            func="binary_search",
            args=(to_search_short_odd_len, 9),
            expected_return=True
        ),
        TestCase(
            name="binary_search chybějící prvek (lichá délka seznamu)",
            func="binary_search",
            args=(to_search_short_odd_len, 10),
            expected_return=False
        ),
        TestCase(
            name="binary_search chybějící prvek (lichá délka seznamu)",
            func="binary_search",
            args=(to_search_short_odd_len, 0),
            expected_return=False
        ),
        TestCase(
            name="binary_search první prvek (sudá délka seznamu)",
            func="binary_search",
            args=(to_search_short_even_len, 1),
            expected_return=True
        ),
        TestCase(
            name="binary_search prostřední prvek (sudá délka seznamu)",
            func="binary_search",
            args=(to_search_short_even_len, 5),
            expected_return=True
        ),
        TestCase(
            name="binary_search poslední prvek (sudá délka seznamu)",
            func="binary_search",
            args=(to_search_short_even_len, 9),
            expected_return=True
        ),
        TestCase(
            name="binary_search chybějící prvek (sudá délka seznamu)",
            func="binary_search",
            args=(to_search_short_even_len, 11),
            expected_return=False
        ),
        TestCase(
            name="binary_search chybějící prvek (sudá délka seznamu)",
            func="binary_search",
            args=(to_search_short_even_len, 0),
            expected_return=False
        )
    ])
    should_success = random.choice([True, False])
    target = random.randint(450_000_000, 550_000_000)
    to_search_large = range(target + 1 if should_success else target - 1)
    result.append(TestCase(
        name="binary_search efektivita",
        func="binary_search",
        args=(to_search_large, target),
        expected_return=should_success
    ))
    return result
