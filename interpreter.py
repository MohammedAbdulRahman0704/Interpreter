# interpreter.py

from ast_1 import Visitor, BooleanLiteral, NilLiteral, NumberLiteral, StringLiteral, Grouping, Unary, Binary
from interpreter_token import TokenType

class Interpreter(Visitor):
    def interpret(self, expression):
        try:
            return self.visit(expression)
        except RuntimeError as error:
            print(error)
            return None

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

        if operator_type == TokenType.MINUS:
            if isinstance(right, (int, float)):
                return -right
            raise RuntimeError("Operand must be a number for '-' operator.")
        elif operator_type == TokenType.BANG:
            return not self._is_truthy(right)
        # Add cases for other unary operators if we have them
        return None

    def visit_binary_expr(self, binary: Binary):
        left = self.visit(binary.left)
        right = self.visit(binary.right)
        operator = binary.operator.type

        if operator == TokenType.PLUS:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            raise RuntimeError(f"Operands must be numbers for '+' operator. Got '{type(left)}' and '{type(right)}'.")
        # Add cases for other binary operators later (MINUS, STAR, etc.)
        return None

    def _is_truthy(self, value):
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True