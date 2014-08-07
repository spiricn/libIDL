from idl.lexer.TokenType import TokenType
from idl.lexer.MethodToken import MethodToken
from idl.lexer.ParameterToken import ParameterToken
from idl.lexer.StructBeginToken import StructBeginToken
from idl.lexer.InterfaceBeginToken import InterfaceBeginToken
from idl.lexer.Token import Token
from idl.lexer.Utils import *
import re

class Lexer:
    def __init__(self, source):
        pass

    @staticmethod
    def tokenize(source):
        # Preprocess source
        source = Lexer.__preprocess(source)
        
        # Tokenize it
        return Lexer.__tokenize(source)
    
    @staticmethod
    def __tokenize(string):
        tokens = []
        
        # Empty string?
        if not string:
            return tokens
        
        lines = string.split('\n')
        
        for line in lines:
            TokenType = Lexer.__getTokenType(line)
            
            if TokenType == None:
                raise RuntimeError('Unrecognized token \"%s\"' % line)
            else:
                tokens.append( TokenType.instantiate(line) )
                
        return tokens
        
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
    def __getTokenType(body):
        for TokenType in Lexer.__tokenTypes:
            if TokenType.matches(body):
                return TokenType

        return None
            
    __tokenTypes = [
            # Parameter
            TokenType(\
                # Parameter name
                r'^' + WHITESPACE_MATCH + PARAM_NAME_MATCH + WHITESPACE_MATCH +
                r'[=]{1}' + 
                # Parameter value
                WHITESPACE_MATCH + PARAM_VALUE_MATCH +
                # Trailing whitespace & semicolon
                WHITESPACE_MATCH + r';' + WHITESPACE_MATCH + r'$',
                TokenType.PARAMETER, ParameterToken),
            
            # Method
            TokenType(\
               '^[^(]+[(]{1}[^)]*[)]{1}[^;]*;$', TokenType.METHOD, MethodToken),
                       
            TokenType(\
               WHITESPACE_MATCH + 'struct' + WHITESPACE_SPLIT_MATCH + PARAM_NAME_MATCH + WHITESPACE_MATCH + '{',
               TokenType.STRUCT_BEGIN, StructBeginToken),
                       
            TokenType(\
               WHITESPACE_MATCH + '}' + WHITESPACE_MATCH + ';' + WHITESPACE_MATCH + '$',
               TokenType.CLOSING_BRACKET, Token),
                       
            TokenType(\
               WHITESPACE_MATCH + \
               # Field type
               PARAM_NAME_MATCH + WHITESPACE_SPLIT_MATCH + \
               # Field name
               PARAM_NAME_MATCH + WHITESPACE_MATCH + ';' + WHITESPACE_MATCH,
               TokenType.STRUCT_FIELD, Token),
                       
             TokenType(\
               WHITESPACE_MATCH + 'interface' + WHITESPACE_SPLIT_MATCH + PARAM_NAME_MATCH + WHITESPACE_MATCH + '{',
               TokenType.INTERFACE_BEGIN, InterfaceBeginToken),
    ]
