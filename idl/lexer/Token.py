class Token:
    # Token types
    UNKOWN, \
    ID, \
    PUNCTUATION, \
    INT_LIT, \
    STRING_LIT, \
    KEYWORD, \
    COMMENT, \
    BLOCK_COMMENT, \
    = range(8)
    
    def __init__(self, tokenizer, tokenId, span):
        self._tokenizer = tokenizer
        self._id = tokenId
        self._span = span
        
    @property
    def tokenizer(self):
        return self._tokenizer
    
    @property
    def span(self):
        return self._span
    
    @property
    def id(self):
        return self._id
    
    @property
    def body(self):
        return self.tokenizer.source[self.span[0]:self.span[1]]
    
    @property
    def location(self):
        '''
        Returns a tuple containing line and column of this token.
        '''
        
        currIndex = 0
        
        for lineNumber, line in enumerate(self._tokenizer.source.splitlines(True)):
            lineSpan = (currIndex, currIndex + len(line))
            
            if self._span[0] >= lineSpan[0] and self._span[1] <= lineSpan[1]:
                return (lineNumber, self._span[0] - currIndex)
            
            currIndex += len(line)
            
        # Sanity check (should never happen)
        assert(0)
        
    @property
    def locationStr(self):
        '''
        Returns a string pointing to the line in the original source where the token is located.
        '''
        
        # Split the source into lies
        lines = self.tokenizer.source.splitlines()
        
        # Construct an error message showing the offending token in line
        locationStr = '%r\n %s ^' % (
            lines[self.location[0]],
            (' ' * self.location[1]))
        
        return locationStr
    
    def __str__(self):
        return '%d %r' % (self.id, self.body)
