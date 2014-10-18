import re

from idl.lexer.Token import Token
from idl.lexer.Utils import *


class AnnotationToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)

        self.text = body.strip().split('@')[1]
        
    def __str__(self):
        return '<EnumFieldToken body="%s">' % self.body
