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
        
    def __str__(self):
        return '%d %r' % (self.id, self.body)
