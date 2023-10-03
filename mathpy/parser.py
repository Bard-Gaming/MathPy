from .parser_nodes import MultipleStatementsNode, BinaryOperationNode, VariableAssignNode


class MathPyParser:
    def __init__(self, ast: list):
        self.ast = ast
        self.current_token = None
        self.current_index = -1

    def advance(self) -> None:
        self.current_index += 1

        if self.current_index >= len(self.ast):
            self.current_token = None
        else:
            self.current_token = self.ast[self.current_index]

    def is_valid_index(self, index) -> bool:
        return len(self.ast) > index

    def parse(self) -> MultipleStatementsNode:
        return self.multiple_statements()

    def atom(self, token=None):
        token = self.current_token if token is None else token

    def term(self):
        return self._binary_operation(['+', '-'], self.atom)

    def factor(self):
        return self._binary_operation(['*', '/', '//', '%'], self.term)

    def statement(self):
        token = self.current_token
        next_token = self.ast[self.current_index + 1] if self.is_valid_index(self.current_index + 1) else None

        if token.tt_type == 'TT_NAME':
            if next_token is not None and next_token.tt_type == 'TT_EQUALS_SIGN':
                return self.assign_variable()

        return self.factor()

    def multiple_statements(self) -> MultipleStatementsNode:
        statement_list = []

        while self.current_token.tt_type == 'TT_NEWLINE':
            while self.current_token.tt_type == 'TT_NEWLINE':
                self.advance()

            if self.current_token is not None:
                statement_list.append(self.statement())

        return MultipleStatementsNode(statement_list)

    def _binary_operation(self, operators: list, function, left_function=None) -> BinaryOperationNode:
        left_function = function if left_function is None else left_function

        left_node = left_function()

        if self.current_token.get_value() in operators:
            operator = self.current_token
            self.advance()

            right_node = function()
            left_node = BinaryOperationNode(left_node, right_node, operator)
        return left_node

    def assign_variable(self) -> VariableAssignNode:
        name = self.current_token
        self.advance()

        if self.current_token.tt_type != 'TT_EQUALS_SIGN':
            raise Exception('Syntax error: bla bla')
        self.advance()

        value = self.atom()

        return VariableAssignNode(name, value)

