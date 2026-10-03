from dataclasses import dataclass, field
from typing import Any, Callable, Union, Optional


@dataclass
class NewInstance:
    """New instance placeholder called dynamically when code runs."""
    class_name: str
    args: tuple[Any, ...] = ()


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
    id: tuple[int, ...]

    # Name will be displayed in the test run result, it should describe what is it testing
    name: str

    # TestCase.test_ function.
    func: Callable
    args: tuple = ()
    kwargs: Optional[dict] = None
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
    prerequisites: set[tuple[int, ...]] = field(default_factory=set)

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
            if isinstance(val, NewInstance):
                args_str_inner = ", ".join(nice_format(a) for a in val.args)
                return f"{val.class_name}({args_str_inner})"

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
                    f"Objekt nemá atribut/metodu '{step.attribute_or_method}'\n\nPostup:\n" + "\n".join(trace) + "\n"
                )

            target = getattr(instance, step.attribute_or_method)

            try:
                if callable(target):
                    if not step.args:
                        call_repr += "()"
                    actual_args = []
                    for arg in step.args:
                        if isinstance(arg, NewInstance):
                            dyn_cl = getattr(assignment, arg.class_name)
                            actual_args.append(dyn_cl(*arg.args))
                        else:
                            actual_args.append(arg)
                    result = target(*actual_args)
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

    @staticmethod
    def test_func(assignment, func_name: str, *args, **kwargs) -> Any:
        if not hasattr(assignment, func_name):
            raise AssertionError(f"Funkce '{func_name}' nebyla nalezena.")

        target = getattr(assignment, func_name)
        if not callable(target):
            raise AssertionError(f"Objekt '{func_name}' není volatelný (není to funkce).")

        actual_args = []
        for arg in args:
            if type(arg).__name__ == "NewInstance":
                dyn_cl = getattr(assignment, arg.class_name)
                actual_args.append(dyn_cl(*arg.args))
            else:
                actual_args.append(arg)

        actual_kwargs = {}
        for k, v in kwargs.items():
            if type(v).__name__ == "NewInstance":
                dyn_cl = getattr(assignment, v.class_name)
                actual_kwargs[k] = dyn_cl(*v.args)
            else:
                actual_kwargs[k] = v

        try:
            return target(*actual_args, **actual_kwargs)
        except Exception as e:
            args_repr = [repr(a) for a in actual_args] + [f"{k}={repr(v)}" for k, v in actual_kwargs.items()]
            call_str = f"{func_name}({', '.join(args_repr)})"
            raise AssertionError(f"Při volání {call_str} nastala výjimka {type(e).__name__}: {e}")
