from idl.Type import Type


class Array(Type):
    def __init__(self, module, baseType, size):
        Type.__init__(self, module, Type.ARRAY)
        
        self.baseType = baseType
        
        self.size = size
        
        self.name = '%s[]' % baseType.name
    