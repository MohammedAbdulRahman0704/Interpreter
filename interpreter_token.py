from enum import Enum, auto

class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()  # Added
    SEMICOLON = auto()  # Added
    EOF = auto()
    EQUAL = 8
    EQUAL_EQUAL = 9
    BANG = auto()          # !
    BANG_EQUAL = auto()    # !=

class Token:
    def __init__(self, type_, lexeme, line):
        self.type = type_
        self.lexeme = lexeme
        self.line = line

    def __repr__(self):
        return f"{self.type.name} '{self.lexeme}' (line {self.line})"