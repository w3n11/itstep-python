import random  # noqa: F401
from typing import Any  # noqa: F401
from test import TestCase, Procedure, NewInstance  # noqa: F401 # type: ignore


def generate(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)

    result: list[TestCase] = [
        TestCase(
            id=(1, 0),
            name="Bus - inicializace",
            func=TestCase.test_class_init,
            args=("Bus", ("SOR",)),
            expected_return=True
        ),
        TestCase(
            id=(1, 1),
            name="Bus - výchozí počet míst musí být 40",
            func=TestCase.test_class,
            args=(
                "Bus", Procedure()
                .add("seats", expected_return_or_value=40),
                ("SOR",)
            ),
            expected_return=True,
            prerequisites={(1, 0)}
        ),
        TestCase(
            id=(1, 2),
            name="Bus - nastavení vlastního počtu míst",
            func=TestCase.test_class,
            args=(
                "Bus", Procedure()
                .add("seats", expected_return_or_value=10),
                ("SOR", 10)
            ),
            expected_return=True,
            prerequisites={(1, 0)}
        ),
        TestCase(
            id=(2, 0),
            name="Vehicle - inicializace",
            func=TestCase.test_class_init,
            args=(
                "Vehicle",
                ("Škoda", 5)
            ),
            expected_return=True,
            prerequisites={(1, 2)}
        ),
        TestCase(
            id=(2, 1),
            name="Car - je potomkem Vehicle",
            func=TestCase.test_class_inheritance,
            args=(
                "Car", "Vehicle"
            ),
            expected_return=True,
            prerequisites={(2, 0)}
        ),
        TestCase(
            id=(2, 2),
            name="Car - stále funguje",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add(
                    "add_passenger",
                    (NewInstance("Human", ("Mrakoplaš",)),),
                    expected_return_or_value=True
                )
                .add(
                    "add_passenger",
                    (NewInstance("Human", ("Cohen",)), 0),
                    expected_return_or_value=False
                )
                .add(
                    "add_passenger",
                    (NewInstance("Human", ("Dvoukvítek",)), 3),
                    expected_return_or_value=True
                )
                .add(
                    "passengers",
                    expected_return_or_value=[
                        NewInstance("Human", ("Mrakoplaš",)),
                        None,
                        None,
                        NewInstance("Human", ("Dvoukvítek",)),
                        None
                    ]
                )
                .add(
                    "brand",
                    expected_return_or_value="Mercedes"
                ), ("Mercedes",)
            ),
            expected_return=True,
            prerequisites={(2, 1)}
        ),
        TestCase(
            id=(2, 3),
            name="Bus - je potomkem Vehicle",
            func=TestCase.test_class_inheritance,
            args=(
                "Bus", "Vehicle"
            ),
            expected_return=True,
            prerequisites={(2, 0)}
        ),
        TestCase(
            id=(2, 4),
            name="Bus - stále funguje",
            func=TestCase.test_class,
            args=(
                "Bus", Procedure()
                .add(
                    "add_passenger",
                    (NewInstance("Human", ("Mrakoplaš",)),),
                    expected_return_or_value=True
                )
                .add(
                    "add_passenger",
                    (NewInstance("Human", ("Cohen",)), 0),
                    expected_return_or_value=False
                )
                .add(
                    "add_passenger",
                    (NewInstance("Human", ("Dvoukvítek",)), 3),
                    expected_return_or_value=True
                )
                .add(
                    "passengers",
                    expected_return_or_value=[
                        NewInstance("Human", ("Mrakoplaš",)),
                        None,
                        None,
                        NewInstance("Human", ("Dvoukvítek",)),
                        None
                    ] + [None] * 35
                )
                .add(
                    "brand",
                    expected_return_or_value="Iveco"
                ), ("Iveco",)
            ),
            expected_return=True,
            prerequisites={(2, 1)}
        ),
        TestCase(
            id=(2, 5),
            name="Car - Deduplikace atributů",
            func=TestCase.test_class_attr_dedup,
            args=(
                "Car",
            ),
            kwargs={
                "forbidden": ("seats", "passengers", "brand"),
            },
            expected_return=True,
            prerequisites={(2, 1), (2, 2)}
        ),
        TestCase(
            id=(2, 6),
            name="Bus - Deduplikace atributů",
            func=TestCase.test_class_attr_dedup,
            args=(
                "Bus",
            ),
            kwargs={
                "forbidden": ("seats", "passengers", "brand"),
            },
            expected_return=True,
            prerequisites={(2, 3), (2, 4)}
        )
    ]
    return result


def generate_bonus(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)
    result: list[TestCase] = []
    return result
