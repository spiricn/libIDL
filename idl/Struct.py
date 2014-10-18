import re

from idl.Type import Type
from idl.lexer.TokenType import TokenType
from idl.lexer.Utils import *
from idl.lexer.VariableToken import VariableToken

from idl.Annotation import Annotation


class Struct(Type):
    def __init__(self, module, tokens):
        Type.__init__(self, module, Type.STRUCTURE)
        
        header = tokens.pop(0)
        
        # Sanity check
        assert(header.type == TokenType.STRUCT_BEGIN)

        fields = []
        
        annotations = []
        
        while tokens:
            token = tokens[0]
            
            if token.type == TokenType.CLOSING_BRACKET:
                # Reached end
                tokens.pop(0)
                break
            
            elif token.type == TokenType.STRUCT_FIELD:
                token.annotations = annotations
                annotations = []
                
                fields.append(tokens.pop(0))
                
            elif token.type == TokenType.ANNOTATION:
                annotations.append(Annotation(tokens))
            
            else:
                raise RuntimeError('Unexpected token of type %d found whlie parsing structure: "%s"' % (token.type, token.body))
            
        self.name = header.name

        # Parse struct fields        
        self.rawFields = []

        for rawField in fields:
            var = VariableToken(rawField.fieldType, rawField.fieldName)
            
            var.annotations = rawField.annotations
            
            self.rawFields.append( var )
            
    def create(self):
        self.fields = []
        
        # Resolve field types
        for rawField in self.rawFields:
            var = self.module.createVariable(rawField)
            
            var.annotations = rawField.annotations
            
            if var == None:
                raise RuntimeError('Could not resolve structure field type %r of structure %r' % (rawField.type, self.name))
            
            self.fields.append(var)
