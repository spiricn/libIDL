class Fragment(object):
    def __init__(self, fragmentType, body):
        self.type = fragmentType
        self.body = body
        
    def __str__(self):
        return '<Fragment type="%s" body="%s">' % (str(self.type), self.body)