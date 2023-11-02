from .types import MathPyString, MathPyInt, MathPyNull
from .errors import MathPyTypeError


def bind(instance, function, name: str = None):
    name = name if name is not None else function.__name__
    setattr(instance, name, function.__get__(instance, instance.__class__))


def function_wrapper(fnc):
    def function_call(self, *args):
        function_output = fnc(*args)

        return function_output

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


builtins_list = (
    builtin_function_log, builtin_function_str,
    builtin_function_int,
)

builtin_functions = {
    fnc.__name__[17:]: function_wrapper(fnc)
    for fnc in builtins_list
}
