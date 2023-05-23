from enum import Enum

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