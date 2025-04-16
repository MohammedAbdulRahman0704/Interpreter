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

# ... (other visit methods will be added later) ...