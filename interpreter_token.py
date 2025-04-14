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

class Token:
    def __init__(self, type_, lexeme, line):
        self.type = type_
        self.lexeme = lexeme
        self.line = line

    def __repr__(self):
        return f"{self.type.name} '{self.lexeme}' (line {self.line})"


# Example scanner method handling identifier
class Scanner:
    def _handle_identifier(self, char):
        lexeme = "identifier_example"  # You would dynamically build this
        self._add_token(TokenType.IDENTIFIER, lexeme)

    def _add_token(self, token_type, lexeme):
        # Example logic for adding the token to a list
        token = Token(token_type, lexeme, self.line)
        self.tokens.append(token)

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