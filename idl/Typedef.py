from idl.Type import Type


class Typedef(Type):
    def __init__(self, module, info):
        Type.__init__(self, module, Type.TYPEDEF, info.typeName)
