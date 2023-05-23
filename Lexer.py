class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def name(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
      while self.current_char is not None:
          if self.current_char.isspace():
              self.skip_whitespace()
              continue

          if self.current_char.isdigit():
              return Token(TokenType.INT, self.integer())

          if self.current_char == ':':
              self.advance()
              return Token(TokenType.COLON, ':')

          if self.current_char == ',':
              self.advance()
              return Token(TokenType.COMMA, ',')

          if self.current_char == '(':
              self.advance()
              return Token(TokenType.LPAREN, '(')

          if self.current_char == ')':
              self.advance()
              return Token(TokenType.RPAREN, ')')

          if self.current_char == '{':
              self.advance()
              return Token(TokenType.LBRACE, '{')

          if self.current_char == '}':
              self.advance()
              return Token(TokenType.RBRACE, '}')

          if self.current_char == '\n':
              self.advance()
              return Token(TokenType.NL, '\n')

          if self.current_char == '+':
              self.advance()
              return Token(TokenType.PLUS, '+')

          if self.current_char == '-':
              self.advance()
              return Token(TokenType.MINUS, '-')

          if self.current_char == '*':
              self.advance()
              return Token(TokenType.MUL, '*')

          if self.current_char.isalpha() or self.current_char == '_':
              name = self.name()
              if name == 'type':
                  return Token(TokenType.TYPE, name)
              elif name == 'query':
                  return Token(TokenType.QUERY, name)
              else:
                  return Token(TokenType.NAME, name)

          self.error()

      return Token(TokenType.EOF, None)