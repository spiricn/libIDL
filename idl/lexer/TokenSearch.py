import re

from idl.lexer.Keywords import KEYWORD_INTERFACE, KEYWORD_ENUM, KEYWORD_STRUCT, \
    KEYWORD_TYPEDEF, KEYWORD_IN, KEYWORD_OUT, KEYWORD_CONST, \
    KEYWORD_CALLBACK_REG, KEYWORD_CALLBACK_UNREG
from idl.lexer.Token import Token


class TokenSearch:
    # Regex | Token ID | keepToken
    
    TOKEN_TYPES = [
                # Discarded delimiters
                [re.compile('\s'), Token.PUNCTUATION, False],
                [re.compile('\\t'), Token.PUNCTUATION, False],
                [re.compile('\\n'), Token.PUNCTUATION, False],
                
                # Delimiters
                [re.compile('\\('), Token.PUNCTUATION, True],
                [re.compile('\\)'), Token.PUNCTUATION, True],
                [re.compile('\\['), Token.PUNCTUATION, True],
                [re.compile('\\]'), Token.PUNCTUATION, True],
                [re.compile('\\{'), Token.PUNCTUATION, True],
                [re.compile('\\}'), Token.PUNCTUATION, True],
                [re.compile('\\@'), Token.PUNCTUATION, True],
                [re.compile('\\;'), Token.PUNCTUATION, True],
                [re.compile('\\='), Token.PUNCTUATION, True],
                [re.compile('\\,'), Token.PUNCTUATION, True],
                
                # Keywords
                [re.compile( '^' + KEYWORD_INTERFACE + '$' ), Token.KEYWORD, True],
                [re.compile('^' + KEYWORD_ENUM  + '$'), Token.KEYWORD, True],
                [re.compile('^' + KEYWORD_STRUCT  + '$'), Token.KEYWORD, True],
                [re.compile('^' + KEYWORD_TYPEDEF + '$' ), Token.KEYWORD, True],
                [re.compile('^' + KEYWORD_IN + '$' ), Token.KEYWORD, True],
                [re.compile('^' + KEYWORD_OUT + '$' ), Token.KEYWORD, True],
                [re.compile('^' + KEYWORD_CONST + '$' ), Token.KEYWORD, True],
                [re.compile('^' + KEYWORD_CALLBACK_REG + '$' ), Token.KEYWORD, True],
                [re.compile('^' + KEYWORD_CALLBACK_UNREG + '$' ), Token.KEYWORD, True],
                
                # ID
                [re.compile('^[a-zA-Z]+[a-zA-Z0-9_]*$'), Token.ID, True],
                
                # Decimal Literal
                [re.compile('^0x[0-9a-fA-F]+$'), Token.LIT, True],
                
                # Hexa decimal literal
                [re.compile('^[0-9]+$'), Token.LIT, True],
    ]
    
    @staticmethod
    def find(body):
        for regex, tokenId, keep in TokenSearch.TOKEN_TYPES:
            matches = [i for i in regex.finditer(body)]
            
            if not matches:
                continue
            
            return [tokenId, matches, keep]
        
        return None
    