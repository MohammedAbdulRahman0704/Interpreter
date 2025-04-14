import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from scanner import Scanner
from interpreter_token import TokenType

class ScannerTest(unittest.TestCase):
    def test_empty_file(self):
        scanner = Scanner("")
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)

    def test_parentheses(self):
        scanner = Scanner("()")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.LEFT_PAREN)
        self.assertEqual(tokens[1].type, TokenType.RIGHT_PAREN)
        self.assertEqual(tokens[2].type, TokenType.EOF)

    def test_braces(self):
        scanner = Scanner("{}")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.LEFT_BRACE)
        self.assertEqual(tokens[1].type, TokenType.RIGHT_BRACE)
        self.assertEqual(tokens[2].type, TokenType.EOF)

    def test_commas_and_semicolons(self):
        scanner = Scanner(";,")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[1].type, TokenType.COMMA)
        self.assertEqual(tokens[2].type, TokenType.EOF)

    def test_lexical_error(self):
        scanner = Scanner("@")
        with self.assertRaises(Exception) as context:
            scanner.scan_tokens()
        self.assertTrue("Lexical Error: Invalid character '@'" in str(context.exception))

    def test_assignment_and_equality(self):
        scanner = Scanner("== =")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.EQUAL_EQUAL)
        self.assertEqual(tokens[1].type, TokenType.EQUAL)
        self.assertEqual(tokens[2].type, TokenType.EOF)

    def test_negation_and_inequality(self):
        scanner = Scanner("! !=")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.BANG)
        self.assertEqual(tokens[0].lexeme, "!")
        self.assertEqual(tokens[1].type, TokenType.BANG_EQUAL)
        self.assertEqual(tokens[1].lexeme, "!=")
        self.assertEqual(tokens[2].type, TokenType.EOF)
    
    def test_relational_operators(self):
        scanner = Scanner("< <= > >=")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.LESS)
        self.assertEqual(tokens[1].type, TokenType.LESS_EQUAL)
        self.assertEqual(tokens[2].type, TokenType.GREATER)
        self.assertEqual(tokens[3].type, TokenType.GREATER_EQUAL)
        self.assertEqual(tokens[4].type, TokenType.EOF)

    # Test Division operator
    def test_divide_operator(self):
        scanner = Scanner("a / b")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.DIVIDE)
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[3].type, TokenType.EOF)

    # Test Single-line Comment
    def test_single_line_comment(self):
        scanner = Scanner("a = 5; // This is a comment")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.EQUAL)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[4].type, TokenType.EOF)

    # Test Multi-line Comment
    def test_multiline_comment(self):
        scanner = Scanner("/* This is a multi-line comment */ a = 10;")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.EQUAL)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[4].type, TokenType.EOF)

if __name__ == '__main__':
    unittest.main()