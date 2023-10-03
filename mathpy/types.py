from .errors import MathPyIndexError, MathPyTypeError


class MathPyString:
    # generated from language_grammar/string_base.json
    base_chars = [" ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                  "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                  "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6",
                  "7", "8", "9", "(", ")", "[", "]", "{", "}", "?", ".", "!", ":", ";", "_", "&", "#", "`", "°", "@",
                  "+", "-", "*", "/", "§", "'", ]

    base_char_lookup = {' ': 0, 'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10,
                        'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20,
                        'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26, 'A': 27, 'B': 28, 'C': 29, 'D': 30,
                        'E': 31, 'F': 32, 'G': 33, 'H': 34, 'I': 35, 'J': 36, 'K': 37, 'L': 38, 'M': 39, 'N': 40,
                        'O': 41, 'P': 42, 'Q': 43, 'R': 44, 'S': 45, 'T': 46, 'U': 47, 'V': 48, 'W': 49, 'X': 50,
                        'Y': 51, 'Z': 52, '0': 53, '1': 54, '2': 55, '3': 56, '4': 57, '5': 58, '6': 59, '7': 60,
                        '8': 61, '9': 62, '(': 63, ')': 64, '[': 65, ']': 66, '{': 67, '}': 68, '?': 69, '.': 70,
                        '!': 71, ':': 72, ';': 73, '_': 74, '&': 75, '#': 76, '`': 77, '°': 78, '@': 79, '+': 80,
                        '-': 81, '*': 82, '/': 83, '§': 84, "'": 85}
    base_number = 86

    def __init__(self, value: str | int):
        match value:
            case str():
                self.value = self.value_from_string(value)
            case int():
                self.value = value
            case _:
                raise Exception("e")

        self.length = len(self.string_from_value(self.value))

    def value_from_string(self, text: str) -> int:
        """follows: sum(digit * base^position) for every digit in a given number """
        return sum(
            self.base_char_lookup[char] * self.base_number ** position for position, char in enumerate(text))

    def string_from_value(self, value: int) -> str:
        quotient, remainder = divmod(value, self.base_number)

        text_string = self.base_chars[remainder]

        while quotient > 0:
            quotient, remainder = divmod(quotient, self.base_number)
            text_string += self.base_chars[remainder]

        return "".join(text_string)

    def reverse(self) -> "MathPyString":
        length = self.length - 1

        return MathPyString(
            sum(((self.value // self.base_number ** i) - (
                    (self.value // self.base_number ** (i + 1)) * self.base_number)) * self.base_number ** (
                        length - i)
                for i in range(length + 1)
                )
        )

    def __binary_operation(self, other, operator: str) -> "MathPyString":
        if type(other) is int:
            return MathPyString(eval(f'self.value {operator} other'))
        elif type(other) is MathPyString:
            return MathPyString(eval(f'self.value {operator} other.value'))

    def __mul__(self, other):
        return self.__binary_operation(other, '*')

    def __truediv__(self, other):
        return self.__binary_operation(other, '//')

    def __floordiv__(self, other):
        return self.__binary_operation(other, '//')

    def __add__(self, other):
        return self.__binary_operation(other, '+')

    def __sub__(self, other):
        return self.__binary_operation(other, '-')

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index: int) -> "MathPyString":
        if type(index) is not int:
            raise MathPyTypeError(f'List indices must be "int", not "{type(index).__name__}"')

        if index >= self.length:
            raise MathPyIndexError(f'Index {index} out of range')

        first_isolation = (self.value // self.base_number ** (index + 1)) * self.base_number ** (index + 1)
        return MathPyString((self.value - first_isolation) // self.base_number ** index)

    def __str__(self) -> str:
        return self.string_from_value(self.value)

    def __repr__(self) -> str:
        return f'MathPyString({self.value})'
