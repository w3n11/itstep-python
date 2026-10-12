import random  # noqa: F401
from typing import Any  # noqa: F401
from test import TestCase, Procedure, NewInstance  # noqa: F401 # type: ignore


# --- HELPER FUNCTIONS START ---

def verify_finally_cleanup(assignment) -> bool:
    try:
        sys_obj = assignment.Server()
    except AttributeError:
        raise AssertionError("Třída 'Server' nebyla nalezena.")

    class SpyStr(str):
        def __eq__(self, other):
            if getattr(sys_obj, "is_connected", False) is not True:
                raise AssertionError("Chyba: 'is_connected' zůstalo na False. (Server se nepřipojil.)")
            return str(self) == other

    try:
        sys_obj.execute_command(SpyStr("CRASH"))
    except SystemError:
        pass
    except AssertionError as e:
        raise e
    except Exception as e:
        raise AssertionError(f"Očekáván SystemError při příkazu 'CRASH', ale vyletěl {type(e).__name__}")

    if getattr(sys_obj, "is_connected", True):
        raise AssertionError("Spojení zůstalo otevřené. Blok 'finally' úklid po chybě neprovedl.")

    try:
        sys_obj.execute_command(SpyStr("PING"))
    except AssertionError as e:
        raise e
    except Exception as e:
        raise AssertionError(f"Při jiném příkazu (např. 'PING') server padat neměl, ale vyletěl {type(e).__name__}")

    if getattr(sys_obj, "is_connected", True):
        raise AssertionError("Spojení zůstalo otevřené. Blok 'finally' musí spojení uzavřít vždy.")

    return True

# --- HELPER FUNCTIONS END ---


def generate(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)

    result: list[TestCase] = [
        TestCase(
            id=(1, 0),
            name="ExceptionRaiser existuje",
            func=TestCase.test_class_init,
            args=(
                "ExceptionRaiser", tuple()
            ),
            expected_return=True
        ),
    ]

    exceptions_tested: dict[str, Any] = {
        "arithmetic_error": ArithmeticError,
        "attribute_error": AttributeError,
        # "import_error": ImportError,
        "lookup_error": LookupError,
        "os_error": OSError,
        "runtime_error": RuntimeError,
        "value_error": ValueError
    }
    for i, key in enumerate(exceptions_tested.keys(), start=1):
        result.append(
            TestCase(
                id=(1, i),
                name=f"ExceptionRaiser.{key}",
                func=TestCase.test_class,
                args=(
                    "ExceptionRaiser", Procedure()
                    .add(key),
                    tuple()
                ),
                expected_exception=exceptions_tested[key],  # type: ignore
                prerequisites={(1, 0)}
            )
        )
    result.extend([
        TestCase(
            id=(1, len(exceptions_tested) + 1),
            name="ExceptionRaiser nesmí použít 'raise'",
            func=TestCase.test_forbidden_raise,
            args=(
                "ExceptionRaiser",
            ),
            expected_return=True,
            prerequisites={(1, len(exceptions_tested))}
        ),
        TestCase(
            id=(2, 0),
            name="Server",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("firewall_enabled", expected_return_or_value=False)
                .add("enable_firewall", expected_return_or_value=None)
                .add("firewall_enabled", expected_return_or_value=True),
                tuple()
            ),
            expected_return=True,
            prerequisites={(1, len(exceptions_tested) + 1)}
        ),
        TestCase(
            id=(2, 1),
            name="receive_payload('0x08DEADDROP')",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("receive_payload", args=("0x08DEADDROP",), expected_return_or_value="DEADDROP"),
            ),
            expected_return=True,
            prerequisites={(2, 0)}
        ),
        TestCase(
            id=(2, 2),
            name="receive_payload('Ox08DEADDROP')",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("receive_payload", args=("Ox08DEADDROP",), ignore=True),
            ),
            expected_exception=ValueError,
            prerequisites={(2, 1)}
        ),
        TestCase(
            id=(2, 3),
            name="receive_payload('08DEADDROP')",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("receive_payload", args=("08DEADDROP",), ignore=True),
            ),
            expected_exception=ValueError,
            prerequisites={(2, 2)}
        ),
        TestCase(
            id=(2, 4),
            name="receive_payload('0x04PINKY')",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("receive_payload", args=("0x04PINKY",), ignore=True),
            ),
            expected_exception=ValueError,
            prerequisites={(2, 3)}
        ),
        TestCase(
            id=(2, 5),
            name="receive_payload('0x04PINKY')",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("receive_payload", args=("0x06LEVEL",), ignore=True),
            ),
            expected_exception=ValueError,
            prerequisites={(2, 4)}
        ),
        TestCase(
            id=(2, 6),
            name="receive_payload('0x00')",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("receive_payload", args=("0x00",), expected_return_or_value=""),
            ),
            expected_return=True,
            prerequisites={(2, 5)}
        ),
        TestCase(
            id=(2, 7),
            name="receive_payload(0x01)",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("receive_payload", args=(0x01,), ignore=True),
            ),
            expected_exception=TypeError,
            prerequisites={(2, 6)}
        ),
        TestCase(
            id=(2, 8),
            name="receive_payload(123456789)",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("receive_payload", args=(123456789,), ignore=True),
            ),
            expected_exception=TypeError,
            prerequisites={(2, 7)}
        ),
        TestCase(
            id=(3, 0),
            name="SecurityError existuje",
            func=TestCase.test_class_init,
            args=(
                "SecurityError", tuple()
            ),
            expected_return=True,
            prerequisites={(2, 8)}
        ),
        TestCase(
            id=(3, 1),
            name="SecurityError dědí z Exception",
            func=TestCase.test_class_inheritance,
            args=(
                "SecurityError", "Exception"
            ),
            expected_return=True,
            prerequisites={(3, 0)}
        ),
        TestCase(
            id=(3, 2),
            name="receive_payload('0x08DEADDROP') (zapnutý firewall)",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("enable_firewall")
                .add("receive_payload", args=("0x08DEADDROP",), expected_return_or_value="DEADDROP"),
            ),
            expected_return=True,
            prerequisites={(3, 1)}
        ),
        TestCase(
            id=(3, 3),
            name="receive_payload('Ox08DEADDROP') (zapnutý firewall)",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("enable_firewall")
                .add("receive_payload", args=("Ox08DEADDROP",), ignore=True),
            ),
            expected_exception=NewInstance("SecurityError"),
            prerequisites={(3, 2)}
        ),
        TestCase(
            id=(3, 4),
            name="receive_payload('08DEADDROP') (zapnutý firewall)",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("enable_firewall")
                .add("receive_payload", args=("08DEADDROP",), ignore=True),
            ),
            expected_exception=NewInstance("SecurityError"),
            prerequisites={(3, 3)}
        ),
        TestCase(
            id=(3, 5),
            name="receive_payload('0x04PINKY') (zapnutý firewall)",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("enable_firewall")
                .add("receive_payload", args=("0x04PINKY",), ignore=True),
            ),
            expected_exception=NewInstance("SecurityError"),
            prerequisites={(3, 4)}
        ),
        TestCase(
            id=(3, 6),
            name="receive_payload('0x04PINKY') (zapnutý firewall)",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("enable_firewall")
                .add("receive_payload", args=("0x06LEVEL",), ignore=True),
            ),
            expected_exception=NewInstance("SecurityError"),
            prerequisites={(3, 5)}
        ),
        TestCase(
            id=(3, 7),
            name="receive_payload('0x00') (zapnutý firewall)",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("enable_firewall")
                .add("receive_payload", args=("0x00",), expected_return_or_value=""),
            ),
            expected_return=True,
            prerequisites={(3, 6)}
        ),
        TestCase(
            id=(3, 8),
            name="receive_payload(0x01) (zapnutý firewall)",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("enable_firewall")
                .add("receive_payload", args=(0x01,), ignore=True),
            ),
            expected_exception=NewInstance("SecurityError"),
            prerequisites={(3, 7)}
        ),
        TestCase(
            id=(3, 9),
            name="receive_payload(123456789) (zapnutý firewall)",
            func=TestCase.test_class,
            args=(
                "Server", Procedure()
                .add("enable_firewall")
                .add("receive_payload", args=(123456789,), ignore=True),
            ),
            expected_exception=NewInstance("SecurityError"),
            prerequisites={(3, 8)}
        )
    ])

    return result


def generate_bonus(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)
    result: list[TestCase] = [
        TestCase(
            id=(4, 0),
            name="Bonus: Server.execute_command() existuje",
            func=TestCase.test_class_definition,
            args=("Server", "execute_command", (), False),
            expected_return=True
        ),
        TestCase(
            id=(4, 1),
            name="Bonus: Spojení se pomocí 'finally' bezpečně uzavře za všech okolností",
            func=verify_finally_cleanup,
            expected_return=True,
            prerequisites={(4, 0)}
        )
    ]
    return result
