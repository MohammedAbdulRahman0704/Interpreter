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
        while not self._is_at_end():
            self.start = self.current  # 🔧 Reset start here
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", self.line))
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
            self._add_token(TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL)
        elif char == '/':
            if self._match('/'):  # Start of a single-line comment
                self._skip_comment()
            elif self._match('*'):  # Start of a multi-line comment
                self._skip_block_comment()
            else:
                self._add_token(TokenType.DIVIDE)  # Regular divide operator
        elif char in [' ', '\r', '\t']:
            # Ignore whitespace
            pass
        elif char == '\n':
            self.line += 1
        elif char == '!':
            self._add_token(TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG)
        elif char == '<':
            self._add_token(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)
        elif char == '>':
            self._add_token(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)
        elif char.isdigit():  # Check if it's a number
            self._handle_number()
        elif char.isalpha() or char == '_':  # Check if it's a valid identifier or keyword
            self._handle_identifier()
        else:
            self._handle_lexical_error(f"Unexpected character: {char}")

    def _handle_string(self):
        string_value = ""
        while self._peek() != '"' and not self._is_at_end():
            char = self._advance()
            if char == '\n':
                self.line += 1
                self._handle_lexical_error("Unterminated string literal")
                return
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
        self._add_token(TokenType.STRING, string_value)

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

    def _add_token(self, type, literal=None):
        """Adds a token to the list of tokens."""
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(type, lexeme, self.line, literal))

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
            elif char == '\n':
                self.line += 1
        raise Exception(f"Lexical Error: Unmatched block comment starting at line {self.line}")

    def _handle_identifier(self):
        """Handles identifiers and keywords."""
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()

        text = self.source[self.start:self.current]
        token_type = TokenType.IDENTIFIER # Default to identifier
        # In a more complete scanner, you would check for keywords here
        # if text in keywords:
        #     token_type = keywords[text]
        self._add_token(token_type)

    def _handle_number(self):
        """Handles number literals."""
        while self._peek().isdigit():
            self._advance()

        # Look for a fractional part
        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance() # Consume the '.'

            while self._peek().isdigit():
                self._advance()

        lexeme = self.source[self.start:self.current]
        try:
            number_value = float(lexeme) if '.' in lexeme else int(lexeme)
            self._add_token(TokenType.NUMBER, number_value)
        except ValueError:
            self._handle_lexical_error(f"Invalid number format: {lexeme}")

    def _peek(self):
        """Returns the next character without consuming it."""
        if self.current >= len(self.source):
            return '\0'
        return self.source[self.current]

    def _peek_next(self):
        """Returns the character after the next one without consuming it."""
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]