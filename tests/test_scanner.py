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

    def test_commas_and_semicolons(self):  # Added test for commas and semicolons
        scanner = Scanner(";,")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[1].type, TokenType.COMMA)
        self.assertEqual(tokens[2].type, TokenType.EOF)

if __name__ == '__main__':
    unittest.main()