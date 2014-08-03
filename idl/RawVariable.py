class RawVariable(object):
    def __init__(self, argType, name):
        self.type = argType
        self.name = name
        
    def __str__(self):
        return '<RawVariable name="%s" type="%s">' % (self.name, self.type)