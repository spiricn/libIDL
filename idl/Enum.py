import re

from idl.EnumField import EnumField
from idl.Type import Type
from idl.lexer.TokenType import TokenType
from idl.lexer.Utils import *

from idl.Annotation import Annotation


class Enum(Type):
    def __init__(self, module, tokens):
        Type.__init__(self, module, Type.ENUM)
        
        header = tokens.pop(0)
        
        # Sanity  check
        assert(header.type == TokenType.ENUM_BEGIN)
        
        self.name = header.name
        
        self.fields = []
        
        annotations = []
        
        while True:
            token = tokens[0]
            
            if token.type == TokenType.ENUM_FIELD:
                tokens.pop(0)
                
                fieldValue = token.value
                
                if fieldValue == -1:
                    # No value given, assign it one
                    fieldValue = 0
                    
                    while fieldValue  in [field.value for field in self.fields]:
                        fieldValue  += 1
                        
                elif fieldValue in [field.value for field in self.fields]:
                    # If a value has been provided, check if it's already taken
                    raise RuntimeError('Enum field for enum %r with value %d already exists' % (self.name, fieldValue))
                        
                # Create a new field
                field = EnumField(token.name, fieldValue)
                
                field.annotations = annotations
                
                annotations = []
                 
                self.fields.append(field)
            
            elif token.type == TokenType.CLOSING_BRACKET:
                # End of enum
                tokens.pop(0)
                break
            
            elif token.type == TokenType.ANNOTATION:
                annotations.append(Annotation(tokens))
            
            else:
                raise RuntimeError("Unexpected token while parsing enum %d" % token.type)
            
    def create(self):
        pass
                
            
    