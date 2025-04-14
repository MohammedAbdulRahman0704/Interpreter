from interpreter_token import TokenType, Token

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens

    def _scan_token(self):
        char = self._advance()

        # Handling for various symbols
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
        elif char == '/':
            if self._match('/'):  # Start of a single-line comment
                self._skip_comment()
            elif self._match('*'):  # Start of a multi-line comment
                self._skip_block_comment()
            else:
                self.tokens.append(Token(TokenType.DIVIDE, char, self.line))  # Regular divide operator
        elif char in [' ', '\r', '\t']:
            # Ignore whitespace
            pass
        elif char == '\n':
            self.line += 1
        elif char == '!':
            if self._match('='):
                self.tokens.append(Token(TokenType.BANG_EQUAL, '!=', self.line))
            else:
                self.tokens.append(Token(TokenType.BANG, '!', self.line))
        elif char == '<':
            self._add_token(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)
        elif char == '>':
            self._add_token(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)
        elif char.isdigit():  # Check if it's a number
            self._handle_number(char)
        elif char.isalpha() or char == '_':  # Check if it's a valid identifier or keyword
            self._handle_identifier(char)
        else:
            self._handle_lexical_error(char)

    def _advance(self):
        """Advance to the next character in the source and return the character."""
        char = self.source[self.current]
        self.current += 1
        return char

    def _match(self, expected):
        """Checks if the next character matches the expected character and advances."""
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def _is_at_end(self):
        """Returns True if the scanner has reached the end of the source."""
        return self.current >= len(self.source)

    def _handle_lexical_error(self, char):
        """Raises an exception when an invalid character is encountered."""
        raise Exception(f"Lexical Error: Invalid character '{char}' at line {self.line}")

    def _add_token(self, type, lexeme=None):
        """Adds a token to the list of tokens."""
        if lexeme is None:
            lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(type, lexeme, self.line))

    def _skip_comment(self):
        """Skips over a single-line comment."""
        while self._peek() != '\n' and not self._is_at_end():
            self._advance()

    def _skip_block_comment(self):
        """Skips over a multi-line comment."""
        while not self._is_at_end():
            char = self._advance()
            if char == '*' and self._peek() == '/':
                self._advance()  # Skip the '/'
                break

    def _handle_identifier(self, char):
        """Handles identifiers (variable names, keywords, etc.)."""
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()
        self._add_token(TokenType.IDENTIFIER)

    def _handle_number(self, char):
        """Handles numbers (integers or floats)."""
        lexeme = char
        while self._peek().isdigit():
            lexeme += self._advance()
        if self._peek() == '.':  # Check for decimal point (float)
            lexeme += self._advance()
            while self._peek().isdigit():
                lexeme += self._advance()
        self._add_token(TokenType.NUMBER, lexeme)

    def _peek(self):
        """Returns the character at the current position, or a null character if at the end."""
        if self._is_at_end():
            return '\0'
        return self.source[self.current]