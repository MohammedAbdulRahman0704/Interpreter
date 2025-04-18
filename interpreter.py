# interpreter.py

from ast_1 import Visitor, BooleanLiteral, NilLiteral, NumberLiteral, StringLiteral, Grouping, Unary, Binary
from interpreter_token import TokenType

class Interpreter(Visitor):
    def interpret(self, expression):
        return self.visit(expression)

    def visit(self, expr):
        return expr.accept(self)

    def visit_literal_expr(self, literal):
        return literal.value

    def visit_nil_literal_expr(self, literal: NilLiteral):
        return literal.value

    def visit_number_literal_expr(self, literal: NumberLiteral):
        return literal.value

    def visit_string_literal_expr(self, literal: StringLiteral):
        return literal.value

    def visit_boolean_literal_expr(self, literal: BooleanLiteral):
        return literal.value

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

    def _is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    def _is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b