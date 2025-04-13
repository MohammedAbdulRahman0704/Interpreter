from enum import Enum, auto

class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()  # Added
    RIGHT_BRACE = auto()  # Added
    EOF = auto()

class Token:
    def __init__(self, type_, lexeme, line):
        self.type = type_
        self.lexeme = lexeme
        self.line = line

    def __repr__(self):
        return f"{self.type.name} '{self.lexeme}' (line {self.line})"