import Lexer
import Token 
import TokenType
import Parser

text = '1 + 2 * 3'

lexer = Lexer(text)
parser = Parser(lexer)
ast = parser.parse()

print(ast)