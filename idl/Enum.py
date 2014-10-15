from idl.lexer.TokenType import TokenType
from idl.EnumField import EnumField
from idl.Type import Type
from idl.lexer.Utils import *
import re

class Enum(Type):
    def __init__(self, tokens):
        Type.__init__(self, Type.ENUM)
        
        self.tokens = tokens
        
        # Sanity  check
        assert(tokens[0].type == TokenType.ENUM_BEGIN)
        
        header = tokens.pop(0)
        
        r = re.compile(WHITESPACE_MATCH + 'enum' + WHITESPACE_SPLIT_MATCH + '(' + PARAM_NAME_MATCH + ')' + WHITESPACE_MATCH + '{')
        
        self.name = r.search(header.body).group(1)
        
        self.fields = []
        
        while True:
            token = tokens.pop(0)
            
            if token.type == TokenType.ENUM_FIELD:
                fieldName = token.body.replace(' ', '').replace('\t', '').split(',')[0]
                
                self.fields.append(  EnumField(fieldName, len(self.fields))  )
            
            elif token.type == TokenType.CLOSING_BRACKET:
                # End of enum
                break
            
            else:
                raise RuntimeError("Unexpected token while parsing enum %d" % token.type)
            
    def create(self):
        pass
                
            
    