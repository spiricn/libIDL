class VariableToken(object):
    '''
    Simple type/name container class
    '''
    
    def __init__(self, argType, name):
        self.type = argType
        self.name = name
        