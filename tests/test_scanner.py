# tests/test_scanner.py

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
        self.assertEqual(tokens[0].lexeme, '"Hello, World!"') # Lexeme includes the quotes
        self.assertEqual(tokens[0].literal, "Hello, World!") # Literal is the actual string value
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
        source = '"Hello\\\\nWorld"' # Corrected escape sequence for backslash
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        self.assertEqual(tokens[0].literal, "Hello\\nWorld")  # Access literal after escape sequence processing

    # Whitespace and newlines
    def test_whitespace(self):
        scanner = Scanner("   \t\n")
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 1)
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

    def test_number_literals(self):
        source = "123 45.67 0.001"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].literal, 123)

        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].literal, 45.67)

        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].literal, 0.001)

        self.assertEqual(tokens[3].type, TokenType.EOF)

    # Scanning: Identifiers
    def test_single_identifier(self):
        source = "variable"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, "variable")
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_identifier_with_underscore(self):
        source = "my_variable"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, "my_variable")
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_identifier_with_numbers(self):
        source = "count123"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, "count123")
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_identifier_starting_with_underscore(self):
        source = "_value"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, "_value")
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_identifiers_separated_by_whitespace(self):
        source = "var1   var_two\tvar3\n_var4"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, "var1")
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].lexeme, "var_two")
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[2].lexeme, "var3")
        self.assertEqual(tokens[3].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[3].lexeme, "_var4")
        self.assertEqual(tokens[4].type, TokenType.EOF)

    def test_identifier_followed_by_symbol(self):
        source = "variable;"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, "variable")
        self.assertEqual(tokens[1].type, TokenType.SEMICOLON)
        self.assertEqual(tokens[2].type, TokenType.EOF)

    # Scanning: Reserved words
    def test_reserved_word_if(self):
        source = "if"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.IF)
        self.assertEqual(tokens[0].lexeme, "if")
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_reserved_word_else(self):
        source = "else"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.ELSE)
        self.assertEqual(tokens[0].lexeme, "else")
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_reserved_word_while(self):
        source = "while"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.WHILE)
        self.assertEqual(tokens[0].lexeme, "while")
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_reserved_word_true(self):
        source = "true"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.TRUE)
        self.assertEqual(tokens[0].lexeme, "true")
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_reserved_word_false(self):
        source = "false"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.FALSE)
        self.assertEqual(tokens[0].lexeme, "false")
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_reserved_words_separated_by_whitespace(self):
        source = "if  else\twhile\ntrue false"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 6)
        self.assertEqual(tokens[0].type, TokenType.IF)
        self.assertEqual(tokens[1].type, TokenType.ELSE)
        self.assertEqual(tokens[2].type, TokenType.WHILE)
        self.assertEqual(tokens[3].type, TokenType.TRUE)
        self.assertEqual(tokens[4].type, TokenType.FALSE)
        self.assertEqual(tokens[5].type, TokenType.EOF)

    def test_reserved_word_as_part_of_identifier(self):
        source = "ifelse whileLoop"
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, "ifelse")
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].lexeme, "whileLoop")
        self.assertEqual(tokens[2].type, TokenType.EOF)

if __name__ == '__main__':
    unittest.main()