from idl2.lexer.Keywords import KEYWORD_STRUCT
from idl2.lexer.Token import Token
from idl2.parser.Parser import Parser


class StructInfo:
    class FieldInfo:
        def __init__(self):
            self.typeName = ''
            self.name = ''

    def __init__(self):
        self.name = ''
        self.fields = []
        
class StructParser(Parser):
    def __init__(self, tokens):
        Parser.__init__(self, tokens)
        
        self.info = StructInfo()
        
    def parse(self):
        self._parseHead()
        
        self._parseBody()
        
        self.eat(Token.PUNCTUATION, ';')

    def _parseHead(self):
        # Struct keyword
        self.eat(Token.KEYWORD, KEYWORD_STRUCT)
        
        # Name
        self.info.name = self.eat(Token.ID).body
    
    def _parseBody(self):
        # Body start
        self.eat(Token.PUNCTUATION, '{')
        
        while True:
            token = self.next()
            
            if token.id == Token.ID:
                self._parseField()
                
            elif token.id == Token.PUNCTUATION and token.body == '}':
                # Body end
                self.pop()
                break
            
    def _parseField(self):
        info = StructInfo.FieldInfo()
        
        info.typeName = self.eat(Token.ID).body
        
        info.name = self.eat(Token.ID).body
        
        self.info.fields.append( info )
        
        self.eat(Token.PUNCTUATION, ';')
