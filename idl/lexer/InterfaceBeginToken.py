import re

from idl.lexer.Token import Token
from idl.lexer.Utils import *


class InterfaceBeginToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)
        
        # Parse interface name
        r = re.compile(WHITESPACE_MATCH + 'interface' + WHITESPACE_SPLIT_MATCH + '(' + PARAM_NAME_MATCH + ')' + WHITESPACE_MATCH + '{')
        
        try:
            self.name = r.search(self.body).group(1)
        except:
            raise RuntimeError("Invalid interface name declaration %r" % self.name)

    def __str__(self):
        return '<InterfaceBeginToken>'
