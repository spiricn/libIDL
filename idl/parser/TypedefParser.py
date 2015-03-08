from idl.lexer import Lang
from idl.lexer.Token import Token
from idl.parser.Parser import Parser

from idl.parser.Desc import TypedefDesc


class TypedefParser(Parser):
    def __init__(self, tokens):
        Parser.__init__(self, tokens)
        
    def parse(self):
        self._desc = TypedefDesc()
        
        # Typedef keyword
        self.eat(Token.KEYWORD, Lang.KEYWORD_TYPEDEF)
        
        # Type name
        self._desc.typeName = self.eat(Token.ID).body
        
        self.eat(Token.PUNCTUATION, ';')
        
        return self._desc
