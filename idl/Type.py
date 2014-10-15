class Type(object):
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
    METHOD, \
    CALLBACK, \
    CALLBACK_REGISTER, \
    CALLBACK_UNREGISTER, \
    STRUCTURE, \
    INTERFACE, \
    ENUM, \
    INVALID, \
    = range(21)
    
    def __init__(self, t):
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
            
        else:
            raise NotImplementedError('Invalid type id')
        
    def isPrimitive(self):
        return self.id in [
               Type.INT64,
               Type.UINT64,
               Type.INT32,
               Type.UINT32,
               Type.INT16,
               Type.UINT16,
               Type.INT8,
               Type.UINT8,
               Type.FLOAT32,
               Type.FLOAT64,
               Type.VOID,
               Type.STRING,
               Type.BOOL
        ]
        
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
        return '<Type id=%d>' % self.id