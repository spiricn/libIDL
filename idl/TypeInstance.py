from idl.Type import Type
from idl.lexer import Lang

from idl.IDLSyntaxError import IDLSyntaxError


class TypeInstance(object):
    def __init__(self, baseType, info):
        self._type = baseType
        
        modStrToInt = {
            Lang.KEYWORD_IN : Type.MOD_IN,
            Lang.KEYWORD_OUT : Type.MOD_OUT,
            Lang.KEYWORD_CALLBACK_REG : Type.MOD_CALLBACK_REG,
            Lang.KEYWORD_CALLBACK_UNREG : Type.MOD_CULLBACK_UNREG,
        }
        
        self._mods = 0
        
        if info:
            # Check for duplicate mods
            for index, i in enumerate(info.mods):
                if index < len(info.mods) - 1:
                    for j in info.mods[index+1:]:
                        if i == j:
                            raise IDLSyntaxError(module=None, line=-1, message='Duplicate type modifier %r for type %r' % (i, self._type.name))
            
            for mod in info.mods:
                if mod not in modStrToInt:
                    raise IDLSyntaxError(module=None, line=-1, message='Unrecognized type modifier %r for type %r' % (mod, self._type.name))
                
                self._mods |= modStrToInt[mod]
            
        self._isArray = False if not info else info.arraySize != None
        
        self._arraySize = None if not info else info.arraySize
        
    @property
    def baseType(self):
        return TypeInstance(self._type, None)
    
    @property
    def annotations(self):
        return self._type.annotations
    
    @property
    def isPrimitive(self):
        return self._type.isPrimitive()
    
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
        '''
        Checks if this type contains a modifier.
        
        @param modId: Modifier bit mask.
        
        @return: True or False
        '''
        
        return False if self._mods & modId == 0 else True
            
    def __eq__(self, other):
        return self._type == other
    
    def __ne__(self, other):
        return not (self == other)
