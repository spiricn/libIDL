from idl.lexer import Lang
from idl.lexer.Token import Token
from idl.parser.Parser import Parser
from idl.parser.ParserError import ParserError

from idl.parser.Desc import StructDesc, StructFieldDesc


class StructParser(Parser):
    def __init__(self, tokens):
        Parser.__init__(self, tokens)
        
    def parse(self):
        self._desc = StructDesc()
        
        self._parseHead()
        
        self._parseBody()
        
        self.eat(Token.PUNCTUATION, ';')
        
        return self._desc
    

    def _parseHead(self):
        # Struct keyword
        self.eat(Token.KEYWORD, Lang.KEYWORD_STRUCT)
        
        # Name
        self._desc.name = self.eat(Token.ID).body
    
    def _parseBody(self):
        # Body start
        self.eat(Token.PUNCTUATION, '{')
        
        while True:
            self.eatAnnotations()
            
            token = self.next
            
            if token.id == Token.ID:
                self._parseField()
                
            elif token.id == Token.PUNCTUATION and token.body == '}':
                # Body end
                self.pop()
                break
            
            else:
                raise ParserError('Unexpected token while parsing structure body', token)
            
    def _parseField(self):
        desc = StructFieldDesc(line=self.next.location[0])
        
        desc.typeDesc = self.eatTypeDesc()
        
        desc.name = self.eat(Token.ID).body
        
        desc.annotations = self.getAnnotations()
        
        self._desc.fields.append( desc )
        
        self.eat(Token.PUNCTUATION, ';')
