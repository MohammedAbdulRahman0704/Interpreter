# tests/test_parser.py

import unittest
from scanner import Scanner
from parser import Parser
from ast_1 import BooleanLiteral, NilLiteral

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

if __name__ == '__main__':
    unittest.main()