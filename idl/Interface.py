import re

from idl.Method import Method
from idl.Type import Type
from idl.lexer.TokenType import TokenType
from idl.lexer.Utils import *


class Interface(Type):
    def __init__(self, module, tokens):
        Type.__init__(self, module, Type.INTERFACE)
        
        header = tokens.pop(0)
        
        # Sanity check
        assert(header.type == TokenType.INTERFACE_BEGIN)
        
        self.name = header.name
        
        # Parse methods
        self.methods = []
        
        while tokens:
            token = tokens[0]
            
            if token.type == TokenType.METHOD:
                # Start of method token
                self.methods.append(  Method(self, self.module, tokens) )
            
            elif token.type == TokenType.CLOSING_BRACKET:
                # End of interface token
                tokens.pop(0)
                break
            
            else:
                # Unexpected token
                raise RuntimeError('Unexpected token type found while parsing interface: "%s"' % token.body)
            
    def getMethod(self, name):
        for i in self.methods:
            if i.name == name:
                return i
            
        return None
    
    def create(self):
        for method in self.methods:
            method.create()
            
    def createVariable(self):
        return self.parent.createVariable()
