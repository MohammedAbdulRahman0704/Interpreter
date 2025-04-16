# tests/test_parser.py

import unittest
from scanner import Scanner
from parser import Parser
from ast_1 import BooleanLiteral, NilLiteral, NumberLiteral, StringLiteral, Grouping, Unary, Binary
from interpreter_token import TokenType

class ParserTest(unittest.TestCase):
    def test_parse_true(self):
        scanner = Scanner("true")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, BooleanLiteral)
        self.assertTrue(expression.value)

    def test_parse_false(self):
        scanner = Scanner("false")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, BooleanLiteral)
        self.assertFalse(expression.value)

    def test_parse_nil(self):
        scanner = Scanner("nil")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, NilLiteral)
        self.assertIsNone(expression.value)

    def test_parse_integer(self):
        scanner = Scanner("123")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, NumberLiteral)
        self.assertEqual(expression.value, 123)

    def test_parse_float(self):
        scanner = Scanner("3.14")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, NumberLiteral)
        self.assertEqual(expression.value, 3.14)

    def test_parse_decimal_start(self):
        scanner = Scanner(".5")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, NumberLiteral)
        self.assertEqual(expression.value, 0.5)

    def test_parse_decimal_end(self):
        scanner = Scanner("5.")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, NumberLiteral)
        self.assertEqual(expression.value, 5.0)

    def test_parse_string(self):
        scanner = Scanner('"hello"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, StringLiteral)
        self.assertEqual(expression.value, "hello")

    def test_parse_string_with_spaces(self):
        scanner = Scanner('"hello world"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, StringLiteral)
        self.assertEqual(expression.value, "hello world")

    def test_parse_string_with_escape_sequences(self):
        scanner = Scanner('"hello\\nworld"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, StringLiteral)
        self.assertEqual(expression.value, "hello\nworld")
        
    def test_parse_grouping(self):
        scanner = Scanner("(true)")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Grouping)
        self.assertIsInstance(expression.expression, BooleanLiteral)
        self.assertTrue(expression.expression.value)

    def test_parse_nested_grouping(self):
        scanner = Scanner("((nil))")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Grouping)
        self.assertIsInstance(expression.expression, Grouping)
        self.assertIsInstance(expression.expression.expression, NilLiteral)
        self.assertIsNone(expression.expression.expression.value)

    def test_parse_grouping_with_other_literal(self):
        scanner = Scanner("(123)")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Grouping)
        self.assertIsInstance(expression.expression, NumberLiteral)
        self.assertEqual(expression.expression.value, 123)

    def test_parse_unclosed_grouping(self):
        scanner = Scanner("(true")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsNone(expression) # Expect parse to return None due to error

    def test_parse_empty_grouping(self):
        scanner = Scanner("()")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Grouping)
        self.assertIsNone(expression.expression) # What should an empty group contain? For now, None.
    
    def test_parse_unary_not_true(self):
        scanner = Scanner("!true")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Unary)
        self.assertEqual(expression.operator.type, TokenType.BANG)
        self.assertIsInstance(expression.right, BooleanLiteral)
        self.assertTrue(expression.right.value)

    def test_parse_unary_negate_number(self):
        scanner = Scanner("-123")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Unary)
        self.assertEqual(expression.operator.type, TokenType.MINUS) # Assuming '-' is scanned as MINUS
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 123)

    def test_parse_nested_unary(self):
        scanner = Scanner("!!false")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Unary)
        self.assertEqual(expression.operator.type, TokenType.BANG)
        self.assertIsInstance(expression.right, Unary)
        self.assertEqual(expression.right.operator.type, TokenType.BANG)
        self.assertIsInstance(expression.right.right, BooleanLiteral)
        self.assertFalse(expression.right.right.value)

    def test_parse_unary_with_grouping(self):
        scanner = Scanner("! (nil)")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Unary)
        self.assertEqual(expression.operator.type, TokenType.BANG)
        self.assertIsInstance(expression.right, Grouping)
        self.assertIsInstance(expression.right.expression, NilLiteral)
    
    def test_parse_addition(self):
        scanner = Scanner("1 + 2")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.PLUS)
        self.assertIsInstance(expression.left, NumberLiteral)
        self.assertEqual(expression.left.value, 1)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 2)

    def test_parse_subtraction(self):
        scanner = Scanner("3 - 4")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.MINUS)
        self.assertIsInstance(expression.left, NumberLiteral)
        self.assertEqual(expression.left.value, 3)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 4)

    def test_parse_addition_subtraction(self):
        scanner = Scanner("1 + 2 - 3")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.MINUS)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 3)
        self.assertIsInstance(expression.left, Binary)
        self.assertEqual(expression.left.operator.type, TokenType.PLUS)
        self.assertIsInstance(expression.left.left, NumberLiteral)
        self.assertEqual(expression.left.left.value, 1)
        self.assertIsInstance(expression.left.right, NumberLiteral)
        self.assertEqual(expression.left.right.value, 2)

    def test_parse_unary_before_addition(self):
        scanner = Scanner("-1 + 2")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.PLUS)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 2)
        self.assertIsInstance(expression.left, Unary)
        self.assertEqual(expression.left.operator.type, TokenType.MINUS)
        self.assertIsInstance(expression.left.right, NumberLiteral)
        self.assertEqual(expression.left.right.value, 1)
    
    def test_parse_multiplication(self):
        scanner = Scanner("5 * 6")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.STAR)
        self.assertIsInstance(expression.left, NumberLiteral)
        self.assertEqual(expression.left.value, 5)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 6)

    def test_parse_division(self):
        scanner = Scanner("7 / 8")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.DIVIDE)
        self.assertIsInstance(expression.left, NumberLiteral)
        self.assertEqual(expression.left.value, 7)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 8)

    def test_parse_multiplication_division(self):
        scanner = Scanner("9 * 10 / 11")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.DIVIDE)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 11)
        self.assertIsInstance(expression.left, Binary)
        self.assertEqual(expression.left.operator.type, TokenType.STAR)
        self.assertIsInstance(expression.left.left, NumberLiteral)
        self.assertEqual(expression.left.left.value, 9)
        self.assertIsInstance(expression.left.right, NumberLiteral)
        self.assertEqual(expression.left.right.value, 10)

    def test_parse_precedence_addition_multiplication(self):
        scanner = Scanner("1 + 2 * 3")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.PLUS)
        self.assertIsInstance(expression.left, NumberLiteral)
        self.assertEqual(expression.left.value, 1)
        self.assertIsInstance(expression.right, Binary)
        self.assertEqual(expression.right.operator.type, TokenType.STAR)
        self.assertIsInstance(expression.right.left, NumberLiteral)
        self.assertEqual(expression.right.left.value, 2)
        self.assertIsInstance(expression.right.right, NumberLiteral)
        self.assertEqual(expression.right.right.value, 3)

    def test_parse_precedence_multiplication_addition(self):
        scanner = Scanner("1 * 2 + 3")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.PLUS)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 3)
        self.assertIsInstance(expression.left, Binary)
        self.assertEqual(expression.left.operator.type, TokenType.STAR)
        self.assertIsInstance(expression.left.left, NumberLiteral)
        self.assertEqual(expression.left.left.value, 1)
        self.assertIsInstance(expression.left.right, NumberLiteral)
        self.assertEqual(expression.left.right.value, 2)

    def test_parse_precedence_grouping(self):
        scanner = Scanner("(1 + 2) * 3")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.STAR)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 3)
        self.assertIsInstance(expression.left, Grouping)
        self.assertIsInstance(expression.left.expression, Binary)
        self.assertEqual(expression.left.expression.operator.type, TokenType.PLUS)
        self.assertIsInstance(expression.left.expression.left, NumberLiteral)
        self.assertEqual(expression.left.expression.left.value, 1)
        self.assertIsInstance(expression.left.expression.right, NumberLiteral)
        self.assertEqual(expression.left.expression.right.value, 2)

if __name__ == '__main__':
    unittest.main()