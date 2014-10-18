from idl.Type import Type
from idl.lexer.TokenType import TokenType
import re
from idl.lexer.VariableToken import VariableToken
from idl.lexer.Utils import *

class Struct(Type):
    def __init__(self, module, tokens):
        Type.__init__(self, module, Type.STRUCTURE)
        
        header = tokens.pop(0)
        
        # Sanity check
        assert(header.type == TokenType.STRUCT_BEGIN)

        fields = []
        
        while tokens:
            token = tokens.pop(0)
            
            if token.type == TokenType.CLOSING_BRACKET:
                # Reached end
                break
            
            elif token.type == TokenType.STRUCT_FIELD:
                fields.append(token)
            
            else:
                raise RuntimeError('Unexpected token found whlie parsing structure: "%s"' % token.body)

        # Parse struct name
        r = re.compile(WHITESPACE_MATCH + 'struct' + WHITESPACE_SPLIT_MATCH + '(' + PARAM_NAME_MATCH + ')' + WHITESPACE_MATCH + '{')
         
        self.name = r.search(header.body).group(1)
 
        # Parse struct fields        
        self.rawFields = []

        for token in fields:
            fieldType, fieldName = [i for i in token.body.replace('\t', '').replace(';', '').split(' ') if i]
              
            self.rawFields.append( VariableToken(fieldType, fieldName) )
            
        
        
    def create(self):
        self.fields = []
        
        for rawField in self.rawFields:
            var = self.module.createVariable(self.module, rawField)
            
            if var == None:
                raise RuntimeError('Could not resolve structure field type "%s"' % rawField.type)
            
            self.fields.append(var)
