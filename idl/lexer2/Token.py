class Token:
    UNKOWN, \
    ID, \
    PUNCTUATION, \
    LIT, \
    KEYWORD, \
    = range(5)
    
    def __init__(self, tokenId, body):
        self.id = tokenId
        self.body = body
        
    def __str__(self):
        return '%d %r' % (self.id, self.body)
