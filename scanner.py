from interpreter_token import TokenType, Token

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self._is_at_end():
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens

    def _scan_token(self):
        char = self._advance()

        if char == '(':
            self.tokens.append(Token(TokenType.LEFT_PAREN, char, self.line))
        elif char == ')':
            self.tokens.append(Token(TokenType.RIGHT_PAREN, char, self.line))
        elif char == '{':
            self.tokens.append(Token(TokenType.LEFT_BRACE, char, self.line))
        elif char == '}':
            self.tokens.append(Token(TokenType.RIGHT_BRACE, char, self.line))
        elif char == ',':
            self.tokens.append(Token(TokenType.COMMA, char, self.line))
        elif char == ';':
            self.tokens.append(Token(TokenType.SEMICOLON, char, self.line))
        elif char == '=':
            if self._match('='):
                self.tokens.append(Token(TokenType.EQUAL_EQUAL, '==', self.line))
            else:
                self.tokens.append(Token(TokenType.EQUAL, '=', self.line))
        elif char in [' ', '\r', '\t']:
            # Ignore whitespace
            pass
        elif char == '\n':
            self.line += 1
        else:
            self._handle_lexical_error(char)


    def _advance(self):
        char = self.source[self.current]
        self.current += 1
        return char

    def _match(self, expected):
        if self._is_at_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        return True

    def _is_at_end(self):
        return self.current >= len(self.source)

    def _handle_lexical_error(self, char):
        raise Exception(f"Lexical Error: Invalid character '{char}' at line {self.line}")