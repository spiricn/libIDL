from idl.Type import Type


class TypeInstance(object):
    def __init__(self, baseType, info):
        self.type = baseType
        
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
        
        self.mods = 0
        
        for mod in info.mods:
            if mod not in modStrToInt:
                raise RuntimeError('Unrecognized argument modifier %r' % mod)
            
            self.mods |= modStrToInt[mod]
            
        
        
        self.isArray = info.arraySize != None
        
        self.arraySize = info.arraySize
        
    @property
    def name(self):
        return self.type.name
    
    @property
    def id(self):
        return self.type.id
        
    def mod(self, modId):
        return False if self.mods & modId == 0 else True
            
    def __eq__(self, other):
        return self.type == other
