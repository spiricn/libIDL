class Argument(object):
    def __init__(self, argType, name):
        self.type = argType
        self.name = name
        
    def __str__(self):
        return '<Argument name="%s" type="%s">' % (self.name, self.type)