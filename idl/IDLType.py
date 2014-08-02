class IDLType(object):
    INT32, \
    VOID, \
    STRING, \
    CALLBACK, \
    INVALID, \
    = range(5)
    
    @staticmethod
    def fromString(string):
        stringToType = {
               'int32' : IDLType.INT32,
               'void' : IDLType.VOID,
               'string' : IDLType.STRING,
        }
        
        if string in stringToType:
            return stringToType[string]
        else:
            return IDLType.INVALID 
    