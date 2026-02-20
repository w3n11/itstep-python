import subprocess
import datetime
import ast
from enum import Enum
from unittest.mock import patch
import io
import contextlib
import sys
import time
import tests


class TimeoutException(BaseException):
    pass


class InputColor(Enum):
    BASE = (255, 255, 255)
    INFO = (46, 121, 220)
    WARNING = (255, 255, 71)
    ERROR = (227, 61, 59)
    SUCCESS = (4, 241, 122)
    SKIP = (191, 191, 191)


class TestResult(Enum):
    SUCCESS = 0,
    FAIL = 1,
    ERROR = 2
    SKIP = 3


def shorten(text: str, max_len: int = 60) -> str:
    text = str(text)
    if len(text) <= max_len:
        return text

    split_point = (max_len - 5) // 2
    begin = text[:split_point]
    tail = text[-split_point:]
    return f"{begin} ... {tail}"


def prerequisite_flake8(file: str) -> bool:
    result = subprocess.run(
        ["flake8", file],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return False
    return True


def prerequisite_noglobals(file: str) -> bool:
    with open(file, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            return False
    return True


def divider(text: str = "", length: int = 45):
    if text == "":
        return "═" * length
    return f" {text} ".center(length, "═")


def colored(color: tuple[int, int, int], text: str) -> str:
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m{text}\033[0m"


def log(text: str, color: InputColor = InputColor.BASE) -> None:
    print(colored(color.value, text))


# --- MODULAR TEST RUNNER START ---
def run_test(test: tests.TestCase) -> TestResult:
    import assignment
    safe_args = test.args or ()
    safe_kwargs = test.kwargs or {}

    program_output = io.StringIO()
    actual_return = None

    timeout_seconds = test.timeout
    start_time = time.time()
    target_func = getattr(assignment, test.func, None)
    if target_func is None:
        log(f"[SKIP] {test.func} (Not implemented)", InputColor.SKIP)
        return TestResult.SKIP

    def tracer(frame, event, arg):
        if time.time() - start_time > timeout_seconds:
            raise TimeoutException()
        return tracer

    try:
        with contextlib.redirect_stdout(program_output):
            with patch('builtins.input', side_effect=test.inputs):
                sys.settrace(tracer)
                try:
                    if test.iterations > 1:
                        actual_return = [target_func(*safe_args, **safe_kwargs) for _ in range(test.iterations)]
                    else:
                        actual_return = target_func(*safe_args, **safe_kwargs)
                finally:
                    sys.settrace(None)
    except TimeoutException:
        log(f"[FAIL] {test.name} (Timeout)", InputColor.ERROR)
        log(f"       The program has exceeded the {timeout_seconds} second time limit.", InputColor.WARNING)
        return TestResult.FAIL
    except Exception as e:
        log(f"[FAIL] {test.name} (Exception)", InputColor.ERROR)
        log(f"       {type(e).__name__}: {e}", InputColor.WARNING)
        return TestResult.ERROR

    program_result = program_output.getvalue()

    if test.expected_print is not None and test.expected_print != program_result:
        log(f"[FAIL] {test.name}", InputColor.ERROR)
        log(f"       Expected output: {shorten(repr(test.expected_print))} (len={len(test.expected_print)})",
            InputColor.WARNING)
        log(f"       Received output: {shorten(repr(program_result))} (len={len(program_result)})", InputColor.WARNING)
        return TestResult.FAIL

    if test.expected_return is not None:
        if callable(test.expected_return):
            if not test.expected_return(actual_return):
                log(f"[FAIL] {test.name}", InputColor.ERROR)
                log(f"       Unexpected return value: {shorten(repr(actual_return))}", InputColor.WARNING)
                return TestResult.FAIL
        elif test.expected_return != actual_return:
            log(f"[FAIL] {test.name}", InputColor.ERROR)
            log(f"       Expected return: {shorten(repr(test.expected_return))}", InputColor.WARNING)
            log(f"       Received return: {shorten(repr(actual_return))}", InputColor.WARNING)
            return TestResult.FAIL

    log(f"[PASS] {test.name}", InputColor.SUCCESS)
    return TestResult.SUCCESS


def run_tests():
    log(divider(f"TEST RUN {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}") + "\n", InputColor.INFO)
    global_start_time = time.time()

    # --- PREREQUISITES START ---
    log("[INFO] Checking prerequisites...", InputColor.INFO)
    prerequisites_passed: bool = True
    file: str = "assignment.py"
    try:
        if not prerequisite_flake8(file):
            log("[FAIL] The assignment does not meet PEP 8 standard.", InputColor.ERROR)
            prerequisites_passed = False
    except Exception as e:
        log(f"[FAIL] Unexpected error: {e}", InputColor.ERROR)
        prerequisites_passed = False

    try:
        if not prerequisite_noglobals(file):
            log("[FAIL] The assignment uses global variables.", InputColor.ERROR)
            prerequisites_passed = False
    except SyntaxError:
        log("[FAIL] Syntax error", InputColor.ERROR)
        prerequisites_passed = False
    except Exception as e:
        log(f"[FAIL] Unexpected error: {e}", InputColor.ERROR)
        prerequisites_passed = False

    try:
        output_on_import: io.StringIO = io.StringIO()
        clean_import = True
        with contextlib.redirect_stdout(output_on_import):
            import assignment  # noqa: F401 # type: ignore
            output_on_import_str = output_on_import.getvalue()
            if output_on_import_str:
                clean_import = False
        if not clean_import:
            log("[FAIL] Side effect on import (print)", InputColor.ERROR)
            log(f"       {shorten(output_on_import_str.strip())}", InputColor.WARNING)
            prerequisites_passed = False
    except Exception as e:
        log(f"[FAIL] Critical error on loading: {e}", InputColor.ERROR)
        # log("[WARN] Address this issue to your teacher.", InputColor.WARNING)
        prerequisites_passed = False

    if not prerequisites_passed:
        log("[FAIL] Prerequisites not met.", InputColor.ERROR)
        log("\n" + divider(), InputColor.INFO)
        return
    log("[PASS] Prerequisites met.", InputColor.SUCCESS)
    # --- PREREQUISITES END ---

    log("\n[INFO] Running tests...", InputColor.INFO)

    # --- TEST DEFINITIONS START ---
    test_cases: list[tests.TestCase] = tests.generate()
    # --- TEST DEFINITIONS END ---

    tests_total: int = len(test_cases)
    tests_passed: int = 0
    tests_failed: int = 0
    tests_error: int = 0
    tests_skipped: int = 0

    if tests_total == 0:
        log("[INFO] No test were defined.", InputColor.INFO)
        return
    not_implemented: list[str] = []
    for case in test_cases:
        if case.func in not_implemented:
            tests_skipped += 1
            continue

        result = run_test(case)
        if result == TestResult.SUCCESS:
            tests_passed += 1
        elif result == TestResult.FAIL:
            tests_failed += 1
        elif result == TestResult.ERROR:
            tests_error += 1
        elif result == TestResult.SKIP:
            tests_skipped += 1
            not_implemented.append(case.func)

    # --- RESULTS ---
    elapsed_time = time.time() - global_start_time
    percentage = int((tests_passed / tests_total) * 100) if tests_total > 0 else 0

    bar_length = 20
    filled = int(bar_length * tests_passed / tests_total) if tests_total > 0 else 0
    bar = "█" * filled + "░" * (bar_length - filled)

    log("\n" + divider("📊 TEST SUMMARY") + "\n", InputColor.INFO)

    log(f" Time Elapsed:    {elapsed_time:.2f}s", InputColor.BASE)
    log(f" Total Tests:     {tests_total}\n", InputColor.BASE)

    log(f" Passed:     {tests_passed}", InputColor.SUCCESS if tests_passed == tests_total else InputColor.WARNING)
    log(f" Failed:     {tests_failed}", InputColor.WARNING if tests_failed > 0 else InputColor.SUCCESS)
    log(f" Exceptions: {tests_error}", InputColor.ERROR if tests_error > 0 else InputColor.SUCCESS)
    log(f" Skipped:    {tests_skipped}", InputColor.WARNING if tests_skipped > 0 else InputColor.SUCCESS)

    print()

    bar_color = InputColor.SUCCESS if percentage == 100 else InputColor.WARNING
    print(colored(InputColor.BASE.value, " Progress: ") + colored(bar_color.value, f"{bar} {percentage}%"))

    log("\n" + divider(), InputColor.INFO)

    print()
    if tests_total == tests_passed:
        log("[PASS] All tests passed.", InputColor.SUCCESS)
    if tests_error > 0 or tests_failed > 0:
        log("[FAIL] Not all tests passed. Fix your code and try again.", InputColor.ERROR)
    if tests_skipped > 0:
        log(f"[WARN] {tests_skipped} tests skipped.", InputColor.WARNING)
    print()

    if tests_total == tests_passed and tests_total > 0:
        test_cases_bonus: list[tests.TestCase] = tests.generate_bonus()
        if len(test_cases_bonus) > 0:
            log(divider("BONUS TESTS") + "\n", InputColor.INFO)
            bonus_success: bool = True
            for case in test_cases_bonus:
                if run_test(case) != TestResult.SUCCESS:
                    bonus_success = False
            print()
            if bonus_success:
                log("[PASS] WELL DONE. YOUR CODE IS PERFECT.\n", InputColor.SUCCESS)
    log("═" * 45, InputColor.INFO)


if __name__ == "__main__":
    run_tests()
