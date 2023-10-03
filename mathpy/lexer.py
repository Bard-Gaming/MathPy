from .tokens import Token
from .common import module_folder
import json

with open(f'{module_folder}/language_grammar/token_types.json', 'rt', encoding='utf-8') as token_types_file:
    token_types = json.loads(token_types_file.read())


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
        name = self.current_char
        self.advance()

        while self.current_char in token_types['TT_NAME'] + token_types['TT_NAME_EXTENSION']:
            name += self.current_char
            self.advance()

        return Token(name, 'TT_NAME')

    def make_string(self) -> Token:
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

        return Token(string_value, 'TT_STRING')

    def tokenize(self) -> list[Token]:
        token_list = []

        while self.current_char is not None:
            if self.current_char in token_types['TT_IGNORE']:
                self.advance()

            elif self.current_char in token_types['TT_NEWLINE']:
                token_list.append(Token(self.current_char, 'TT_NEWLINE', self.current_line, self.current_column))
                self.advance()

            elif self.current_char in token_types['TT_EQUALS_SIGN']:
                token_list.append(Token(self.current_char, 'TT_EQUALS_SIGN', self.current_line, self.current_column))
                self.advance()

            elif self.current_char in token_types['TT_NAME']:
                token = self.make_name()
                token_list.append(token)

            elif self.current_char in token_types['TT_QUOTE']:
                token = self.make_string()
                token_list.append(token)

            else:
                raise Exception(
                    f'Illegal char {self.current_char !r} at line {self.current_line}, column {self.current_column}')

        return token_list
