from dataclasses import dataclass, field
import random  # noqa: F401
from typing import Any, Callable
import math
import statistics as stats


def is_dice_roll_valid(results: list[int], dice_faces: list[int]) -> bool:
    total_min = len(dice_faces)
    total_max = sum(dice_faces)
    
    total_expected_mean = sum((k + 1) / 2.0 for k in dice_faces)
    total_expected_variance = sum((k**2 - 1) / 12.0 for k in dice_faces)

    actual_values = set(results)
    if not actual_values or min(actual_values) < total_min or max(actual_values) > total_max:
        return False
    if len(results) < 2: 
        return False
        
    actual_mean = stats.mean(results)
    sem = stats.stdev(results) / math.sqrt(len(results))
    if abs(actual_mean - total_expected_mean) > 4 * sem:
        return False

    if dice_faces:
        actual_variance = stats.variance(results)
        if abs(actual_variance - total_expected_variance) > (total_expected_variance * 0.1):
            return False
        
    return True


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
    result: list[TestCase] = [
        TestCase(
            name="print_menu",
            func="print_menu",
            args=(["Hello", "World", "Ukončit"],),
            expected_print="[1] Hello\n[2] World\n[0] Ukončit\n"
        ),
        TestCase(
            name="print_menu (pouze jedna položka)",
            func="print_menu",
            args=(["Ukončit"],),
            expected_print="[0] Ukončit\n"
        ),
        TestCase(
            name="get_user_input",
            func="get_user_input",
            args=([0],),
            inputs=["0"],
            expected_return=0
        ),
        TestCase(
            name="get_user_input (nepovolený vstup)",
            func="get_user_input",
            args=([1],),
            inputs=["0", "1"],
            expected_return=1
        ),
        TestCase(
            name="get_user_input (chybný vstup)",
            func="get_user_input",
            args=([0],),
            inputs=["zero", "", "0"],
            expected_return=0
        ),
        TestCase(
            name="dumb_menu",
            func="dumb_menu",
            inputs=["1", "2", "0", "0"],
            expected_return=[1, 2, 0, 0],
            verify_print=lambda _ : True
        ),
        TestCase(
            name="dumb_menu",
            func="dumb_menu",
            inputs=["0"],
            expected_return=[0],
            verify_print=lambda _ : True
        ),
        TestCase(
            name="dumb_menu",
            func="dumb_menu",
            inputs=["1", "1", "2", "0", "2", "1", "2", "3", "0", "1", "0", "3",
                    "3", "2", "1", "0", "1", "3", "0", "0"],
            expected_return=[1, 1, 2, 0, 2, 1, 2, 0, 1, 0, 3, 2, 1, 0, 1, 0, 0],
            verify_print=lambda _ : True
        )
    ]
    return result


def generate_bonus() -> list[TestCase]:
    result: list[TestCase] = [
        TestCase(
            name="dice_roll('1d6')",
            func="dice_roll",
            args=("1d6",),
            expected_return=lambda x : is_dice_roll_valid(x, [6]),
            iterations=10_000
        ),
        TestCase(
            name="dice_roll('2d6')",
            func="dice_roll",
            args=("2d6",),
            expected_return=lambda x : is_dice_roll_valid(x, [6, 6]),
            iterations=10_000
        ),
        TestCase(
            name="dice_roll('2d6+1d12')",
            func="dice_roll",
            args=("2d6+1d12",),
            expected_return=lambda x : is_dice_roll_valid(x, [6, 6, 12]),
            iterations=10_000
        ),
        TestCase(
            name="dice_roll('1d6+1d8+1d10+1d12')",
            func="dice_roll",
            args=('1d6+1d8+1d10+1d12',),
            expected_return=lambda x : is_dice_roll_valid(x, [6, 8, 10, 12]),
            iterations=10_000
        ),
        TestCase(
            name="dice_roll('3d20')",
            func="dice_roll",
            args=('3d20',),
            expected_return=lambda x : is_dice_roll_valid(x, [20, 20, 20]),
            iterations=10_000
        ),
    ]
    return result
