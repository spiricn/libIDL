import os

from idl.TypeGetter import TypeGetter
from idl.TypeInstance import TypeInstance


class Module(TypeGetter):
    def __init__(self, env, name, filePath=None):
        self._env = env
        self._name = name
        self._types = []
        self._filePath = '' if not filePath else os.path.abspath(filePath)

    @property
    def env(self):
        '''
        Parent environment of this module.
        '''
        
        return self._env
    
    @property
    def name(self):
        '''
        Module name.
        '''
        
        return self._name
    
    @property
    def types(self):
        '''
        Types defined by this module.
        '''
        
        return self._types
    
    @property
    def filePath(self):
        '''
        File path of this module (may be None).
        '''
        
        return self._filePath
    
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
