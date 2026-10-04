import random  # noqa: F401
from typing import Any  # noqa: F401
from test import TestCase, Procedure, NewInstance  # noqa: F401 # type: ignore


def generate(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)

    result: list[TestCase] = [
        TestCase(
            id=(1, 0),
            name="Passenger - inicializace",
            func=TestCase.test_class_init,
            args=("Passenger", ("Neznámý",)),
            expected_return=True
        ),
        TestCase(
            id=(1, 1),
            name="Passenger - textová reprezentace (__str__)",
            func=TestCase.test_class,
            args=(
                "Passenger", Procedure()
                .add("__str__", expected_return_or_value="Neznámý (Passenger)"),
                ("Neznámý",)
            ),
            expected_return=True,
            prerequisites={(1, 0)}
        ),
        TestCase(
            id=(1, 2),
            name="Human - je potomkem Passenger",
            func=TestCase.test_class_inheritance,
            args=("Human", "Passenger"),
            expected_return=True,
            prerequisites={(1, 0)}
        ),
        TestCase(
            id=(1, 3),
            name="Dog - je potomkem Passenger",
            func=TestCase.test_class_inheritance,
            args=("Dog", "Passenger"),
            expected_return=True,
            prerequisites={(1, 0)}
        ),

        TestCase(
            id=(2, 0),
            name="Vehicle - inicializace",
            func=TestCase.test_class_init,
            args=("Vehicle", ("Škoda", 5)),
            expected_return=True,
            prerequisites={(1, 0)}
        ),

        TestCase(
            id=(3, 0),
            name="Car - je potomkem Vehicle",
            func=TestCase.test_class_inheritance,
            args=("Car", "Vehicle"),
            expected_return=True,
            prerequisites={(2, 0)}
        ),
        TestCase(
            id=(3, 1),
            name="Bus - je potomkem Vehicle",
            func=TestCase.test_class_inheritance,
            args=("Bus", "Vehicle"),
            expected_return=True,
            prerequisites={(2, 0)}
        ),
        TestCase(
            id=(3, 2),
            name="Car - Deduplikace atributů",
            func=TestCase.test_class_attr_dedup,
            args=("Car",),
            kwargs={"forbidden": ("seats", "passengers", "brand")},
            expected_return=True,
            prerequisites={(3, 0)}
        ),
        TestCase(
            id=(3, 3),
            name="Bus - Deduplikace atributů",
            func=TestCase.test_class_attr_dedup,
            args=("Bus",),
            kwargs={"forbidden": ("seats", "passengers", "brand")},
            expected_return=True,
            prerequisites={(3, 1)}
        ),
        TestCase(
            id=(3, 4),
            name="Car - stále funguje s novými pasažéry",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", (NewInstance("Human", ("Mrakoplaš",)),), expected_return_or_value=True)
                .add("add_passenger", (NewInstance("Dog", ("Cohen",)), 0), expected_return_or_value=False)
                .add("add_passenger", (NewInstance("Human", ("Dvoukvítek",)), 3), expected_return_or_value=True)
                .add("passengers", expected_return_or_value=[
                    NewInstance("Human", ("Mrakoplaš",)),
                    None, None,
                    NewInstance("Human", ("Dvoukvítek",)),
                    None
                ])
                .add("brand", expected_return_or_value="Mercedes"),
                ("Mercedes",)
            ),
            expected_return=True,
            prerequisites={(3, 0), (1, 2), (1, 3)}
        ),
        TestCase(
            id=(3, 5),
            name="Bus - výchozí počet míst musí být 40",
            func=TestCase.test_class,
            args=(
                "Bus", Procedure()
                .add("seats", expected_return_or_value=40),
                ("SOR",)
            ),
            expected_return=True,
            prerequisites={(3, 1)}
        ),
        TestCase(
            id=(3, 6),
            name="Bus - nastavení vlastního počtu míst",
            func=TestCase.test_class,
            args=(
                "Bus", Procedure()
                .add("seats", expected_return_or_value=10),
                ("SOR", 10)
            ),
            expected_return=True,
            prerequisites={(3, 1)}
        ),
        TestCase(
            id=(3, 7),
            name="Bus - stále funguje s novými pasažéry",
            func=TestCase.test_class,
            args=(
                "Bus", Procedure()
                .add("add_passenger", (NewInstance("Human", ("Mrakoplaš",)),), expected_return_or_value=True)
                .add("add_passenger", (NewInstance("Dog", ("Cohen",)), 0), expected_return_or_value=False)
                .add("add_passenger", (NewInstance("Human", ("Dvoukvítek",)), 3), expected_return_or_value=True)
                .add("passengers", expected_return_or_value=[
                    NewInstance("Human", ("Mrakoplaš",)),
                    None, None,
                    NewInstance("Human", ("Dvoukvítek",)),
                ] + [None] * 36)
                .add("brand", expected_return_or_value="Iveco"),
                ("Iveco",)
            ),
            expected_return=True,
            prerequisites={(3, 1), (1, 2), (1, 3)}
        ),

        TestCase(
            id=(4, 0),
            name="Car nesmí mít metodu collect_fares",
            func=TestCase.test_class_definition,
            args=(
                "Car",
                (),
                "collect_fares",
                False
            ),
            expected_return=True,
            prerequisites={(3, 0)}
        ),
        TestCase(
            id=(4, 1),
            name="Bus musí mít metodu collect_fares",
            func=TestCase.test_class_definition,
            args=(
                "Bus",
                "collect_fares",
                (),
                False
            ),
            expected_return=True,
            prerequisites={(3, 1)}
        ),
        TestCase(
            id=(4, 2),
            name="Bus - výběr jízdného (výchozí cena 20)",
            func=TestCase.test_class,
            args=(
                "Bus", Procedure()
                .add("collect_fares", expected_return_or_value=0)
                .add("add_passenger", (NewInstance("Human", ("Mrakoplaš",)),), expected_return_or_value=True)
                .add("add_passenger", (NewInstance("Dog", ("Cohen",)),), expected_return_or_value=True)
                .add("add_passenger", (NewInstance("Human", ("Dvoukvítek",)),), expected_return_or_value=True)
                .add("collect_fares", expected_return_or_value=60),
                ("SOR",)
            ),
            expected_return=True,
            prerequisites={(4, 1), (3, 7)}
        ),
        TestCase(
            id=(4, 3),
            name="Bus - výběr jízdného s vlastní cenou",
            func=TestCase.test_class,
            args=(
                "Bus", Procedure()
                .add("add_passenger", (NewInstance("Human", ("Mrakoplaš",)), 0), expected_return_or_value=True)
                .add("add_passenger", (NewInstance("Human", ("Cohen",)), 39), expected_return_or_value=True)
                .add("collect_fares", expected_return_or_value=100),
                ("Karosa", 40, 50)
            ),
            expected_return=True,
            prerequisites={(4, 2)}
        )
    ]
    return result


def generate_bonus(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)
    result: list[TestCase] = [
        TestCase(
            id=(1, 0),
            name="Bonus - Třída Bus obsahuje metodu board_group",
            func=TestCase.test_class_definition,
            args=(
                "Bus",
                "board_group",
                (),
                True
            ),
            expected_return=True
        ),
        TestCase(
            id=(1, 1),
            name="Bonus - Nástup malé skupiny do prázdného autobusu",
            func=TestCase.test_class,
            args=(
                "Bus", Procedure()
                .add(
                    "board_group",
                    ([
                        NewInstance("Human", ("Bábi Zlopočasná",)),
                        NewInstance("Human", ("Stařenka Oggová",)),
                        NewInstance("Dog", ("Greebo",))
                    ],),
                    expected_return_or_value=0
                )
                .add(
                    "passengers",
                    expected_return_or_value=[
                        NewInstance("Human", ("Bábi Zlopočasná",)),
                        NewInstance("Human", ("Stařenka Oggová",)),
                        NewInstance("Dog", ("Greebo",))
                    ] + [None] * 3
                ),
                ("SOR", 6)
            ),
            expected_return=True,
            prerequisites={(1, 0)}
        ),
        TestCase(
            id=(1, 2),
            name="Bonus - Nástup velké skupiny do poloprázdného minibusu",
            func=TestCase.test_class,
            args=(
                "Bus", Procedure()
                .add(
                    "add_passenger",
                    (NewInstance("Human", ("Řidič",)), 0),
                    expected_return_or_value=True
                )
                .add(
                    "board_group",
                    ([
                        NewInstance("Human", ("Cestující 1",)),
                        NewInstance("Human", ("Cestující 2",)),
                        NewInstance("Dog", ("Pes 1",)),
                        NewInstance("Human", ("Cestující 3",))
                    ],),
                    expected_return_or_value=2
                )
                .add(
                    "passengers",
                    expected_return_or_value=[
                        NewInstance("Human", ("Řidič",)),
                        NewInstance("Human", ("Cestující 1",)),
                        NewInstance("Human", ("Cestující 2",))
                    ]
                ),
                ("Minibus", 3)
            ),
            expected_return=True,
            prerequisites={(1, 0)}
        )
    ]
    return result
