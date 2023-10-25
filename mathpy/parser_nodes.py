class NumberNode:
    def __init__(self, value_token):
        self.value_token = value_token

    def get_value(self):
        return self.value_token.get_value()

    def __repr__(self) -> str:
        return f'NumberNode({self.value_token !r})'


class StringNode:
    def __init__(self, value_token):
        self.value_token = value_token

    def get_value(self):
        return self.value_token.get_value()

    def __repr__(self) -> str:
        return f'StringNode({self.value_token !r})'


class BinaryOperationNode:
    def __init__(self, left_expression, right_expression, operator):
        self.left_expression = left_expression
        self.right_expression = right_expression
        self.operator = operator

    def get_value(self) -> tuple:
        return self.left_expression, self.right_expression, self.operator

    def __repr__(self) -> str:
        return f'BinaryOperationNode({self.left_expression !r}, {self.right_expression !r}, {self.operator !r})'


class VariableDefineNode:
    def __init__(self, name, value: any = None):
        self.name = name  # name is a Token
        self.value = value  # None or a Node

    def get_name(self) -> str:
        return self.name.get_value()  # get Token's value

    def get_value(self) -> any:
        return self.value  # is either None or a Node

    def __repr__(self) -> str:
        return f'VariableDefineNode({self.name !r}, {self.value !r})'


class VariableAssignNode:
    def __init__(self, name, value: any):
        self.name = name  # name is a Token
        self.value = value  # value is a Node

    def get_name(self):
        return self.name.get_value()  # get Token's value

    def get_value(self):
        return self.value  # value is a Node

    def __repr__(self) -> str:
        return f'VariableAssignNode({self.name !r}, {self.value !r})'


class MultipleStatementsNode:
    def __init__(self, statement_list: list):
        self.statement_list = statement_list

    def get_value(self) -> list:
        return self.statement_list

    def __repr__(self) -> str:
        return f'MultipleStatementsNode({self.statement_list !r})'

