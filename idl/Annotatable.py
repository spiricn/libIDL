from idl.Annotation import Annotation


class Annotatable(object):
    '''
    Base class for all objects that may have annotations assigned to them.
    '''
    
    def __init__(self):
        self._annotations = []
        
    def getAnnotation(self, name):
        '''
        Get an annotation object associated with this object with the given name.
        
        @param name: Annotation name
        
        @return: Annotation object if it exists, None otherwise 
        '''
        
        for i in self.annotations:
            if i.name == name:
                return i

        return None
    
    def getAnnotationVal(self, name):
        '''
        Get an annotation value with the given name associated with this object.
        
        @param name: Annotation name
        
        @return: Annotation value if it exists, otherwise None
        '''
        
        annotation = self.getAnnotation(name)
        
        return None if not annotation else annotation.value

    @property
    def annotations(self):
        '''
        List of annotations assigned to this object.
        '''
        
        return self._annotations


    def _assignAnnotations(self, annotationDescs):
        for desc in annotationDescs:
            self.annotations.append( Annotation(desc) )