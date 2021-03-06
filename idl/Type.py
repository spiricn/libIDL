from idl.Annotatable import Annotatable
from idl.lexer import Lang


class Type(Annotatable):
    # Possible type modifiers bit fields
    MOD_IN = 1 << 0
    MOD_OUT = 1 << 1
    MOD_CALLBACK_REG = 1 << 2
    MOD_CULLBACK_UNREG = 1 << 3

    BOOL8, \
    BOOL16, \
    BOOL32, \
    INT64, \
    UINT64, \
    INT32, \
    UINT32, \
    INT16, \
    UINT16, \
    INT8, \
    UINT8, \
    FLOAT32, \
    FLOAT64, \
    VOID, \
    STRING, \
    STRUCTURE, \
    INTERFACE, \
    ENUM, \
    TYPEDEF, \
    INVALID, \
    = range(20)
    
    # List of type primitives
    primitives = [
        BOOL8, \
        BOOL16, \
        BOOL32, \
        INT64, \
        UINT64, \
        INT32, \
        UINT32, \
        INT16, \
        UINT16, \
        INT8, \
        UINT8, \
        FLOAT32, \
        FLOAT64, \
        VOID, \
        STRING, \
    ]
    
    def __init__(self, module, t, name=''):
        Annotatable.__init__(self)
                
        self._module = module
        
        self._name = name
        
        if isinstance(t, str):
            # Primitive types
            stringToType = {
               Lang.TYPE_INT64 : Type.INT64,
               Lang.TYPE_UINT64 : Type.UINT64,
               Lang.TYPE_INT32 : Type.INT32,
               Lang.TYPE_UINT32 : Type.UINT32,
               Lang.TYPE_INT16 : Type.INT16,
               Lang.TYPE_UINT16 : Type.UINT16,
               Lang.TYPE_INT8 : Type.INT8,
               Lang.TYPE_UINT8 : Type.UINT8,
               Lang.TYPE_FLOAT32 : Type.FLOAT32,
               Lang.TYPE_FLOAT64 : Type.FLOAT64,
               Lang.TYPE_VOID : Type.VOID,
               Lang.TYPE_STRING : Type.STRING,
               Lang.TYPE_BOOL8 : Type.BOOL8,
               Lang.TYPE_BOOL16 : Type.BOOL16,
               Lang.TYPE_BOOL32  : Type.BOOL32,
            }
            
            if t in stringToType:
                self._id = stringToType[t]
            else:
                self._id = Type.INVALID 
            
        elif isinstance(t, int):
            self._id = t
            
            if t in Type.primitives:
                typeToName = {
                   Type.INT64 : Lang.TYPE_INT64,
                   Type.UINT64 : Lang.TYPE_UINT64,
                   Type.INT32 : Lang.TYPE_INT32,
                   Type.UINT32 : Lang.TYPE_UINT32,
                   Type.INT16 : Lang.TYPE_INT16,
                   Type.UINT16 : Lang.TYPE_UINT16,
                   Type.INT8 : Lang.TYPE_INT8,
                   Type.UINT8 : Lang.TYPE_UINT8,
                   Type.FLOAT32 : Lang.TYPE_FLOAT32,
                   Type.FLOAT64 : Lang.TYPE_FLOAT64,
                   Type.VOID : Lang.TYPE_VOID,
                   Type.STRING : Lang.TYPE_STRING,
                   Type.BOOL8 : Lang.TYPE_BOOL8,
                   Type.BOOL16 : Lang.TYPE_BOOL16,
                   Type.BOOL32 : Lang.TYPE_BOOL32,
                }
                
                self._name = typeToName[t]
            
        else:
            raise NotImplementedError('Invalid type id')
    
    @property
    def path(self):
        path = self.module.package.path
        
        path.append( self.name )
        
        return path


    @property
    def pathStr(self):
        '''
        Path string for this type (e.g. com.exmple.TestInterface)
        '''
         
        return '.'.join(self.path)
        
    @property
    def name(self):
        '''
        Type name.
        '''
        
        return self._name
    
    @property
    def module(self):
        '''
        Type parent module.
        '''
        
        return self._module
    
    @property
    def package(self):
        '''
        Type parent package.
        '''

        return self._module.package
    
    @property
    def id(self):
        '''
        Type identification integer.
        '''
        
        return self._id
    
    @property
    def dependencies(self):
        '''
        List of types this type is dependent on.
        '''
        
        return []
    
    @property
    def isPrimitive(self):
        return self._id in Type.primitives
        
    def __eq__(self, other):
        if isinstance(other, Type):
            if self.isPrimitive:
                return self._id == other.id
            else:
                return self._id == other.id and self.name == other.name and \
                    self.module.package == other.module.package
        
        elif isinstance(other, int):
            return self._id == other
        
        else:
            return NotImplemented
        
    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return '<Type %s(%d)>' % (self._name, self._id)
    
    def _link(self):
        pass
