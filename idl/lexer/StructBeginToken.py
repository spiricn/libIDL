import re

from idl.lexer.Token import Token
from idl.lexer.Utils import *


class StructBeginToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)

        # Parse struct name
        r = re.compile(WHITESPACE_MATCH + 'struct' + WHITESPACE_SPLIT_MATCH + '(' + PARAM_NAME_MATCH + ')' + WHITESPACE_MATCH + '{')
         
        try:
            self.name = r.search(self.body).group(1)
        except:
            raise RuntimeError("Invalid struct declaration %r" % self.body)
        
    def __str__(self):
        return '<StructBeginToken body="%s">' % self.body
