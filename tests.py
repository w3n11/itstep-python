import random  # noqa: F401
from typing import Any
from test import TestCase, Procedure, NewInstance  # noqa: F401


class expect_passengers:  # noqa: N801
    def __init__(self, expected: list[str | None]) -> None:
        self.expected = expected
        self.expected_repr: str = "[" + ", ".join(repr(x) if x else "None" for x in expected) + "]"

    def __call__(self, passengers: Any) -> bool:
        if len(passengers) != len(self.expected):
            return False

        for i in range(len(self.expected)):
            if self.expected[i] is None:
                if passengers[i] is not None:
                    return False
            else:
                if type(passengers[i]).__name__ != "Human" or str(passengers[i]) != self.expected[i]:
                    return False
        return True


def generate(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)

    result: list[TestCase] = [
        TestCase(
            id=(1, 0),
            name="Human - existence",
            func=TestCase.test_class_existence,
            args=("Human",),
            expected_return=True
        ),
        TestCase(
            id=(1, 1),
            name="Human - inicializace",
            func=TestCase.test_class_init,
            args=("Human",),
            expected_return=True,
            prerequisites={(1, 0)}
        ),
        TestCase(
            id=(1, 2),
            name="Human - vlastní jméno",
            func=TestCase.test_class,
            args=(
                "Human", Procedure()
                .add("name", expected_return_or_value="Pepíno"),
                ("Pepíno",)
            ),
            expected_return=True,
            prerequisites={(1, 0), (1, 1)}
        ),
        TestCase(
            id=(1, 3),
            name="Human - výchozí jméno je \"John Doe\"",
            func=TestCase.test_class,
            args=(
                "Human", Procedure()
                .add("name", expected_return_or_value="John Doe")
            ),
            expected_return=True,
            prerequisites={(1, 0), (1, 1)}
        ),
        TestCase(
            id=(1, 4),
            name="Human - metoda __str__",
            func=TestCase.test_class,
            args=(
                "Human", Procedure()
                .add("__str__", expected_return_or_value="Pepíno"),
                ("Pepíno",)
            ),
            expected_return=True,
            prerequisites={(1, 2), (1, 3)}
        ),
        TestCase(
            id=(2, 0),
            name="Car - existence",
            func=TestCase.test_class_existence,
            args=("Car",),
            expected_return=True,
            prerequisites={(1, 4)}
        ),
        TestCase(
            id=(2, 1),
            name="Car - inicializace",
            func=TestCase.test_class_init,
            args=(
                "Car", Procedure()
                .add("seats", expected_return_or_value=5),
                ("Mercedes",)
            ),
            expected_return=True,
            prerequisites={(2, 0)}
        ),
        TestCase(
            id=(2, 2),
            name="Car - značka auta",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("brand", expected_return_or_value="Mercedes")
                .add("seats", expected_return_or_value=5),
                ("Mercedes",)
            ),
            expected_return=True,
            prerequisites={(2, 1)}
        ),
        TestCase(
            id=(2, 3),
            name="Car - vlastní počet míst",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("seats", expected_return_or_value=2),
                ("Mercedes", 2)
            ),
            expected_return=True,
            prerequisites={(2, 2)}
        ),
        TestCase(
            id=(2, 4),
            name="Car - 1 pasažér",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", ("Mrakoplaš",), expected_return_or_value=True)
                .add("passengers", expected_return_or_value=expect_passengers(
                    ["Mrakoplaš", None, None, None, None])),
                ("Mercedes",)
            ),
            expected_return=True,
            prerequisites={(2, 3)}
        ),
        TestCase(
            id=(2, 5),
            name="Car - 2 pasažéři",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", ("Mrakoplaš",), expected_return_or_value=True)
                .add("add_passenger", ("Dvoukvítek",), expected_return_or_value=True)
                .add("passengers", expected_return_or_value=expect_passengers(
                    ["Mrakoplaš", "Dvoukvítek", None, None, None])),
                ("Mercedes",)
            ),
            expected_return=True,
            prerequisites={(2, 4)}
        ),
        TestCase(
            id=(2, 6),
            name="Car - 2 pasažéři, specifická místa",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", ("Mrakoplaš", 1), expected_return_or_value=True)
                .add("add_passenger", ("Dvoukvítek", 3), expected_return_or_value=True)
                .add("passengers", expected_return_or_value=expect_passengers(
                    [None, "Mrakoplaš", None, "Dvoukvítek", None])),
                ("Mercedes",)
            ),
            expected_return=True,
            prerequisites={(2, 5)}
        ),
        TestCase(
            id=(2, 7),
            name="Car - více pasažérů, obsazeno",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", ("Mrakoplaš", 1), expected_return_or_value=True)
                .add("add_passenger", ("Dvoukvítek", 2), expected_return_or_value=True)
                .add("add_passenger", ("Hrun Barbar", 1), expected_return_or_value=False)
                .add("passengers", expected_return_or_value=expect_passengers(
                    [None, "Mrakoplaš", "Dvoukvítek", None, None])),
                ("Mercedes",)
            ),
            expected_return=True,
            prerequisites={(2, 6)}
        ),
        TestCase(
            id=(2, 8),
            name="Car - plně obsazeno",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", ("Mrakoplaš",), expected_return_or_value=True)
                .add("add_passenger", ("Dvoukvítek",), expected_return_or_value=True)
                .add("add_passenger", ("Hrun Barbar",), expected_return_or_value=False)
                .add("passengers", expected_return_or_value=expect_passengers(["Mrakoplaš", "Dvoukvítek"])),
                ("Audi", 2)
            ),
            expected_return=True,
            prerequisites={(2, 7)}
        ),
        TestCase(
            id=(2, 9),
            name="Car - usazení mimo auto",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", ("Mrakoplaš", 2), expected_return_or_value=False)
                .add("passengers", expected_return_or_value=expect_passengers([None, None])),
                ("Audi", 2)
            ),
            expected_return=True,
            prerequisites={(2, 8)}
        ),
        TestCase(
            id=(2, 10),
            name="Car - usazení mimo auto",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", ("Mrakoplaš", 0), expected_return_or_value=False)
                .add("passengers", expected_return_or_value=expect_passengers([])),
                ("Audi", 0)
            ),
            expected_return=True,
            prerequisites={(2, 9)}
        )
    ]
    return result


def generate_bonus(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)
    result: list[TestCase] = [
        TestCase(
            id=(0, 1),
            name="Car - metoda __str__",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("passengers", expected_return_or_value=expect_passengers([None, None]))
                .add("__str__", expected_return_or_value="BMW\n  (the car is empty)"),
                ("BMW", 2)
            ),
            expected_return=True
        ),
        TestCase(
            id=(0, 2),
            name="Car - metoda __str__",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", ("Mrakoplaš",), expected_return_or_value=True)
                .add("passengers", expected_return_or_value=expect_passengers(["Mrakoplaš", None]))
                .add("__str__", expected_return_or_value="BMW\n  - Mrakoplaš\n  - (empty seat)"),
                ("BMW", 2)
            ),
            expected_return=True,
            prerequisites={(0, 1)}
        ),
        TestCase(
            id=(0, 3),
            name="Car - metoda __str__",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", ("Mrakoplaš",), expected_return_or_value=True)
                .add("add_passenger", ("Dvoukvítek",), expected_return_or_value=True)
                .add("add_passenger", ("Hrun Barbar",), expected_return_or_value=True)
                .add("add_passenger", ("Mort",), expected_return_or_value=False)
                .add("passengers", expected_return_or_value=expect_passengers(
                    ["Mrakoplaš", "Dvoukvítek", "Hrun Barbar"]))
                .add("__str__", expected_return_or_value="Škoda\n  - Mrakoplaš\n  - Dvoukvítek\n  - Hrun Barbar"),
                ("Škoda", 3)
            ),
            expected_return=True,
            prerequisites={(0, 2)}
        )
    ]
    return result
