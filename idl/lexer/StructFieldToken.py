import re

from idl.lexer.Token import Token
from idl.lexer.Utils import *


class StructFieldToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)

        try:        
            r = re.compile(PARAM_TYPE_MATCH)
            
            t = r.search(body)
            
            self.fieldType = t.group(0)
            
            body = body[t.span()[1]:]
            
            self.fieldName = re.compile(PARAM_NAME_MATCH).search(body).group(0)
        except:
            raise RuntimeError('Invalid struct field declaration %r' % self.body)
                        
    def __str__(self):
        return '<EnumFieldToken body="%s">' % self.body
