import re

from idl.Type import Type
from idl.lexer.TokenType import TokenType
from idl.lexer.Utils import *
from idl.lexer.VariableToken import VariableToken


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
                raise RuntimeError('Unexpected token of type %d found whlie parsing structure: "%s"' % (token.type, token.body))
            
        self.name = header.name

        # Parse struct fields        
        self.rawFields = []

        for rawField in fields:
            self.rawFields.append( VariableToken(rawField.fieldType, rawField.fieldName) )
            
    def create(self):
        self.fields = []
        
        # Resolve field types
        for rawField in self.rawFields:
            var = self.module.createVariable(rawField)
            
            if var == None:
                raise RuntimeError('Could not resolve structure field type %r of structure %r' % (rawField.type, self.name))
            
            self.fields.append(var)
