from idl.Annotatable import Annotatable
from idl.IDLSyntaxError import IDLSyntaxError
from idl.Type import Type
from idl.lexer import Lang


class Variable(Annotatable):
    def __init__(self,  variableType, name=None, mods=0, arraySize=-1):
        Annotatable.__init__(self)
        
        self._type = variableType
        
        self._name = name
        
        self._mods = mods
        
        self._arraySize = arraySize
        
    @staticmethod
    def _resolveModifiers(typeObj, mods):
        modStrToInt = {
            Lang.KEYWORD_IN : Type.MOD_IN,
            Lang.KEYWORD_OUT : Type.MOD_OUT,
            Lang.KEYWORD_CALLBACK_REG : Type.MOD_CALLBACK_REG,
            Lang.KEYWORD_CALLBACK_UNREG : Type.MOD_CULLBACK_UNREG,
        }
         
        res = 0
         
        # Check for duplicate mods
        for index, i in enumerate(mods):
            if index < len(mods) - 1:
                for j in mods[index+1:]:
                    if i == j:
                        raise IDLSyntaxError(module=None, line=-1, message='Duplicate type modifier %r for type %r' % (i, typeObj.name))
         
        for mod in mods:
            if mod not in modStrToInt:
                raise IDLSyntaxError(module=None, line=-1, message='Unrecognized type modifier %r for type %r' % (mod, typeObj.name))
             
            res |= modStrToInt[mod]
            
        return res 

    @property
    def type(self):
        '''
        Base type object of this instance (i.e. idl.Type stored in environment/module lists)
        '''
          
        return self._type
    
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
        
        return self._arraySize != None
    
    @property
    def arraySize(self):
        '''
        Array size (only valid if self.isArray is True)
        '''
        
        return None if self._arraySize == None else self._arraySize
    
    @property
    def name(self):
        '''
        Name of the type this instance is associated with.
        '''
        
        return self._name
        
    def mod(self, modId):
        '''
        Checks if this type contains a modifier.
        
        @param modId: Modifier bit mask.
        
        @return: True or False
        '''
        
        return False if self._mods & modId == 0 else True
