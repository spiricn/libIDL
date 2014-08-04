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
    INVALID, \
    = range(19)
    
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
               'bool' : Type.BOOL,
               }
            
            if t in stringToType:
                self.type = stringToType[t]
            else:
                self.type = Type.INVALID 
            
        elif isinstance(t, int):
            self.type = t
            
        else:
            raise NotImplementedError('Invalid type id')
        
    def __eq__(self, other):
        if isinstance(other, Type):
            return self.type == other.type
        elif isinstance(other, int):
            return self.type == other
        else:
            return NotImplemented

    def __str__(self):
        return '<Type id=%d>' % self.type