import re

from idl.lexer.Token import Token
from idl.lexer.Utils import *
from idl.lexer.VariableToken import VariableToken


class MethodToken(Token):
    def __init__(self, tokenType, body):
        Token.__init__(self, tokenType, body)
        
        body = body
        
        # Method return type
        self.returnType = re.compile(WHITESPACE_MATCH + '(' + PARAM_NAME_MATCH + ')' + WHITESPACE_SPLIT_MATCH).search(body).group(1)
        
        # Method name
        self.name = re.compile(
                # Whitespace splitting the return value from name
                r'(' + WHITESPACE_SPLIT_MATCH + r')' +
                # Function name
                r'(' + PARAM_NAME_MATCH + r')' +
                # Potential whitespace between the openning bracket, and the bracket itself
                r'(' + WHITESPACE_MATCH + r'[(]{1})'
                ).search(body).group(2)
                
        # Method arguments
        args = re.compile('[(]{1}(.*)[)]{1}').search(body).group(1)
        self.__parseArguments(args)
                
        # Method modifiers
        modifiers = re.compile(r'[)]{1}(.*);').search(body).group(1)
        self.__parseModifiers(modifiers)
        
        # Entire method body
        self.body = body
    
    def __parseArguments(self, args):
            self.args = []
            
            try:
                for arg in [i for i in args.split(',') if i]:
                    argType, argVlaue = [i for i in arg.replace('\t', '').split(' ') if i]
                    
                    self.args.append( VariableToken(argType, argVlaue) )
            except:
                raise RuntimeError('Malformed method argument list "%s"' % args)
        
    def __parseModifiers(self, mods):
        self.mods = [i for i in mods.replace('\t', '').split(' ') if i]
            
    def __str__(self):
        return '<RawMethod name="%s" args="%s" mods="%s" return="%s">' % (self.name, self.args, self.mods, self.returnType)
