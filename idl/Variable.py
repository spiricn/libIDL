from idl.Annotatable import Annotatable


class Variable(Annotatable):
    '''
    Simple type/name container class
    '''
    
    def __init__(self, argType, name):
        Annotatable.__init__(self)
        
        self.type = argType
        self.name = name
        
    def __str__(self):
        return '<IDLVariable type=%s name="%s"' % (self.type, self.name)
