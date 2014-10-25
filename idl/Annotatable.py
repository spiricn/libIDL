from idl.Annotation import Annotation


class Annotatable(object):
    def __init__(self):
        self.annotations = []
        
    def _assignAnnotations(self, annotationInfos):
        for i in annotationInfos:
            self.annotations.append( Annotation(i) )
        
    def getAnnotation(self, name):
        for i in self.annotations:
            if i.name == name:
                return i

        return None
    
    def getAnnotationVal(self, name):
        a = self.getAnnotation(name)
        
        return None if not a else a.value
