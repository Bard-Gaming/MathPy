from .lexer import MathPyLexer
from .parser import MathPyParser
from .interpreter import MathPyInterpreter


def run_file(file: open) -> None:
    file_contents = file.read() + "\n"
    file.close()

    mp_lexer = MathPyLexer(file_contents)
    tokens = mp_lexer.tokenize()

    mp_parser = MathPyParser(tokens)
    ast = mp_parser.parse()

    print(ast)

    mp_interpreter = MathPyInterpreter(ast)
    mp_interpreter.interpret()

    print(mp_interpreter.context.symbol_table.table)
