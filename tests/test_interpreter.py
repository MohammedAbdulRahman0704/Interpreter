import unittest
from scanner import Scanner
from parser import Parser
from interpreter import Interpreter
from ast_1 import BooleanLiteral, NilLiteral

class InterpreterTest(unittest.TestCase):
    def test_evaluate_true(self):
        scanner = Scanner("true")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_false(self):
        scanner = Scanner("false")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, False)
        self.assertIsInstance(result, bool)

    def test_evaluate_nil(self):
        scanner = Scanner("nil")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertIsNone(result)

    def test_evaluate_grouping_boolean(self):
        scanner = Scanner("(true)")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_nested_grouping_nil(self):
        scanner = Scanner("((nil))")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertIsNone(result)
    
    def test_evaluate_number_integer(self):
        scanner = Scanner("123")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 123)
        self.assertIsInstance(result, int)

    def test_evaluate_number_float(self):
        scanner = Scanner("3.14")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 3.14)
        self.assertIsInstance(result, float)

    def test_evaluate_string(self):
        scanner = Scanner('"hello"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, "hello")
        self.assertIsInstance(result, str)

    def test_evaluate_grouping_number(self):
        scanner = Scanner("(42)")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 42)
        self.assertIsInstance(result, int)

    def test_evaluate_grouping_string(self):
        scanner = Scanner('("world")')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, "world")
        self.assertIsInstance(result, str)