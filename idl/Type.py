from idl.Annotatable import Annotatable


class Type(Annotatable):
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
    ARRAY, \
    INVALID, \
    = range(19)
    
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
                
        self.module = module
        
        self.name = name
        
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
                self.id = stringToType[t]
            else:
                self.id = Type.INVALID 
            
        elif isinstance(t, int):
            self.id = t
            
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
                
                self.name = typeToName[t]
            
        else:
            raise NotImplementedError('Invalid type id')
        
    def isPrimitive(self):
        return self.id in Type.primitives
        
    def __eq__(self, other):
        if isinstance(other, Type):
            return self.id == other.id
        
        elif isinstance(other, int):
            return self.id == other
        
        else:
            return NotImplemented
        
    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return '<Type %s(%d)>' % (self.name, self.id)
    
    def create(self):
        pass