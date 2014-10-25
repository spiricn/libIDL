from idl.Annotatable import Annotatable


class Type(Annotatable):
    # Possible type modifiers bit fields
    MOD_IN = 1 << 0
    MOD_OUT = 1 << 1
    MOD_CONST = 1 << 2
    MOD_CALLBACK_REG = 1 << 3
    MOD_CULLBACK_UNREG = 1 << 4

    # Possible types
    BOOL, \
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
    = range(18)
    
    # List of type primitives
    primitives = [
        BOOL, \
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
               'int64' : Type.INT64,
               'uint64' : Type.UINT64,
               'int32' : Type.INT32,
               'uint32' : Type.UINT32,
               'int16' : Type.INT16,
               'uint16' : Type.UINT16,
               'int8' : Type.INT8,
               'uint8' : Type.UINT8,
               'float32' : Type.FLOAT32,
               'float64' : Type.FLOAT64,
               'void' : Type.VOID,
               'string' : Type.STRING,
               'boolean' : Type.BOOL,
               }
            
            if t in stringToType:
                self._id = stringToType[t]
            else:
                self._id = Type.INVALID 
            
        elif isinstance(t, int):
            self._id = t
            
            if t in Type.primitives:
                typeToName = {
                   Type.INT64 : 'int64',
                   Type.UINT64 : 'uint64',
                   Type.INT32 : 'int32',
                   Type.UINT32 : 'uint32',
                   Type.INT16 : 'int16' ,
                   Type.UINT16 : 'uint16',
                   Type.INT8 : 'int8',
                   Type.UINT8 : 'uint8',
                   Type.FLOAT32 : 'float32',
                   Type.FLOAT64 : 'float64',
                   Type.VOID : 'void',
                   Type.STRING : 'string',
                   Type.BOOL : 'boolean',
                }
                
                self._name = typeToName[t]
            
        else:
            raise NotImplementedError('Invalid type id')
        
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
    def id(self):
        '''
        Type identification integer.
        '''
        
        return self._id
    
    def isPrimitive(self):
        return self._id in Type.primitives
        
    def __eq__(self, other):
        if isinstance(other, Type):
            return self._id == other.id
        
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
