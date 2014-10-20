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
            
            r = re.compile( '\((' + '.*' + '\))' )
            
            # Find the value
            
            try:
                valueExpr = r.search(bodyStripped).group(0)
                
                # Strip the brackets
                valueExpr = valueExpr[1:-1]
                 
            except Exception as e:
                raise RuntimeError("Invalid enum field %r declaration: %s" % (self.body, str(e)))

            # Preform value evaluation
            try:
                self.value = eval(valueExpr)
            except Exception as e:
                raise RuntimeError("Error evaluating enum value expression %r: %s" % (valueExpr, str(e)))
            
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
