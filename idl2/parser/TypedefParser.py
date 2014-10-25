from idl2.lexer.Token import Token

from idl2.lexer.Keywords import KEYWORD_TYPEDEF
from idl2.parser.Parser import Parser


class TypedefInfo:
    def __init__(self):
        self.typeName = ''
        
        
class TypedefParser(Parser):
    def __init__(self, tokens):
        Parser.__init__(self, tokens)
        
        self.info = TypedefInfo()
        
        
    def parse(self):
        # Typedef keyword
        self.eat(Token.KEYWORD, KEYWORD_TYPEDEF)
        
        # Type name
        self.info.typeName = self.eat(Token.ID)
        
        self.eat(Token.PUNCTUATION, ';')
        
        return self.info

    