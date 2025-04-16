# tests/test_parser.py

import unittest
from scanner import Scanner
from parser import Parser
from ast_1 import BooleanLiteral, NilLiteral, NumberLiteral, StringLiteral, Grouping, Unary
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

if __name__ == '__main__':
    unittest.main()