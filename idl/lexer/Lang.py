import re

from idl.lexer.Token import Token


KEYWORD_INTERFACE = r'interface'

KEYWORD_STRUCT = r'struct'

KEYWORD_ENUM = r'enum'

KEYWORD_TYPEDEF = r'typedef'

KEYWORD_IN = r'in'

KEYWORD_OUT = r'out'

KEYWORD_CALLBACK_REG = r'callback_register'

KEYWORD_CALLBACK_UNREG = r'callback_unregister'

class TokenTypeInfo:
    def __init__(self, regex, tokenId, keep, flags=0):
        self.regex = re.compile(regex, flags)
        
        self.tokenId = tokenId
        
        self.keep = keep

TOKEN_TYPES = [
                # Comments
                TokenTypeInfo(r'\/\/[^\n]*', Token.COMMENT, False, re.DOTALL),
                
                TokenTypeInfo(r'/\*' + r'.*?' + r'\*/', Token.BLOCK_COMMENT, False, re.DOTALL),
                
                # String literals
                TokenTypeInfo(r'\"[^\"]*\"', Token.STRING_LIT, True),
                TokenTypeInfo(r"\'[^\"]*\'", Token.STRING_LIT, True),
                
                # Discarded delimiters
                TokenTypeInfo(r'\s', Token.PUNCTUATION, False),
                TokenTypeInfo(r'\t', Token.PUNCTUATION, False),
                TokenTypeInfo(r'\n', Token.PUNCTUATION, False),
                TokenTypeInfo(r'\r', Token.PUNCTUATION, False),
                 
                # Delimiters
                TokenTypeInfo(r'\(', Token.PUNCTUATION, True),
                TokenTypeInfo(r'\)', Token.PUNCTUATION, True),
                TokenTypeInfo(r'\[', Token.PUNCTUATION, True),
                TokenTypeInfo(r'\]', Token.PUNCTUATION, True),
                TokenTypeInfo(r'\{', Token.PUNCTUATION, True),
                TokenTypeInfo(r'\}', Token.PUNCTUATION, True),
                TokenTypeInfo(r'\@', Token.PUNCTUATION, True),
                TokenTypeInfo(r'\;', Token.PUNCTUATION, True),
                TokenTypeInfo(r'\=', Token.PUNCTUATION, True),
                TokenTypeInfo(r'\,', Token.PUNCTUATION, True),
                
                # Keywords
                TokenTypeInfo(r'^' + KEYWORD_INTERFACE + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_ENUM  + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_STRUCT  + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_TYPEDEF + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_IN + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_OUT + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_CALLBACK_REG + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_CALLBACK_UNREG + r'$', Token.KEYWORD, True),
                
                # ID
                TokenTypeInfo(r'^[a-zA-Z]+[a-zA-Z0-9_]*$', Token.ID, True),
                
                # Decimal literal
                TokenTypeInfo(r'^[0-9]+$', Token.INT_LIT, True),
                
                # Hexadecimal literal
                TokenTypeInfo(r'^0x[0-9a-fA-F]+$', Token.INT_LIT, True),
]
