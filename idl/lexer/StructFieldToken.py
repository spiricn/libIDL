import re

from idl.lexer.Token import Token
from idl.lexer.Utils import *


class StructFieldToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)

        r = re.compile(PARAM_NAME_MATCH)
        
        typeName = r.findall(body)
        
        if len(typeName) != 2:
            raise RuntimeError("Invalid struct field declaration %r" % body)
        
        self.fieldType, self.fieldName= typeName
                        
    def __str__(self):
        return '<EnumFieldToken body="%s">' % self.body
