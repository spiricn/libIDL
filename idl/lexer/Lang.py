import re

from idl.lexer.Token import Token

# Keywords
KEYWORD_INTERFACE = r'interface'

KEYWORD_STRUCT = r'struct'

KEYWORD_ENUM = r'enum'

KEYWORD_TYPEDEF = r'typedef'

KEYWORD_IN = r'in'

KEYWORD_OUT = r'out'

KEYWORD_CALLBACK_REG = r'callback_register'

KEYWORD_CALLBACK_UNREG = r'callback_unregister'

KEYWORD_PACKAGE = r'package'

KEYWORD_IMPORT = r'import'

KEYWORD_EXTENDS = r'extends'

# Type names
TYPE_INT64 = r'int64'

TYPE_UINT64 = r'uint64'

TYPE_INT32 = r'int32'

TYPE_UINT32 = r'uint32'

TYPE_INT16 = r'int16'

TYPE_UINT16 = r'uint16'

TYPE_INT8 = r'int8'

TYPE_UINT8 = r'uint8'

TYPE_FLOAT32 = r'float32'

TYPE_FLOAT64 = r'float64'

TYPE_VOID = r'void'

TYPE_STRING = r'string'

TYPE_BOOLEAN = r'boolean'
               
class TokenTypeInfo:
    '''
    Helper class used for defining token types.
    '''
    
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
                TokenTypeInfo(r"\'[^\']*\'", Token.STRING_LIT, True),
                
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
                TokenTypeInfo(r'\.', Token.PUNCTUATION, True),
                TokenTypeInfo(r'\*', Token.PUNCTUATION, True),
                
                # Keywords
                TokenTypeInfo(r'^' + KEYWORD_INTERFACE + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_ENUM  + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_STRUCT  + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_TYPEDEF + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_IN + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_OUT + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_CALLBACK_REG + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_CALLBACK_UNREG + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_PACKAGE + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_IMPORT + r'$', Token.KEYWORD, True),
                TokenTypeInfo(r'^' + KEYWORD_EXTENDS + r'$', Token.KEYWORD, True),
                
                # ID
                TokenTypeInfo(r'^[a-zA-Z]+[a-zA-Z0-9_]*$', Token.ID, True),
                
                # Decimal literal
                TokenTypeInfo(r'^[0-9]+$', Token.INT_LIT, True),
                
                # Hexadecimal literal
                TokenTypeInfo(r'^0x[0-9a-fA-F]+$', Token.INT_LIT, True),
                
                # Binary literal
                TokenTypeInfo(r'^0b[0-1]+$', Token.INT_LIT, True),
                
                # Octal literal
                TokenTypeInfo(r'^0[0-7]+$', Token.INT_LIT, True),
]
