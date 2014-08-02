class IDLMethodArgument(object):
    def __init__(self, argType, name):
        self.type = argType
        self.name = name
        
    def __str__(self):
        return '<IDLMethodArgument type=%d name="%s"' % (self.type, self.name)
