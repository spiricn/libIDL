import os

from idl.TypeGetter import TypeGetter

from idl2.Array import Array


class Module(TypeGetter):
    def __init__(self, env, name, filePath=None):
        self.env = env
        self.name = name
        self.types = []
        self.filePath = '' if not filePath else os.path.abspath(filePath)

    def _resolveType(self, typeInfo):
        for i in self.env.types:
            if i.name == typeInfo.name:
                if typeInfo.arraySize != None:
                    return Array(self, i, typeInfo.arraySize)
                else:
                    return i

        return None