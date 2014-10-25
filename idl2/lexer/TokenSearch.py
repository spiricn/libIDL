import re

from idl2.lexer.Keywords import KEYWORD_INTERFACE, KEYWORD_ENUM, KEYWORD_STRUCT, \
    KEYWORD_TYPEDEF
from idl2.lexer.Token import Token


class TokenSearch:
    # Regex | Token ID | keepToken
    
    TOKEN_TYPES = [
                # Discarded delimiters
                [re.compile('\s'), Token.PUNCTUATION, False],
                [re.compile('\\t'), Token.PUNCTUATION, False],
                [re.compile('\\n'), Token.PUNCTUATION, False],
                
                # Actual tokens
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
                [re.compile( '^' + KEYWORD_INTERFACE + '$' ), Token.KEYWORD, True],
                [re.compile('^' + KEYWORD_ENUM  + '$'), Token.KEYWORD, True],
                [re.compile('^' + KEYWORD_STRUCT  + '$'), Token.KEYWORD, True],
                [re.compile('^' + KEYWORD_TYPEDEF + '$' ), Token.KEYWORD, True],
                [re.compile('^[a-zA-Z]+[a-zA-Z0-9_]*$'), Token.ID, True],
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
    