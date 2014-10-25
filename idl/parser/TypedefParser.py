from idl.lexer2.Keywords import KEYWORD_TYPEDEF
from idl.lexer2.Token import Token
from idl.parser.Parser import Parser


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

    