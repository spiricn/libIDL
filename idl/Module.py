import os

from idl.Type import Type
from idl.TypeGetter import TypeGetter

from idl.TypeInstance import TypeInstance


class Module(TypeGetter):
    def __init__(self, env, name, filePath=None):
        self.env = env
        self.name = name
        self.types = []
        self.filePath = '' if not filePath else os.path.abspath(filePath)

    def _resolveType(self, typeInfo):
        baseType = None 
        for i in self.env.types:
            if i.name == typeInfo.name:
                baseType = i
                break
            
        if not baseType:
            # undefined reference
            return None
        
        return TypeInstance(baseType, typeInfo)
        
