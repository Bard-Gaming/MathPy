from .lexer import MathPyLexer
from .parser import MathPyParser
from .interpreter import MathPyInterpreter
from .common import update_program_start_time


def run_file(file: open) -> None:
    file_contents = file.read()
    update_program_start_time()  # update program runtime counter

    mp_lexer = MathPyLexer(file_contents)
    tokens = mp_lexer.tokenize()

    mp_parser = MathPyParser(tokens)
    ast = mp_parser.parse()

    mp_interpreter = MathPyInterpreter()
    mp_interpreter.interpret(ast)
