from idl.lexer.Keywords import KEYWORD_ENUM
from idl.lexer.Token import Token
from idl.parser.Parser import Parser


class EnumInfo:
    class FieldInfo:
        def __init__(self):
            self.name = ''
            self.value = ''

    def __init__(self):
        self.name = ''
        self.fields = []
        

class EnumParser(Parser):
    def __init__(self, tokens):
        Parser.__init__(self, tokens)
        
        self.info = EnumInfo()
        
    def parse(self):
        self._parseHead()
        
        self._parseBody()
        
        self.eat(Token.PUNCTUATION, ';')
        
        return self.info
    
    def _parseHead(self):
        # Enum keyword
        self.eat(Token.KEYWORD, KEYWORD_ENUM)
        
        # Name
        self.info.name = self.eat(Token.ID).body
    
    def _parseBody(self):
        # Openning bracket
        self.eat(Token.PUNCTUATION, '{')
        
        while True:
            self.eatAnnotations()
            
            token = self.next()
            
            if token.id == Token.PUNCTUATION and token.body == '}':
                # End of enumeration
                self.pop()
                break
            
            elif token.id == Token.ID:
                self._parseField()
                
            else:
                raise RuntimeError('Invalid token')
    
    def _parseField(self):
        info = EnumInfo.FieldInfo()
        
        info.name = self.pop().body
        
        # Field declaration
        if self.tokens and self.next().id == Token.PUNCTUATION and self.next().body == '(':
            # Has explicit vlaue
            self.eat(Token.PUNCTUATION, '(')
            
            info.value = self.eat(Token.LIT).body
            
            self.eat(Token.PUNCTUATION, ')')
            
        info.annotations = self.getAnnotations()
        
        self.info.fields.append(info)
