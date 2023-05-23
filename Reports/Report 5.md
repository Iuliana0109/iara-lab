# Topic: Parsing

### Course: Formal Languages & Finite Automata
### Author: Iuliana Stețenco

----

## Overview
The process of gathering syntactical meaning or doing a syntactical analysis over some text can also be called parsing. It usually results in a parse tree which can also contain semantic information that could be used in subsequent stages of compilation, for example.

 Similarly to a parse tree, in order to represent the structure of an input text one could create an Abstract Syntax Tree (AST). This is a data structure that is organized hierarchically in abstraction layers that represent the constructs or entities that form up the initial text. These can come in handy also in the analysis of programs or some processes involved in compilation.


## Objectives:
1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.

## Implementation:
Firstly, I modified a couple of things from my 3rd laboratory work in order to proceed with the given tasks.
I implemented the class TokenType:
```python
class TokenType(Enum):
    INT = 'INT'
    COLON = 'COLON'
    COMMA = 'COMMA'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    NL = 'NL'
    TYPE = 'TYPE'
    QUERY = 'QUERY'
    NAME = 'NAME'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    EOF = 'EOF'
```
Class AST defines the Abstract Syntax Tree node: it returns a string representation of the AST by calling the _str_recursive() method.
The _str_recursive() method is marked as NotImplementedError, which means it must be implemented in the subclasses, otherwise it will not print properly.

```python
class AST:
    def __str__(self):
        return self._str_recursive(0)

    def _str_recursive(self, indent_level):
        raise NotImplementedError("'_str_recursive' method must be implemented in subclasses.")

```


The class NumberNode represents a numeric value in the AST.
The _str_recursive() method is implemented to generate a string representation of the NumberNode by indenting it based on the indent_level and including the value of the number.

```python
class NumberNode(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def _str_recursive(self, indent_level):
        indent = "  " * indent_level
        return f"{indent}NumberNode({self.value})"
```


class BinOpNode(AST):

This class represents an operation (e.g., addition, subtraction, multiplication) in the AST. It takes three parameters: left (the left operand), op (the operator token), and right (the right operand).
The _str_recursive() method is implemented to generate a string representation of the BinOpNode. It includes the left and right operands, the operator token with its type, and indents the output based on the indent_level.
Additionally, there is a get_op_symbol() method that returns the operator symbol as a string.
```python
class BinOpNode(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def _str_recursive(self, indent_level):
        indent = "  " * indent_level
        op_str = self.op.value
        left_str = self.left._str_recursive(indent_level + 1)
        right_str = self.right._str_recursive(indent_level + 1)
        return f"{indent}BinOpNode(\n{left_str},\n{indent}  op=Token({self.op.type}, {op_str}),\n{right_str}\n{indent})"

    # To retrieve the operator symbol
    def get_op_symbol(self):
        return self.op.value
```

Note that this parser implements a simple arithmetic expression parser using the tokens we have declared so far. It can be modified according to the grammar and syntax rules.

The Parser has several methods. The method "eat" consumes the current token and advance to the next token. It checks if the type of the current token matches the expected token_type and if so, it updates the current_token by calling get_next_token() from the Lexer.

```python
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
```
The factor method handles numbers and parentheses.
It retrieves the current token and checks its type.
If the type is TokenType.INT (an integer), it consumes the token and returns a NumberNode with the token as its value.
If the type is TokenType.LPAREN (an opening parenthesis), it consumes the token, recursively calls expr() to parse the expression within the parentheses, and then consumes the closing parenthesis token (TokenType.RPAREN)

```python
    def factor(self):
        token = self.current_token
        if token.type == TokenType.INT:
            self.eat(TokenType.INT)
            return NumberNode(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
```

The term method handles multiplication and division operations.
It starts by calling factor() to get the leftmost operand.
Then it enters a loop that continues as long as the current token is either TokenType.MUL or TokenType.DIV.
Inside the loop, it retrieves the current token and checks its type.
If it's TokenType.MUL or DIV, it consumes the token, calls factor() to get the right operand, and creates a BinOpNode with the left operand, operator token, and right operand.
```python
    def term(self):
        node = self.factor()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)

            node = BinOpNode(left=node, op=token, right=self.factor())

        return node
```

The expr method handles addition and subtraction operations pretty much the same as the term method
```python
    def expr(self):
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOpNode(left=node, op=token, right=self.term())

        return node

    def parse(self):
        return self.expr()
```

* Output
```
BinOpNode(
  NumberNode(1),
  op=Token(TokenType.PLUS, +),
  BinOpNode(
    NumberNode(2),
    op=Token(TokenType.MUL, *),
    NumberNode(3)
  )
)
```
# Conclusion
During the course of this lab, I gained a solid understanding of AST (Abstract Syntax Trees). I was able to apply this knowledge by implementing a parser that constructs an AST using a set of tokens. By creating the AST data structure and developing the Parser, my comprehension of Formal Languages and their implementation has significantly improved. (I just want this to be over and I think I've done enough)