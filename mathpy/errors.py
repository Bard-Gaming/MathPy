class MathPySyntaxError(SyntaxError):
    def __init__(self, expected_char, error_token = None):
        if error_token is None:
            super().__init__(f'Incomplete syntax (missing {expected_char})')
        else:
            line, column = error_token.get_position()
            super().__init__(f'Expected {expected_char !r}. Got {error_token.get_value() !r} instead (line {line}, column {column})')


class MathPyIndexError(IndexError):
    pass


class MathPyIllegalCharError(SyntaxError):
    pass


class MathPyTypeError(TypeError):
    pass