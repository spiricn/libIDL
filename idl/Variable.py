class Variable(object):
    def __init__(self, argType, name):
        self.type = argType
        self.name = name
        
    def __str__(self):
        return '<IDLVariable type=%s name="%s"' % (self.type, self.name)