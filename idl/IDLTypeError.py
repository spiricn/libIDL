from idl.IDLError import IDLError

class IDLTypeError(IDLError):
    NAME = 'Type'
    
    def __init__(self, module, line, message):
        IDLError.__init__(self, IDLTypeError.NAME, message, module, line)
