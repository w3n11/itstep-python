from dataclasses import dataclass, field
import random  # noqa: F401
from typing import Any, Callable, Union
import qrcode
import os


@dataclass
class TestCase:
    name: str
    func: str
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


def validate_exact_text(expected_content: str) -> Callable[[str], bool]:
    def validator(filepath: str) -> bool:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read() == expected_content
    return validator

def validate_lines(condition: Callable[[list[str]], bool]) -> Callable[[str], bool]:
    def validator(filepath: str) -> bool:
        with open(filepath, "r", encoding="utf-8") as f:
            return condition(f.read().splitlines())
    return validator


def create_dummy_file(filepath: str, content: str) -> Callable[[], None]:
    def _setup():
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    return _setup


def delete_file(filepath: str) -> Callable[[], None]:
    def _teardown():
        import os
        if os.path.exists(filepath):
            os.remove(filepath)
    return _teardown


def numbers_between_1_and_100(lines: list[str]) -> bool:
    for line in lines:
        try:
            if int(line) < 1 or int(line) > 100:
                return False
        except ValueError:
            return False
    return True


def numbers_between_1_and_200(lines: list[str]) -> bool:
    for line in lines:
        try:
            if int(line) < 1 or int(line) > 200:
                return False
        except ValueError:
            return False
    return True


def get_file_content(path: str) -> str:
    try:
        with open(file=path, mode="r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def generate() -> list[TestCase]:
    result: list[TestCase] = []

    result.extend([
        TestCase(
            name="Hello world v souboru",
            func="hello_world_in_file",
            file_validators={
                "hello_world.txt": validate_exact_text("Hello World\n")
            },
            teardown=delete_file("hello_world.txt")
        ),
        TestCase(
            name="Číslování řádků",
            func="read_and_order",
            args=("test_files/words.txt",),
            expected_print=get_file_content("test_files/words_ordered.txt")
        ),
        TestCase(
            name="5 náhodných čísel v souboru",
            func="random_numbers_to_file",
            args=(5,),
            file_validators={
                "random_numbers.txt": lambda filepath: (
                    validate_lines(numbers_between_1_and_100)(filepath) and 
                    validate_lines(lambda lines: len(lines) == 5)(filepath)
                )
            },
            teardown=delete_file("random_numbers.txt")
        ),
        TestCase(
            name="100 náhodných čísel v souboru",
            func="random_numbers_to_file",
            args=(100,),
            file_validators={
                "random_numbers.txt": lambda filepath: (
                    validate_lines(numbers_between_1_and_100)(filepath) and 
                    validate_lines(lambda lines: len(lines) == 100)(filepath)
                )
            },
            teardown=delete_file("random_numbers.txt")
        ),
        TestCase(
            name="10 náhodných unikátních čísel v souboru",
            func="unique_random_numbers_to_file",
            args=(10,),
            file_validators={
                "unique_random_numbers.txt": lambda filepath: (
                    validate_lines(numbers_between_1_and_100)(filepath) and 
                    validate_lines(lambda lines: len(lines) == 10)(filepath) and
                    validate_lines(lambda lines: len(lines) == len(set(lines)))(filepath)
                )
            },
            teardown=delete_file("unique_random_numbers.txt")
        ),
        TestCase(
            name="100 náhodných unikátních čísel v souboru",
            func="unique_random_numbers_to_file",
            args=(100,),
            file_validators={
                "unique_random_numbers.txt": lambda filepath: (
                    validate_lines(numbers_between_1_and_100)(filepath) and 
                    validate_lines(lambda lines: len(lines) == 100)(filepath) and
                    validate_lines(lambda lines: len(lines) == len(set(lines)))(filepath)
                )
            },
            teardown=delete_file("unique_random_numbers.txt")
        ),
        TestCase(
            name="200 náhodných unikátních čísel v souboru",
            func="unique_random_numbers_to_file",
            args=(200,),
            file_validators={
                "unique_random_numbers.txt": lambda filepath: (
                    validate_lines(numbers_between_1_and_200)(filepath) and 
                    validate_lines(lambda lines: len(lines) == 200)(filepath) and
                    validate_lines(lambda lines: len(lines) == len(set(lines)))(filepath)
                )
            },
            teardown=delete_file("unique_random_numbers.txt")
        )
    ])
    return result


def generate_bonus() -> list[TestCase]:
    result: list[TestCase] = [
        TestCase(
            name="Login - uživatel existuje (1. řádek)",
            func="simple_login",
            args=("test_database.txt",),
            inputs=["admin", "heslo"],
            expected_return=True,
            expected_print="Logged in.\n",
            file_validators={
                "test_database.txt": validate_exact_text("admin;heslo\nluděk;nevim123\n")
            },

            setup=create_dummy_file("test_database.txt", "admin;heslo\nluděk;nevim123\n"),
            teardown=delete_file("test_database.txt")
        ),
        TestCase(
            name="Login - uživatel existuje (2. řádek)",
            func="simple_login",
            args=("test_database.txt",),
            inputs=["admin", "heslo"],
            expected_return=True,
            expected_print="Logged in.\n",
            file_validators={
                "test_database.txt": validate_exact_text("luděk;nevim123\nadmin;heslo\n")
            },

            setup=create_dummy_file("test_database.txt", "luděk;nevim123\nadmin;heslo\n"),
            teardown=delete_file("test_database.txt")
        ),
        TestCase(
            name="Login - uživatel neexistuje",
            func="simple_login",
            args=("test_database.txt",),
            inputs=["anežka", "česká"],
            expected_return=False,
            expected_print="Invalid credentials.\n",
            file_validators={
                "test_database.txt": validate_exact_text("luděk;nevim123\nadmin;heslo\n")
            },

            setup=create_dummy_file("test_database.txt", "luděk;nevim123\nadmin;heslo\n"),
            teardown=delete_file("test_database.txt")
        ),
        TestCase(
            name="Register - vytvoření účtu",
            func="simple_register",
            args=("test_database.txt",),
            inputs=["hello", "world", "world"],
            expected_return=True,
            expected_print="Account created.\n",
            file_validators={
                "test_database.txt": validate_exact_text("admin;heslo\nluděk;nevim123\nhello;world\n")
            },

            setup=create_dummy_file("test_database.txt", "admin;heslo\nluděk;nevim123\n"),
            teardown=delete_file("test_database.txt")
        ),
        TestCase(
            name="Register - neshodující se hesla",
            func="simple_register",
            args=("test_database.txt",),
            inputs=["hello", "world", "word"],
            expected_return=False,
            expected_print="Passwords do not match.\n",
            file_validators={
                "test_database.txt": validate_exact_text("admin;heslo\nluděk;nevim123\n")
            },

            setup=create_dummy_file("test_database.txt", "admin;heslo\nluděk;nevim123\n"),
            teardown=delete_file("test_database.txt")
        ),
        TestCase(
            name="Register - uživatel již existuje",
            func="simple_register",
            args=("test_database.txt",),
            inputs=["luděk", "world", "world"],
            expected_return=False,
            expected_print="Username already exists.\n",
            file_validators={
                "test_database.txt": validate_exact_text("admin;heslo\nluděk;nevim123\n")
            },

            setup=create_dummy_file("test_database.txt", "admin;heslo\nluděk;nevim123\n"),
            teardown=delete_file("test_database.txt")
        ),
        TestCase(
            name="Login - použití getpass",
            func="simple_login",
            args=("test_database.txt",),
            inputs=["admin", "heslo"],
            expected_return=True,
            expected_print="Logged in.\n",
            file_validators={
                "test_database.txt": validate_exact_text("admin;heslo\nluděk;nevim123\n")
            },

            setup=create_dummy_file("test_database.txt", "admin;heslo\nluděk;nevim123\n"),
            teardown=delete_file("test_database.txt"),
            required_calls={
                "getpass.getpass": 1,
                "builtins.input": 1
            },
            max_calls={
                "getpass.getpass": 1,
                "builtins.input": 1
            },
        ),
        TestCase(
            name="Register - použití getpass",
            func="simple_register",
            args=("test_database.txt",),
            inputs=["hello", "world", "world"],
            expected_return=True,
            expected_print="Account created.\n",
            file_validators={
                "test_database.txt": validate_exact_text("admin;heslo\nluděk;nevim123\nhello;world\n")
            },

            setup=create_dummy_file("test_database.txt", "admin;heslo\nluděk;nevim123\n"),
            teardown=delete_file("test_database.txt"),
            required_calls={
                "getpass.getpass": 2,
                "builtins.input": 1
            },
            max_calls={
                "getpass.getpass": 2,
                "builtins.input": 1
            }
        ),
        
    ]
    return result
