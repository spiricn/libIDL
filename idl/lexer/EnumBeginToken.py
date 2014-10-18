import re

from idl.lexer.Token import Token
from idl.lexer.Utils import *


class EnumBeginToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)

        # Enum name matching regex
        r = re.compile(WHITESPACE_MATCH + 'enum' + WHITESPACE_SPLIT_MATCH + '(' + PARAM_NAME_MATCH + ')' + WHITESPACE_MATCH + '{')
        
        # Find out enum name
        try:
            self.name = r.search(self.body).group(1)
        except:
            raise RuntimeError("Malformed enum declaration %r" % self.body)
        
    def __str__(self):
        return '<EnumBeginToken body="%s">' % self.body
