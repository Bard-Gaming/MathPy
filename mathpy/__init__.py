from .lexer import MathPyLexer

def run_file(file: open) -> None:
    file_contents = file.read() + "\n"
    file.close()

    lexer = MathPyLexer(file_contents)
    tokens = lexer.tokenize()

    print(tokens)
