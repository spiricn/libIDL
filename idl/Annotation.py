class Annotation(object):
    def __init__(self, info):
        self._name = Annotation._stripLiteral( info.name )
        
        self._value = Annotation._stripLiteral( info.value )

    @staticmethod
    def _stripLiteral(value):
        if ( value.startswith('"') and value.endswith('"') ) or ( value.startswith('\'') and value.endswith('\'') ):
            return value[1:-1]
        
        return value
        
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
