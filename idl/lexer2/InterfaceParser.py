from idl.lexer2.Keywords import KEYWORD_INTERFACE
from idl.lexer2.MethodParser import MethodParser
from idl.lexer2.Parser import Parser
from idl.lexer2.Token import Token

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
        
        self.assertNext(Token.PUNCTUATION, ';')
        self.pop()
        
        return self.interface
        
    def _parseHead(self):
        # Check start keyword
        self.assertNext(Token.KEYWORD , KEYWORD_INTERFACE)
        self.tokens.pop(0)
        
        # Interface name
        self.assertNext(Token.ID)
        self.interface.name = self.tokens.pop(0).body
    
    def _parseBody(self):
        # Body start
        self.assertNext(Token.PUNCTUATION , '{')
        self.pop()
        
        while True:
            token = self.tokens[0]

            # End of body ?
            if token.id == Token.PUNCTUATION and token.body == '}':
                self.tokens.pop(0)
                break

            # Parse method
            method = MethodParser(self.tokens).parse()
            
            self.interface.methods.append( method )
