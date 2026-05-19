from dataclasses import dataclass, field
import random  # noqa: F401
from typing import Any, Callable, Union
import os
import difflib
import collections


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
        if os.path.exists(filepath):
            os.remove(filepath)
    return _teardown


class LazyArgs:
    def __init__(self, plaintext: str, key: int):
        self.plaintext = plaintext
        self.key = key
        import assignment
        try:
            self.ciphertext = assignment.my_encrypt(self.plaintext, self.key)  # type: ignore
        except AttributeError:
            self.ciphertext = None

    def __iter__(self):
        yield self.ciphertext
        yield self.key

    def __bool__(self):
        return True


def verify_avalanche_effect(ct_pair: tuple[str, str]) -> bool:
    ct1, ct2 = ct_pair
    if len(ct1) != len(ct2):
        return True
    same_chars = sum(1 for c1, c2 in zip(ct1, ct2) if c1 == c2)
    return (same_chars / len(ct1)) < 0.5


def verify_low_repetition(ct: str) -> bool:
    if not ct:
        return True
    counts = collections.Counter(ct)
    most_common_char = counts.most_common(1)[0][1]
    return (most_common_char / len(ct)) < 0.3


def verify_word_lengths_destroyed(pt: str, ct: str) -> bool:
    return pt.count(" ") != ct.count(" ") and (
        [i for i in range(len(pt)) if pt[i] == " "] != [i for i in range(len(ct)) if ct[i] == " "]
    )


def verify_encryption_strength(pt: str, ct: str) -> bool:
    pt = pt.lower()
    ct = ct.lower()
    matcher = difflib.SequenceMatcher(None, pt, ct)
    return matcher.ratio() < 0.35


def most(elems: list[bool], ratio: float = 0.5) -> bool:
    trues = 0
    for e in elems:
        trues += 1 if e else 0
    return trues / len(elems) >= ratio


def get_key() -> int:
    return random.randint(0, 2 ** 32 - 1)


def get_pt(length: int = 8) -> str:
    return "".join(
        random.choices([chr(i) for i in range(97, 123)], k=length)
    )


def verify_determinism(results: list[str]) -> bool:
    return len(set(results)) == 1


def generate(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)
    result: list[TestCase] = []

    result.append(
        TestCase(
            name='Síla šifry: encrypt("hello world", 1)',
            func="my_encrypt",
            args=("hello world", 1),
            expected_return=lambda x: verify_encryption_strength("hello world", x)
        )
    )
    result.append(
        TestCase(
            name='Síla šifry: encrypt("hello world", 0)',
            func="my_encrypt",
            args=("hello world", 0),
            expected_return=lambda x: verify_encryption_strength("hello world", x)
        )
    )
    key = get_key()
    result.append(
        TestCase(
            name=f'Síla šifry: encrypt("hello world", {key})',
            func="my_encrypt",
            args=("hello world", key),
            expected_return=lambda x: verify_encryption_strength("hello world", x)
        )
    )
    result.append(
        TestCase(
            name='Dešifrování: decrypt(encrypt("hello world", 1), 1)',
            func="my_decrypt",
            args=LazyArgs("hello world", 1),  # type: ignore
            expected_return=lambda x: x == "hello world"
        )
    )
    result.append(
        TestCase(
            name='Dešifrování: decrypt(encrypt("hello world", 0), 0)',
            func="my_decrypt",
            args=LazyArgs("hello world", 0),  # type: ignore
            expected_return=lambda x: x == "hello world"
        )
    )
    result.append(
        TestCase(
            name='Determinismus: Šifra vrací pro stejný vstup vždy stejný výstup',
            func="my_encrypt",
            args=("hello world from the other side", 42),
            iterations=3,
            expected_return=verify_determinism
        )
    )
    for i in range(5):
        plaintext: str = get_pt()
        key: int = get_key()
        result.append(
            TestCase(
                name=f'Zátěžový test #{i + 1}: pt={plaintext}, key={key}',
                func="my_decrypt",
                args=LazyArgs(plaintext, key),  # type: ignore
                expected_return=plaintext
            )
        )
    args = LazyArgs("hello world", 1)
    result.append(
        TestCase(
            name="Šifrování souboru",
            func="my_encrypt_file",
            setup=create_dummy_file("test_files/to_encrypt", "hello world"),
            teardown=[
                delete_file("test_files/to_encrypt"),
                delete_file("test_files/to_encrypt.enc")
                ],
            file_validators={
                "test_files/to_encrypt.enc": validate_exact_text(args.ciphertext)  # type: ignore
            },
            args=("test_files/to_encrypt", args.key)  # type: ignore
        )
    )
    args = LazyArgs("hello world", 1)
    result.append(
        TestCase(
            name="Dešifrování souboru",
            func="my_decrypt_file",
            setup=create_dummy_file("test_files/to_decrypt.enc", args.ciphertext),  # type: ignore
            teardown=[
                delete_file("test_files/to_decrypt"),
                delete_file("test_files/to_decrypt.enc")
                ],
            file_validators={
                "test_files/to_decrypt": validate_exact_text(args.plaintext)
            },
            args=("test_files/to_decrypt.enc", args.key)  # type: ignore
        )
    )
    for i in range(3):
        plaintext: str = get_pt(256)
        key: int = get_key()
        args = LazyArgs(plaintext, key)
        result.append(
            TestCase(
                name=f"Zátěžový test šifrování souboru #{i + 1}",
                func="my_encrypt_file",
                setup=create_dummy_file("test_files/tmp", plaintext),
                teardown=[
                    delete_file("test_files/tmp"),
                    delete_file("test_files/tmp.enc")
                    ],
                file_validators={
                    "test_files/tmp.enc": validate_exact_text(args.ciphertext)  # type: ignore
                },
                args=("test_files/tmp", args.key)  # type: ignore
            )
        )
    for i in range(3):
        plaintext: str = get_pt(256)
        key: int = get_key()
        args = LazyArgs(plaintext, key)
        result.append(
            TestCase(
                name=f"Zátěžový test dešifrování souboru #{i + 1}",
                func="my_decrypt_file",
                setup=create_dummy_file("test_files/tmp.enc", args.ciphertext),  # type: ignore
                teardown=[
                    delete_file("test_files/tmp"),
                    delete_file("test_files/tmp.enc")
                    ],
                file_validators={
                    "test_files/tmp": validate_exact_text(args.plaintext)
                },
                args=("test_files/tmp.enc", args.key)  # type: ignore
            )
        )
    return result


def generate_bonus(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)
    result: list[TestCase] = []

    import assignment
    pt1 = "hello world from the other side"
    pt2 = "iello world from the other side"
    key = 5
    ct = assignment.my_encrypt(pt2, key)

    result.append(TestCase(
        name="KRYPTO-ANALÝZA: Test lavinového efektu (změna 1 znaku musí změnit celou šifru)",
        func="my_encrypt",
        args=(pt1, key),
        expected_return=lambda x, ct=ct: verify_avalanche_effect((ct, x))
    ))

    pt_mono = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    result.append(TestCase(
        name="KRYPTO-ANALÝZA: Nízká odolnost proti frekvenční analýze (vstup 'aaa...' nesmí generovat stejné znaky)",
        func="my_encrypt",
        args=(pt_mono, 0),
        expected_return=lambda x: verify_low_repetition(x)
    ))

    pt = "hello world to my dearest love"
    result.append(TestCase(
        name="KRYPTO-ANALÝZA: Nejsou vyzrazeny délky slov",
        func="my_encrypt",
        args=(pt, 42),
        expected_return=lambda x: verify_word_lengths_destroyed(pt, x)
    ))

    return result
