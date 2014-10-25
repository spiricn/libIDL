class Token:
    # Token types
    UNKOWN, \
    ID, \
    PUNCTUATION, \
    LIT, \
    KEYWORD, \
    = range(5)
    
    def __init__(self, tokenId, body):
        self._id = tokenId
        self._body = body
        
    @property
    def id(self):
        return self._id
    
    @property
    def body(self):
        return self._body
        
    def __str__(self):
        return '%d %r' % (self.id, self.body)
