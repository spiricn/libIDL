from idl.lexer2.Keywords import KEYWORD_INTERFACE
from idl.lexer2.Token import Token
from idl.parser.MethodParser import MethodParser
from idl.parser.Parser import Parser


class InterfaceInfo:
    def __init__(self):
        self.name = []
        self.methods = []

class InterfaceParser(Parser):
    def __init__(self, tokens):
        Parser.__init__(self, tokens)
        
        self.interface = InterfaceInfo()
        
    def parse(self):
        self._parseHead()
        
        self._parseBody()
        
        self.eat(Token.PUNCTUATION, ';')
        
        return self.interface
        
    def _parseHead(self):
        # Check start keyword
        self.eat(Token.KEYWORD , KEYWORD_INTERFACE)
        
        # Interface name
        self.interface.name = self.eat(Token.ID).body
    
    def _parseBody(self):
        # Body start
        self.eat(Token.PUNCTUATION , '{')
        
        while True:
            token = self.next()

            # End of body ?
            if token.id == Token.PUNCTUATION and token.body == '}':
                self.pop()
                break

            # Parse method
            method = MethodParser(self.tokens).parse()
            
            self.interface.methods.append( method )
