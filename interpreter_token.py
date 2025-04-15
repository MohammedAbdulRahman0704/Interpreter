# interpreter_token.py

from enum import Enum, auto

class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()
    EOF = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    DIVIDE = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()

    # Reserved words (keywords)
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

class Token:
    def __init__(self, type, lexeme, line, literal=None):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.literal = literal

    def __repr__(self):
        return f'{self.type} {self.lexeme} {self.literal}'

# Example scanner method handling identifier
class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def _advance(self):
        char = self.source[self.current]
        self.current += 1
        if char == '\n':
            self.line += 1
        return char

    def _peek(self):
        if self._is_at_end():
            return '\0'
        return self.source[self.current]

    def _peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def _is_at_end(self):
        return self.current >= len(self.source)

    def _add_token(self, type_, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, self.line, literal))

    def _handle_identifier_or_keyword(self):
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()

        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self._add_token(token_type)

    def _handle_number(self):
        while self._peek().isdigit():
            self._advance()

        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()  # consume '.'
            while self._peek().isdigit():
                self._advance()

        lexeme = self.source[self.start:self.current]
        number_value = float(lexeme) if '.' in lexeme else int(lexeme)
        self._add_token(TokenType.NUMBER, number_value)

    def _handle_string(self):
        string_value = ""
        while not self._is_at_end() and self._peek() != '"':
            char = self._advance()
            if char == '\n':
                self.line += 1
                self._handle_lexical_error("Unterminated string literal")
                return
            elif char == '\\':
                next_char = self._advance()
                if next_char == 'n':
                    string_value += '\n'
                elif next_char == 't':
                    string_value += '\t'
                elif next_char == '"':
                    string_value += '"'
                elif next_char == '\\':
                    string_value += '\\'
                else:
                    string_value += '\\' + next_char
            else:
                string_value += char

        if self._is_at_end():
            self._handle_lexical_error("Unterminated string literal")
            return

        self._advance()  # consume closing "
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(TokenType.STRING, lexeme, self.line, string_value))

    def _handle_lexical_error(self, message):
        raise Exception(f"Lexical Error at line {self.line}: {message}")