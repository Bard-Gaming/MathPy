from .types import MathPyNull
from .errors import MathPyTypeError


def bind(instance, function, name: str = None):
    name = name if name is not None else function.__name__
    setattr(instance, name, function.__get__(instance, instance.__class__))


def function_wrapper(fnc):
    def function_call(self, *args):
        if len(args) != builtin_function_parameters[fnc.__name__]:
            raise MathPyTypeError(
                f'{self.function_name}() takes {builtin_function_parameters[fnc.__name__]} arguments, {len(args)} given.')

        function_output = fnc(*args)

        return function_output

    return function_call


# ----------- Builtin Function Implementations ----------- :
def builtin_function_log(value):
    print(value)
    return MathPyNull()


builtin_function_parameters = {
    "builtin_function_log": 1,
}

builtin_functions = {
    "log": function_wrapper(builtin_function_log),
}
