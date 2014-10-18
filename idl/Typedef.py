import re

from idl.EnumField import EnumField
from idl.Type import Type
from idl.lexer.TokenType import TokenType
from idl.lexer.Utils import *


class Typedef(Type):
    def __init__(self, module, tokens):
        Type.__init__(self, module, Type.TYPEDEF)
        
        # Sanity  check
        assert(tokens[0].type == TokenType.TYPEDEF)
        
        header = tokens.pop(0)
        
        r = re.compile(WHITESPACE_MATCH + 'typedef' + WHITESPACE_SPLIT_MATCH + PARAM_NAME_MATCH + WHITESPACE_MATCH + ';')
        
        self.name = r.search(header.body).group(1)
                    
    def create(self):
        pass
                
            
    