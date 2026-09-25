from dataclasses import dataclass, field
import random  # noqa: F401
from typing import Any, Callable, Union


class Procedure:
    @dataclass
    class ProcedureStep:
        attribute_or_method: str
        args: tuple[Any, ...] = ()
        expect_return_or_value: bool = True
        expected_return_or_value: Any = None

    def __init__(self) -> None:
        self.steps: list[Procedure.ProcedureStep] = []

    def add(
        self,
        attribute_or_method: str,
        args: tuple[Any, ...] = (),
        expected_return_or_value: Any = None,
        expect_return_or_value: bool = True
    ):
        self.steps.append(
            self.ProcedureStep(
                attribute_or_method=attribute_or_method,
                args=args,
                expect_return_or_value=expect_return_or_value,
                expected_return_or_value=expected_return_or_value,
            )
        )
        return self

    def __iter__(self):
        return iter(self.steps)


@dataclass
class TestCase:
    # Unique id, eg. 1.0, 1.1, 2.4, 3.5.2
    id: str

    # Name will be displayed in the test run result, it should describe what is it testing
    name: str

    # Either a name of the function from the assignment (str) or local function (Callable).
    # In the second case the assignment module will be passed as a parameter.
    func: Union[str, Callable]
    args: tuple = ()
    kwargs: dict | None = None
    inputs: list[str] = field(default_factory=list)
    expected_print: str | None = None
    expected_return: Any | Callable[[Any], bool] = None
    expected_exception: type[Exception] | None = None
    file_validators: dict[str, Callable[[str], bool]] = field(default_factory=dict)
    setup: Union[Callable[[], None], list[Callable[[], None]], None] = None
    teardown: Union[Callable[[], None], list[Callable[[], None]], None] = None
    timeout: float = 2.0
    iterations: int = 1
    verify_print: Any | Callable[[Any], bool] = None
    max_calls: dict[str, int] = field(default_factory=dict)
    required_calls: dict[str, int] = field(default_factory=dict)
    prerequisites: set[str] = field(default_factory=set)

    @staticmethod
    def test_class_existence(assignment, class_name: str) -> bool:
        try:
            cl = getattr(assignment, class_name)
            cl = cl
            return True
        except Exception:
            return False

    @staticmethod
    def test_class_init(assignment, class_name: str, *args: Any) -> bool:
        try:
            cl = getattr(assignment, class_name)
            instance = cl(args)
            instance = instance
            return True
        except Exception:
            return False

    @staticmethod
    def test_class(
        assignment,
        class_name: str,
        procedure: Procedure,
        init_args: tuple[Any, ...] = (),
    ) -> bool:

        def nice_format(val: Any) -> str:
            if callable(val):
                return getattr(val, "expected_repr", "")

            if isinstance(val, list):
                return "[" + ", ".join(nice_format(x) for x in val) + "]"

            if hasattr(val, "__class__") and type(val).__name__ not in (
                    "int", "str", "float", "bool", "NoneType", "tuple", "dict"):
                try:
                    return f"{type(val).__name__}('{str(val)}')"
                except Exception:
                    pass

            if isinstance(val, str):
                return repr(val)
            return str(val)

        args_str = ", ".join(nice_format(a) for a in init_args)
        trace = [f"x = {class_name}({args_str})"]

        try:
            cl = getattr(assignment, class_name)
            instance = cl(*init_args)
        except Exception as e:
            raise AssertionError(
                f"Selhala inicializace {type(e).__name__}: {e}\n\nPostup:\n" + "\n".join(trace) + "\n"
            )

        for step in procedure:
            if step.args:
                step_args = ", ".join(nice_format(a) for a in step.args)
                call_repr = f"x.{step.attribute_or_method}({step_args})"
            else:
                call_repr = f"x.{step.attribute_or_method}"

            if not hasattr(instance, step.attribute_or_method):
                trace.append(call_repr)
                raise AssertionError(
                    f"Objekt nemá atribut/metodu '{step.attribute_or_method}'\n\nPostup:\n""\n".join(trace) + "\n"
                )

            target = getattr(instance, step.attribute_or_method)

            try:
                if callable(target):
                    if not step.args:
                        call_repr += "()"
                    result = target(*step.args)
                else:
                    result = target
            except Exception as e:
                trace.append(call_repr)
                raise AssertionError(
                    f"Při volání nastala výjimka {type(e).__name__}: {e}\n\nPostup:\n" + "\n".join(trace) + "\n"
                )

            if step.expect_return_or_value:
                call_repr += f" == {nice_format(step.expected_return_or_value)}"

            trace.append(call_repr)

            if step.expect_return_or_value:
                if callable(step.expected_return_or_value):
                    if not step.expected_return_or_value(result):
                        raise AssertionError(
                            f"Obdrženo: {nice_format(result)}\n\nPostup:\n" + "\n".join(trace) + "\n"
                        )
                else:
                    if result != step.expected_return_or_value:
                        raise AssertionError(
                            f"Očekáváno: {nice_format(step.expected_return_or_value)}, Obdrženo: "
                            f"{nice_format(result)}\n\nPostup:\n" + "\n".join(trace) + "\n"
                        )
        return True


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
            id="1.0",
            name="Human - existence",
            func=TestCase.test_class_existence,
            args=("Human",),
            expected_return=True
        ),
        TestCase(
            id="1.1",
            name="Human - inicializace",
            func=TestCase.test_class_init,
            args=("Human",),
            expected_return=True,
            prerequisites={"1.0"}
        ),
        TestCase(
            id="1.2",
            name="Human - výchozí jméno je \"John Doe\"",
            func=TestCase.test_class,
            args=(
                "Human", Procedure()
                .add("name", expected_return_or_value="John Doe")
            ),
            expected_return=True,
            prerequisites={"1.0", "1.1"}
        ),
        TestCase(
            id="1.3",
            name="Human - vlastní jméno",
            func=TestCase.test_class,
            args=(
                "Human", Procedure()
                .add("name", expected_return_or_value="Pepíno"),
                ("Pepíno",)
            ),
            expected_return=True,
            prerequisites={"1.0", "1.1"}
        ),
        TestCase(
            id="1.4",
            name="Human - metoda __str__",
            func=TestCase.test_class,
            args=(
                "Human", Procedure()
                .add("__str__", expected_return_or_value="Pepíno"),
                ("Pepíno",)
            ),
            expected_return=True,
            prerequisites={"1.2", "1.3"}
        ),
        TestCase(
            id="2.0",
            name="Car - existence",
            func=TestCase.test_class_existence,
            args=("Car",),
            expected_return=True,
            prerequisites={"1.0", "1.1", "1.2", "1.3"}
        ),
        TestCase(
            id="2.1",
            name="Car - inicializace",
            func=TestCase.test_class_init,
            args=(
                "Car", Procedure()
                .add("seats", expected_return_or_value=5),
                ("Mercedes",)
            ),
            expected_return=True,
            prerequisites={"2.0"}
        ),
        TestCase(
            id="2.2",
            name="Car - značka auta",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("brand", expected_return_or_value="Mercedes")
                .add("seats", expected_return_or_value=5),
                ("Mercedes",)
            ),
            expected_return=True,
            prerequisites={"2.1"}
        ),
        TestCase(
            id="2.3",
            name="Car - vlastní počet míst",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("seats", expected_return_or_value=2),
                ("Mercedes", 2)
            ),
            expected_return=True,
            prerequisites={"2.2"}
        ),
        TestCase(
            id="2.4",
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
            prerequisites={"2.3"}
        ),
        TestCase(
            id="2.5",
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
            prerequisites={"2.4"}
        ),
        TestCase(
            id="2.6",
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
            prerequisites={"2.5"}
        ),
        TestCase(
            id="2.7",
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
            prerequisites={"2.6"}
        ),
        TestCase(
            id="2.8",
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
            prerequisites={"2.7"}
        ),
        TestCase(
            id="2.9",
            name="Car - usazení mimo auto",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", ("Mrakoplaš", 2), expected_return_or_value=False)
                .add("passengers", expected_return_or_value=expect_passengers([None, None])),
                ("Audi", 2)
            ),
            expected_return=True,
            prerequisites={"2.8"}
        ),
        TestCase(
            id="2.10",
            name="Car - usazení mimo auto",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", ("Mrakoplaš", 0), expected_return_or_value=False)
                .add("passengers", expected_return_or_value=expect_passengers([])),
                ("Audi", 0)
            ),
            expected_return=True,
            prerequisites={"2.9"}
        )
    ]
    return result


def generate_bonus(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)
    result: list[TestCase] = [
        TestCase(
            id="B.1",
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
            id="B.2",
            name="Car - metoda __str__",
            func=TestCase.test_class,
            args=(
                "Car", Procedure()
                .add("add_passenger", ("Mrakoplaš",), expected_return_or_value=True)
                .add("passengers", expected_return_or_value=expect_passengers(["Mrakoplaš", None]))
                .add("__str__", expected_return_or_value="BMW\n  - Mrakoplaš"),
                ("BMW", 2)
            ),
            expected_return=True,
            prerequisites={"B.1"}
        ),
        TestCase(
            id="B.3",
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
            prerequisites={"B.2"}
        )
    ]
    return result
