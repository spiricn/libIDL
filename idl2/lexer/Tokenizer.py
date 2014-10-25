from idl2.lexer.Token import Token
from idl2.lexer.TokenSearch import TokenSearch


class Tokenizer:
    DEBUG = False
    
    def __init__(self, source):
        self.source = source
        
        self.tokens = []
        
    @staticmethod
    def tokenize(source):
        if Tokenizer.DEBUG:
            print('IN: %r' % source)
            
        return Tokenizer(source)._tokenize()
    
    def _tokenize(self):
        # Split an input string to a list of unkown tokens (i.e. tokens split by whitespace)
        self._createUnkowns()
        
        while not self._done():
            if Tokenizer.DEBUG:
                print('='*80)
                print('IN: ', [str(i) for i in self.tokens])
                
            currIndex, currToken = self._findUnkown()
            
            # Remove the current unkown token
            self.tokens.pop(currIndex)
            
            newTokens = self._splitUnkown(currToken)
            
            if Tokenizer.DEBUG:
                print('NW: ', [str(i) for i in newTokens])
            
            for index, token in enumerate(newTokens):
                # Insert the identified / new unkown tokens in its place
                self.tokens.insert(currIndex + index, token)
                
            if Tokenizer.DEBUG:
                print('OUT: ', [str(i) for i in self.tokens])
                
        return self.tokens
            
    def _splitUnkown(self, token):
        '''
        Split an unkown token into potentialy multiple unkowns and identified tokens
        '''
        
        newTokens = []
        
        searchResult = TokenSearch.find(token.body)
        
        if not searchResult:
            raise RuntimeError('No tokens in %r' % token.body)
        
        tokenId, tokenMatches = searchResult
        
        newTokenSpans = []
        
        # Iterate over list of matches
        for index, match in enumerate(tokenMatches):
            # Match span
            span = match.span()
            
            # Check for tokens before the first match
            if index == 0 and span[0] > 0:
                newTokenSpans.append( (True, (0, span[0]) ) )
                
            # Check for tokens before last match and this one
            if index > 0 and len(newTokenSpans):
                isUnkown, prevSpan = newTokenSpans[-1]
                     
                if span[0] != prevSpan[1]:
                    # There's an unkown token between the match and the previous token
                    newTokenSpans.append( (True, (prevSpan[1], span[1] - 1) ) )

            # Match
            newTokenSpans.append( (False, span) )
            
            # After match 
            if index == len(tokenMatches) - 1 and span[1] <= len(token.body) - 1:
                # There is an unkown token after the match
                newTokenSpans.append( (True, (span[1], len(token.body)) ) )
        
        for isUnkown, indices in newTokenSpans:
            start, end = indices
            
            sliceBody = token.body[start:end]
            
            if isUnkown:
                newToken = Token(Token.UNKOWN, sliceBody)
            else:
                newToken = Token(tokenId, sliceBody)
                
            newTokens.append(newToken)

        return newTokens
    
    def _findUnkown(self):
        for index, token in enumerate(self.tokens):
            if token.id == Token.UNKOWN:
                return (index, token)
            
        return None
        
    def _done(self):
        for token in self.tokens:
            if token.id == Token.UNKOWN:
                return False
            
        return True

    def _createUnkowns(self):
        tokens = []
        
        # Split by spaces
        tokens += self.source.split(' ')
        
        # Split by tabs
        res = []
        
        for i in tokens:
            for j in i.split('\t'):
                res.append(j)
                
        tokens = res
                
        res = []
        
        for i in tokens:
            for j in i.split('\n'):
                res.append(j)
                
        tokens = res
                
        self.tokens += [Token(Token.UNKOWN, i) for i in res if i]
