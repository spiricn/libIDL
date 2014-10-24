import re

from idl.lexer2.Keywords import KEYWORD_INTERFACE
from idl.lexer2.Token import Token
from idl.lexer2.Tokenizer import Tokenizer


source = '''

interface Test{
    void test();
};

'''


class InterfaceParser:
    def __init__(self, tokens):
        self.tokens = tokens
        
        self._parseHead()
        
        self._parseBody()
        
    def _parseHead(self):
        # Interface header needs at least 3 tokens
        assert(len(self.tokens) >= 2)
        
        # Check start keyword
        token = self.tokens.pop(0)
        assert(token.id == Token.KEYWORD and token.body == KEYWORD_INTERFACE)
        
        # Interface name
        token = self.tokens.pop(0)
        assert(token.id == Token.ID)
        
        self.name = token.body
    
    def _parseBody(self):
        # Body start
        assert(len(self.tokens) >= 2)
        
        # Body start
        token = self.tokens.pop(0)
        assert(token.id == Token.PUNCTUATION and token.body == '{')
        
        while True:
            token = self.tokens[0]

            # End of body ?
            if token.id == Token.PUNCTUATION and token.body == '}':
                self.tokens.pop(0)
                break

            self._parseHead()            

    def _parseMethod(self):
        # Return type
        token = self.tokens[0]
        
        if token.id != Token.ID:
            raise RuntimeError("Invalid method")
    
    def _parseTail(self):
        pass
    
InterfaceParser( Tokenizer.tokenize(source) ) 
