from idl.IDLError import IDLError

class IDLTypeError(IDLError):
    def __init__(self, module, line, message):
        # Exception message
        IDLError.__init__(self, 'Type', message, module, line)
