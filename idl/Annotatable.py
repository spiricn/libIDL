from idl.Annotation import Annotation


class Annotatable(object):
    '''
    Base class for all objects that can have annotations assigned to them.
    '''
    
    def __init__(self):
        self._annotations = []
        
    def _assignAnnotations(self, annotationDescs):
        for desc in annotationDescs:
            self.annotations.append( Annotation(desc) )
        
    def getAnnotation(self, name):
        '''
        Get an annotation object associated with this object with the given name.
        '''
        
        for i in self.annotations:
            if i.name == name:
                return i

        return None
    
    def getAnnotationVal(self, name):
        '''
        Get an annotation value with the given name associated with this object.
        '''
        
        annotation = self.getAnnotation(name)
        
        return None if not annotation else annotation.value

    @property
    def annotations(self):
        return self._annotations
