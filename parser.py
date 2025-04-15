# parser.py

from interpreter_token import Token, TokenType
from ast_1 import Expr, Literal, BooleanLiteral, NilLiteral, NumberLiteral, Visitor

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression() # For now, we're just parsing a single expression
        except ParseError as error:
            print(error)
            return None

    def expression(self):
        return self.literal() # For now, the only expressions are literals

    def literal(self):
        if self._match(TokenType.FALSE):
            return BooleanLiteral(False)
        if self._match(TokenType.TRUE):
            return BooleanLiteral(True)
        if self._match(TokenType.NIL):
            return NilLiteral()
        if self._match(TokenType.NUMBER):
            return NumberLiteral(self._previous().literal) # Get the actual number value

        # If no literal is matched, we might need to handle other expression types
        # or report an error. For now, we'll return None and handle errors later
        # in a more robust way.
        return None

    def _match(self, *types):
        for type in types:
            if self._check(type):
                self._advance()
                return True
        return False

    def _check(self, type):
        if self._is_at_end():
            return False
        return self._peek().type == type

    def _advance(self):
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current - 1]

    def _is_at_end(self):
        return self._peek().type == TokenType.EOF

    def _error(self, token, message):
        return ParseError(token, message)

    def _synchronize(self):
        self._advance()

        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return

            if self._peek().type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN
            ]:
                return

            self._advance()

class ParseError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message

    def __str__(self):
        return f"ParseError at {self.token}: {self.message}"