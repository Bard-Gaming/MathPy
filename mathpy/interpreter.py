from .errors import MathPyNameError
from .types import MathPyNull, MathPyString, MathPyInt, MathPyFloat


class MathPySymbolTable:
    def __init__(self, *, parent: "MathPySymbolTable" = None):
        self.parent = parent
        self.table: dict = {}

    def get(self, symbol: str, *, raise_error: bool = True) -> any:
        value = self.table.get(symbol)
        if value is None and self.parent is not None:
            value = self.parent.get(symbol, raise_error=raise_error)  # propagate raise_error

        elif value is None and self.parent is None and raise_error is True:
            raise MathPyNameError(f'Name {symbol !r} is not defined')

        elif value is None and self.parent is None and raise_error is False:
            value = None

        return value

    def set(self, symbol: str, new_value: any) -> None:
        if self.parent is not None and self.parent.get(symbol) is not None:
            self.parent.set(symbol, new_value)  # change value in parent table
            return

        symbol_value = self.get(symbol, raise_error=False)  # store value to avoid multiple calls

        if symbol_value is None:
            raise MathPyNameError(f'Name {symbol !r} was not declared in current scope')

        self.table[symbol] = new_value  # safe to set value now

    def declare(self, symbol: str, value: any) -> None:
        self.table[symbol] = value if value is not None else MathPyNull()

    def __repr__(self) -> str:
        return f'MathPySymbolTable(parent={self.parent !r})'


class MathPyContext:
    def __init__(self, *, parent: "MathPyContext" = None, load_builtins: bool = False):
        self.parent = parent
        self.symbol_table = MathPySymbolTable() if parent is None else MathPySymbolTable(parent=parent.symbol_table)

    def get(self, symbol: str) -> any:
        return self.symbol_table.get(symbol)

    def set(self, symbol: str, new_value: any) -> None:
        return self.symbol_table.set(symbol, new_value)

    def declare(self, symbol: str, value: any) -> None:
        return self.symbol_table.declare(symbol, value)

    def __repr__(self) -> str:
        return f'MathPyContext(parent={self.parent !r})'


class MathPyInterpreter:
    def __init__(self, abstract_syntax_tree):
        self.abstract_syntax_tree = abstract_syntax_tree
        self.context = MathPyContext(load_builtins=True)

    def interpret(self):
        self.visit(self.abstract_syntax_tree, self.context)

    def visit(self, node, context: MathPyContext):
        node_name = node.__class__.__name__  # get node class name in 'str'
        method = getattr(self, f"visit_{node_name}", self.visit_error)
        return method(node, context)

    def visit_StringNode(self, node, context: MathPyContext):
        return MathPyString(node.get_value())

    def visit_NumberNode(self, node, context: MathPyContext):
        raw_number = node.get_value()
        if '.' in raw_number:
            return MathPyFloat(float(raw_number))
        else:
            return MathPyInt(int(raw_number))

    def visit_VariableDefineNode(self, node, context: MathPyContext):
        variable_name: str = node.get_name()
        variable_value = node.get_value()
        if variable_value is not None:
            variable_value = self.visit(variable_value, context)  # visit node if it's not None

        context.declare(variable_name, variable_value)

    def visit_VariableAssignNode(self, node, context: MathPyContext):
        variable_name: str = node.get_name()
        variable_value = self.visit(node.get_value(), context)

        context.set(variable_name, variable_value)

    def visit_BinaryOperationNode(self, node, context: MathPyContext):
        left_value, operator, right_value = node.get_value()
        left_value = self.visit(left_value, context)
        operator = operator.get_value()  # operator was Token, now str
        right_value = self.visit(right_value, context)

        print(eval(f"left_value {operator} right_value"))

        return eval(f"left_value {operator} right_value")

    def visit_MultipleStatementsNode(self, node, context):
        visits: list = []
        for value in node.get_value():
            visits.append(self.visit(value, context))

        return visits

    def visit_error(self, node, context):
        raise Exception(f'Unknown node name {node.__class__.__name__ !r}')
