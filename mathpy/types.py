from .errors import MathPyIndexError, MathPyTypeError, MathPyValueError, MathPyAttributeError, MathPyZeroDivisionError
from math import log


class MathPyObject:
    # --------- Attributes --------- :
    def attribute_error(self, attribute_name):
        raise MathPyAttributeError(f'{self.__class__.__name__ !r} has no attribute {attribute_name !r}')

    # --------- Methods --------- :
    def method_error(self, method_name):
        raise MathPyAttributeError(f'{self.__class__.__name__ !r} has no method {method_name !r}')

    # --------- Miscellaneous --------- :
    def class_name(self) -> str:
        return self.__class__.__name__[6:]  # skip the "MathPy" in the class name

    def __int__(self):
        raise MathPyValueError(f"Can't turn {self.__class__.__name__ !r} to integer")

    def __getitem__(self, item):
        raise MathPyTypeError(f'{self.class_name() !r} is not subscriptable')

    def __repr__(self) -> str:
        return "MathPyObject()"


class MathPyIterable(MathPyObject):
    # --------- Attributes --------- :
    def attribute_length(self) -> "MathPyInt":
        return MathPyInt(len(self))

    # --------- Miscellaneous --------- :
    def __len__(self) -> int:
        raise NotImplementedError('Can\'t take length of \'MathPyIterableObject\' object (sub-class needed)')

    def __repr__(self) -> str:
        return 'MathPyIterable()'


class MathPyList(MathPyIterable, MathPyObject):
    def __init__(self, __iter):
        self.value = list(__iter)

    # --------- Methods --------- :
    def method_append(self, *args):
        if len(args) > 1:
            raise MathPyTypeError(f'list.append() takes 1 argument, {len(args)} given')

        self.value.append(args[0])

    def method_extend(self, *args):
        if len(args) > 1:
            raise MathPyTypeError(f'list.extend() takes 1 argument, {len(args)} given')
        elif not issubclass(args[0], MathPyIterable):
            raise MathPyValueError(f'list.extend() takes an iterable, got {args[0].class_name()}')

        self.value.extend(args[0])

    def method_reversed(self, *args) -> "MathPyList":
        if args:
            raise MathPyTypeError(f'list.reversed() takes 0 arguments, {len(args)} given')

        return MathPyList(reversed(self.value))

    # --------- Miscellaneous --------- :
    def __getitem__(self, __i: int) -> any:
        if __i >= len(self.value):
            raise MathPyIndexError('Index out of bounds')

        return self.value[__i]

    def __len__(self) -> int:
        return len(self.value)

    def __str__(self) -> str:
        return f'[{", ".join(str(element) for element in self.value)}]'

    def __repr__(self) -> str:
        return f'MathPyList({self.value !r})'


class MathPyNull(MathPyObject):
    # ------- Binary Operations ------- :
    def __add__(self, other):
        return other.__add__(MathPyInt(0))

    def __sub__(self, other):
        return other.__sub__(MathPyInt(0))

    def __mul__(self, other):
        return other.__mul__(MathPyInt(0))

    def __truediv__(self, other):
        raise MathPyZeroDivisionError("Can't divide by 0")

    def __floordiv__(self, other):
        raise MathPyZeroDivisionError("Can't divide by 0")

    # ------- Miscellaneous ------- :

    def __int__(self) -> int:
        return 0

    def __str__(self) -> str:
        return "null"

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "MathPyNull()"


class MathPyBool(MathPyObject):
    def __init__(self, value):
        if not isinstance(value, bool):
            raise MathPyValueError('MathPyBool value must be \'bool\'')

        self.value = value

    # ------- Binary Operations ------- :

    def __add__(self, other):
        return other.__add__(MathPyInt(int(self)))  # commutative, so this works

    def __sub__(self, other):
        other = MathPyInt(0) - other  # subtraction is non-commutative, so get opposite first, then add
        return other.__add__(MathPyInt(int(self)))

    def __mul__(self, other):
        return other.__mul__(MathPyInt(int(self)))  # commutative, so this works

    def __truediv__(self, other):
        return MathPyInt(int(self)) / other.value

    def __floordiv__(self, other):
        return MathPyInt(int(self)) // other.value

    # ------- Logic Operations ------- :
    def __or__(self, other) -> "MathPyBool":
        return MathPyBool(bool(self.value and other.value))

    def __and__(self, other) -> "MathPyBool":
        return MathPyBool(bool(self.value and other.value))

    # ------- Miscellaneous ------- :

    def __int__(self) -> int:
        return 1 * self.value  # 1 * False = 0; 1 * True = 1

    def __str__(self) -> str:
        return str(self.value).lower()

    def __bool__(self) -> bool:
        return self.value

    def __repr__(self) -> str:
        return f"MathPyBool({self.value})"


class MathPyNumber(MathPyObject):
    def __init__(self, value: int | float):  # To be called before self.accepted_values is changed
        self.accepted_operations = (MathPyFloat, MathPyInt, MathPyString, MathPyBool)
        self.value = value

    # ------- Binary Operations ------- :
    def _binary_operation(self, other, operator: str):
        if MathPyString in self.accepted_operations and isinstance(other, MathPyString):  # if you are allowed to, cast
            return MathPyString(eval(f'self.value {operator} other.value'))

        elif MathPyFloat in self.accepted_operations and isinstance(other, MathPyFloat):  # if you are allowed to, cast
            return MathPyFloat(eval(f'self.value {operator} other.value'))

        elif isinstance(other, self.accepted_operations):  # if priorities are unset, use own class
            return self.__class__(eval(f'self.value {operator} other.value'))

        else:  # Unsupported operand types error
            raise MathPyTypeError(
                f'Invalid operand types for {operator !r}: {type(self).__name__ !r} and {type(other).__name__ !r}'
            )

    def _binary_operation_divide(self, other) -> "MathPyFloat":  # always return floats for normal/true division
        if isinstance(other, self.accepted_operations):
            return MathPyFloat(self.value / other.value)
        else:
            raise MathPyTypeError(
                f'Invalid operand types for \'/\': {type(self).__name__ !r} and {type(other).__name__ !r}'
            )

    def __mul__(self, other):
        return self._binary_operation(other, '*')

    def __truediv__(self, other):
        return self._binary_operation_divide(other)

    def __floordiv__(self, other):
        return self._binary_operation(other, '//')

    def __add__(self, other):
        return self._binary_operation(other, '+')

    def __sub__(self, other):
        return self._binary_operation(other, '-')

    # ------- Logic Operations ------- :
    def _logic_operation(self, other, operator: str) -> MathPyBool:
        if isinstance(other, (MathPyString, MathPyInt, MathPyFloat)):
            return MathPyBool(eval(f'self.value {operator} other.value'))

        else:
            raise MathPyTypeError(
                f'Invalid operand types for {operator !r}: \'{self.__class__.__name__}\' and {type(other).__name__ !r}')

    def __lt__(self, other) -> MathPyBool:
        return self._logic_operation(other, '<')

    def __le__(self, other) -> MathPyBool:
        return self._logic_operation(other, '<=')

    def __eq__(self, other) -> MathPyBool:
        return self._logic_operation(other, '==')

    def __ge__(self, other) -> MathPyBool:
        return self._logic_operation(other, '>=')

    def __gt__(self, other) -> MathPyBool:
        return self._logic_operation(other, '>')

    def __or__(self, other):
        return MathPyBool(bool(self.value or other.value))

    def __and__(self, other) -> MathPyBool:
        return MathPyBool(bool(self.value and other.value))

    # ------- Miscellaneous ------- :
    def __str__(self) -> str:
        return str(self.value)

    def __bool__(self) -> bool:
        return bool(self.value)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value})'


class MathPyInt(MathPyNumber):
    def __init__(self, value):
        if not isinstance(value, int):
            raise ValueError(f'{value !r} is not of type \'int\'')

        super().__init__(value)  # cast to 'int' in case it's a float
        self.accepted_operations = (MathPyInt, MathPyFloat, MathPyString, MathPyBool)

    # --------- Methods --------- :
    def method_to_str(self, *args) -> "MathPyString":
        if args:
            raise MathPyTypeError(f'int.to_str() takes 0 arguments, {len(args)} given')

        return MathPyString(self.value)

    # --------- Miscellaneous --------- :
    def __int__(self) -> int:
        return self.value


class MathPyFloat(MathPyNumber):
    def __init__(self, value):
        if not isinstance(value, float):
            raise ValueError(f'{value !r} is not of type \'float\'')

        super().__init__(value)
        self.accepted_operations = (MathPyFloat, MathPyInt, MathPyBool)

    def __int__(self) -> int:
        return int(self.value)


class MathPyString(MathPyIterable, MathPyNumber):
    # generated from language_grammar/string_base.json
    base_chars = [
        " ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
        "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q",
        "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "ä", "ö", "ü", "é", "è", "ê", "à", "ù", "Ä", "Ö", "Ü", "È", "Ê",
        "À", "Ù", "ß", "µ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", "[", "]", "{", "}", "?", ".",
        "!", ":", ";", "_", "&", "#", "`", "°", "@", "§", "'", "\"", "+", "-", "*", "/", "%", "<", ">"
    ]

    base_char_lookup = {char: index for index, char in enumerate(base_chars)}
    base_number = len(base_chars)

    def __init__(self, value: str | int):
        match value:
            case str():
                value = self.value_from_string(value)
            case int():
                pass
            case _:
                raise MathPyTypeError(f'Expected either \'str\' or \'int\', got {type(value).__name__ !r}')

        super().__init__(value)
        self.accepted_operations = (MathPyInt, MathPyString)

    def value_from_string(self, text: str) -> int:
        """ follows: sum(digit * base^position) for every digit in a given number """
        text = reversed(text)  # 'hello' --> 'o' has position 0 --> reverse string to 'olleh' for [index = position]

        return sum(
            self.base_char_lookup[char] * self.base_number ** position for position, char in enumerate(text)
        )

    def string_from_value(self, value: int) -> str:
        quotient, remainder = divmod(value, self.base_number)

        text_string = self.base_chars[remainder]

        while quotient > 0:
            quotient, remainder = divmod(quotient, self.base_number)
            text_string += self.base_chars[remainder]

        return "".join(reversed(text_string))  # result is reversed --> reverse reversed string for original

    # ------- Binary Operations ------- :
    def __truediv__(self, other) -> "MathPyString":
        return self._binary_operation(other, '//')  # division = integer division for Strings

    # --------- Attributes --------- :
    def attribute_value(self) -> MathPyInt:
        return MathPyInt(self.value)

    # --------- Methods --------- :
    def method_to_int(self, *args) -> MathPyInt:
        if args:
            raise MathPyTypeError(f'str.to_int() takes 0 arguments, {len(args)} given')

        return MathPyInt(self.value)

    def method_reversed(self, *args) -> "MathPyString":
        if args:
            raise MathPyTypeError(f'str.reversed() takes 0 arguments, {len(args)} given')

        length = len(self) - 1

        return MathPyString(
            sum(((self.value // self.base_number ** i) - (
                    (self.value // self.base_number ** (i + 1)) * self.base_number)) * self.base_number ** (
                        length - i) for i in range(length + 1))
        )

    # ------- Miscellaneous ------- :
    def __len__(self) -> int:
        return int(log(self.value, self.base_number)) + 1  # ceil(log_{b}(x)) = len(x)

    def __getitem__(self, index: int) -> "MathPyString":
        if type(index) is not int:
            raise MathPyTypeError(f'List indices must be "int", not "{type(index).__name__}"')

        length = len(self)  # save length to variable (don't call it twice) --> O(2n) to O(n)

        if index >= length:
            raise MathPyIndexError(f'Index {index} out of range')

        index = (length - 1) - index

        first_term = self.value // self.base_number ** index
        second_term = self.value // self.base_number ** (index + 1)
        new_value = first_term - (second_term * self.base_number)
        return MathPyString(new_value)

    def __contains__(self, char) -> bool:
        if isinstance(char, (MathPyInt, MathPyString)):
            if len(char) > 1:
                raise MathPyValueError(f'Char must be \'MathPyString\' of length 1')

            raise NotImplementedError('Optimized way still yet to be found')

    def __int__(self):
        try:
            return int(str(self))
        except ValueError:
            raise MathPyValueError(f"Couldn't get 'int' value for {self}")

    def __str__(self) -> str:
        return self.string_from_value(self.value)

    def __repr__(self) -> str:
        return f"MathPyString({self.value})"


class MathPyFunction(MathPyObject):
    def __init__(self, parameter_names: list, body, parent_context, function_name: str = None):
        self.parameter_names = parameter_names
        self.body = body
        self.parent_context = parent_context
        self.function_name = function_name

    def call(self, *args):
        if len(args) != len(self.parameter_names):
            raise MathPyTypeError(
                f'{self.function_name}() takes {len(self.parameter_names)} arguments, {len(args)} given.')

        from .interpreter import MathPyContext, MathPyInterpreter
        function_context = MathPyContext(
            parent=self.parent_context, display_name=f"function {self.function_name !r}")
        function_interpreter = MathPyInterpreter()

        # Set all values for parameters in local context
        for i in range(len(args)):
            argument = args[i]
            argument_name = self.parameter_names[i]
            function_context.declare(argument_name, argument)

        function_output = function_interpreter.visit(self.body, function_context)
        return function_output

    # --------- Attributes --------- :
    def attribute_name(self):
        return MathPyString(self.function_name)

    # --------- Methods --------- :

    # --------- Miscellaneous --------- :
    def __str__(self) -> str:
        return f"<function {self.function_name !r}>"

    def __repr__(self) -> str:
        return f'MathPyFunction({self.parameter_names !r}, {self.body !r}, {self.parent_context !r}, {self.function_name !r})'
