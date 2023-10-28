from .errors import MathPyIndexError, MathPyTypeError, MathPyValueError
from math import log


class MathPyNull:
    def __repr__(self) -> str:
        return 'MathPyNull()'


class MathPyNumber:
    def __init__(self, value: int | float):  # To be called before self.accepted_values is changed
        self.accepted_operations = (MathPyNumber, MathPyInt, MathPyString)
        self.value = value

    # ------- Binary Operations ------- :
    def __binary_operation(self, other, operator: str):
        if isinstance(other, (float, int)):
            return self.__class__(eval(f'self.value {operator} other'))

        elif isinstance(other, self.accepted_operations):
            if isinstance(other, MathPyString):  # turn to MathPyString if 'self' or 'other' is MathPyString
                return MathPyString(eval(f'self.value {operator} other.value'))

            return self.__class__(eval(f'self.value {operator} other.value'))

        else:
            raise MathPyTypeError(
                f'Invalid operand types for {operator !r}: \'{type(self).__name__ !r}\' and {type(other).__name__ !r}')

    def __mul__(self, other):
        return self.__binary_operation(other, '*')

    def __truediv__(self, other):
        return self.__binary_operation(other, '/')

    def __floordiv__(self, other):
        return self.__binary_operation(other, '//')

    def __add__(self, other):
        return self.__binary_operation(other, '+')

    def __sub__(self, other):
        return self.__binary_operation(other, '-')

    # ------- Miscellaneous ------- :
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value})'


class MathPyInt(MathPyNumber):
    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f'{value !r} is not of type \'int\' or \'float\'')

        super().__init__(int(value))  # cast to 'int' in case it's a float


class MathPyFloat(MathPyNumber):
    def __init__(self, value):
        if not isinstance(value, float):
            raise ValueError(f'{value !r} is not of type \'float\'')

        super().__init__(value)


class MathPyString(MathPyNumber):
    # generated from language_grammar/string_base.json
    base_chars = [
        ' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'ä', 'ö', 'ü', 'é', 'è', 'ê', 'à', 'ù', 'Ä', 'Ö', 'Ü', 'È', 'Ê',
        'À', 'Ù', 'ß', 'µ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '[', ']', '{', '}', '?', '.',
        '!', ':', ';', '_', '&', '#', '`', '°', '@', '+', '-', '*', '/', '§', "'", '%',
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
        self.accepted_types = (MathPyString, MathPyInt)

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

    def reverse(self) -> "MathPyString":
        length = len(self) - 1

        return MathPyString(
            sum(
                ((self.value // self.base_number ** i) - (
                        (self.value // self.base_number ** (i + 1)) * self.base_number)) * self.base_number ** (
                        length - i) for i in range(length + 1)
            )
        )

    # ------- Binary Operations ------- :
    def __binary_operation(self, other, operator: str) -> "MathPyString":
        if isinstance(other, int):
            return MathPyString(eval(f'self.value {operator} other'))

        elif isinstance(other, self.accepted_types):
            return MathPyString(eval(f'self.value {operator} other.value'))

        else:
            raise MathPyTypeError(
                f'Invalid operand types for {operator !r}: \'MathPyString\' and {type(other).__name__ !r}')

    def __mul__(self, other) -> "MathPyString":
        return self.__binary_operation(other, '*')

    def __truediv__(self, other) -> "MathPyString":
        return self.__binary_operation(other, '//')

    def __floordiv__(self, other) -> "MathPyString":
        return self.__binary_operation(other, '//')

    def __add__(self, other) -> "MathPyString":
        return self.__binary_operation(other, '+')

    def __sub__(self, other) -> "MathPyString":
        return self.__binary_operation(other, '-')

    # ------- Logic Operations ------- :
    def __logic_operation(self, other, operator: str) -> bool:
        if isinstance(other, int):  # TODO: Change int to MathPyInt
            return eval(f'self.value {operator} other')

        elif isinstance(other, MathPyString):
            return eval(f'self.value {operator} other.value')

        else:
            raise MathPyTypeError(
                f'Invalid operand types for {operator !r}: \'MathPyString\' and {type(other).__name__ !r}')

    def __lt__(self, other) -> bool:
        return self.__logic_operation(other, '<')

    def __le__(self, other) -> bool:
        return self.__logic_operation(other, '<=')

    def __eq__(self, other) -> bool:
        return self.__logic_operation(other, '==')

    def __ge__(self, other) -> bool:
        return self.__logic_operation(other, '>=')

    def __gt__(self, other) -> bool:
        return self.__logic_operation(other, '>')

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

        first_isolation = (self.value // self.base_number ** (index + 1)) * self.base_number ** (index + 1)
        return MathPyString((self.value - first_isolation) // self.base_number ** index)

    def __contains__(self, char) -> bool:
        if isinstance(char, (str, MathPyString)):
            if len(char) > 1:
                raise MathPyValueError(f'Char must be \'MathPyString\' of length 1')

            raise NotImplementedError('Optimized way still yet to be found')

        elif isinstance(char, int):  # TODO: Change int to MathPyInt
            if char >= self.base_number:
                raise MathPyValueError(f'Char must have a value between 0 and {self.base_number - 1}')

            raise NotImplementedError('Optimized way still yet to be found')

        else:
            raise MathPyTypeError(
                f'\'in {self !s}\' requires \'MathPyString\' or \'MathPyInt\' as left operand, not {type(char).__name__ !r}')

    def __str__(self) -> str:
        return self.string_from_value(self.value)
