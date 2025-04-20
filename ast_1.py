# ast_1.py

from abc import ABC, abstractmethod
from interpreter_token import Token, TokenType

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

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

    def visit_unary_expr(self, unary: Unary):
        right = self.visit(unary.right)
        operator_type = unary.operator.type

        if operator_type is TokenType.MINUS:
            if isinstance(right, (int, float)):
                return -right
            raise RuntimeError("Operand must be a number for '-' operator.")
        elif operator_type is TokenType.BANG:
            return not self._is_truthy(right)
        return None

    def visit_binary_expr(self, binary: Binary):
        left = self.visit(binary.left)
        right = self.visit(binary.right)
        operator = binary.operator.type

        if operator is TokenType.PLUS:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            elif isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError(f"Operands must be either both numbers or both strings for '+' operator. Got '{type(left)}' and '{type(right)}'.")
        elif operator is TokenType.MINUS:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left - right
            raise RuntimeError(f"Operands must be numbers for '-' operator. Got '{type(left)}' and '{type(right)}'.")
        elif operator is TokenType.STAR:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left * right
            raise RuntimeError(f"Operands must be numbers for '*' operator. Got '{type(left)}' and '{type(right)}'.")
        elif operator is TokenType.DIVIDE:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                if right == 0:
                    raise RuntimeError("Division by zero.")
                return left / right
            raise RuntimeError(f"Operands must be numbers for '/' operator. Got '{type(left)}' and '{type(right)}'.")
        elif operator is TokenType.GREATER:
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise RuntimeError(f"Operands must be numbers for '>' operator. Got '{type(left)}' and '{type(right)}'.")
            return left > right
        elif operator is TokenType.GREATER_EQUAL:
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise RuntimeError(f"Operands must be numbers for '>=' operator. Got '{type(left)}' and '{type(right)}'.")
            return left >= right
        elif operator is TokenType.LESS:
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise RuntimeError(f"Operands must be numbers for '<' operator. Got '{type(left)}' and '{type(right)}'.")
            return left < right
        elif operator is TokenType.LESS_EQUAL:
            if not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise RuntimeError(f"Operands must be numbers for '<=' operator. Got '{type(left)}' and '{type(right)}'.")
            return left <= right
        elif operator is TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)
        elif operator is TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)
        return None

    def visit_print_stmt(self, stmt: 'Print'):
        value = self.visit(stmt.expression)
        print(self._stringify(value))
        return None  # Print statements don't return a value

    def _is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    def _stringify(self, value):
        if value is None:
            return "nil"
        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        if isinstance(value, bool):
            return str(value).lower()
        return str(value)

class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)