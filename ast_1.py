# ast_1.py

from abc import ABC, abstractmethod
from interpreter_token import Token

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)

# Represents 'true' or 'false'
class BooleanLiteral(Literal):
    pass

# Represents 'nil'
class NilLiteral(Literal):
    def __init__(self):
        super().__init__(None)

    def accept(self, visitor):
        return visitor.visit_nil_literal_expr(self)

# Represents number literals (integers and floats)
class NumberLiteral(Literal):
    pass

    def accept(self, visitor):
        return visitor.visit_number_literal_expr(self)

# Represents string literals
class StringLiteral(Literal):
    pass

    def accept(self, visitor):
        return visitor.visit_string_literal_expr(self)

# Represents an expression grouped in parentheses
class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

# Represents a unary operation (e.g., -value, !condition)
class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

# Represents a binary operation (e.g., a + b, a - b)
class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)

class Visitor(ABC):
    @abstractmethod
    def visit_literal_expr(self, expr: Literal):
        pass

    @abstractmethod
    def visit_nil_literal_expr(self, expr: NilLiteral):
        pass

    @abstractmethod
    def visit_number_literal_expr(self, expr: NumberLiteral):
        pass

    @abstractmethod
    def visit_string_literal_expr(self, expr: StringLiteral):
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping):
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: Unary):
        pass

    @abstractmethod
    def visit_binary_expr(self, expr: Binary):
        pass

class Interpreter(Visitor):
    def interpret(self, expression):
        try:
            return self.visit(expression)
        except RuntimeError as error:
            print(error)
            return None

    def visit_boolean_literal_expr(self, literal: BooleanLiteral):
        return literal.value

    def visit_nil_literal_expr(self, literal: NilLiteral):
        return literal.value

    def visit_literal_expr(self, literal):
        # We might handle other basic literals here if needed in the future
        pass

    def visit_number_literal_expr(self, literal):
        pass

    def visit_string_literal_expr(self, literal):
        pass

    def visit_grouping_expr(self, grouping):
        return self.visit(grouping.expression)

    def visit_unary_expr(self, unary):
        pass

    def visit_binary_expr(self, binary):
        pass