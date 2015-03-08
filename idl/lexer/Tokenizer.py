from idl.Trace import Trace
from idl.lexer import Lang
from idl.lexer.LexerError import LexerError
from idl.lexer.Token import Token


class Tokenizer:
    DEBUG = False
    
    def __init__(self, source):
        self._originalSource = source
        
        self._source = source
        
        self._tokens = []
        
    @property
    def source(self):
        '''
        Original tokenizer source
        '''
        
        return self._originalSource
        
    @staticmethod
    def tokenize(source):
        if Tokenizer.DEBUG:
            Trace.debug('IN: %r' % source)
            
        return Tokenizer(source)._tokenize()
    
    def _tokenize(self):
        # Create the initial unknown token from the source
        self._tokens = [ Token(self, Token.UNKOWN, (0, len(self._source))) ]
        
        while not self._done():
            if Tokenizer.DEBUG:
                Trace.debug('='*80)
                Trace.debug('IN: ', [str(i) for i in self._tokens])
                
            currIndex, currToken = self._findUnkown()
            
            # Remove the current unknown token
            self._tokens.pop(currIndex)
            
            newTokens = self._splitUnkown(currToken)
            
            if Tokenizer.DEBUG:
                Trace.debug('NW: ', [str(i) for i in newTokens])
            
            for index, token in enumerate(newTokens):
                # Insert the identified / new unknown tokens in its place
                self._tokens.insert(currIndex + index, token)
                
            if Tokenizer.DEBUG:
                Trace.debug('OUT: ', [str(i) for i in self._tokens])
                
        return self._tokens
            
    def _splitUnkown(self, token):
        '''
        Split an unkown token into potentialy multiple unkowns and identified tokens
        '''
        
        newTokens = []
        
        searchResult = self.findMatches(token)
        
        if not searchResult:
            raise LexerError(token)
        
        tokenId, tokenMatches, keep = searchResult
        
        newTokenSpans = []
        
        # Iterate over list of matches
        for index, match in enumerate(tokenMatches):
            # Match span
            span = match.span()
            
            # Check for tokens before the first match
            if index == 0 and span[0] > 0:
                newTokenSpans.append( (True, (0, span[0]), True) )
                
            # Check for tokens before last match and this one
            if index > 0 and len(newTokenSpans):
                isUnkown, prevSpan, keepToken = newTokenSpans[-1]
                     
                if span[0] != prevSpan[1]:
                    # There's an unknown token between the match and the previous token
                    newTokenSpans.append( (True, (prevSpan[1], span[0]), True ) )


            # Match
            newTokenSpans.append( (False, span, keep) )
            
            # After match 
            if index == len(tokenMatches) - 1 and span[1] <= len(token.body) - 1:
                # There is an unknown token after the match
                newTokenSpans.append( (True, (span[1], len(token.body)), True) )
                
        for isUnkown, indices, keepNewToken in newTokenSpans:
            if not keepNewToken:
                continue
            
            start, end = indices
            
            tokenStart = token.span[0]
                        
            newSpan = (tokenStart + start, tokenStart + end)
            
            if isUnkown:
                newToken = Token(self, Token.UNKOWN, newSpan)
            else:
                newToken = Token(self, tokenId, newSpan)
                
            newTokens.append(newToken)

        return newTokens
    

    def findMatches(self, token):
        for tokenTypeInfo in Lang.TOKEN_TYPES:
            matches = [i for i in tokenTypeInfo.regex.finditer(token.body)]
            
            if not matches:
                continue

            return [tokenTypeInfo.tokenId, matches, tokenTypeInfo.keep]
        
        return None
    
    def _findUnkown(self):
        for index, token in enumerate(self._tokens):
            if token.id == Token.UNKOWN:
                return (index, token)
            
        return None
        
    def _done(self):
        for token in self._tokens:
            if token.id == Token.UNKOWN:
                return False
            
        return True
