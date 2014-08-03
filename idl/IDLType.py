class IDLType(object):
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
               'int64' : IDLType.INT64,
               'uint64' : IDLType.UINT64,
               'int32' : IDLType.INT32,
               'uint32' : IDLType.UINT32,
               'int16' : IDLType.INT16,
               'uint16' : IDLType.UINT16,
               'int8' : IDLType.INT8,
               'uint8' : IDLType.UINT8,
               'float32' : IDLType.FLOAT32,
               'float64' : IDLType.FLOAT64,
               'void' : IDLType.VOID,
               'string' : IDLType.STRING,
               }
            
            if t in stringToType:
                self.type = stringToType[t]
            else:
                self.type = IDLType.INVALID 
            
        elif isinstance(t, int):
            self.type = t
            
        else:
            raise NotImplementedError('Invalid type id')
        
    def __eq__(self, other):
        if isinstance(other, IDLType):
            return self.type == other.type
        elif isinstance(other, int):
            return self.type == other
        else:
            return NotImplemented

    def __str__(self):
        return '<IDLType id=%d>' % self.type