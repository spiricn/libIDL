from idl.lexer import Lang
from idl.lexer.Token import Token
from idl.parser.Parser import Parser
from idl.parser.ParserError import ParserError


class EnumInfo:
    class FieldInfo:
        def __init__(self):
            self.name = ''
            self.value = ''
            self.line = None

    def __init__(self):
        self.name = ''
        self.line = None
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
        keywordToken = self.eat(Token.KEYWORD, Lang.KEYWORD_ENUM)
        
        # Save enum location
        self.info.line = keywordToken.location[0]
        
        # Name
        self.info.name = self.eat(Token.ID).body
    
    def _parseBody(self):
        # Openning bracket
        self.eat(Token.PUNCTUATION, '{')
        
        while True:
            self.eatAnnotations()
            
            token = self.next
            
            if token.id == Token.PUNCTUATION and token.body == '}':
                # End of enumeration
                self.pop()
                break
            
            elif token.id == Token.ID:
                self._parseField()
                
            else:
                raise ParserError('Unexpected token while parsing enumeration body', token)
    
    def _parseField(self):
        info = EnumInfo.FieldInfo()

        nameToken = self.pop()
        
        # Save field location
        info.line = nameToken.location[0]
        
        info.name = nameToken.body
        
        # Field declaration
        if self.tokens and self.next.id == Token.PUNCTUATION and self.next.body == '(':
            # Has explicit vlaue
            self.eat(Token.PUNCTUATION, '(')
            
            info.value = self.eat(Token.INT_LIT).body
            
            self.eat(Token.PUNCTUATION, ')')
            
        if self.next.id == Token.PUNCTUATION and self.next.body == ',':
            self.pop()
            
        info.annotations = self.getAnnotations()
        
        self.info.fields.append(info)
