from idl.Type import Type
from idl.lexer.Utils import *
from idl.lexer.TokenType import TokenType
from idl.Method import Method

import re

class Interface(Type):
    def __init__(self, module, tokens):
        Type.__init__(self, Type.INTERFACE)
        
        self.module = module
        
        header = tokens.pop(0)
        # Sanity check
        assert(header.type == TokenType.INTERFACE_BEGIN)
        
        # Parse interface name
        r = re.compile(WHITESPACE_MATCH + 'interface' + WHITESPACE_SPLIT_MATCH + '(' + PARAM_NAME_MATCH + ')' + WHITESPACE_MATCH + '{')
        
        self.name = r.search(header.body).group(1)
        
        # Parse methods
        self.methods = []
        
        while tokens:
            token = tokens[0]
            
            if token.type == TokenType.METHOD:
                # Start of method token
                method = self.createMethod(tokens)
                
                self.methods.append( method )
            
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
        
    def createMethod(self, tokens):
        token = tokens.pop(0)
        
        # Sanity check
        assert(token.type == TokenType.METHOD)
        
        method = Method(self, self.module, token)
        
        return method 
    
    def create(self):
        for method in self.methods:
            method.create()
            
    def createVariable(self):
        return self.parent.createVariable()