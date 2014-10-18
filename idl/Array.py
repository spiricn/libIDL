import re

from idl.EnumField import EnumField
from idl.Type import Type
from idl.lexer.TokenType import TokenType
from idl.lexer.Utils import *


class Array(Type):
    def __init__(self, module, baseType, size):
        Type.__init__(self, module, Type.ARRAY)
        
        self.baseType = baseType
        
        self.size = size
        
        self.name = '%s[]' % baseType.name
    