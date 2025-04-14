from interpreter_token import TokenType, Token

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1  # Initialize line number
        self.end = len(source)
    
    def scan_tokens(self):
        while self.current < self.end:
            self.start = self.current
            self._scan_token()  # Call _scan_token to scan each token
        
        self.tokens.append(Token(TokenType.EOF, "", self.line))  # Adding EOF token
        return self.tokens

    def _scan_token(self):
        char = self._advance()

        # Handling for various symbols
        if char == '"':  # Start of a string literal
            self._handle_string()
        elif char == '(':
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

    def _handle_string(self):
        string_value = ""
        while self._peek() != '"' and not self._is_at_end():
            char = self._advance()
            if char == '\n':
                self.line += 1
                self._handle_lexical_error("Unterminated string literal")
            elif char == '\\':  # Escape sequence
                next_char = self._peek()
                if next_char == 'n':
                    string_value += '\n'
                    self._advance()
                elif next_char == 't':
                    string_value += '\t'
                    self._advance()
                elif next_char == '\\':
                    string_value += '\\'
                    self._advance()
                elif next_char == '"':
                    string_value += '"'
                    self._advance()
                else:
                    string_value += '\\' + next_char
                    self._advance()
            else:
                string_value += char

        if self._is_at_end():
            self._handle_lexical_error("Unterminated string literal")
            return  # Important to return after raising the error

        # Consume the closing quote
        self._advance()
        self.tokens.append(Token(TokenType.STRING, string_value, self.line))

    def _advance(self):
        """Advance to the next character in the source and return the character."""
        char = self.source[self.current]
        self.current += 1
        return char

    def _match(self, expected):
        if self.current < self.end and self.source[self.current] == expected:
            self.current += 1
            return True
        return False

    def _is_at_end(self):
        """Returns True if the scanner has reached the end of the source."""
        return self.current >= len(self.source)

    def _handle_lexical_error(self, message):
        raise Exception(f"Lexical Error at line {self.line}: {message}")

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
        """Skips over a multi-line comment, raises an error if the block is not properly closed."""
        while not self._is_at_end():
            char = self._advance()
            if char == '*' and self._peek() == '/':
                self._advance()  # Skip the '/'
                return
        raise Exception(f"Lexical Error: Unmatched block comment starting at line {self.line}")

    def _handle_identifier(self, char):
        # Handle identifiers, which may include alphabetic characters and underscores
        identifier = char
        while True:
            next_char = self._peek()  # Peek at the next character
            if next_char and (next_char.isalnum() or next_char == '_'):  # Only proceed if it's a valid character
                identifier += self._advance()  # Advance and add to the identifier
            else:
                break

        # Append the identifier token
        self.tokens.append(Token(TokenType.IDENTIFIER, identifier, self.line))

    def _handle_number(self, char):
        """Handles numbers (integers or floats)."""
        lexeme = char
        while self._peek().isdigit():
            lexeme += self._advance()
        if self._peek() == '.':  # Check for decimal point (float)
            lexeme += self._advance()
            if not self._peek().isdigit():
                self._handle_lexical_error('Invalid number format')
            while self._peek().isdigit():
                lexeme += self._advance()
        self._add_token(TokenType.NUMBER, lexeme)

    def _peek(self):
        # Return the next character or a special marker indicating end of input
        return self.source[self.current] if self.current < len(self.source) else ''