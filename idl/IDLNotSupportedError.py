from idl.IDLError import IDLError


class IDLNotSupportedError(IDLError):
    NAME = 'Support'
    
    def __init__(self, module, line, message):
        IDLError.__init__(self, IDLNotSupportedError.NAME, message, module, line)
