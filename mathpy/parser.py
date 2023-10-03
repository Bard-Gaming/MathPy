from .errors import MathPySyntaxError
from .parser_nodes import MultipleStatementsNode, BinaryOperationNode, VariableAssignNode, StringNode, NumberNode


class MathPyParser:
    def __init__(self, token_list: list):
        self.token_list = token_list
        self.current_token = None
        self.current_index = -1

        self.advance()

    def advance(self) -> None:
        self.current_index += 1

        if self.current_index >= len(self.token_list):
            self.current_token = None
        else:
            self.current_token = self.token_list[self.current_index]

    def is_valid_index(self, index) -> bool:
        return len(self.token_list) > index

    def parse(self) -> MultipleStatementsNode:
        return self.multiple_statements()

    # ------------ GRAMMAR IMPLEMENTATION ------------

    def atom(self, token=None):
        token = self.current_token if token is None else token

        if token.tt_type == 'TT_STRING':
            return StringNode(token)

        elif token.tt_type == 'TT_NUMBER':
            return NumberNode(token)

    def term(self) -> BinaryOperationNode:
        return self._binary_operation(['+', '-'], self.atom)

    def factor(self) -> BinaryOperationNode:
        return self._binary_operation(['*', '/', '//', '%'], self.term)

    def statement(self):
        token = self.current_token
        next_token = self.token_list[self.current_index + 1] if self.is_valid_index(self.current_index + 1) else None

        if token.tt_type == 'TT_NAME':
            if next_token is not None and next_token.tt_type == 'TT_EQUALS_SIGN':
                return self.assign_variable()

        return self.factor()

    def multiple_statements(self) -> MultipleStatementsNode:
        statement_list = []

        if self.current_token.tt_type != 'TT_NEWLINE':
            statement_list.append(self.statement())

        while self.current_token is not None and self.current_token.tt_type == 'TT_NEWLINE':
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
            raise MathPySyntaxError("=", self.current_token)
        self.advance()

        value = self.atom()
        if value is None:
            raise MathPySyntaxError("value")

        return VariableAssignNode(name, value)
