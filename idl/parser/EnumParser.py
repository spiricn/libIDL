from idl.lexer import Lang
from idl.lexer.Token import Token
from idl.parser.Parser import Parser
from idl.parser.ParserError import ParserError

from idl.parser.Desc import EnumDesc, EnumFieldDesc


class EnumParser(Parser):
    def __init__(self, tokens):
        Parser.__init__(self, tokens)
        
    def parse(self):
        self._desc = EnumDesc()
        
        self._parseHead()
        
        self._parseBody()
        
        self.eat(Token.PUNCTUATION, ';')
        
        return self._desc
    
    def _parseHead(self):
        # Enum keyword
        keywordToken = self.eat(Token.KEYWORD, Lang.KEYWORD_ENUM)
        
        # Save enum location
        self._desc.line = keywordToken.location[0]
        
        # Name
        self._desc.name = self.eat(Token.ID).body
    
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
        desc = EnumFieldDesc()

        nameToken = self.pop()
        
        # Save field location
        desc.line = nameToken.location[0]
        
        desc.name = nameToken.body
        
        # Field declaration
        if self.tokens and self.next.id == Token.PUNCTUATION and self.next.body == '(':
            # Has explicit value
            self.eat(Token.PUNCTUATION, '(')
            
            desc.value = self.eat(Token.INT_LIT).body
            
            self.eat(Token.PUNCTUATION, ')')
            
        if self.next.id == Token.PUNCTUATION and self.next.body == ',':
            self.pop()
            
        desc.annotations = self.getAnnotations()
        
        self._desc.fields.append(desc)
