# Lexer

### Course: Formal Languages & Finite Automata
### Author: Iuliana Stețenco

----

## Theory
The initial phase in the construction of a computer program is lexical analysis, also knowns as scanning or tokenization. Its major goal is to convert a string of characters that represents the program's code into a series of tokens or lexemes that will be used in the compilation process.

A token, is a group of characters that represents a single piece of computer language, such as a literal, symbol, keyword etc.

The lexer is a program that reads the code, which is a stream of characters, and groups them into tokens based on predefined rules (regular expressions) which describe patterns of characters that correspond to different token types.


## Objectives:

1. Understand what lexical analysis is.

2. Get familiar with the inner workings of a lexer/scanner/tokenizer.

3. Implement a sample lexer and show how it works.

## Implementation description

The code defines two classes: Token and Lexer. 

The Token class is very short and represents a single token with a type and a value and will show the token in a "Token(type, value)" form. 

```
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()
```

The Lexer class is responsible for scanning the input text, which is the code itself, and generating a sequence of tokens. At start, the current position is set to the beginning of the text and so is the current_char variable.

The "error" method raises an exception if an invalid character is encountered in the code.

The "advance" method moves the current position in the text forward by one character. The spaces, tabs and newlines will be skipped with the "skip_whitespace" method.

The "integer" method scans the input text for a sequence of digits and returns the corresponding integer value.

The "name" method scans the input text for a sequence of alphanumeric characters or underscores and returns the resulting name.

The "get_next_token" scans the code and returns a corresponding Token object. It loops over the input text until the end is reached or an exception is raised. It checks whether it is a digit, comma, a left/right parenthesis, a left/riht brace, or a letter/underscore. Based on this, it returns the appropriate Token object.

```
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
                return Token('INT', self.integer())

            if self.current_char == ':':
                self.advance()
                return Token('COLON', ':')

            if self.current_char == ',':
                self.advance()
                return Token('COMMA', ',')

            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')

            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')

            if self.current_char == '{':
                self.advance()
                return Token('LBRACE', '{')

            if self.current_char == '}':
                self.advance()
                return Token('RBRACE', '}')

            if self.current_char == '\n':
                self.advance()
                return Token('NL', '\n')

            if self.current_char.isalpha() or self.current_char == '_':
                name = self.name()
                if name == 'type':
                    return Token('TYPE', name)
                elif name == 'query':
                    return Token('QUERY', name)
                else:
                    return Token('NAME', name)

            self.error()

        return Token('EOF', None)
```

## Conclusions / Screenshots / Results
In conclusion, I must say that I had the opportunity to implement a lexer in Python. The code implements several methods in the Lexer class to handle different types of tokens and if any invalid character is encountered, the program states an error.

Overall, this laboratory work provides a good introduction to the process of lexical analysis