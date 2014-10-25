class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        
    def assertNext(self, typeId, body=None):
        if len(self.tokens) == 0:
            raise RuntimeError('Token missing (expecting %d)' % typeId)
        
        else:
            # Type check
            if self.next().id != typeId:
                raise RuntimeError('Invalid token while parsing; expected %d got %d' % (typeId, self.next().id))
            
            # Body check
            if body != None and body != self.next().body:
                raise RuntimeError('Invalid token while parsing; expected %r got %r' % (body, self.next().body))
            
    def pop(self):
        return self.tokens.pop(0)
    
    def next(self):
        return self.tokens[0]
