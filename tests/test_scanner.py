import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from scanner import Scanner
from interpreter_token import TokenType

class ScannerTest(unittest.TestCase):
    # Basic symbol tests
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
        source = "{}"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        self.assertEqual(len(tokens), 3)  # Expect 3 tokens: LEFT_BRACE, RIGHT_BRACE, EOF
        self.assertEqual(tokens[0].type, TokenType.LEFT_BRACE)
        self.assertEqual(tokens[0].line, 1)  # Ensure the line number is 1
        self.assertEqual(tokens[1].type, TokenType.RIGHT_BRACE)
        self.assertEqual(tokens[1].line, 1)  # Ensure the line number is correct


    def test_commas_and_semicolons(self):
        scanner = Scanner(";,")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[1].type, TokenType.COMMA)
        self.assertEqual(tokens[2].type, TokenType.EOF)

    # Lexical error
    def test_lexical_error(self):
        scanner = Scanner("@")
        with self.assertRaises(Exception) as context:
            scanner.scan_tokens()
        self.assertTrue("Lexical Error" in str(context.exception))

    # Equality and comparison
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
        self.assertEqual(tokens[1].type, TokenType.BANG_EQUAL)
        self.assertEqual(tokens[2].type, TokenType.EOF)

    def test_relational_operators(self):
        scanner = Scanner("< <= > >=")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.LESS)
        self.assertEqual(tokens[1].type, TokenType.LESS_EQUAL)
        self.assertEqual(tokens[2].type, TokenType.GREATER)
        self.assertEqual(tokens[3].type, TokenType.GREATER_EQUAL)
        self.assertEqual(tokens[4].type, TokenType.EOF)

    # Operators and comments
    def test_divide_operator(self):
        scanner = Scanner("a / b")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.DIVIDE)
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[3].type, TokenType.EOF)

    def test_single_line_comment(self):
        scanner = Scanner("a = 5; // This is a comment")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.EQUAL)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[4].type, TokenType.EOF)

    def test_multiline_comment(self):
        scanner = Scanner("/* This is a multi-line comment */ a = 10;")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.EQUAL)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[4].type, TokenType.EOF)

    def test_unmatched_multiline_comment(self):
        scanner = Scanner("/* This is a multi-line comment")
        with self.assertRaises(Exception) as context:
            scanner.scan_tokens()
        self.assertTrue("Unmatched block comment" in str(context.exception))

    # ✅ String literal tests
    def test_string_literal(self):
        source = '"Hello, World!"'
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        self.assertEqual(len(tokens), 2)  # Expect two tokens: STRING and EOF
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].lexeme, "Hello, World!")
        self.assertEqual(tokens[0].line, 1)  # Ensure the line is correct

    def test_unterminated_string_literal(self):
        input_code = '"This is an unterminated string'  # Unterminated string literal
        scanner = Scanner(input_code)

        # Expecting the lexical error to be raised
        with self.assertRaises(Exception) as context:
            scanner.scan_tokens()

        print(f"Exception message: {context.exception}")  # Print the exception to debug
        
        # Check if the exception message contains 'Unterminated string literal'
        self.assertTrue('Unterminated string literal' in str(context.exception))

    def test_string_with_escape_sequences(self):
        source = '"Hello\\nWorld"'
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        self.assertEqual(tokens[0].lexeme, "Hello\nWorld")  # Access lexeme, not literal

    # Whitespace and newlines
    def test_whitespace(self):
        scanner = Scanner("   \t\n")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.EOF)

    def test_newline(self):
        scanner = Scanner("a = 5;\nb = 10;")
        tokens = scanner.scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.EQUAL)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[4].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[5].type, TokenType.EQUAL)
        self.assertEqual(tokens[6].type, TokenType.NUMBER)
        self.assertEqual(tokens[7].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[8].type, TokenType.EOF)

if __name__ == '__main__':
    unittest.main()