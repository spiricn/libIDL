from idl.Utils import *
from idl.Argument import Argument

import re
    
class Method(object):
    def __init__(self, fragment):
        body = fragment.body
        
        # Method return type
        self.returnType = re.compile('[^ \t]*').search(body).group(0)

        # Method name
        self.name = re.compile(
                # Whitespace splitting the return value from name
                '(' + WHITESPACE_SPLIT_MATCH + ')' +
                # Function name
                '(' + PARAM_NAME_MATCH + ')' +
                # Potential whitespace between the openning bracket, and the bracket itself
                '(' + WHITESPACE_MATCH + '[(]{1})'
                ).search(body).group(2)
                
        # Method arguments
        args = re.compile(
                '[(]{1}(.*)[)]{1}').search(body).group(1)
        self.__parseArguments(args)
                
        # Method modifiers
        modifiers = re.compile(
                '[)]{1}(.*);').search(body).group(1)
        self.__parseModifiers(modifiers)
        
        # Entire method body
        self.body = body
        
    def __parseArguments(self, args):
        self.args = []
        
        try:
            for arg in [i for i in args.split(',') if i]:
                argType, argVlaue = [i for i in arg.replace('\t', '').split(' ') if i]
                
                self.args.append( Argument(argType, argVlaue) )
        except:
            raise RuntimeError('Malformed method argument list "%s"' % args)
    
    def __parseModifiers(self, mods):
        self.mods = [i for i in mods.replace('\t', '').split(' ') if i]
        
    def __str__(self):
        return '<Method name="%s" args="%s" mods="%s" return="%s">' % (self.name, self.args, self.mods, self.returnType)
