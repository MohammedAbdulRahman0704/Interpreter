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

# Represents 'true', 'false', or 'nil'
class BooleanLiteral(Literal):
    pass

class NilLiteral(Literal):
    def __init__(self):
        super().__init__(None) # Nil has a value of None

    def accept(self, visitor):
        return visitor.visit_nil_literal_expr(self)

# ... (other expression types will be added later) ...

class Visitor(ABC):
    @abstractmethod
    def visit_literal_expr(self, expr: Literal):
        pass

    @abstractmethod
    def visit_nil_literal_expr(self, expr: NilLiteral):
        pass

# ... (other visit methods will be added later) ...