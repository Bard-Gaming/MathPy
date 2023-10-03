from .lexer import MathPyLexer
from .parser import MathPyParser


def run_file(file: open) -> None:
    file_contents = file.read() + "\n"
    file.close()

    mp_lexer = MathPyLexer(file_contents)
    tokens = mp_lexer.tokenize()

    mp_parser = MathPyParser(tokens)
    ast = mp_parser.parse()

    print(ast)
