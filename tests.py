from dataclasses import dataclass, field
import random  # noqa: F401
from typing import Any, Callable
import qrcode


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


def make_qrcode(data: str) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        border=2
    )
    qr.add_data(data)
    qr.make(True)

    matrix: list[list[bool]] = qr.get_matrix()
    result: str = ""
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            result += "1" if matrix[i][j] else "0"
    return result


def load_as_bytes(filename: str) -> bytes:
    with open(file="test_files/" + filename + ".bytes", mode="rb") as f:
        return f.read()


def test_colorprint(test_file: str, value: str) -> bool:
    test_value: bytes = load_as_bytes(test_file)
    return test_value == value.encode("utf-8")


def generate() -> list[TestCase]:
    result: list[TestCase] = []

    result.extend([
        TestCase(
            name="hello_world_green",
            func="hello_world_green",
            verify_print=lambda x: test_colorprint("hello_world_green", x)
        ),
        TestCase(
            name="censor_print() příklad ze zadání",
            func="censor_print",
            args=("Hello world!", ["Hell"]),
            expected_return=1,
            verify_print=lambda x: test_colorprint("censor_print_hello_world", x)
        ),
        TestCase(
            name="censor_print() delší zpráva",
            func="censor_print",
            args=("Přísně tajný projekt X-42 byl včera přesunut do oblasti 51. Heslo k trezoru je modrý banán.",
                  ["tajný", "X-42", "oblasti 51", "modrý banán"]),
            expected_return=4,
            verify_print=lambda x: test_colorprint("censor_print_tajny_projekt", x)
        ),
        TestCase(
            name="print_qrcode() #1",
            func="print_qrcode",
            args=(make_qrcode("https://theuselessweb.com"),),
            verify_print=lambda x: test_colorprint("theuselessweb.com", x)
        ),
        TestCase(
            name="print_qrcode() #2",
            func="print_qrcode",
            args=(make_qrcode("https://pointerpointer.com"),),
            verify_print=lambda x: test_colorprint("pointerpointer.com", x)
        ),
        TestCase(
            name="print_qrcode() #3",
            func="print_qrcode",
            args=(make_qrcode("https://hackertyper.com"),),
            verify_print=lambda x: test_colorprint("hackertyper.com", x)
        ),
    ])

    return result


def generate_bonus() -> list[TestCase]:
    result: list[TestCase] = []
    return result
