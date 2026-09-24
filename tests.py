from dataclasses import dataclass, field
import random  # noqa: F401
from typing import Any, Callable, Union
import string


@dataclass
class TestCase:

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

    @staticmethod
    def test_class_existence(assignment, class_name: str) -> bool:
        try:
            cl = getattr(assignment, class_name)
            cl = cl
            return True
        except Exception:
            return False

    @staticmethod
    def test_class_instantiation(assignment, class_name: str, *args: Any) -> bool:
        try:
            cl = getattr(assignment, class_name)
            instance = cl(args)
            instance = instance
            return True
        except Exception:
            return False

    # def test_attribute_exist(assignment, attribute_name: str) -> bool:
    #     try:
    #         pet_instance = assignment.Pet("Bobík")
    #         getattr(pet_instance, attribute_name)
    #         return True
    #     except AttributeError:
    #         return False

    # def test_pet_name(assignment) -> bool:
    #     try:
    #         pet_name: str = "".join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))
    #         pet_instance = assignment.Pet(pet_name)
    #         return getattr(pet_instance, "name") == pet_name
    #     except AttributeError:
    #         return False

    # def test_attribute_value(assignment, attribute_name: str, expected_value: Any) -> bool:
    #     try:
    #         pet_name: str = "".join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))
    #         pet_instance = assignment.Pet(pet_name)
    #         return getattr(pet_instance, attribute_name) == expected_value
    #     except AttributeError:
    #         return False


def generate(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)

    result: list[TestCase] = [
        TestCase(
            name="1.1 Existence třídy Human",
            func=TestCase.test_class_existence,
            args=("Human",),
            expected_return=True
        ),
        TestCase(
            name="1.2 Human()",
            func=TestCase.test_class_instantiation,
            args=("Human",),
            expected_return=True
        ),
        TestCase(
            name="1.3 Human() default name is John Doe",
            func=TestCase.test_class_instantiation,
            args=("Human",),
            expected_return=True
        ),
    ]
    return result


def generate_bonus(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)
    result: list[TestCase] = []
    return result
