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

class Token:
    def __init__(self, type_, lexeme, line):
        self.type = type_
        self.lexeme = lexeme
        self.line = line

    def __repr__(self):
        return f"{self.type.name} '{self.lexeme}' (line {self.line})"