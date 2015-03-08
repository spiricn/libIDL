class Annotation(object):
    DECORATOR, \
    VARIABLE, \
    COMMENT, \
    = range(3)

    def __init__(self, desc):
        self._name = Annotation._stripLiteral( desc.name )
        
        self._value = Annotation._stripLiteral( desc.value )
        
        if desc.isComment:
            self._type = Annotation.COMMENT
            
        elif  self._name and self._value:
            self._type = Annotation.VARIABLE
            
        elif self._name and not self._value:
            self._type = Annotation.DECORATOR
            
        else:
            # Sanity check
            assert(0)
    
    @property
    def type(self):
        '''
        Type of the annotation.
        '''
        return self._type
    
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
