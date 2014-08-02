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
    CALLBACK, \
    INVALID, \
    = range(14)
    
    @staticmethod
    def fromString(string):
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
        
        if string in stringToType:
            return stringToType[string]
        else:
            return IDLType.INVALID 
    