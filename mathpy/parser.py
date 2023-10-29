from .errors import MathPySyntaxError
from .parser_nodes import (MultipleStatementsNode, BinaryOperationNode, VariableDefineNode, VariableAssignNode,
                           VariableAccessNode, StringNode, NumberNode, CodeBlockNode, NullTypeNode)


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

    @property
    def future_token(self):
        return self.token_list[self.current_index + 1] if self.is_valid_index(self.current_index + 1) else None

    def parse(self) -> MultipleStatementsNode:
        return self.multiple_statements()

    # ------------------ Language Grammar ------------------ :

    def atom(self, token=None):
        token = self.current_token if token is None else token

        if token.tt_type == 'TT_NAME':
            return self.access_variable()

        elif token.tt_type == 'TT_STRING':
            self.advance()
            return StringNode(token)

        elif token.tt_type == 'TT_NUMBER':
            self.advance()
            return NumberNode(token)

        elif token.tt_type == 'TT_NULL':
            self.advance()
            return NullTypeNode()

        elif token.tt_type == 'TT_LEFT_PARENTHESIS':
            self.advance()  # skip left parenthesis
            expression = self.expression()
            if self.current_token.tt_type == 'TT_RIGHT_PARENTHESIS':
                self.advance()  # skip right parenthesis
                return expression
            else:
                raise MathPySyntaxError(")", self.current_token)

    def factor(self):
        return self._binary_operation(['*', '/', '//', '%'], self.atom)

    def term(self):
        return self._binary_operation(['+', '-'], self.factor)

    def expression(self):
        return self.term()

    def statement(self):
        token = self.current_token

        if token.tt_type == 'TT_VARIABLE_DEFINE':
            return self.define_variable()

        elif token.tt_type == 'TT_NAME':
            if self.future_token is not None and self.future_token.tt_type == 'TT_EQUALS_SIGN':
                return self.assign_variable()

        elif token.tt_type == 'TT_LEFT_BRACE':
            self.advance()  # skip left brace
            code_block_body = self.multiple_statements()

            if self.current_token.tt_type == 'TT_RIGHT_BRACE':
                self.advance()  # skip right brace
                return CodeBlockNode(code_block_body)
            else:
                raise MathPySyntaxError('}', self.current_token)

        return self.expression()

    def multiple_statements(self) -> MultipleStatementsNode:
        statement_list = []

        if self.current_token.tt_type != 'TT_NEWLINE':
            statement_list.append(self.statement())

        while self.current_token is not None and self.current_token.tt_type == 'TT_NEWLINE':
            while self.current_token is not None and self.current_token.tt_type == 'TT_NEWLINE':
                self.advance()

            if self.current_token is not None:
                statement_list.append(self.statement())

        return MultipleStatementsNode(statement_list)

    # ------------------ Implementation ------------------ :

    def _binary_operation(self, operators: list, function) -> BinaryOperationNode:
        left_node = function()

        while self.current_token.get_value() in operators:
            operator = self.current_token
            self.advance()

            right_node = function()
            left_node = BinaryOperationNode(left_node, right_node, operator)

        return left_node

    def define_variable(self) -> VariableDefineNode:
        self.advance()  # skip 'var' token

        if self.current_token.tt_type != 'TT_NAME':
            raise MathPySyntaxError('name', self.current_token)
        name = self.current_token

        self.advance()

        if self.current_token.tt_type != 'TT_EQUALS_SIGN':
            return VariableDefineNode(name)  # declare without value

        else:
            self.advance()  # skip equals sign

            value = self.expression()
            return VariableDefineNode(name, value)  # declare with value

    def assign_variable(self) -> VariableAssignNode:
        name = self.current_token
        self.advance()

        if self.current_token.tt_type != 'TT_EQUALS_SIGN':
            raise MathPySyntaxError("=", self.current_token)
        self.advance()

        value = self.expression()
        if value is None:
            raise MathPySyntaxError("value")

        return VariableAssignNode(name, value)

    def access_variable(self) -> VariableAccessNode:
        if self.current_token.tt_type != 'TT_NAME':
            raise MathPySyntaxError("name", self.current_token)
        name = self.current_token

        self.advance()
        return VariableAccessNode(name)
