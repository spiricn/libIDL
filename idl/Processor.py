from idl.FragmentType import FragmentType
from idl.MethodFragment import MethodFragment
from idl.ParameterFragment import ParameterFragment
from idl.StructBeginFragment import StructBeginFragment
from idl.Fragment import Fragment
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
        
        # Empty string?
        if not string:
            return fragments
        
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
        
        # Remove comment blocks
        blockComment = re.compile(  r'/\*' + r'.*?' + r'\*/', re.DOTALL )
        
        match = True
        
        while match:
            match = blockComment.search(string)
            
            if match:
                span = match.span()
                
                string = string[:span[0]] + string[span[1]:]

        for line in string.split('\n'):
            # Remove comments
            commentStart = line.find('//')
            
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
                r'^' + WHITESPACE_MATCH + PARAM_NAME_MATCH + WHITESPACE_MATCH +
                r'[=]{1}' + 
                # Parameter value
                WHITESPACE_MATCH + PARAM_VALUE_MATCH +
                # Trailing whitespace & semicolon
                WHITESPACE_MATCH + r';' + WHITESPACE_MATCH + r'$',
                FragmentType.PARAMETER, ParameterFragment),
            
            # Method
            FragmentType(\
               # Method return value
               r'^' + WHITESPACE_MATCH + PARAM_NAME_MATCH + \
               # Method name
               WHITESPACE_SPLIT_MATCH + PARAM_NAME_MATCH  + WHITESPACE_MATCH + \
               # Method arguments
               r'[(]{1}' + r'[^)]*' + r'[)]{1}' + \
               # Modifiers
               r'(' + WHITESPACE_MATCH + PARAM_NAME_MATCH + WHITESPACE_MATCH + r')*' +
               # Trailing whitespace & semicolon
               WHITESPACE_MATCH + r';' + WHITESPACE_MATCH + r'$', FragmentType.METHOD, MethodFragment),
                       
            FragmentType(\
               WHITESPACE_MATCH + 'struct' + WHITESPACE_SPLIT_MATCH + PARAM_NAME_MATCH + WHITESPACE_MATCH + '{',
               FragmentType.STRUCT_BEGIN, StructBeginFragment),
                       
            FragmentType(\
               WHITESPACE_MATCH + '}' + WHITESPACE_MATCH + ';' + WHITESPACE_MATCH + '$',
               FragmentType.CLOSING_BRACKET, Fragment),
                       
            FragmentType(\
               WHITESPACE_MATCH + \
               # Field type
               PARAM_NAME_MATCH + WHITESPACE_SPLIT_MATCH + \
               # Field name
               PARAM_NAME_MATCH + WHITESPACE_MATCH + ';' + WHITESPACE_MATCH,
               FragmentType.STRUCT_FIELD, Fragment),
    ]
