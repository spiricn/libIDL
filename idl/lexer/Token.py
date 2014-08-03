class Token(object):
    def __init__(self, tokenType, body):
        self.type = tokenType
        self.body = body
        
    def __str__(self):
        return '<Token type="%s" body="%s">' % (str(self.type), self.body)