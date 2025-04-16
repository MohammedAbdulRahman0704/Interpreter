# parser.py

from interpreter_token import Token, TokenType
from ast_1 import Expr, Literal, BooleanLiteral, NilLiteral, NumberLiteral, Visitor, StringLiteral, Grouping, Unary, Binary

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except ParseError as error:
            print(error)
            return None

    def expression(self):
        return self.comparison() # Comparison operators have lower precedence than arithmetic

    def comparison(self):
        left = self.addition() # Comparison operates on terms (addition/subtraction)

        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self._previous()
            right = self.addition()
            left = Binary(left, operator, right)

        return left

    def addition(self):
        left = self.multiplication() # Addition and subtraction operate on terms (multiplication/division)

        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self.multiplication()
            left = Binary(left, operator, right)

        return left

    def multiplication(self):
        left = self.unary() # Multiplication and division operate on unary expressions

        while self._match(TokenType.STAR, TokenType.DIVIDE):
            operator = self._previous()
            right = self.unary()
            left = Binary(left, operator, right)

        return left

    def unary(self):
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        if self._match(TokenType.FALSE):
            return BooleanLiteral(False)
        if self._match(TokenType.TRUE):
            return BooleanLiteral(True)
        if self._match(TokenType.NIL):
            return NilLiteral()
        if self._match(TokenType.NUMBER):
            return NumberLiteral(self._previous().literal)
        if self._match(TokenType.STRING):
            return StringLiteral(self._previous().literal)
        if self._match(TokenType.LEFT_PAREN):
            expression = self.expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expression)

        return None # For now, if no primary expression is found

    def _consume(self, type, message):
        if self._check(type):
            return self._advance()
        raise self._error(self._peek(), message)

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