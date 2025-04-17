# tests/test_parser.py

import unittest
from scanner import Scanner
from parser import Parser, ParseError
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
        
    def test_parse_less_than(self):
        scanner = Scanner("1 < 2")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.LESS)
        self.assertIsInstance(expression.left, NumberLiteral)
        self.assertEqual(expression.left.value, 1)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 2)

    def test_parse_less_equal(self):
        scanner = Scanner("3 <= 4")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.LESS_EQUAL)
        self.assertIsInstance(expression.left, NumberLiteral)
        self.assertEqual(expression.left.value, 3)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 4)

    def test_parse_greater_than(self):
        scanner = Scanner("5 > 6")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.GREATER)
        self.assertIsInstance(expression.left, NumberLiteral)
        self.assertEqual(expression.left.value, 5)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 6)

    def test_parse_greater_equal(self):
        scanner = Scanner("7 >= 8")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.GREATER_EQUAL)
        self.assertIsInstance(expression.left, NumberLiteral)
        self.assertEqual(expression.left.value, 7)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 8)

    def test_parse_comparison_chaining(self):
        scanner = Scanner("1 < 2 < 3")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.LESS)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 3)
        self.assertIsInstance(expression.left, Binary)
        self.assertEqual(expression.left.operator.type, TokenType.LESS)
        self.assertIsInstance(expression.left.left, NumberLiteral)
        self.assertEqual(expression.left.left.value, 1)
        self.assertIsInstance(expression.left.right, NumberLiteral)
        self.assertEqual(expression.left.right.value, 2)

    def test_parse_precedence_arithmetic_comparison(self):
        scanner = Scanner("1 + 2 < 3 * 4")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.LESS)
        self.assertIsInstance(expression.left, Binary)
        self.assertEqual(expression.left.operator.type, TokenType.PLUS)
        self.assertIsInstance(expression.left.left, NumberLiteral)
        self.assertEqual(expression.left.left.value, 1)
        self.assertIsInstance(expression.left.right, NumberLiteral)
        self.assertEqual(expression.left.right.value, 2)
        self.assertIsInstance(expression.right, Binary)
        self.assertEqual(expression.right.operator.type, TokenType.STAR)
        self.assertIsInstance(expression.right.left, NumberLiteral)
        self.assertEqual(expression.right.left.value, 3)
        self.assertIsInstance(expression.right.right, NumberLiteral)
        self.assertEqual(expression.right.right.value, 4)
    
    def test_parse_equal(self):
        scanner = Scanner("1 == 2")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.EQUAL_EQUAL)
        self.assertIsInstance(expression.left, NumberLiteral)
        self.assertEqual(expression.left.value, 1)
        self.assertIsInstance(expression.right, NumberLiteral)
        self.assertEqual(expression.right.value, 2)

    def test_parse_not_equal(self):
        scanner = Scanner("true != false")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.BANG_EQUAL)
        self.assertIsInstance(expression.left, BooleanLiteral)
        self.assertTrue(expression.left.value)
        self.assertIsInstance(expression.right, BooleanLiteral)
        self.assertFalse(expression.right.value)

    def test_parse_equality_chaining(self):
        scanner = Scanner("true == true == false")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.EQUAL_EQUAL)
        self.assertIsInstance(expression.right, BooleanLiteral)
        self.assertFalse(expression.right.value)
        self.assertIsInstance(expression.left, Binary)
        self.assertEqual(expression.left.operator.type, TokenType.EQUAL_EQUAL)
        self.assertIsInstance(expression.left.left, BooleanLiteral)
        self.assertTrue(expression.left.left.value)
        self.assertIsInstance(expression.left.right, BooleanLiteral)
        self.assertTrue(expression.left.right.value)

    def test_parse_precedence_comparison_equality(self):
        scanner = Scanner("1 < 2 == true")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.EQUAL_EQUAL)
        self.assertIsInstance(expression.right, BooleanLiteral)
        self.assertTrue(expression.right.value)
        self.assertIsInstance(expression.left, Binary)
        self.assertEqual(expression.left.operator.type, TokenType.LESS)
        self.assertIsInstance(expression.left.left, NumberLiteral)
        self.assertEqual(expression.left.left.value, 1)
        self.assertIsInstance(expression.left.right, NumberLiteral)
        self.assertEqual(expression.left.right.value, 2)

    def test_parse_precedence_equality_comparison(self):
        scanner = Scanner("true == 1 < 2")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        self.assertIsInstance(expression, Binary)
        self.assertEqual(expression.operator.type, TokenType.EQUAL_EQUAL)
        self.assertIsInstance(expression.left, BooleanLiteral)
        self.assertTrue(expression.left.value)
        self.assertIsInstance(expression.right, Binary)
        self.assertEqual(expression.right.operator.type, TokenType.LESS)
        self.assertIsInstance(expression.right.left, NumberLiteral)
        self.assertEqual(expression.right.left.value, 1)
        self.assertIsInstance(expression.right.right, NumberLiteral)
        self.assertEqual(expression.right.right.value, 2)
    
    def test_parse_empty_grouping(self): # Moved to ParserErrorTest
        pass

    def test_parse_unclosed_grouping(self): # Moved to ParserErrorTest
        pass

class ParserErrorTest(unittest.TestCase):

    def assertParseError(self, text, expected_message_part=None):
        scanner = Scanner(text)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        with self.assertRaises(ParseError) as context:
            parser.parse()
        if expected_message_part:
            self.assertIn(expected_message_part, str(context.exception))

    def test_unclosed_parentheses(self):
        self.assertParseError("(1 + 2", "Expect ')' after expression.")

    def test_missing_right_operand(self):
        self.assertParseError("1 +", "Expect expression after operator.")

    def test_unexpected_token(self):
        scanner = Scanner("1 $ 2")
        with self.assertRaises(Exception) as context: # Expect a general Exception from the scanner
            scanner.scan_tokens()
        self.assertIn("Lexical Error", str(context.exception))
        self.assertIn("Unexpected character: $", str(context.exception))

    def test_expression_followed_by_junk(self):
        self.assertParseError("1 + 2 )", "Expect end of input after expression.")

    def test_empty_expression_in_parentheses(self):
        self.assertParseError("()", "Expect expression.")

    def test_missing_operator(self):
        self.assertParseError("1 2", "Expect operator after expression.")

    def test_parse_empty_grouping(self): # Moved from ParserTest
        self.assertParseError("()", "Expect expression.")

    def test_parse_unclosed_grouping(self): # Moved from ParserTest
        self.assertParseError("(true", "Expect ')' after expression.")

if __name__ == '__main__':
    unittest.main()