from idl.FragmentType import FragmentType
from idl.MethodFragment import MethodFragment
from idl.ParameterFragment import ParameterFragment
from idl.Utils import *

import re

class Processor:
    def __init__(self, source):
        pass

    @staticmethod
    def process(source):
        # Preprocess source
        source = Processor.__preprocess(source)
        
        # Fragment it
        return Processor.__fragment(source)
    
    @staticmethod
    def __fragment(string):
        fragments = []
        
        lines = string.split('\n')
        
        for line in lines:
            fragmentType = Processor.__getFragmentType(line)
            
            if fragmentType == None:
                raise RuntimeError('Unrecognized fragment \"%s\"' % line)
            else:
                fragments.append( fragmentType.instantiate(line) )
                
        return fragments
        
    @staticmethod
    def __preprocess(string):
        # Replace CR LF with LF
        string = string.replace('\r\n', '\n')
        
        res = ''
        
        for line in string.split('\n'):
            # Remove comments
            commentStart = line.find('#')
            
            if commentStart != -1:
                line = line[:commentStart]
                
            # Remove empty lines
            if re.compile(WHITESPACE_LINE_MATCH).match(line):
                continue
                            
            res += '%s\n' % line
            
        # Remove ending new line
        res = res[:-1]
                
        return res
            
    @staticmethod   
    def __getFragmentType(body):
        for fragmentType in Processor.__fragmentTypes:
            if fragmentType.matches(body):
                return fragmentType

        return None
            
    __fragmentTypes = [
            # Parameter
            FragmentType(\
                # Parameter name
                '^' + WHITESPACE_MATCH + PARAM_NAME_MATCH + WHITESPACE_MATCH +
                '[=]{1}' + 
                # Parameter value
                WHITESPACE_MATCH + PARAM_VALUE_MATCH +
                # Trailing whitespace & semicolon
                WHITESPACE_MATCH + ';' + WHITESPACE_MATCH + '$',
                FragmentType.PARAMETER, ParameterFragment),
            
            # Method
            FragmentType(\
               # Method return value
               '^' + WHITESPACE_MATCH + PARAM_NAME_MATCH + \
               # Method name
               WHITESPACE_SPLIT_MATCH + PARAM_NAME_MATCH  + WHITESPACE_MATCH + \
               # Method arguments
               '[(]{1}' + '[^)]*' + '[)]{1}' + \
               # Modifiers
               '(' + WHITESPACE_MATCH + PARAM_NAME_MATCH + WHITESPACE_MATCH + ')*' +
               # Trailing whitespace & semicolon
               WHITESPACE_MATCH + ';' + WHITESPACE_MATCH + '$', FragmentType.METHOD, MethodFragment)
    ]
    
 

# import re

# print( re.compile('^(' + PARAM_NAME_MATCH + WHITESPACE_MATCH + '){3}$').match('asdf23   asfji213 asf') )

