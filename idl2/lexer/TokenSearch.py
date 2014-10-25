import re

from idl2.lexer.Keywords import KEYWORD_INTERFACE, KEYWORD_ENUM, KEYWORD_STRUCT, \
    KEYWORD_TYPEDEF
from idl2.lexer.Token import Token


class TokenSearch:
    TOKEN_TYPES = [
                [re.compile('\\('), Token.PUNCTUATION],
                [re.compile('\\)'), Token.PUNCTUATION],
                [re.compile('\\['), Token.PUNCTUATION],
                [re.compile('\\]'), Token.PUNCTUATION],
                [re.compile('\\{'), Token.PUNCTUATION],
                [re.compile('\\}'), Token.PUNCTUATION],
                [re.compile('\\@'), Token.PUNCTUATION],
                [re.compile('\\;'), Token.PUNCTUATION],
                [re.compile('\\='), Token.PUNCTUATION],
                [re.compile('\\,'), Token.PUNCTUATION],
                [re.compile( KEYWORD_INTERFACE ), Token.KEYWORD],
                [re.compile(KEYWORD_ENUM), Token.KEYWORD],
                [re.compile(KEYWORD_STRUCT), Token.KEYWORD],
                [re.compile(KEYWORD_TYPEDEF), Token.KEYWORD],
                [re.compile('[a-zA-Z]+[a-zA-Z0-9_]'), Token.ID],
                [re.compile('[0-9]+'), Token.LIT],
    ]
    
    @staticmethod
    def find(body):
        for regex, tokenId in TokenSearch.TOKEN_TYPES:
            matches = [i for i in regex.finditer(body)]
            
            if not matches:
                continue
            
            return [tokenId, matches]
        
        return None
    