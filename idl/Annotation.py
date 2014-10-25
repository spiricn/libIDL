class Annotation(object):
    def __init__(self, info):
        self._name = info.name
        
        self._value = info.value
        
    @property
    def name(self):
        '''
        Annotation name.
        '''
        
        return self._name
    
    @property
    def value(self):
        '''
        Annotation value.
        '''
        
        return self._value
