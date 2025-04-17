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

    def visit_unary_expr(self, unary):
        # Implement unary evaluation later
        return None

    def visit_binary_expr(self, binary: Binary):
        left = self.visit(binary.left)
        right = self.visit(binary.right)
        operator = binary.operator.type

        if operator == TokenType.PLUS:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            # Add error handling for invalid operand types later
            raise RuntimeError(f"Operands must be numbers for '+' operator. Got '{type(left)}' and '{type(right)}'.")
        # Add cases for other binary operators later (MINUS, STAR, etc.)
        return None