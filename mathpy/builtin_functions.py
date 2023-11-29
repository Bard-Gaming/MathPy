from .types import MathPyString, MathPyInt, MathPyFloat, MathPyNull, MathPyBool
from .interpreter import RuntimeResult
from .errors import MathPyTypeError
from random import random


def bind(instance, function, name: str = None):
    name = name if name is not None else function.__name__
    setattr(instance, name, function.__get__(instance, instance.__class__))


def function_wrapper(fnc):
    def function_call(self, *args):
        function_output = fnc(*args)

        return RuntimeResult(return_value=function_output)  # wrap in RuntimeResult

    return function_call


# ----------- Builtin Function Implementations ----------- :
def builtin_function_log(*args):
    print(*args)
    return MathPyNull()


def builtin_function_str(value, *args):
    if args:
        raise MathPyTypeError(f'str() takes 1 argument, {len(args) + 1} given.')

    return MathPyString(str(value))


def builtin_function_int(value, *args):
    if args:
        raise MathPyTypeError(f'int() takes 1 argument, {len(args) + 1} given.')

    return MathPyInt(int(value))


def builtin_function_random(*args):
    if args:
        raise MathPyTypeError(f'int() takes no arguments, {len(args)} given.')

    return MathPyFloat(random())


def builtin_function_bool(value, *args):
    if args:
        raise MathPyTypeError(f'bool() takes 1 argument, {len(args) + 1} given.')

    return MathPyBool(bool(value))


builtins_list = (
    builtin_function_log, builtin_function_str,
    builtin_function_int, builtin_function_random,
    builtin_function_bool
)

builtin_functions = {
    fnc.__name__[17:]: function_wrapper(fnc)  # [17:] to remove "builtin_function_"
    for fnc in builtins_list
}
