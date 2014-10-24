import re

from idl.lexer2.Keywords import *
from idl.lexer2.Token import Token


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
                [re.compile( KEYWORD_INTERFACE ), Token.KEYWORD],
                [re.compile(KEYWORD_ENUM), Token.KEYWORD],
                [re.compile('struct'), Token.KEYWORD],
                [re.compile('typedef'), Token.KEYWORD],
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
    