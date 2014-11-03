from idl.lexer import Lang
from idl.lexer.Token import Token
from idl.parser.Parser import Parser
from idl.parser.ParserError import ParserError


class StructInfo:
    class FieldInfo:
        def __init__(self, line):
            self.typeInfo = Parser.TypeInfo()
            self.name = ''
            self.line = line

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
        
        return self.info
    

    def _parseHead(self):
        # Struct keyword
        self.eat(Token.KEYWORD, Lang.KEYWORD_STRUCT)
        
        # Name
        self.info.name = self.eat(Token.ID).body
    
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
        info = StructInfo.FieldInfo(self.next.location[0])
        
        info.typeInfo = self.eatTypeInfo()
        
        info.name = self.eat(Token.ID).body
        
        info.annotations = self.getAnnotations()
        
        self.info.fields.append( info )
        
        self.eat(Token.PUNCTUATION, ';')
