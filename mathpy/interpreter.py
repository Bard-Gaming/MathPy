from .errors import MathPyNameError, MathPySyntaxError
from .types import MathPyNull, MathPyBool, MathPyString, MathPyInt, MathPyFloat, MathPyFunction


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
    def __init__(self, *, parent: "MathPyContext" = None, top_level: bool = False, display_name: str = None):
        self.parent = parent
        self.display_name = display_name
        self.symbol_table = MathPySymbolTable() if parent is None else MathPySymbolTable(parent=parent.symbol_table)
        self.top_level = top_level

        if top_level is True:
            from .builtin_functions import builtin_functions, bind
            for fnc_name, fnc in builtin_functions.items():
                mathpy_function = MathPyFunction([], "", self, fnc_name)

                bind(mathpy_function, fnc, "call")  # set mathpy.call() to fnc() (need to bind to instance)

                self.declare(fnc_name, mathpy_function)

    def is_top_level(self) -> bool:
        return self.top_level

    def get(self, symbol: str) -> any:
        return self.symbol_table.get(symbol)

    def set(self, symbol: str, new_value: any) -> None:
        return self.symbol_table.set(symbol, new_value)

    def declare(self, symbol: str, value: any) -> None:
        return self.symbol_table.declare(symbol, value)

    def __str__(self) -> str:
        return f"<context at {self.display_name}>" if self.display_name is not None else "<context>"

    def __repr__(self) -> str:
        return f'MathPyContext(display_name={self.display_name !r}, parent={self.parent !r})'


class MathPyInterpreter:
    def __init__(self):
        self.context = MathPyContext(top_level=True, display_name="'main'")

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

    @staticmethod
    def visit_BooleanNode(node, context: MathPyContext):
        return MathPyBool(node.get_value())

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

    @staticmethod
    def visit_VariableAccessNode(node, context: MathPyContext):
        variable_name: str = node.get_name()
        return context.get(variable_name)

    def visit_BinaryOperationNode(self, node, context: MathPyContext):
        left_value, operator, right_value = node.get_value()
        left_value = self.visit(left_value, context)  # is Parser Node, turn to Custom Type (ex: MathPyString)
        operator = operator.get_value()  # operator is Token, get 'str' value
        right_value = self.visit(right_value, context)  # is Parser Node, turn to Custom Type

        if operator in ("&&", "||"):
            operator = operator[0]

        return eval(f"left_value {operator} right_value")  # return MathPyString(x) + MathPyInt(y) for instance

    def visit_MultipleStatementsNode(self, node, context: MathPyContext):
        for value in node.get_value():
            if value.__class__.__name__ == 'ReturnNode':
                if context.is_top_level():  # returns are illegal at top level
                    raise MathPySyntaxError("Illegal 'return' statement at top level", default_message_format=False)

                return self.visit(value, context)  # return value of ReturnNode, stop visiting further nodes

            self.visit(value, context)  # if not a return, keep visiting node

        return MathPyNull()

    def visit_CodeBlockNode(self, node, context: MathPyContext):
        code_block_context = MathPyContext(
            parent=context, display_name=f'code block in {context.display_name !r}', top_level=context.top_level
        )  # inherit top level of parent (keep main if code block in main) for return statement
        visit_output = self.visit(node.get_value(), code_block_context)  # node.get_value() is MultipleStatementsNode

        return visit_output

    @staticmethod
    def visit_FunctionDefineNode(node, context: MathPyContext):
        function = MathPyFunction(node.get_parameter_names(), node.get_body(), context, node.get_name())
        context.declare(node.get_name(), function)

    def visit_FunctionCallNode(self, node, context: MathPyContext):
        function: MathPyFunction = self.visit(node.get_function_atom(), context)  # get function from atom

        parameter_values = [self.visit(value, context) for value in node.get_parameter_values()]

        function_output = function.call(*parameter_values)
        return function_output

    def visit_ReturnNode(self, node, context: MathPyContext):
        return_value = node.get_value()
        if return_value is None:
            return MathPyNull()

        return_value = self.visit(return_value, context)
        return return_value

    def visit_AttributeAccessNode(self, node, context: MathPyContext):
        atom = self.visit(node.get_atom(), context)
        attribute_name = node.get_attribute_name()

        attribute = getattr(atom, f'attribute_{attribute_name}', None)
        if attribute is None:
            atom.attribute_error(attribute_name)

        return attribute()  # attribute is a method without params

    def visit_MethodCallNode(self, node, context: MathPyContext):
        atom = self.visit(node.get_atom(), context)
        method_name = node.get_method_name()
        parameter_list = [self.visit(arg, context) for arg in node.get_parameter_values()]

        method = getattr(atom, f'method_{method_name}', None)
        if method is None:
            atom.method_error(method_name)

        return method(*parameter_list)

    def visit_error(self, node, context: MathPyContext):
        raise Exception(f'Unknown node name {node.__class__.__name__ !r}')
