from .tokens import Token
from .errors import MathPyIllegalCharError
from .common import module_folder
import json

with open(f'{module_folder}/language_grammar/token_types.json', 'rt', encoding='utf-8') as token_types_file:
    token_types = json.loads(token_types_file.read())

with open(f'{module_folder}/language_grammar/keywords.json', 'rt', encoding='utf-8') as keywords_file:
    token_keywords: dict = json.loads(keywords_file.read())


class MathPyLexer:
    default_treatment_types = token_types['TT_NEWLINE'] + token_types['TT_EQUALS_SIGN']

    def __init__(self, code_text: str):
        self.code_text = code_text
        self.current_char = None
        self.current_index = -1

        self.current_line = 0
        self.current_column = 0

        self.advance()

    def advance(self) -> None:
        if self.current_char == '\n':
            self.current_line += 1
            self.current_column = 0

        self.current_index += 1

        if self.current_index >= len(self.code_text):
            self.current_char = None
        else:
            self.current_column += 1
            self.current_char = self.code_text[self.current_index]

    def make_name(self) -> Token:
        line_start = self.current_line
        column_start = self.current_column

        name = self.current_char
        self.advance()

        while self.current_char in token_types['TT_NAME'] + token_types['_TT_NAME_EXTENSION']:
            name += self.current_char
            self.advance()

        if name in token_keywords.keys():
            return Token(name, token_keywords[name], line_start, column_start)

        return Token(name, 'TT_NAME', line_start, column_start)

    def make_string(self) -> Token:
        line_start = self.current_line
        column_start = self.current_column

        quote = self.current_char
        string_value = ''
        self.advance()

        while self.current_char not in [quote, '\n']:
            string_value += self.current_char
            self.advance()

        if self.current_char == quote:
            self.advance()
        else:
            Exception('Incomplete input')

        return Token(string_value, 'TT_STRING', line_start, column_start)

    def make_number(self) -> Token:
        line_start = self.current_line
        column_start = self.current_column

        number_string = self.current_char
        self.advance()

        while self.current_char in token_types['TT_DIGIT']:
            number_string += self.current_char
            self.advance()

        return Token(int(number_string), 'TT_NUMBER', line_start, column_start)

    # -------------------------- Tokenize process --------------------------

    def default_tokenize_treatment(self, token_list: list, token_type: str) -> None:
        token_list.append(Token(self.current_char, token_type, self.current_line, self.current_column))
        self.advance()

    def tokenize(self) -> list[Token]:
        token_list = []
        token_type_table = {
            "TT_IGNORE": lambda: self.advance(),
            "TT_NAME": lambda: token_list.append(self.make_name()),
            "TT_QUOTE": lambda: token_list.append(self.make_string()),
            "TT_DIGIT": lambda: token_list.append(self.make_number()),
        }

        while self.current_char is not None:
            current_tt_type = None
            for current_tt, tt_values in token_types.items():
                if current_tt[0] != '_' and self.current_char in tt_values:  # ignore keys that start with "_"
                    current_tt_type = current_tt

            if current_tt_type is None:  # illegal char
                raise MathPyIllegalCharError(f'Invalid character {self.current_char !r} at line {self.current_line}, column {self.current_column}')

            else:
                function = token_type_table.get(current_tt_type, lambda: self.default_tokenize_treatment(token_list, current_tt_type))
                function()

        return token_list
