from idl.Type import Type


class Typedef(Type):
    def __init__(self, module, desc):
        Type.__init__(self, module, Type.TYPEDEF, desc.typeName)
