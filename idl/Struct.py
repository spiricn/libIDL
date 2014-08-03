from idl.Type import Type
from idl.lexer.TokenType import TokenType
import re
from idl.lexer.VariableToken import VariableToken
from idl.lexer.Utils import *

class Struct(Type):
    def __init__(self, module, name, rawFields):
        Type.__init__(self, Type.STRUCTURE)
        
        self.module = module
        
        self.name = name
        
        self.rawFields = rawFields
        
    def create(self):
        self.fields = []
        
        for rawField in self.rawFields:
            var = self.module.createVariable(self.module, rawField)
            
            if var == None:
                raise RuntimeError('Could not resolve structure field type "%s"' % rawField.type)
            
            self.fields.append(var)
            
    @staticmethod
    def generate(module, tokens):
        header = tokens.pop(0)
        
        # Sanity check
        assert(header.type == TokenType.STRUCT_BEGIN)

        fields = []
        
        while tokens:
            fragment = tokens.pop(0)
            
            if fragment.type == TokenType.CLOSING_BRACKET:
                # Reached end
                break
            
            elif fragment.type == TokenType.STRUCT_FIELD:
                fields.append(fragment)
            
            else:
                raise RuntimeError('Unexpected fragment found whlie parsing structure: "%s"' % fragment.body)

        # Parse struct name
        r = re.compile(WHITESPACE_MATCH + 'struct' + WHITESPACE_SPLIT_MATCH + '(' + PARAM_NAME_MATCH + ')' + WHITESPACE_MATCH + '{')
         
        name = r.search(header.body).group(1)
 
        # Parse struct fields        
        rawFields = []

        for fragment in fields:
            fieldType, fieldName = [i for i in fragment.body.replace('\t', '').replace(';', '').split(' ') if i]
              
            rawFields.append( VariableToken(fieldType, fieldName) )
            
        return Struct(module, name, rawFields)
