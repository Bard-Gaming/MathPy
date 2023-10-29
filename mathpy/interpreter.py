from .errors import MathPyNameError
from .types import MathPyNull, MathPyString, MathPyInt, MathPyFloat, MathPyFunction


class MathPySymbolTable:
    def __init__(self, *, parent: "MathPySymbolTable" = None):
        self.parent = parent
        self.table: dict = {}

    def get(self, symbol: str, *, raise_error: bool = True) -> any:
        value = self.table.get(symbol)

        if value is None:
            if self.parent is not None:  # if value not found, search in parent (if it exists)
                return self.parent.get(symbol)

            raise MathPyNameError(f'Name {symbol !r} is not defined')

        return value

    def set(self, symbol: str, new_value: any) -> None:
        if self.get(symbol) is None:
            raise MathPyNameError(f'Name {symbol !r} was not declared in current scope')

        if self.parent is not None and self.table.get(symbol) is None:
            self.parent.set(symbol, new_value)  # symbol defined in a parent, so change in parent

        self.table[symbol] = new_value  # symbol defined in self, so change own symbol table

    def declare(self, symbol: str, value: any) -> None:
        # even if symbol is declared in parent, declare new local variable
        self.table[symbol] = value if value is not None else MathPyNull()

    def __repr__(self) -> str:
        return f'MathPySymbolTable(parent={self.parent !r})'


class MathPyContext:
    def __init__(self, *, parent: "MathPyContext" = None, load_builtins: bool = False, display_name: str = "main"):
        self.parent = parent
        self.display_name = display_name
        self.symbol_table = MathPySymbolTable() if parent is None else MathPySymbolTable(parent=parent.symbol_table)

    def get(self, symbol: str) -> any:
        return self.symbol_table.get(symbol)

    def set(self, symbol: str, new_value: any) -> None:
        return self.symbol_table.set(symbol, new_value)

    def declare(self, symbol: str, value: any) -> None:
        return self.symbol_table.declare(symbol, value)

    def __str__(self) -> str:
        return f"<context at {self.display_name !r}>"

    def __repr__(self) -> str:
        return f'MathPyContext(display_name={self.display_name !r}, parent={self.parent !r})'


class MathPyInterpreter:
    def __init__(self):
        self.context = MathPyContext(load_builtins=True)

    def interpret(self, ast):
        self.visit(ast, self.context)

    def visit(self, node, context: MathPyContext):
        node_name = node.__class__.__name__  # get node class name in 'str'
        method = getattr(self, f"visit_{node_name}", self.visit_error)
        return method(node, context)

    @staticmethod
    def visit_StringNode(node, context: MathPyContext):
        return MathPyString(node.get_value())

    @staticmethod
    def visit_NumberNode(node, context: MathPyContext):
        raw_number: str = node.get_value()
        if '.' in raw_number:
            return MathPyFloat(float(raw_number))
        else:
            return MathPyInt(int(raw_number))

    @staticmethod
    def visit_NullTypeNode(node, context: MathPyContext):
        return MathPyNull()

    def visit_VariableDefineNode(self, node, context: MathPyContext):
        variable_name: str = node.get_name()
        variable_value: any = node.get_value()
        if variable_value is not None:
            variable_value = self.visit(variable_value, context)  # visit node if it's not None

        context.declare(variable_name, variable_value)

    def visit_VariableAssignNode(self, node, context: MathPyContext):
        variable_name: str = node.get_name()
        variable_value: any = self.visit(node.get_value(), context)

        context.set(variable_name, variable_value)

    def visit_VariableAccessNode(self, node, context: MathPyContext):
        variable_name: str = node.get_name()
        return self.context.get(variable_name)

    def visit_BinaryOperationNode(self, node, context: MathPyContext):
        left_value, operator, right_value = node.get_value()
        left_value = self.visit(left_value, context)  # is Parser Node, turn to Custom Type (ex: MathPyString)
        operator = operator.get_value()  # operator is Token, get 'str' value
        right_value = self.visit(right_value, context)  # is Parser Node, turn to Custom Type

        return eval(f"left_value {operator} right_value")  # return MathPyString(x) + MathPyInt(y) for instance

    def visit_MultipleStatementsNode(self, node, context: MathPyContext):
        visits: list = []
        for value in node.get_value():
            visits.append(self.visit(value, context))

        return visits

    def visit_CodeBlockNode(self, node, context: MathPyContext):
        code_block_context = MathPyContext(parent=context, load_builtins=False)
        visits = self.visit(node.get_value(), code_block_context)  # node.get_value() is MultipleStatementsNode
        return visits

    def visit_error(self, node, context):
        raise Exception(f'Unknown node name {node.__class__.__name__ !r}')
