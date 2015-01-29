from idl.lexer import Lang
from idl.lexer.Token import Token
from idl.parser.MethodParser import MethodParser
from idl.parser.Parser import Parser
from idl.parser.ParserError import ParserError


class InterfaceInfo:
    def __init__(self):
        self.name = []
        self.methods = []
        self.bases = []
        self.line = 0

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
        self.interface.line = self.next.location[0]
        
        # Check start keyword
        self.eat(Token.KEYWORD , Lang.KEYWORD_INTERFACE)
        
        # Interface name
        self.interface.name = self.eat(Token.ID).body
        
        if self.isNext(Token.KEYWORD, Lang.KEYWORD_EXTENDS):
            self.eat(Token.KEYWORD)
            
            while True:
                # Eat interface bases
                self.interface.bases.append( self.eatTypeInfo() )
                
                if self.isNext(Token.PUNCTUATION, ','):
                    self.eat(Token.PUNCTUATION)
                    
                elif self.isNext(Token.PUNCTUATION, '{'):
                    break

                else:
                    raise ParserError('Unexpected token', self.next())

    def _parseBody(self):
        # Body start
        self.eat(Token.PUNCTUATION , '{')
        
        while True:
            self.eatAnnotations()
            
            token = self.next

            # End of body ?
            if token.id == Token.PUNCTUATION and token.body == '}':
                self.pop()
                break

            # Parse method
            method = MethodParser(self.tokens).parse()
            
            method.annotations = self.getAnnotations()
            
            self.interface.methods.append( method )
