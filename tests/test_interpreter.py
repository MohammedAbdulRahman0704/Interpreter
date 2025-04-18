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
    
    def test_evaluate_grouping_with_operation(self):
        scanner = Scanner("(1 + 2)")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 3)
        self.assertIsInstance(result, int)
    
    def test_evaluate_unary_negate_number(self):
        scanner = Scanner("-5")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, -5)
        self.assertIsInstance(result, int)

    def test_evaluate_unary_negate_float(self):
        scanner = Scanner("-3.14")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, -3.14)
        self.assertIsInstance(result, float)

    def test_evaluate_unary_not_true(self):
        scanner = Scanner("!true")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, False)
        self.assertIsInstance(result, bool)

    def test_evaluate_unary_not_false(self):
        scanner = Scanner("!false")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_unary_not_nil(self):
        scanner = Scanner("!nil")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_unary_not_number(self):
        scanner = Scanner("!123")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, False)
        self.assertIsInstance(result, bool)

    def test_evaluate_unary_not_string(self):
        scanner = Scanner('!"hello"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, False)
        self.assertIsInstance(result, bool)

    def test_evaluate_nested_unary(self):
        scanner = Scanner("!!true")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_unary_with_grouping(self):
        scanner = Scanner("! (false)")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)
    
    def test_evaluate_binary_addition_integers(self):
        scanner = Scanner("1 + 2")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 3)
        self.assertIsInstance(result, int)

    def test_evaluate_binary_addition_floats(self):
        scanner = Scanner("3.14 + 2.0")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertAlmostEqual(result, 5.14)
        self.assertIsInstance(result, float)

    def test_evaluate_binary_subtraction_integers(self):
        scanner = Scanner("5 - 3")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 2)
        self.assertIsInstance(result, int)

    def test_evaluate_binary_subtraction_floats(self):
        scanner = Scanner("7.5 - 2.5")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 5.0)
        self.assertIsInstance(result, float)

    def test_evaluate_binary_addition_with_grouping(self):
        scanner = Scanner("(1 + 2) + 3")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 6)
        self.assertIsInstance(result, int)

    def test_evaluate_binary_subtraction_with_grouping(self):
        scanner = Scanner("5 - (3 - 1)")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 3)
        self.assertIsInstance(result, int)

    def test_evaluate_mixed_addition_subtraction(self):
        scanner = Scanner("1 + 2 - 3")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 0)
        self.assertIsInstance(result, int)
    
    def test_evaluate_binary_multiplication_integers(self):
        scanner = Scanner("3 * 4")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 12)
        self.assertIsInstance(result, int)

    def test_evaluate_binary_multiplication_floats(self):
        scanner = Scanner("2.5 * 2.0")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertAlmostEqual(result, 5.0)
        self.assertIsInstance(result, float)

    def test_evaluate_binary_division_integers(self):
        scanner = Scanner("10 / 2")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 5.0)  # Division typically results in a float
        self.assertIsInstance(result, float)

    def test_evaluate_binary_division_floats(self):
        scanner = Scanner("7.5 / 2.5")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertAlmostEqual(result, 3.0)
        self.assertIsInstance(result, float)

    def test_evaluate_binary_division_by_zero(self):
        scanner = Scanner("5 / 0")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        with self.assertRaises(RuntimeError) as context:
            interpreter.interpret(expression)
        self.assertEqual(str(context.exception), "Division by zero.")

    def test_evaluate_mixed_arithmetic(self):
        scanner = Scanner("1 + 2 * 3 - 4 / 2")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertAlmostEqual(result, 5.0) # (2 * 3) = 6, (4 / 2) = 2, 1 + 6 - 2 = 5
        self.assertIsInstance(result, float)

    def test_evaluate_arithmetic_with_grouping(self):
        scanner = Scanner("(1 + 2) * (4 - 1)")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, 9)
        self.assertIsInstance(result, int)
    
    def test_evaluate_string_concatenation(self):
        scanner = Scanner('"hello" + " world"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, "hello world")
        self.assertIsInstance(result, str)

    def test_evaluate_string_concatenation_with_grouping(self):
        scanner = Scanner('("part1" + "part") + "2"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, "part1part2")
        self.assertIsInstance(result, str)

    def test_evaluate_string_concatenation_mixed_types(self):
        scanner = Scanner('"hello" + 123')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        with self.assertRaises(RuntimeError) as context:
            interpreter.interpret(expression)
        self.assertEqual(str(context.exception), "Operands must be either both numbers or both strings for '+' operator. Got '<class 'str'>' and '<class 'int'>'.")

    def test_evaluate_number_addition_mixed_types(self):
        scanner = Scanner('123 + "hello"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        with self.assertRaises(RuntimeError) as context:
            interpreter.interpret(expression)
        self.assertEqual(str(context.exception), "Operands must be either both numbers or both strings for '+' operator. Got '<class 'int'>' and '<class 'str'>'.")
    
    def test_evaluate_equality_true(self):
        scanner = Scanner("true == true")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_equality_false(self):
        scanner = Scanner("false == false")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_inequality_true(self):
        scanner = Scanner("true != false")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_inequality_false(self):
        scanner = Scanner("false != false")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, False)
        self.assertIsInstance(result, bool)

    def test_evaluate_equality_numbers(self):
        scanner = Scanner("5 == 5")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_inequality_numbers(self):
        scanner = Scanner("5 != 6")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_equality_strings(self):
        scanner = Scanner('"hello" == "hello"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_inequality_strings(self):
        scanner = Scanner('"hello" != "world"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_equality_nil(self):
        scanner = Scanner("nil == nil")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_inequality_nil(self):
        scanner = Scanner("nil != 5")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_equality_mixed_types_false(self):
        scanner = Scanner("5 == true")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, False)
        self.assertIsInstance(result, bool)

    def test_evaluate_inequality_mixed_types_true(self):
        scanner = Scanner('"hello" != true')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_equality_nil_mixed_types_false(self):
        scanner = Scanner("nil == false")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, False)
        self.assertIsInstance(result, bool)

    def test_evaluate_inequality_nil_mixed_types_true(self):
        scanner = Scanner("nil != 0")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_equality_grouping(self):
        scanner = Scanner("(5 == 5) == true")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)

    def test_evaluate_inequality_grouping(self):
        scanner = Scanner("(5 != 5) != true")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, True)
        self.assertIsInstance(result, bool)
    
    def test_evaluate_string_concatenation(self):
        scanner = Scanner('"hello" + " world"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, "hello world")
        self.assertIsInstance(result, str)

    def test_evaluate_string_concatenation_empty_strings(self):
        scanner = Scanner('"" + ""')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, "")
        self.assertIsInstance(result, str)

    def test_evaluate_string_concatenation_one_empty(self):
        scanner = Scanner('"hello" + ""')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(expression)
        self.assertEqual(result, "hello")
        self.assertIsInstance(result, str)

    def test_evaluate_addition_string_number(self):
        scanner = Scanner('"hello" + 5')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        with self.assertRaises(RuntimeError) as context:
            interpreter.interpret(expression)
        self.assertEqual(str(context.exception), "Operands must be either both numbers or both strings for '+' operator. Got '<class 'str'>' and '<class 'int'>'.")

    def test_evaluate_addition_number_string(self):
        scanner = Scanner('5 + "hello"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        with self.assertRaises(RuntimeError) as context:
            interpreter.interpret(expression)
        self.assertEqual(str(context.exception), "Operands must be either both numbers or both strings for '+' operator. Got '<class 'int'>' and '<class 'str'>'.")

    def test_evaluate_addition_string_boolean(self):
        scanner = Scanner('"hello" + true')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        with self.assertRaises(RuntimeError) as context:
            interpreter.interpret(expression)
        self.assertEqual(str(context.exception), "Operands must be either both numbers or both strings for '+' operator. Got '<class 'str'>' and '<class 'bool'>'.")

    def test_evaluate_addition_boolean_string(self):
        scanner = Scanner('false + "world"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        with self.assertRaises(RuntimeError) as context:
            interpreter.interpret(expression)
        self.assertEqual(str(context.exception), "Operands must be either both numbers or both strings for '+' operator. Got '<class 'bool'>' and '<class 'str'>'.")

    def test_evaluate_addition_string_nil(self):
        scanner = Scanner('"hello" + nil')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        with self.assertRaises(RuntimeError) as context:
            interpreter.interpret(expression)
        self.assertEqual(str(context.exception), "Operands must be either both numbers or both strings for '+' operator. Got '<class 'str'>' and '<class 'NoneType'>'.")

    def test_evaluate_addition_nil_string(self):
        scanner = Scanner('nil + "world"')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        interpreter = Interpreter()
        with self.assertRaises(RuntimeError) as context:
            interpreter.interpret(expression)
        self.assertEqual(str(context.exception), "Operands must be either both numbers or both strings for '+' operator. Got '<class 'NoneType'>' and '<class 'str'>'.")