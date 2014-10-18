import re

from idl.Method import Method
from idl.Type import Type
from idl.lexer.TokenType import TokenType
from idl.lexer.Utils import *

from idl.Annotation import Annotation


class Interface(Type):
    def __init__(self, module, tokens):
        Type.__init__(self, module, Type.INTERFACE)
        
        header = tokens.pop(0)
        
        # Sanity check
        assert(header.type == TokenType.INTERFACE_BEGIN)
        
        self.name = header.name
        
        # Parse methods
        self.methods = []
        
        annotations = []
        
        while tokens:
            token = tokens[0]
            
            if token.type == TokenType.METHOD:
                method = Method(self, self.module, tokens)
                
                method.annotations = annotations
                
                annotations = []
                
                # Start of method token
                self.methods.append( method )
            
            elif token.type == TokenType.CLOSING_BRACKET:
                # End of interface token
                tokens.pop(0)
                break
            
            elif token.type == TokenType.ANNOTATION:
                annotations.append( Annotation(tokens) )
            
            else:
                # Unexpected token
                raise RuntimeError('Unexpected token type found while parsing interface: "%s"' % token.body)

    def create(self):
        for method in self.methods:
            method.create()
