from enum import Enum, auto

class TokenType(Enum):
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    COMMA = 5
    SEMICOLON = 6
    EOF = 7
    EQUAL = 8
    EQUAL_EQUAL = 9
    BANG = 10
    BANG_EQUAL = 11
    LESS = 12
    LESS_EQUAL = 13
    GREATER = 14
    GREATER_EQUAL = 15
    DIVIDE = 16
    IDENTIFIER = 17  # Added identifier
    NUMBER = "NUMBER"
    STRING = 19

class Token:
    def __init__(self, type, lexeme, line):
        self.type = type
        self.lexeme = lexeme  # You can use this to store the string value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.lexeme}, {self.line})"


# Example scanner method handling identifier
class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def _advance(self):
        """Advance to the next character in the source and return the character."""
        char = self.source[self.current]
        self.current += 1
        if char == '\n':  # Increment line number on newline
            self.line += 1
        return char

    def _peek(self):
        """Returns the character at the current position, or a null character if at the end."""
        if self._is_at_end():
            return '\0'
        return self.source[self.current]

    def _is_at_end(self):
        """Returns True if the scanner has reached the end of the source."""
        return self.current >= len(self.source)

    def _add_token(self, type_, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, literal, self.line))

    def _handle_identifier(self, char):
        """Handles identifiers (variable names, keywords, etc.)."""
        lexeme = char
        while self._peek().isalnum() or self._peek() == '_':
            lexeme += self._advance()  # Build identifier dynamically
        self._add_token(TokenType.IDENTIFIER, lexeme)

    def _handle_number(self, char):
        """Handles numbers (integers or floats)."""
        lexeme = char
        while self._peek().isdigit():
            lexeme += self._advance()
        if self._peek() == '.':  # Check for decimal point (float)
            lexeme += self._advance()
            while self._peek().isdigit():
                lexeme += self._advance()
        self._add_token(TokenType.NUMBER, lexeme)  # Correct usage of TokenType.NUMBER
        
    def _handle_string(self):
        string_value = ""
        while True:
            char = self._advance()

            if char == '"':  # End of string literal
                break
            elif char == '\n':  # Newline within string (should not happen in a valid string)
                self.line += 1
                self._handle_lexical_error("Unterminated string literal")
            elif char == '\\':  # Escape sequence
                next_char = self._peek()
                if next_char == 'n':
                    string_value += '\n'
                    self._advance()  # Skip the 'n'
                elif next_char == 't':
                    string_value += '\t'
                    self._advance()  # Skip the 't'
                elif next_char == '\\':
                    string_value += '\\'
                    self._advance()  # Skip the '\\'
                elif next_char == '"':
                    string_value += '"'
                    self._advance()  # Skip the '"'
                else:
                    string_value += '\\' + next_char
                    self._advance()  # Skip the next character
            else:
                string_value += char  # Regular character

        # If we finish the loop without encountering a closing quote, raise an error
        if self._peek() != '"':
            self._handle_lexical_error("Unterminated string literal")

        self.tokens.append(Token(TokenType.STRING, string_value, self.line))