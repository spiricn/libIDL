

class LangConfig:
    def __init__(self, inheritance=True, operatorOverload=True, preprocessor=True):
        self._inheritance = inheritance
        self._operatorOverload = operatorOverload
        self._preprocessor = preprocessor
    
    @property
    def preprocessor(self):
        '''
        Set to True to enable preprocessor.
        '''
        return self._preprocessor

    @property
    def operatorOverload(self):
        '''
        Set to True to enable operator overloading in interface methods.
        '''
        
        return self._operatorOverload
    
    @property
    def inheritance(self):
        '''
        Set to True to enable interface inheritance.
        '''
        
        return self._inheritance

    
    @property
    def explicitArgumentModifiers(self):
        '''
        Set to True to force explicit method argument modifiers (e.g. in, out, inout)
        '''
        # TODO
        pass