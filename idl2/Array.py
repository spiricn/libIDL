from idl.Type import Type


class Array(Type):
    def __init__(self, module, baseType, size):
        Type.__init__(self, module, Type.ARRAY, baseType.name)
        
        self.baseType = baseType
        
        self.size = size
    