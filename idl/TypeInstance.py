from idl.Type import Type


class TypeInstance(object):
    def __init__(self, baseType, info):
        self._type = baseType
        
        modStrToInt = {
            'const' : Type.MOD_CONST,
            'in' : Type.MOD_IN,
            'out' : Type.MOD_OUT,
            'callback_register' : Type.MOD_CALLBACK_REG,
            'callback_unregister' : Type.MOD_CULLBACK_UNREG,
        }
        
        # Check for duplicate mods
        for index, i in enumerate(info.mods):
            if index < len(info.mods) - 1:
                for j in info.mods[index+1:]:
                    if i == j:
                        raise RuntimeError('Duplicate argument modifier %r' % i) 
        
        self._mods = 0
        
        for mod in info.mods:
            if mod not in modStrToInt:
                raise RuntimeError('Unrecognized argument modifier %r' % mod)
            
            self._mods |= modStrToInt[mod]
            
        
        
        self._isArray = info.arraySize != None
        
        self._arraySize = info.arraySize
        
    @property
    def mods(self):
        '''
        Type modifier integer bit field.
        '''
        
        return self._mods
    
    @property
    def isArray(self):
        return self._isArray
    
    @property
    def arraySize(self):
        return self._arraySize
    
    @property
    def name(self):
        '''
        Name of the type this instance is associated with.
        '''
        
        return self._type.name
    
    @property
    def id(self):
        '''
        Id of the type this instance is associated with.
        '''
        
        return self._type.id
        
    def mod(self, modId):
        return False if self._mods & modId == 0 else True
            
    def __eq__(self, other):
        return self._type == other
