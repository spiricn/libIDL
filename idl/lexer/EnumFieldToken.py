import re

from idl.lexer.Token import Token
from idl.lexer.Utils import *


class EnumFieldToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)
        
        # Don't need spaces & tabs
        bodyStripped = body.strip()

        # Explicit value enum field ?
        if '(' in bodyStripped:
            
            r = re.compile( '\((' + NUMBER_MATCH + '\))' )
            
            # Find the value
            
            try:
                valueStr = r.search(bodyStripped).group(0)
                
                # Strip the brackets
                valueStr = valueStr[1:-1]
                 
            except:
                raise RuntimeError("Invalid enum field %r declaration" % self.body)

            # Prefrom a conversion (either hex or dec based)            
            self.value = int(valueStr, 16 if valueStr.startswith('0x') else 10)
            
            try:
                # Get the name (string before the first bracket
                self.name = re.compile('[^(]*').search(bodyStripped).group(0)
            except:
                raise RuntimeError("Invalid enum field declaration %r" % self.body)
        else:
            # Name is the body before the comma
            self.name = bodyStripped[:-1]
            
            # No value given
            self.value = -1
                        
    def __str__(self):
        return '<EnumFieldToken body="%s">' % self.body
