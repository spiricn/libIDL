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
    def type(self):
        '''
        Base type object of this instance (i.e. idl.Type stored in environment/module lists)
        '''
          
        return self._type
    
    @property
    def annotations(self):
        '''
        A list of annotations associated with this type instance.
        '''
        
        return self._type.annotations
    
    @property
    def isPrimitive(self):
        '''
        Checks if type instance is a primitive.
        '''
        
        if self.isArray:
            return False
        
        else:
            return self._type.isPrimitive()
    
    @property
    def mods(self):
        '''
        Type modifier integer bit field.
        '''
        
        return self._mods
    
    @property
    def isArray(self):
        '''
        Is this instance an array?
        '''
        
        return self._isArray
    
    @property
    def arraySize(self):
        '''
        Array size (only valid if self.isArray is True)
        '''
        
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
        if isinstance(other, TypeInstance):
            if not self.isPrimitive and not other.isPrimitive:
                # Not the same type
                if self.type != other.type:
                    return False
                
                elif self.isArray == other.isArray:
                    # Both are either arrays or not arrays, in either way compare names
                    return self.type.name == other.type.name
                
                else:
                    # One is an array the other isn't
                    return False
            else:
                # Both are primitives, so compare types
                return self.type == other.type
            
        elif isinstance(other, Type):
            # Since Type objects can't be arrays this is alwas false
            if self.isArray:
                return False
            elif self.isPrimitive and other.isPrimitive:
                # Compare base type
                return self.type == other
            
            else:
                return (self.type == other) and (self.name == other.name)
            
        elif isinstance(other, int):
            # Compare ids
            if self.isArray:
                return False
            else:
                # Compare base type
                return self.type == other
            
        else:
            raise RuntimeError('Invalid comparison of types %s' % str(other))
    
    def __ne__(self, other):
        return not (self == other)
