import re

from idl.lexer.Utils import WHITESPACE_LINE_MATCH

from idl.lexer.Token import Token
from idl.lexer.TokenSearch import TokenSearch


class Tokenizer:
    DEBUG = False
    
    def __init__(self, source):
        self._source = source
        
        self._tokens = []
        
    @staticmethod
    def tokenize(source):
        if Tokenizer.DEBUG:
            print('IN: %r' % source)
            
        return Tokenizer(source)._tokenize()
    
    def _preprocess(self):
        # Replace CR LF with LF
        self._source = self._source.replace('\r\n', '\n')
        
        res = ''
        
        # Remove escaped new lines
        self._source = self._source.replace('\\\n', '')
        
        # Remove comment blocks
        blockComment = re.compile(  r'/\*' + r'.*?' + r'\*/', re.DOTALL )
        
        match = True
        
        while match:
            match = blockComment.search(self._source)
            
            if match:
                span = match.span()
                
                self._source = self._source[:span[0]] + self._source[span[1]:]

        for line in self._source.split('\n'):
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
        
        self._source = res
    
    def _tokenize(self):
        self._preprocess()
        
        # Create the initial unkown token from the source
        self._tokens = [ Token(Token.UNKOWN, self._source) ]
        
        while not self._done():
            if Tokenizer.DEBUG:
                print('='*80)
                print('IN: ', [str(i) for i in self._tokens])
                
            currIndex, currToken = self._findUnkown()
            
            # Remove the current unkown token
            self._tokens.pop(currIndex)
            
            newTokens = self._splitUnkown(currToken)
            
            if Tokenizer.DEBUG:
                print('NW: ', [str(i) for i in newTokens])
            
            for index, token in enumerate(newTokens):
                # Insert the identified / new unkown tokens in its place
                self._tokens.insert(currIndex + index, token)
                
            if Tokenizer.DEBUG:
                print('OUT: ', [str(i) for i in self._tokens])
                
        return self._tokens
            
    def _splitUnkown(self, token):
        '''
        Split an unkown token into potentialy multiple unkowns and identified tokens
        '''
        
        newTokens = []
        
        searchResult = TokenSearch.find(token.body)
        
        if not searchResult:
            raise RuntimeError('No tokens in %r' % token.body)
        
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
                    # There's an unkown token between the match and the previous token
                    newTokenSpans.append( (True, (prevSpan[1], span[1] - 1), True ) )

            # Match
            newTokenSpans.append( (False, span, keep) )
            
            # After match 
            if index == len(tokenMatches) - 1 and span[1] <= len(token.body) - 1:
                # There is an unkown token after the match
                newTokenSpans.append( (True, (span[1], len(token.body)), True) )
        
        for isUnkown, indices, keepNewToken in newTokenSpans:
            if not keepNewToken:
                continue
            
            start, end = indices
            
            sliceBody = token.body[start:end]
            
            if isUnkown:
                newToken = Token(Token.UNKOWN, sliceBody)
            else:
                newToken = Token(tokenId, sliceBody)
                
            newTokens.append(newToken)

        return newTokens
    
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
