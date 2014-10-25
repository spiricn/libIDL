import re

from idl.lexer.Utils import WHITESPACE_LINE_MATCH

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
    
    def _preprocess(self):
        # Replace CR LF with LF
        self.source = self.source.replace('\r\n', '\n')
        
        res = ''
        
        # Remove escaped new lines
        self.source = self.source.replace('\\\n', '')
        
        # Remove comment blocks
        blockComment = re.compile(  r'/\*' + r'.*?' + r'\*/', re.DOTALL )
        
        match = True
        
        while match:
            match = blockComment.search(self.source)
            
            if match:
                span = match.span()
                
                self.source = self.source[:span[0]] + self.source[span[1]:]

        for line in self.source.split('\n'):
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
        
        self.source = res
    
    def _tokenize(self):
        self._preprocess()
        
        # Create the initial unkown token from the source
        self.tokens = [ Token(Token.UNKOWN, self.source) ]
        
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
        for index, token in enumerate(self.tokens):
            if token.id == Token.UNKOWN:
                return (index, token)
            
        return None
        
    def _done(self):
        for token in self.tokens:
            if token.id == Token.UNKOWN:
                return False
            
        return True
