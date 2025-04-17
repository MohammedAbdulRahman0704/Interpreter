# parser.py

from interpreter_token import Token, TokenType
from ast_1 import Expr, Literal, BooleanLiteral, NilLiteral, NumberLiteral, Visitor, StringLiteral, Grouping, Unary, Binary

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            expression = self.expression()
            if not self._is_at_end():
                raise self._error(self._peek(), "Expect end of input after expression.")
            return expression
        except ParseError as error:
            print(error)
            self._synchronize()
            raise error

    def expression(self):
        left = self.equality()
        if not self._is_at_end() and self._peek().type not in [TokenType.EOF, TokenType.RIGHT_PAREN]:
            # If there's something left after a complete expression
            # and it's not a valid follower, assume a missing operator.
            # We might need to expand this list of valid followers as the grammar grows.
            raise self._error(self._peek(), "Expect operator after expression.")
        return left

    def equality(self):
        left = self.comparison()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self.comparison()
            left = Binary(left, operator, right)
        if not self._is_at_end() and self._peek().type not in [TokenType.EOF, TokenType.RIGHT_PAREN]:
            # Add more valid following tokens if needed for more complex grammar
            pass # For now, let lower precedence rules handle this
        return left

    def comparison(self):
        left = self.addition()
        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self._previous()
            right = self.addition()
            left = Binary(left, operator, right)
        return left

    def addition(self):
        left = self.multiplication()
        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            if self._is_at_end():
                raise self._error(self._previous(), "Expect expression after operator.")
            right = self.multiplication()
            left = Binary(left, operator, right)
        return left

    def multiplication(self):
        left = self.unary()
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

        raise self._error(self._peek(), "Expect expression.") # Error if no primary is found

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

    def _peek_previous(self):
        if self.current > 0:
            return self.tokens[self.current - 1]
        return None

    def _previous(self):
        return self.tokens[self.current - 1]

    def _is_at_end(self):
        return self._peek().type == TokenType.EOF

    def _error(self, token, message):
        return ParseError(token, message, token.line)

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
    def __init__(self, token, message, line):
        self.token = token
        self.message = message
        self.line = line

    def __str__(self):
        return f"ParseError at line {self.line}, {self.token}: {self.message}"