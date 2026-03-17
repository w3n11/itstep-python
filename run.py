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
    SUCCESS = 0
    FAIL = 1
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


def prerequisite_flake8(file: str) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "-m", "flake8", file],
        capture_output=True,
        text=True
    )

    return result.returncode == 0, result.stdout


def prerequisite_noglobals(file: str) -> bool:
    with open(file, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            return False
    return True


def prerequisite_forbidden_modules(file: str) -> tuple[bool, str]:
    with open(file, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    default_allowed_modules = {
        "random",
        "math",
        "datetime",
        "typing",
        "collections",
        "time"
    }
    extra: set[str] = {}  # type: ignore
    allowed_modules = default_allowed_modules.union(extra)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base_module = alias.name.split('.')[0]
                if base_module not in allowed_modules:
                    return False, alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                base_module = node.module.split('.')[0]
                if base_module not in allowed_modules:
                    return False, node.module
    return True, ""


def prerequisite_mypy(file: str) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "-m", "mypy", file, "--ignore-missing-imports"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stdout


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

    caught_exception: Exception | None = None
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
    except StopIteration:
        log(f"[FAIL] {test.name} (Waiting for another input)", InputColor.ERROR)
        log("       Called input() too many times.", InputColor.WARNING)
        return TestResult.FAIL
    except TimeoutException:
        log(f"[FAIL] {test.name} (Timeout)", InputColor.ERROR)
        log(f"       The program has exceeded the {timeout_seconds} second time limit.", InputColor.WARNING)
        return TestResult.FAIL
    except Exception as e:
        caught_exception = e

    if test.expected_exception is not None:
        if caught_exception is None:
            log(f"[FAIL] {test.name} (Expected exception)", InputColor.ERROR)
            log(f"       Expected: {test.expected_exception.__name__}", InputColor.WARNING)
            log(f"       But your code returned {actual_return}", InputColor.WARNING)
            return TestResult.FAIL
        elif not isinstance(caught_exception, test.expected_exception):
            log(f"[FAIL] {test.name} (Invalid exception)", InputColor.ERROR)
            log(f"       Expected: {test.expected_exception.__name__}", InputColor.WARNING)
            log(f"       Received: {type(caught_exception).__name__}: {caught_exception}", InputColor.WARNING)
            return TestResult.ERROR
        else:
            log(f"[PASS] {test.name}", InputColor.SUCCESS)
            return TestResult.SUCCESS
    if caught_exception is not None:
        log(f"[FAIL] {test.name} (Exception)", InputColor.ERROR)
        log(f"       {type(caught_exception).__name__}: {caught_exception}", InputColor.WARNING)
        return TestResult.ERROR

    program_print = program_output.getvalue()

    if test.expected_print is not None and test.expected_print != program_print:
        log(f"[FAIL] {test.name} (Invalid output)", InputColor.ERROR)
        log(f"       Expected: {shorten(repr(test.expected_print))} (len={len(test.expected_print)})",
            InputColor.WARNING)
        log(f"       Received: {shorten(repr(program_print))} (len={len(program_print)})", InputColor.WARNING)
        return TestResult.FAIL

    if test.verify_print is not None and not test.verify_print(program_print):
        log(f"[FAIL] {test.name} (Invalid output)", InputColor.ERROR)
        log("       The print does not meet the specified criteria.", InputColor.WARNING)
        return TestResult.FAIL

    if test.expected_print is None and program_print != "" and test.verify_print is None:
        log(f"[FAIL] {test.name} (Unexpected output)", InputColor.ERROR)
        log(f"       {shorten(repr(program_print))} (len={len(program_print)})", InputColor.WARNING)
        return TestResult.FAIL

    if test.expected_return is not None:
        if callable(test.expected_return):
            if not test.expected_return(actual_return):
                log(f"[FAIL] {test.name} (Unexpected return value)", InputColor.ERROR)
                log(f"       {shorten(repr(actual_return))}", InputColor.WARNING)
                return TestResult.FAIL
        elif test.expected_return != actual_return:
            log(f"[FAIL] {test.name} (Invalid return)", InputColor.ERROR)
            log(f"       Expected: {shorten(repr(test.expected_return))}", InputColor.WARNING)
            log(f"       Received: {shorten(repr(actual_return))}", InputColor.WARNING)
            return TestResult.FAIL

    if test.expected_return is None and actual_return is not None:
        log(f"[FAIL] {test.name} (Unexpected return value)", InputColor.ERROR)
        log(f"       {shorten(repr(actual_return))}", InputColor.WARNING)
        return TestResult.FAIL

    log(f"[PASS] {test.name}", InputColor.SUCCESS)
    return TestResult.SUCCESS


def run_tests():
    log(divider(f"TEST RUN {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}") + "\n", InputColor.INFO)

    # --- PREREQUISITES START ---
    log("[INFO] Checking prerequisites...", InputColor.INFO)
    prerequisites_passed: bool = True
    file: str = "assignment.py"
    try:
        pep8_fulfilled, flake8_stdout = prerequisite_flake8(file)
        if not pep8_fulfilled:
            log("[FAIL] The assignment does not meet PEP 8 standard.", InputColor.ERROR)
            log(f"       {flake8_stdout}")
            prerequisites_passed = False
    except Exception as e:
        log(f"[FAIL] Unexpected error: {e}", InputColor.ERROR)
        prerequisites_passed = False

    try:
        if not prerequisite_noglobals(file):
            log("[FAIL] The assignment uses global variables.", InputColor.ERROR)
            prerequisites_passed = False
        only_allowed_modules, bad_module = prerequisite_forbidden_modules(file)
        if not only_allowed_modules:
            log(f"[FAIL] The assignment uses a forbidden module: {bad_module}", InputColor.ERROR)
            prerequisites_passed = False
        mypy_passed, mypy_stderr = prerequisite_mypy(file)
        if not mypy_passed:
            log("[FAIL] The assignment does not use stricter typing.", InputColor.ERROR)
            log(f"       {mypy_stderr}")
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
    global_start_time = time.time()

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

    log(f" Passed:          {tests_passed}", InputColor.SUCCESS if tests_passed == tests_total else InputColor.WARNING)
    log(f" Failed:          {tests_failed}", InputColor.WARNING if tests_failed > 0 else InputColor.SUCCESS)
    log(f" Exceptions:      {tests_error}", InputColor.ERROR if tests_error > 0 else InputColor.SUCCESS)
    log(f" Skipped:         {tests_skipped}", InputColor.WARNING if tests_skipped > 0 else InputColor.SUCCESS)

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
